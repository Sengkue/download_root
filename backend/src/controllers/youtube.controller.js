import { google } from 'googleapis';
import fs from 'fs';
import YouTubeChannel from '../models/YouTubeChannel.js';
import { progressMap } from './download.controller.js';

const SCOPES = [
  'https://www.googleapis.com/auth/youtube.upload',
  'https://www.googleapis.com/auth/youtube.readonly'
];

function getOAuth2Client() {
  return new google.auth.OAuth2(
    process.env.YOUTUBE_CLIENT_ID || 'dummy_client_id',
    process.env.YOUTUBE_CLIENT_SECRET || 'dummy_client_secret',
    process.env.YOUTUBE_REDIRECT_URI || 'http://localhost:3005/api/youtube/callback'
  );
}

export const getAuthUrl = (req, res) => {
  const oauth2Client = getOAuth2Client();
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent'
  });
  res.json({ url: authUrl });
};

export const authCallback = async (req, res) => {
  const code = req.query.code;
  if (!code) return res.status(400).send('No code provided');

  try {
    const oauth2Client = getOAuth2Client();
    const { tokens } = await oauth2Client.getToken(code);
    oauth2Client.setCredentials(tokens);

    const youtube = google.youtube({ version: 'v3', auth: oauth2Client });
    
    // Get channel details
    const channelRes = await youtube.channels.list({
      part: 'snippet',
      mine: true
    });

    if (!channelRes.data.items || channelRes.data.items.length === 0) {
      return res.status(404).send('No YouTube channel found for this account.');
    }

    const channel = channelRes.data.items[0];
    const channelId = channel.id;
    const channelTitle = channel.snippet.title;
    const thumbnailUrl = channel.snippet.thumbnails?.default?.url || '';

    // Save to DB
    const [ytChannel, created] = await YouTubeChannel.findOrCreate({
      where: { channelId },
      defaults: {
        channelTitle,
        thumbnailUrl,
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        tokenExpiry: tokens.expiry_date ? new Date(tokens.expiry_date) : null
      }
    });

    if (!created) {
      ytChannel.channelTitle = channelTitle;
      ytChannel.thumbnailUrl = thumbnailUrl;
      ytChannel.accessToken = tokens.access_token;
      if (tokens.refresh_token) {
        ytChannel.refreshToken = tokens.refresh_token;
      }
      if (tokens.expiry_date) {
        ytChannel.tokenExpiry = new Date(tokens.expiry_date);
      }
      await ytChannel.save();
    }

    // Redirect back to frontend
    res.redirect('http://localhost:3000/editor/video-mixer?youtube_auth=success');
  } catch (error) {
    console.error('YouTube Auth Error:', error);
    res.status(500).send('Authentication failed');
  }
};

export const getConnectedChannels = async (req, res) => {
  try {
    const channels = await YouTubeChannel.findAll({
      attributes: ['id', 'channelId', 'channelTitle', 'thumbnailUrl']
    });
    res.json(channels);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

export const uploadVideo = async (req, res) => {
  const { channelId, videoPath, title, description, tags, privacyStatus = 'private', jobId } = req.body;

  if (!channelId || !videoPath || !fs.existsSync(videoPath)) {
    return res.status(400).json({ error: 'Missing required fields or video not found.' });
  }

  try {
    const ytChannel = await YouTubeChannel.findOne({ where: { channelId } });
    if (!ytChannel) return res.status(404).json({ error: 'Channel not found in database.' });

    const oauth2Client = getOAuth2Client();
    oauth2Client.setCredentials({
      access_token: ytChannel.accessToken,
      refresh_token: ytChannel.refreshToken,
      expiry_date: ytChannel.tokenExpiry ? ytChannel.tokenExpiry.getTime() : null
    });

    // Check if we need to refresh token (google-auth-library usually handles this automatically if refresh_token is present)
    const youtube = google.youtube({ version: 'v3', auth: oauth2Client });

    const fileSize = fs.statSync(videoPath).size;
    
    // Enable progress updates
    if (jobId) progressMap.set(jobId, { progress: 0, status: 'Starting upload...' });

    const uploadRes = await youtube.videos.insert({
      part: 'snippet,status',
      requestBody: {
        snippet: {
          title,
          description,
          tags: tags ? tags.split(',').map(t => t.trim()) : [],
          categoryId: '22' // 22 = People & Blogs, change as needed
        },
        status: {
          privacyStatus,
          selfDeclaredMadeForKids: false
        }
      },
      media: {
        body: fs.createReadStream(videoPath)
      }
    }, {
      onUploadProgress: evt => {
        const progress = Math.round((evt.bytesRead / fileSize) * 100);
        if (jobId) {
          progressMap.set(jobId, { progress, status: 'Uploading to YouTube...' });
        }
      }
    });

    if (jobId) {
      progressMap.set(jobId, { progress: 100, status: 'Upload complete!' });
      setTimeout(() => progressMap.delete(jobId), 5000);
    }
    res.json({ url: `https://youtu.be/${uploadRes.data.id}` });
  } catch (error) {
    console.error('YouTube Upload Error:', error);
    if (!res.headersSent) {
      res.status(500).json({ error: error.message });
    } else {
      res.status(500).json({ error: error.message });
    }
  }
};
