import fs from 'fs';
import axios from 'axios';
import crypto from 'crypto';
import TikTokChannel from '../models/TikTokChannel.js';
import { progressMap } from './download.controller.js';
import FormData from 'form-data';

const pkceStore = new Map();

// Add these to your .env file
const CLIENT_KEY = process.env.TIKTOK_CLIENT_KEY || 'your_tiktok_client_key';
const CLIENT_SECRET = process.env.TIKTOK_CLIENT_SECRET || 'your_tiktok_client_secret';
const REDIRECT_URI = process.env.TIKTOK_REDIRECT_URI || 'http://localhost:3005/api/tiktok/callback';

export const getAuthUrl = (req, res) => {
  const CLIENT_KEY = process.env.TIKTOK_CLIENT_KEY;
  const REDIRECT_URI = process.env.TIKTOK_REDIRECT_URI || 'http://localhost:3005/api/tiktok/callback';

  // TikTok uses CSRF state token
  const csrfState = crypto.randomBytes(16).toString('hex');
  
  // PKCE - TikTok non-standard requirement: code_challenge must be hex, not base64url!
  const codeVerifier = crypto.randomBytes(32).toString('hex');
  const codeChallenge = crypto.createHash('sha256').update(codeVerifier).digest('hex');
  
  pkceStore.set(csrfState, codeVerifier);
  // cleanup after 10 mins
  setTimeout(() => pkceStore.delete(csrfState), 10 * 60 * 1000);
  
  let url = 'https://www.tiktok.com/v2/auth/authorize/';
  url += `?client_key=${CLIENT_KEY}`;
  url += '&scope=user.info.basic,video.publish,video.upload';
  url += '&response_type=code';
  url += `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`;
  url += `&state=${csrfState}`;
  url += `&code_challenge=${codeChallenge}`;
  url += '&code_challenge_method=S256';
  
  res.json({ url });
};

