import 'dotenv/config';
import express from 'express';
import { GoogleGenAI } from '@google/genai';
import cors from 'cors';
import youtubeDl from 'youtube-dl-exec';
import ffmpegPath from 'ffmpeg-static';
import { connectDB } from './config/database.js';
import fs from 'fs';
import path from 'path';
import os from 'os';
import crypto from 'crypto';
import * as cheerio from 'cheerio';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import multer from 'multer';
import { connectGoogleSheets, getGoogleSheetLinks, addGoogleSheetLink, deleteGoogleSheetLink, updateGoogleSheetLink, getTypingLessons, saveTypingResult, addTypingLesson } from './config/googleSheets.js';
import { User } from './models/User.js';
import { Post } from './models/Post.js';
import { WebviewLink } from './models/WebviewLink.js';
import { API_KEYS } from './config/apiKeys.js';

let currentKeyIndex = 0;

const app = express();
const PORT = process.env.PORT || 3001;

// Middlewares
app.use(cors());
app.use(express.json());

// Serve uploads folder
const uploadDir = path.join(process.cwd(), 'uploads');
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);
app.use('/uploads', express.static(uploadDir));

// Multer Config
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => cb(null, Date.now() + path.extname(file.originalname))
});
const upload = multer({ storage });

const JWT_SECRET = 'super-secret-key-123'; // In production, use env var

const progressMap = new Map();

