import youtubeDl from 'youtube-dl-exec';
import ffmpegPath from 'ffmpeg-static';
import fs from 'fs';
import path from 'path';
import os from 'os';
import crypto from 'crypto';

export const progressMap = new Map();
export const activeJobsMap = new Map();

export const getProgress = (req, res) => {
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
};

export const downloadMedia = async (req, res) => {
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

      // Use a temp file so yt-dlp can do ffmpeg post-processing
      const tmpId = crypto.randomBytes(8).toString('hex');
      const tmpDir = os.tmpdir();
      const tmpBase = path.join(tmpDir, `yt-${tmpId}`);
      const tmpTemplate = `${tmpBase}_%(title)s.%(ext)s`;

      console.log(`[yt-dlp] Downloading ${type} to temp template: ${tmpTemplate}`);
      if (jobId) progressMap.set(jobId, { progress: 0, status: 'Starting download...' });

      try {
        let cleanUrl = url;
        try {
          const parsed = new URL(url);
          parsed.searchParams.delete('list');
          parsed.searchParams.delete('start_radio');
          parsed.searchParams.delete('index');
          cleanUrl = parsed.toString();
        } catch (_) {}

        const ytOptions = isAudio ? {
          extractAudio: true,
          audioFormat: 'mp3',
          audioQuality: 0,          // best quality
          noPlaylist: true,
          ffmpegLocation: `"${ffmpegPath}"`,
          jsRuntimes: 'node',
          o: tmpTemplate,
        } : {
          f: quality ? `"bestvideo[height<=${quality}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=${quality}]+bestaudio/best"` : '"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"',
          mergeOutputFormat: 'mp4',
          noPlaylist: true,
          ffmpegLocation: `"${ffmpegPath}"`,
          jsRuntimes: 'node',
          o: tmpTemplate,
        };

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

        const tmpDirFiles = fs.readdirSync(tmpDir);
        const outputFile = tmpDirFiles
          .filter(f => f.startsWith(`yt-${tmpId}_`))
          .map(f => path.join(tmpDir, f))
          .find(f => fs.statSync(f).isFile());

        if (!outputFile) {
          return res.status(500).json({ error: 'yt-dlp finished but the output file was not found.' });
        }

        console.log(`[yt-dlp] Output file found: ${outputFile}`);
        
        let actualFilename = `youtube-${type}.${ext}`;
        const parsedPath = path.parse(outputFile);
        const prefixLength = `yt-${tmpId}_`.length;
        if (parsedPath.name.length > prefixLength) {
           actualFilename = `${parsedPath.name.substring(prefixLength)}${parsedPath.ext}`;
        }
        
        const stat = fs.statSync(outputFile);

        res.setHeader('Content-Disposition', `attachment; filename*=UTF-8''${encodeURIComponent(actualFilename)}`);
        res.setHeader('Content-Type', isAudio ? 'audio/mpeg' : 'video/mp4');
        res.setHeader('Content-Length', stat.size.toString());
        res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition, Content-Length');

        const fileStream = fs.createReadStream(outputFile);
        fileStream.pipe(res);

        res.on('finish', () => {
          if (jobId) progressMap.delete(jobId);
          fs.unlink(outputFile, (err) => {
            if (err) console.error('Failed to clean up temp file:', err.message);
            else console.log(`[yt-dlp] Cleaned up temp file: ${outputFile}`);
          });
        });

      } catch (ytError) {
        if (jobId) progressMap.delete(jobId);
        const tmpDirFiles2 = fs.readdirSync(tmpDir);
        tmpDirFiles2.filter(f => f.startsWith(`yt-${tmpId}_`)).forEach(f => {
          try { fs.unlinkSync(path.join(tmpDir, f)); } catch (_) {}
        });
        
        // Log the full error to see stderr
        console.error('yt-dlp error full:', ytError);
        console.error('yt-dlp stderr:', ytError.stderr || ytError.message);
        
        if (!res.headersSent) {
          return res.status(500).json({ error: 'Failed to download. Please check the URL or try again later.' });
        }
      }
    } else {
      return res.status(400).json({ error: 'Invalid file type. Must be "image", "video", or "audio".' });
    }
  } catch (error) {
    console.error('Download error:', error);
    if (!res.headersSent) {
      res.status(500).json({ error: 'Internal Server Error while processing the download.' });
    }
  }
};

export const getInfo = async (req, res) => {
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
            qualities: [1080],
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
      qualities: uniqueHeights.length ? uniqueHeights : [1080, 720, 480, 360],
      duration: info.duration
    });
  } catch (error) {
    console.error('Info error:', error.message || error);
    res.status(500).json({ error: 'Failed to fetch video information.' });
  }
};