export const authCallback = async (req, res) => {
  const CLIENT_KEY = process.env.TIKTOK_CLIENT_KEY;
  const CLIENT_SECRET = process.env.TIKTOK_CLIENT_SECRET;
  const REDIRECT_URI = process.env.TIKTOK_REDIRECT_URI || 'http://localhost:3005/api/tiktok/callback';

  const code = req.query.code;
  const state = req.query.state;
  const err = req.query.error;

  if (err) return res.status(400).send('Authentication failed or was cancelled.');
  if (!code) return res.status(400).send('No code provided');
  
  const codeVerifier = pkceStore.get(state);
  if (!codeVerifier) return res.status(400).send('Invalid state or session expired.');
  pkceStore.delete(state);

  try {
    // 1. Get Access Token
    const tokenParams = new URLSearchParams({
      client_key: CLIENT_KEY,
      client_secret: CLIENT_SECRET,
      code: code,
      grant_type: 'authorization_code',
      redirect_uri: REDIRECT_URI,
      code_verifier: codeVerifier
    });

    const tokenRes = await axios.post('https://open.tiktokapis.com/v2/oauth/token/', tokenParams.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    const tokens = tokenRes.data;
    if (tokens.error) throw new Error(tokens.error_description || 'Failed to get token');

    const accessToken = tokens.access_token;
    const refreshToken = tokens.refresh_token;
    const expiresIn = tokens.expires_in; // in seconds
    const tokenExpiry = new Date(Date.now() + expiresIn * 1000);

    // 2. Get User Info (Channel details)
    const userRes = await axios.get('https://open.tiktokapis.com/v2/user/info/?fields=open_id,union_id,avatar_url,display_name', {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    });

    const userInfo = userRes.data.data.user;
    const channelId = userInfo.open_id;
    const channelTitle = userInfo.display_name;
    const thumbnailUrl = userInfo.avatar_url;

    // 3. Save to DB
    const [tkChannel, created] = await TikTokChannel.findOrCreate({
      where: { channelId },
      defaults: {
        channelTitle,
        thumbnailUrl,
        accessToken,
        refreshToken,
        tokenExpiry
      }
    });

    if (!created) {
      tkChannel.channelTitle = channelTitle;
      tkChannel.thumbnailUrl = thumbnailUrl;
      tkChannel.accessToken = accessToken;
      if (refreshToken) tkChannel.refreshToken = refreshToken;
      tkChannel.tokenExpiry = tokenExpiry;
      await tkChannel.save();
    }

    // Redirect back to frontend
    res.redirect('http://localhost:3000/editor/video-mixer?tiktok_auth=success');
  } catch (error) {
    console.error('TikTok Auth Error:', error.response?.data || error.message);
    res.status(500).send('Authentication failed: ' + (error.response?.data?.error?.message || error.message));
  }
};

export const getConnectedChannels = async (req, res) => {
  try {
    const channels = await TikTokChannel.findAll({
      attributes: ['id', 'channelId', 'channelTitle', 'thumbnailUrl']
    });
    res.json(channels);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

export const uploadVideo = async (req, res) => {
  const { channelId, videoPath, title, tags, jobId } = req.body;

  if (!channelId || !videoPath || !fs.existsSync(videoPath)) {
    return res.status(400).json({ error: 'Missing required fields or video not found.' });
  }

  try {
    const tkChannel = await TikTokChannel.findOne({ where: { channelId } });
    if (!tkChannel) return res.status(404).json({ error: 'Channel not found in database.' });

    // Enable progress updates
    if (jobId) progressMap.set(jobId, { progress: 10, status: 'Initializing upload...' });

    const fileSize = fs.statSync(videoPath).size;

    // 1. Init Upload via TikTok Direct Post API
    const initPayload = {
      post_info: {
        title: `${title} ${tags ? tags.split(',').map(t => `#${t.trim().replace('#','')}`).join(' ') : ''}`.trim(),
        privacy_level: 'SELF_ONLY', // Default to private/self-only for safety
        disable_duet: false,
        disable_comment: false,
        disable_stitch: false,
        video_cover_timestamp_ms: 1000
      },
      source_info: {
        source: 'FILE_UPLOAD',
        video_size: fileSize,
        chunk_size: fileSize, // Note: For very large videos, TikTok requires chunked upload
        total_chunk_count: 1
      }
    };

    const initRes = await axios.post('https://open.tiktokapis.com/v2/post/publish/video/init/', initPayload, {
      headers: {
        'Authorization': `Bearer ${tkChannel.accessToken}`,
        'Content-Type': 'application/json'
      }
    });

    if (initRes.data.error && initRes.data.error.code !== 'ok') {
      throw new Error(initRes.data.error.message || 'Failed to initialize upload');
    }

    const uploadUrl = initRes.data.data.upload_url;
    const publishId = initRes.data.data.publish_id;

    if (jobId) progressMap.set(jobId, { progress: 30, status: 'Uploading to TikTok...' });

    // 2. Upload the video file
    const fileStream = fs.createReadStream(videoPath);
    
    await axios.put(uploadUrl, fileStream, {
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Range': `bytes 0-${fileSize - 1}/${fileSize}`
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        // Map 0-100 to 30-90 range for overall progress
        const mappedProgress = 30 + (percentCompleted * 0.6);
        if (jobId) progressMap.set(jobId, { progress: mappedProgress, status: 'Uploading to TikTok...' });
      }
    });

    if (jobId) {
      progressMap.set(jobId, { progress: 100, status: 'Upload complete!' });
      setTimeout(() => progressMap.delete(jobId), 5000);
    }
    
    res.json({ success: true, publishId, message: 'Upload initiated successfully. It may take a moment to process on TikTok.' });
  } catch (error) {
    console.error('TikTok Upload Error:', error.response?.data || error.message);
    if (!res.headersSent) {
      res.status(500).json({ error: error.response?.data?.error?.message || error.message });
    }
  }
};
