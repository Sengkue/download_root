import ffmpegPath from 'ffmpeg-static';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import os from 'os';
import crypto from 'crypto';
import { progressMap } from './download.controller.js';

/**
 * Parse time value to seconds (supports HH:MM:SS.ms and raw microseconds).
 */
function parseTimeToSeconds(val) {
  if (!val) return 0;
  if (/^\d+$/.test(val)) return parseInt(val, 10) / 1_000_000;
  const parts = val.split(':');
  if (parts.length === 3) {
    return (parseFloat(parts[0]) || 0) * 3600 +
           (parseFloat(parts[1]) || 0) * 60 +
           (parseFloat(parts[2]) || 0);
  }
  return parseFloat(val) || 0;
}

/**
 * Probe an audio file's duration in seconds using FFmpeg.
 */
async function probeAudioDuration(audioPath) {
  return new Promise((resolve) => {
    const probe = spawn(ffmpegPath, ['-i', audioPath, '-hide_banner', '-f', 'null', '-']);
    let output = '';
    probe.stderr.on('data', (d) => { output += d.toString(); });
    probe.on('close', () => {
      const match = output.match(/Duration: (\d{2}:\d{2}:\d{2}\.\d{2})/);
      resolve(match ? parseTimeToSeconds(match[1]) : 0);
    });
    probe.on('error', () => resolve(0));
  });
}

/**
 * Run an FFmpeg command as a promise. Optionally tracks progress via progressMap.
 */