// Auth Endpoints
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, password, name, gender, location } = req.body;
    if (!username || !password) return res.status(400).json({ error: 'Username and password required' });

    const existingUser = await User.findOne({ where: { username } });
    if (existingUser) return res.status(400).json({ error: 'Username already exists' });

    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await User.create({
      username,
      password: hashedPassword,
      name,
      gender,
      location,
      profileImage: ''
    });

    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user.id, username, name, profileImage: user.profileImage } });
  } catch (err) {
    console.error('Register error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await User.findOne({ where: { username } });
    if (!user) return res.status(400).json({ error: 'Invalid credentials' });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(400).json({ error: 'Invalid credentials' });

    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user.id, username: user.username, name: user.name, profileImage: user.profileImage } });
  } catch (err) {
    console.error('Login error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

// Middleware to protect routes
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Post Endpoints
app.post('/api/posts/upload', authMiddleware, upload.single('image'), async (req, res) => {
  try {
    const { description } = req.body;
    if (!req.file) return res.status(400).json({ error: 'Image file is required' });

    const post = await Post.create({
      userId: req.userId,
      image: `/uploads/${req.file.filename}`,
      description: description || ''
    });

    // Fetch the post with user details
    const newPost = await Post.findByPk(post.id, {
      include: [{ model: User, as: 'user', attributes: ['name', 'gender', 'location', 'profileImage'] }]
    });

    res.json({ post: newPost });
  } catch (err) {
    console.error('Upload error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.get('/api/posts/local', async (req, res) => {
  try {
    const posts = await Post.findAll({
      include: [{ model: User, as: 'user', attributes: ['name', 'gender', 'location', 'profileImage'] }],
      order: [['createdAt', 'DESC']]
    });
    res.json({ posts });
  } catch (err) {
    console.error('Fetch local posts error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

// Progress SSE Endpoint
app.get('/api/progress', (req, res) => {
  const { jobId } = req.query;
  if (!jobId) return res.status(400).end();

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  res.write(`data: ${JSON.stringify({ progress: 0, status: 'Connecting...' })}\n\n`);

  const interval = setInterval(() => {
    const jobData = progressMap.get(jobId);
    if (jobData) {
      res.write(`data: ${JSON.stringify(jobData)}\n\n`);
    }
  }, 500);

  req.on('close', () => {
    clearInterval(interval);
  });
});

// Main Download Endpoint
app.post('/api/download', async (req, res) => {
  try {
    const { url, type, quality, jobId } = req.body;

    if (!url || !type) {
      return res.status(400).json({ error: 'URL and type are required.' });
    }

    if (type === 'image') {
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Referer': 'https://pixabay.com/'
        }
      });
      
      if (!response.ok) {
        return res.status(400).json({ error: `Failed to fetch the image from the provided URL. Status: ${response.status} ${response.statusText}` });
      }

      const urlObj = new URL(url);
      const filename = urlObj.pathname.split('/').pop() || 'downloaded-image.jpg';
      const contentType = response.headers.get('content-type') || 'application/octet-stream';
      const contentLength = response.headers.get('content-length');

      res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
      res.setHeader('Content-Type', contentType);
      if (contentLength) {
        res.setHeader('Content-Length', contentLength);
      }
      res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition, Content-Length');

      // Convert Web Stream to Node.js stream and pipe to response
      // This ensures the frontend receives chunks in real-time as Pixabay sends them!
      const { Readable } = await import('stream');
      const webStream = response.body;
      if (!webStream) {
         return res.status(500).json({ error: 'Failed to read response body from origin.' });
      }
      Readable.fromWeb(webStream).pipe(res);
    }
    
    else if (type === 'video' || type === 'audio') {
      const isAudio = type === 'audio';
      const ext = isAudio ? 'mp3' : 'mp4';

      if (url.includes('tiktok.com')) {
         try {
           if (jobId) progressMap.set(jobId, { progress: 10, status: 'Fetching TikTok info...' });
           const resp = await fetch(`https://www.tikwm.com/api/?url=${encodeURIComponent(url)}`);
           const data = await resp.json();
           
           if (data.code === 0 && data.data) {
             const videoUrl = isAudio ? data.data.music : (data.data.play || data.data.wmplay);
             if (!videoUrl) throw new Error('Could not find stream URL');
             
             if (jobId) progressMap.set(jobId, { progress: 50, status: 'Downloading from TikTok...' });
             
             const videoResp = await fetch(videoUrl);
             if (!videoResp.ok) throw new Error(`Failed to fetch video stream: ${videoResp.statusText}`);
             
             const contentLength = videoResp.headers.get('content-length');
             const contentType = videoResp.headers.get('content-type') || (isAudio ? 'audio/mpeg' : 'video/mp4');
             
             res.setHeader('Content-Disposition', `attachment; filename="tiktok-${type}.${ext}"`);
             res.setHeader('Content-Type', contentType);
             if (contentLength) res.setHeader('Content-Length', contentLength);
             res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition, Content-Length');
             
             if (jobId) progressMap.set(jobId, { progress: 100, status: 'Streaming to browser...' });
             
             const { Readable } = await import('stream');
             const webStream = videoResp.body;
             if (!webStream) throw new Error('No body in response');
             
             Readable.fromWeb(webStream).pipe(res);
             
             res.on('finish', () => {
               if (jobId) progressMap.delete(jobId);
             });
             return; // Done handling TikTok!
           }
         } catch (err) {
           console.error('TikTok download proxy error:', err);
           if (jobId) progressMap.set(jobId, { progress: 10, status: 'Falling back to alternative method...' });
         }
      }

      // Use a temp file so yt-dlp can do ffmpeg post-processing (audio extraction, muxing)
      const tmpId = crypto.randomBytes(8).toString('hex');
      const tmpDir = os.tmpdir();
      const tmpBase = path.join(tmpDir, `yt-${tmpId}`);
      // Let yt-dlp determine the final extension via %(ext)s
      const tmpTemplate = `${tmpBase}.%(ext)s`;

      console.log(`[yt-dlp] Downloading ${type} to temp template: ${tmpTemplate}`);
      if (jobId) progressMap.set(jobId, { progress: 0, status: 'Starting download...' });

      try {
        // Sanitize URL: strip playlist/radio params that cause issues with cmd.exe on Windows
        // The '&' in URLs like ?v=xxx&list=yyy gets interpreted as a command separator
        let cleanUrl = url;
        try {
          const parsed = new URL(url);
          parsed.searchParams.delete('list');
          parsed.searchParams.delete('start_radio');
          parsed.searchParams.delete('index');
          cleanUrl = parsed.toString();
        } catch (_) {
          // If URL parsing fails, use the original URL
        }

        const ytOptions = isAudio ? {
          extractAudio: true,
          audioFormat: 'mp3',
          audioQuality: 0,          // best quality
          noPlaylist: true,
          ffmpegLocation: `"${ffmpegPath}"`,
          o: tmpTemplate,
        } : {
          f: quality ? `"bestvideo[height<=${quality}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=${quality}]+bestaudio/best"` : '"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"',
          mergeOutputFormat: 'mp4',
          noPlaylist: true,
          ffmpegLocation: `"${ffmpegPath}"`,
          o: tmpTemplate,
        };

        // Run yt-dlp and wait for it to complete
        const subprocess = youtubeDl.exec(cleanUrl, ytOptions);
        
        subprocess.stdout.on('data', (data) => {
          const text = data.toString();
          const match = text.match(/\[download\]\s+([\d\.]+)%/);
          if (match && jobId) {
            progressMap.set(jobId, { progress: parseFloat(match[1]), status: 'Downloading from YouTube...' });
          } else if (text.includes('[Merger]') && jobId) {
            progressMap.set(jobId, { progress: 100, status: 'Merging Audio/Video...' });
          } else if (text.includes('[ExtractAudio]') && jobId) {
            progressMap.set(jobId, { progress: 100, status: 'Extracting Audio...' });
          }
        });

        await subprocess;

        // Find the actual output file (yt-dlp may have used a different extension)
        const tmpDirFiles = fs.readdirSync(tmpDir);
        const outputFile = tmpDirFiles
          .filter(f => f.startsWith(`yt-${tmpId}.`))
          .map(f => path.join(tmpDir, f))
          .find(f => fs.statSync(f).isFile());

        if (!outputFile) {
          return res.status(500).json({ error: 'yt-dlp finished but the output file was not found.' });
        }

        console.log(`[yt-dlp] Output file found: ${outputFile}`);

        const stat = fs.statSync(outputFile);

        res.setHeader('Content-Disposition', `attachment; filename="youtube-${type}.${ext}"`);
        res.setHeader('Content-Type', isAudio ? 'audio/mpeg' : 'video/mp4');
        res.setHeader('Content-Length', stat.size.toString());
        res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition, Content-Length');

        // Stream the completed file to the client
        const fileStream = fs.createReadStream(outputFile);
        fileStream.pipe(res);

        // Clean up the temp file after the response is sent
        res.on('finish', () => {
          if (jobId) progressMap.delete(jobId);
          fs.unlink(outputFile, (err) => {
            if (err) console.error('Failed to clean up temp file:', err.message);
            else console.log(`[yt-dlp] Cleaned up temp file: ${outputFile}`);
          });
        });

      } catch (ytError) {
        if (jobId) progressMap.delete(jobId);
        // Clean up any temp files on error
        const tmpDirFiles2 = fs.readdirSync(tmpDir);
        tmpDirFiles2.filter(f => f.startsWith(`yt-${tmpId}.`)).forEach(f => {
          try { fs.unlinkSync(path.join(tmpDir, f)); } catch (_) {}
        });
        console.error('yt-dlp error:', ytError.message || ytError);
        if (!res.headersSent) {
          return res.status(500).json({ error: 'Failed to download. Please check the URL or try again later.' });
        }
      }
    }
    
    else {
      return res.status(400).json({ error: 'Invalid file type. Must be "image", "video", or "audio".' });
    }
  } catch (error) {
    console.error('Download error:', error);
    if (!res.headersSent) {
      res.status(500).json({ error: 'Internal Server Error while processing the download.' });
    }
  }
});

// Info Endpoint
app.post('/api/info', async (req, res) => {
  try {
    const { url } = req.body;
    if (!url) return res.status(400).json({ error: 'URL is required.' });

    let cleanUrl = url;
    try {
      const parsed = new URL(url);
      parsed.searchParams.delete('list');
      parsed.searchParams.delete('start_radio');
      parsed.searchParams.delete('index');
      cleanUrl = parsed.toString();
    } catch (_) {}

    if (cleanUrl.includes('tiktok.com')) {
      try {
        const resp = await fetch(`https://www.tikwm.com/api/?url=${encodeURIComponent(cleanUrl)}`);
        const data = await resp.json();
        if (data.code === 0 && data.data) {
          return res.json({
            title: data.data.title,
            thumbnail: data.data.cover,
            qualities: [1080], // Provide a default quality
            duration: data.data.duration
          });
        }
      } catch (err) {
        console.error('TikTok API info fallback error:', err);
      }
    }

    const info = await youtubeDl(cleanUrl, {
      dumpJson: true,
      noWarnings: true,
      noPlaylist: true
    });

    const formats = info.formats || [];
    const videoFormats = formats
      .filter(f => f.vcodec && f.vcodec !== 'none')
      .map(f => f.height)
      .filter(h => h && h > 0);
    
    const uniqueHeights = [...new Set(videoFormats)].sort((a, b) => b - a);

    return res.json({
      title: info.title,
      thumbnail: info.thumbnail,
      qualities: uniqueHeights.length ? uniqueHeights : [1080, 720, 480, 360], // Fallback if formats is empty
      duration: info.duration
    });
  } catch (error) {
    console.error('Info error:', error.message || error);
    res.status(500).json({ error: 'Failed to fetch video information.' });
  }
});

// Stock Search Proxy Endpoint to bypass browser CORS / Adblockers
app.get('/api/search', async (req, res) => {
  try {
    const { key, q, image_type, per_page, page, video } = req.query;
    
    if (!key || !q) {
        return res.status(400).json({ error: 'Pixabay API key and search query are required.' });
    }

    let url = '';
    if (video === 'true') {
        url = `https://pixabay.com/api/videos/?key=${key}&q=${encodeURIComponent(q)}&per_page=${per_page || 30}&page=${page || 1}`;
    } else {
        url = `https://pixabay.com/api/?key=${key}&q=${encodeURIComponent(q)}&image_type=${image_type || 'photo'}&per_page=${per_page || 30}&page=${page || 1}`;
    }

    const response = await fetch(url);
    if (!response.ok) {
        return res.status(response.status).json({ error: `Pixabay API Connection Error: ${response.statusText}` });
    }

    const data = await response.json();
    return res.json(data);
  } catch (error) {
    console.error('Search proxy error:', error);
    res.status(500).json({ error: 'Backend failed to proxy the search request to Pixabay.' });
  }
});

// Lyrics Endpoints
app.get('/api/lyrics/home', async (req, res) => {
  try {
    const response = await fetch('https://hmonglyrics.net/', {
       headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5'
       }
    });

    if (!response.ok) {
        return res.status(response.status).json({ error: `Failed to fetch hmonglyrics homepage: ${response.statusText}` });
    }

    const html = await response.text();
    const $ = cheerio.load(html);

    const featured = [];
    $('#popular-listr li.gradient').each((i, el) => {
        const title = $(el).find('h3 a').text().trim();
        const artist = $(el).find('.item-text > a').text().trim();
        const url = $(el).find('h3 a').attr('href');
        
        let bgStyle = $(el).attr('style') || '';
        let image = '';
        const imgMatch = bgStyle.match(/url\(['"]?(.*?)['"]?\)/);
        if (imgMatch && imgMatch[1]) {
            image = imgMatch[1];
        }

        if (title && url) {
            featured.push({ title, artist, url, image });
        }
    });

    const latest = [];
    $('.latest-lyrics li').each((i, el) => {
        const title = $(el).find('h5 a').text().trim();
        const artist = $(el).find('.lyric-content > a').text().trim();
        const url = $(el).find('h5 a').attr('href');
        
        if (title && url) {
            latest.push({ title, artist, url });
        }
    });

    res.json({ featured, latest });
  } catch (error) {
    console.error('Lyrics home proxy error:', error);
    res.status(500).json({ error: 'Backend failed to proxy the request.' });
  }
});

app.get('/api/lyrics/search', async (req, res) => {
  try {
    const { q } = req.query;
    if (!q) return res.status(400).json({ error: 'Search query is required' });

    const searchUrl = `https://hmonglyrics.net/?s=${encodeURIComponent(q)}&post_type=lyrics`;
    const response = await fetch(searchUrl, {
       headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5'
       }
    });
    if (!response.ok) throw new Error(`Failed to fetch from hmonglyrics.net: ${response.status}`);
    
    const html = await response.text();
    const $ = cheerio.load(html);
    const results = [];

    $('.list-line').each((i, el) => {
       const titleEl = $(el).find('.col-lg-6 a');
       const artistEl = $(el).find('.col-lg-3').last().find('a');
       
       if (titleEl.length) {
         results.push({
            title: titleEl.text().trim(),
            url: titleEl.attr('href'),
            artist: artistEl.length ? artistEl.text().trim() : 'Unknown'
         });
       }
    });

    res.json({ results });
  } catch (error) {
    console.error('Lyrics search error:', error);
    res.status(500).json({ error: 'Failed to search lyrics' });
  }
});

app.post('/api/lyrics/song', async (req, res) => {
  try {
    const { url } = req.body;
    if (!url) return res.status(400).json({ error: 'Song URL is required' });

    const response = await fetch(url, {
       headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5'
       }
    });
    if (!response.ok) throw new Error(`Failed to fetch song from hmonglyrics.net: ${response.status}`);
    
    const html = await response.text();
    const $ = cheerio.load(html);

    const title = $('.lyrics-title h1').text().trim() || 'Unknown Title';
    const artist = $('.lyrics-title h3 a').text().trim() || 'Unknown Artist';

    // Extract background image
    let backgroundImage = '';
    const bgDiv = $('.background-single-lyrics');
    if (bgDiv.length) {
       const style = bgDiv.attr('style') || '';
       const match = style.match(/background:\s*url\(([^)]+)\)/);
       if (match && match[1]) backgroundImage = match[1].replace(/['"]/g, '');
    }

    // Extract YouTube video
    let videoUrl = '';
    const iframe = $('.single-lyric-video iframe');
    if (iframe.length) {
       videoUrl = iframe.attr('src') || '';
    }

    const lyricDiv = $('.lyric-text');
    lyricDiv.find('.ads').remove();
    lyricDiv.find('script').remove();
    lyricDiv.find('ins').remove();
    lyricDiv.find('.related-list').remove();
    
    lyricDiv.find('br').replaceWith('\n');
    lyricDiv.find('p').each(function() {
       $(this).replaceWith($(this).text() + '\n\n');
    });

    const rawText = lyricDiv.text().trim();
    const cleanText = rawText.replace(/\n{3,}/g, '\n\n');

    res.json({
       title,
       artist,
       lyrics: cleanText,
       backgroundImage,
       videoUrl
    });
  } catch (error) {
    console.error('Lyrics fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch lyrics' });
  }
});

// AI Chat Endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { messages } = req.body;
    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ error: 'Messages array is required' });
    }

    // We can still try process.env.GEMINI_API_KEY first if it exists, but the user provided a massive array of keys.
    // Let's rely entirely on the API_KEYS array from config/apiKeys.js.
    if (!API_KEYS || API_KEYS.length === 0) {
      console.error('Missing API_KEYS');
      return res.status(500).json({ error: 'AI features are not configured properly.' });
    }
    
    // Format messages for Gemini API
    const contents = messages.map(msg => ({
      role: msg.role === 'user' ? 'user' : 'model',
      parts: [{ text: msg.content }]
    }));

    let response;
    let success = false;
    let lastError = null;
    let keysTried = 0;

    while (keysTried < API_KEYS.length && !success) {
      const apiKey = API_KEYS[currentKeyIndex];
      const ai = new GoogleGenAI({ apiKey });
      
      try {
        response = await ai.models.generateContent({
          model: 'gemini-2.5-flash',
          contents: contents,
          config: {
            systemInstruction: "You are a helpful, friendly AI assistant built into a media downloading app. Give concise and helpful answers.",
          }
        });
        success = true;
      } catch (error) {
        console.error(`Key at index ${currentKeyIndex} failed with status ${error.status}:`, error.message);
        lastError = error;
        
        // If it's a quota error, auth error, or server error, rotate to the next key
        if ([429, 403, 400, 503].includes(error.status)) {
          console.log(`Rotating to next key... (${keysTried + 1}/${API_KEYS.length} keys tried)`);
          currentKeyIndex = (currentKeyIndex + 1) % API_KEYS.length;
          keysTried++;
        } else {
          // Other unknown error, don't necessarily rotate, just break
          break;
        }
      }
    }

    if (success) {
      return res.json({ message: response.text });
    } else {
      console.error('All keys exhausted or failed.');
      let errorMessage = 'Failed to communicate with AI';
      
      if (lastError && lastError.status === 429) {
        errorMessage = 'The AI is currently receiving too many requests and all backup API keys have hit their rate limit. Please try again later.';
      } else if (lastError && [403, 400].includes(lastError.status)) {
        errorMessage = 'All backup API keys have been denied access or are invalid.';
      }
      
      return res.status(lastError?.status || 500).json({ error: errorMessage });
    }
  } catch (error) {
    console.error('AI Chat Error:', error);
    res.status(500).json({ error: 'Failed to communicate with AI' });
  }
});