function runFFmpeg(args, { jobId, expectedDuration, progressOffset = 0, progressScale = 100 } = {}) {
  return new Promise((resolve, reject) => {
    const proc = spawn(ffmpegPath, args);
    let stdoutBuffer = '';

    proc.stdout.on('data', (data) => {
      stdoutBuffer += data.toString();
      const lines = stdoutBuffer.split('\n');
      stdoutBuffer = lines.pop();

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('out_time_us=') && jobId && expectedDuration > 0) {
          const us = parseInt(trimmed.split('=')[1], 10);
          if (!isNaN(us) && us > 0) {
            let pct = (us / 1_000_000 / expectedDuration) * progressScale + progressOffset;
            pct = Math.max(progressOffset, Math.min(pct, progressOffset + progressScale));
            progressMap.set(jobId, {
              progress: parseFloat(pct.toFixed(1)),
              status: `Encoding video... ${Math.round(pct)}%`
            });
          }
        }
      }
    });

    proc.stderr.on('data', () => { /* suppress */ });

    proc.on('close', (code) => {
      // When this pass finishes, immediately set progress to the end of its range
      if (jobId && code === 0) {
        progressMap.set(jobId, {
          progress: progressOffset + progressScale,
          status: `Encoding video... ${Math.round(progressOffset + progressScale)}%`
        });
      }
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exited with code ${code}`));
    });
    proc.on('error', reject);
  });
}

export const mergeMedia = async (req, res) => {
  const tmpFiles = []; // Track all temp files for cleanup

  try {
    if (!req.files || !req.files['image'] || !req.files['audio']) {
      return res.status(400).json({ error: 'Both image(s) and audio files are required' });
    }

    const { jobId, zoomDir = 'alternate', zoomSpeed = 'normal' } = req.body;
    const imageFiles = req.files['image'];
    const audioFile = req.files['audio'][0];
    const audioPath = path.resolve(audioFile.path);

    const tmpId = crypto.randomBytes(8).toString('hex');
    const tmpDir = os.tmpdir();
    const outputPath = path.join(tmpDir, `merged-${tmpId}.mp4`);
    tmpFiles.push(outputPath);

    // ─── Probe audio duration ───
    if (jobId) progressMap.set(jobId, { progress: 0, status: 'Analyzing audio track...' });
    const audioDuration = await probeAudioDuration(audioPath);
    console.log(`[FFmpeg] Audio duration: ${audioDuration.toFixed(2)}s`);

    // ─── Zoom settings ───
    const FPS = 25;
    const speedMap = { slow: 0.0005, normal: 0.0015, fast: 0.003 };
    const zoomStep = speedMap[zoomSpeed] || speedMap.normal;
    const centerMath = `x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'`;

    const getZoompanFilter = (dir, durationFrames) => {
      if (dir === 'none') {
        return `zoompan=z='1':d=${durationFrames}:fps=${FPS}:s=1280x720`;
      } else if (dir === 'out') {
        return `zoompan=z='if(eq(on,1),1.5,max(1.0,zoom-${zoomStep}))':${centerMath}:d=${durationFrames}:fps=${FPS}:s=1280x720`;
      } else {
        return `zoompan=z='min(zoom+${zoomStep},1.5)':${centerMath}:d=${durationFrames}:fps=${FPS}:s=1280x720`;
      }
    };

    // ══════════════════════════════════════════════════════════
    // SINGLE IMAGE — simple: zoom across the full audio length
    // ══════════════════════════════════════════════════════════
    if (imageFiles.length === 1) {
      const imagePath = path.resolve(imageFiles[0].path);
      const actualDir = zoomDir === 'alternate' ? 'in' : zoomDir;
      const totalFrames = Math.max(1, Math.ceil(audioDuration * FPS));
      const singleZoompan = getZoompanFilter(actualDir, totalFrames);

      if (jobId) progressMap.set(jobId, { progress: 2, status: 'Encoding video... 2%' });

      await runFFmpeg([
        '-loop', '1', '-t', '0.04', '-i', imagePath,
        '-i', audioPath,
        '-c:v', 'libx264', '-tune', 'stillimage',
        '-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p',
        '-vf', `scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1,${singleZoompan},setpts=PTS-STARTPTS,format=yuv420p`,
        '-shortest', '-y', '-progress', 'pipe:1',
        outputPath
      ], { jobId, expectedDuration: audioDuration, progressOffset: 2, progressScale: 97 });

    // ══════════════════════════════════════════════════════════
    // MULTIPLE IMAGES — Two-Pass: create slideshow, then loop
    // ══════════════════════════════════════════════════════════
    } else {
      const durationPerImage = 4;
      const transitionDuration = 1;
      const durationFrames = durationPerImage * FPS;
      const slideshowPath = path.join(tmpDir, `slideshow-${tmpId}.mp4`);
      tmpFiles.push(slideshowPath);

      // Slideshow duration with overlapping transitions
      const slideshowDuration = (imageFiles.length * durationPerImage) - ((imageFiles.length - 1) * transitionDuration);

      // ── Pass 1: Build the slideshow clip (no audio) ──
      if (jobId) progressMap.set(jobId, { progress: 2, status: 'Creating slideshow effects...' });

      const pass1Args = [];
      // Feed exactly 1 frame per image
      for (const img of imageFiles) {
        pass1Args.push('-loop', '1', '-t', '0.04', '-i', path.resolve(img.path));
      }

      let filterComplex = '';
      for (let i = 0; i < imageFiles.length; i++) {
        let currentDir = zoomDir;
        if (zoomDir === 'alternate') {
          currentDir = (i % 2 === 0) ? 'in' : 'out';
        }
        const zp = getZoompanFilter(currentDir, durationFrames);
        filterComplex += `[${i}:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1,${zp},setpts=PTS-STARTPTS,format=yuv420p[v${i}]; `;
      }

      let lastNode = '[v0]';
      let currentOffset = durationPerImage - transitionDuration;
      for (let i = 1; i < imageFiles.length; i++) {
        const outNode = (i === imageFiles.length - 1) ? '[vout]' : `[xf${i}]`;
        filterComplex += `${lastNode}[v${i}]xfade=transition=fade:duration=${transitionDuration}:offset=${currentOffset}${outNode}`;
        if (i < imageFiles.length - 1) filterComplex += '; ';
        lastNode = outNode;
        currentOffset += (durationPerImage - transitionDuration);
      }

      pass1Args.push(
        '-filter_complex', filterComplex,
        '-map', '[vout]',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-r', FPS.toString(),   // Explicit output framerate
        '-crf', '18',           // High quality (lower = better, 18 is visually lossless)
        '-preset', 'medium',    // Good quality/speed balance
        '-y', '-progress', 'pipe:1',
        slideshowPath
      );

      await runFFmpeg(pass1Args, {
        jobId, expectedDuration: slideshowDuration, progressOffset: 2, progressScale: 60
      });

      console.log(`[FFmpeg] ✅ Pass 1 done: slideshow clip (${slideshowDuration.toFixed(1)}s)`);

      // ── Pass 2: Loop the slideshow over the full audio ──
      if (jobId) progressMap.set(jobId, { progress: 65, status: 'Looping slideshow over audio...' });

      await runFFmpeg([
        '-stream_loop', '-1', '-i', slideshowPath,
        '-i', audioPath,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'copy',         // NO re-encoding! Preserves exact quality from Pass 1
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest', '-y', '-progress', 'pipe:1',
        outputPath
      ], { jobId, expectedDuration: audioDuration, progressOffset: 65, progressScale: 34 });

      console.log(`[FFmpeg] ✅ Pass 2 done: looped over audio (${audioDuration.toFixed(1)}s)`);
    }

    // ─── Send the result ───
    if (jobId) progressMap.set(jobId, { progress: 100, status: 'Video ready!' });
    console.log(`[FFmpeg] ✅ Final video: ${outputPath}`);

    const stat = fs.statSync(outputPath);
    res.setHeader('Content-Disposition', `attachment; filename="generated-slideshow.mp4"`);
    res.setHeader('Content-Type', 'video/mp4');
    res.setHeader('Content-Length', stat.size.toString());
    res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition, Content-Length');

    const fileStream = fs.createReadStream(outputPath);
    fileStream.pipe(res);

    res.on('finish', () => {
      if (jobId) progressMap.delete(jobId);
      cleanup(imageFiles, audioPath, tmpFiles);
    });

  } catch (error) {
    console.error('[FFmpeg] Error:', error.message || error);
    if (req.body?.jobId) {
      progressMap.set(req.body.jobId, { progress: 0, status: 'Error: encoding failed' });
      setTimeout(() => progressMap.delete(req.body.jobId), 5000);
    }
    cleanup(imageFiles || [], audioPath || '', tmpFiles);
    if (!res.headersSent) {
      res.status(500).json({ error: 'Failed to generate video' });
    }
  }
};

/**
 * Clean up all temporary files (uploaded images, audio, intermediate clips).
 */
function cleanup(imageFiles, audioPath, tmpFiles) {
  if (imageFiles) {
    for (const img of imageFiles) {
      try { fs.unlinkSync(path.resolve(img.path)); } catch (_) {}
    }
  }
  if (audioPath) {
    try { fs.unlinkSync(audioPath); } catch (_) {}
  }
  if (tmpFiles) {
    for (const f of tmpFiles) {
      try { fs.unlinkSync(f); } catch (_) {}
    }
  }
}