// Webview Links Endpoints
app.get('/api/webview-links', async (req, res) => {
  try {
    const googleLinks = await getGoogleSheetLinks();
    if (googleLinks) {
      return res.json(googleLinks);
    }
    const links = await WebviewLink.findAll({ order: [['createdAt', 'DESC']] });
    res.json(links);
  } catch (err) {
    console.error('Fetch webview links error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/webview-links', async (req, res) => {
  try {
    const { title, url } = req.body;
    if (!title || !url) return res.status(400).json({ error: 'Title and URL are required' });

    const googleLink = await addGoogleSheetLink(title, url);
    if (googleLink) {
      return res.json(googleLink);
    }

    const newLink = await WebviewLink.create({ title, url });
    res.json(newLink);
  } catch (err) {
    console.error('Create webview link error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.delete('/api/webview-links/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const isGoogleDeleted = await deleteGoogleSheetLink(id);
    if (isGoogleDeleted) {
      return res.json({ success: true });
    }

    const deleted = await WebviewLink.destroy({ where: { id } });
    if (!deleted) return res.status(404).json({ error: 'Link not found in SQLite' });
    res.json({ success: true });
  } catch (err) {
    console.error('Delete webview link error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.put('/api/webview-links/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { title, url } = req.body;
    
    if (!title || !url) return res.status(400).json({ error: 'Title and URL are required' });

    const isGoogleUpdated = await updateGoogleSheetLink(id, title, url);
    if (isGoogleUpdated) {
      return res.json({ success: true, link: { id: parseInt(id), title, url } });
    }

    const link = await WebviewLink.findByPk(id);
    if (!link) return res.status(404).json({ error: 'Link not found in SQLite' });
    
    link.title = title;
    link.url = url;
    await link.save();
    
    res.json({ success: true, link });
  } catch (err) {
    console.error('Update webview link error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

// Typing Test Endpoints
app.get('/api/typing-lessons', async (req, res) => {
  try {
    const lessons = await getTypingLessons();
    res.json(lessons);
  } catch (err) {
    console.error('Fetch typing lessons error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/typing-lessons', async (req, res) => {
  try {
    const { title, content } = req.body;
    if (!title || !content) return res.status(400).json({ error: 'Title and content are required' });
    
    const newLesson = await addTypingLesson(title, content);
    if (newLesson) {
      res.json(newLesson);
    } else {
      res.status(500).json({ error: 'Failed to save lesson to Google Sheets' });
    }
  } catch (err) {
    console.error('Create typing lesson error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/typing-results', async (req, res) => {
  try {
    const { lessonTitle, cpm, wpm, accuracy } = req.body;
    if (!lessonTitle) return res.status(400).json({ error: 'Lesson Title is required' });
    
    const success = await saveTypingResult(lessonTitle, cpm, wpm, accuracy);
    if (success) {
      res.json({ success: true });
    } else {
      res.status(500).json({ error: 'Failed to save to Google Sheets' });
    }
  } catch (err) {
    console.error('Save typing result error:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

// Start Server
app.listen(PORT, async () => {
    await connectDB();
    await connectGoogleSheets();
    console.log(`🚀 Dedicated Backend server running on http://localhost:${PORT}`);
});

// Restart trigger
