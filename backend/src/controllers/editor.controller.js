import ffmpegPath from 'ffmpeg-static';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import os from 'os';
import crypto from 'crypto';
import { progressMap, activeJobsMap } from './download.controller.js';

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
export async function probeAudioDuration(audioPath) {
  return new Promise((resolve) => {
    const probe = spawn(ffmpegPath, ['-i', audioPath, '-hide_banner', '-f', 'null', '-']);
    let output = '';
    probe.stderr.on('data', (d) => { output += d.toString(); });
    probe.on('close', () => {
      const match = output.match(/Duration:\s*(\d{2}:\d{2}:\d{2}(?:\.\d+)?)/i);
      resolve(match ? parseTimeToSeconds(match[1]) : 0);
    });
    probe.on('error', () => resolve(0));
  });
}

/**
 * Run an FFmpeg command as a promise. Optionally tracks progress via progressMap.
 */
export function runFFmpeg(args, { jobId, expectedDuration, progressOffset = 0, progressScale = 100 } = {}) {
  return new Promise((resolve, reject) => {
    const proc = spawn(ffmpegPath, args);
    if (jobId) activeJobsMap.set(jobId, proc);
    
    let stdoutBuffer = '';
    let stderrBuffer = '';

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

    proc.stderr.on('data', (d) => {
      stderrBuffer += d.toString();
    });

    proc.on('close', (code) => {
      if (jobId) {
        activeJobsMap.delete(jobId);
        if (code === 0) {
          progressMap.set(jobId, {
            progress: progressOffset + progressScale,
            status: `Encoding video... ${Math.round(progressOffset + progressScale)}%`
          });
        }
      }
      
      // Treat SIGKILL / code 255 as a normal rejection but allow cleanup
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exited with code ${code}: ${stderrBuffer.slice(-500)}`));
    });
    proc.on('error', (err) => {
      if (jobId) activeJobsMap.delete(jobId);
      reject(err);
    });
  });
}

export const mergeMedia = async (req, res) => {
  const tmpFiles = []; // Track all temp files for cleanup
  let imageFiles = [];
  let audioFile = null;
  let audioPath = '';

  try {
    if (!req.files || !req.files['image'] || !req.files['audio'] || req.files['image'].length === 0 || req.files['audio'].length === 0) {
      return res.status(400).json({ error: 'Both image(s) and audio files are required' });
    }

    const { jobId, zoomDir = 'alternate', zoomSpeed = 'normal', imageDuration = 4, transitionTypes, transitionDuration: reqTransitionDuration = 1, targetDuration, resolution = '1280:720' } = req.body;
    imageFiles = req.files['image'];
    audioFile = req.files['audio'][0];
    audioPath = path.resolve(audioFile.path);

    const tmpId = crypto.randomBytes(8).toString('hex');
    const tmpDir = os.tmpdir();
    const outputPath = path.join(tmpDir, `merged-${tmpId}.mp4`);
    tmpFiles.push(outputPath);

    // ─── Pass 0: Merge Audio (if multiple) ───
    if (req.files['audio'].length > 1) {
      if (jobId) progressMap.set(jobId, { progress: 0, status: 'Merging audio tracks...' });
      const mergedAudioPath = path.join(tmpDir, `merged-audio-${tmpId}.aac`);
      tmpFiles.push(mergedAudioPath);
      
      const audioArgs = [];
      let filterComplex = '';
      
      let concatInputs = '';
      for (let i = 0; i < req.files['audio'].length; i++) {
        audioArgs.push('-i', path.resolve(req.files['audio'][i].path));
        filterComplex += `[${i}:a]aformat=sample_rates=48000:channel_layouts=stereo[a${i}];`;
        concatInputs += `[a${i}]`;
      }
      filterComplex += `${concatInputs}concat=n=${req.files['audio'].length}:v=0:a=1[aout]`;
      
      audioArgs.push(
        '-filter_complex', filterComplex,
        '-map', '[aout]',
        '-c:a', 'aac', '-b:a', '192k',
        '-y', mergedAudioPath
      );
      
      await runFFmpeg(audioArgs);
      audioPath = mergedAudioPath;
    }

    // ─── Probe audio duration ───
    if (jobId) progressMap.set(jobId, { progress: 0, status: 'Analyzing audio track...' });
    let audioDuration = await probeAudioDuration(audioPath);
    console.log(`[FFmpeg] Audio duration: ${audioDuration.toFixed(2)}s`);

    if (!audioDuration || audioDuration <= 0) {
      audioDuration = 10; // safe default if duration couldn't be probed
    }

    const tTarget = parseFloat(targetDuration) || 0;
    const targetLength = tTarget > 0 ? tTarget : audioDuration;

    // ─── Zoom settings (jitter-free Ken Burns) ───
    const FPS = 30; // 30fps perfectly divides 60Hz screens, drastically reducing panning judder

    // Zoom range: how much total zoom is applied (e.g. 0.3 = zoom from 1.0x to 1.3x)
    let zoomRange = 0.3; // Default to 30%
    if (zoomSpeed) {
      if (!isNaN(zoomSpeed)) {
        // Numeric slider value (0-100) -> Convert to 0.0 - 1.0 range
        zoomRange = Math.max(0.01, Math.min(parseFloat(zoomSpeed) / 100, 1.5));
      } else {
        // Fallback for old string values
        const zoomRangeMap = { slow: 0.15, normal: 0.3, fast: 0.5 };
        zoomRange = zoomRangeMap[zoomSpeed] || 0.3;
      }
    }

    // SUPER FIX for jitter:
    // 1. Remove `trunc()`! Truncation causes erratic 1-px jumps (1, 2, 2, 1) rather than smooth decimal rounding.
    const centerExpr = `x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2'`;

    // 2. Upscale to 8K (8192x4608) before zoompan! 
    // FFmpeg's zoompan crops to integer pixels. At 8K, a 1-pixel jump is invisible when downscaled to 1080p.
    const ZP_INPUT_W = 8192;
    const ZP_INPUT_H = 4608;

    const getZoompanFilter = (dir, durationFrames) => {
      // CRITICAL: Use absolute position formula (on/d) instead of incremental (zoom+step).
      if (dir === 'none') {
        return `zoompan=z='1':d=${durationFrames}:fps=${FPS}:s=${ZP_INPUT_W}x${ZP_INPUT_H}`;
      } else if (dir === 'out') {
        // Zoom out: start at (1+range), smoothly ease down to 1.0
        return `zoompan=z='if(lte(on,1),1+${zoomRange},1+${zoomRange}*(1-on/${durationFrames}))':${centerExpr}:d=${durationFrames}:fps=${FPS}:s=${ZP_INPUT_W}x${ZP_INPUT_H}`;
      } else {
        // Zoom in: start at 1.0, smoothly ease up to (1+range)
        return `zoompan=z='if(lte(on,1),1,1+${zoomRange}*on/${durationFrames})':${centerExpr}:d=${durationFrames}:fps=${FPS}:s=${ZP_INPUT_W}x${ZP_INPUT_H}`;
      }
    };

    // ══════════════════════════════════════════════════════════
    // SINGLE IMAGE — simple: zoom across the full audio length
    // ══════════════════════════════════════════════════════════
    if (imageFiles.length === 1) {
      const imagePath = path.resolve(imageFiles[0].path);
      const actualDir = zoomDir === 'alternate' ? 'in' : zoomDir;
      const totalFrames = Math.max(1, Math.ceil(targetLength * FPS));
      const singleZoompan = getZoompanFilter(actualDir, totalFrames);

      if (jobId) progressMap.set(jobId, { progress: 2, status: 'Encoding video... 2%' });

      const singleArgs = [
        '-loop', '1', '-t', '0.04', '-i', imagePath
      ];
      
      if (tTarget > 0) {
        singleArgs.push('-stream_loop', '-1');
      }
      singleArgs.push(
        '-i', audioPath,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'libx264', '-preset', 'veryfast',
        '-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p',
        '-vf', `scale=${ZP_INPUT_W}:${ZP_INPUT_H}:force_original_aspect_ratio=increase,crop=${ZP_INPUT_W}:${ZP_INPUT_H},setsar=1,${singleZoompan},scale=${resolution}:flags=bilinear,setpts=PTS-STARTPTS,format=yuv420p`,
        '-t', targetLength.toString(),
        '-y', '-progress', 'pipe:1',
        outputPath
      );

      await runFFmpeg(singleArgs, { jobId, expectedDuration: targetLength, progressOffset: 2, progressScale: 97 });

    // ══════════════════════════════════════════════════════════
    // MULTIPLE IMAGES — Two-Pass: create slideshow, then loop
    // ══════════════════════════════════════════════════════════
    } else {
      const durationPerImage = parseInt(imageDuration, 10) || 4;
      const transitionDuration = parseFloat(reqTransitionDuration) || 1;
      const durationFrames = durationPerImage * FPS;
      const slideshowPath = path.join(tmpDir, `slideshow-${tmpId}.mp4`);
      tmpFiles.push(slideshowPath);
      const allTransitions = [
        'fade', 'fadeblack', 'fadewhite', 'wipeleft', 'wiperight', 
        'circlecrop', 'rectcrop', 'distance', 'radial', 'pixelize', 'hblur'
      ];

      let parsedTransitionTypes = [];
      try {
        if (transitionTypes) {
          parsedTransitionTypes = JSON.parse(transitionTypes);
        }
      } catch (e) {
        console.warn('Failed to parse transitionTypes', e);
      }
      
      if (!Array.isArray(parsedTransitionTypes) || parsedTransitionTypes.length === 0) {
        parsedTransitionTypes = allTransitions;
      }

      // Fix: Only disable transitions if 'none' is the ONLY transition selected, or duration is 0
      const isNoneTransition = transitionDuration <= 0 || (parsedTransitionTypes.length === 1 && parsedTransitionTypes[0] === 'none');

      // Slideshow duration with overlapping transitions
      const slideshowDuration = isNoneTransition 
        ? (imageFiles.length * durationPerImage)
        : (imageFiles.length * durationPerImage) - ((imageFiles.length - 1) * transitionDuration);

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
        filterComplex += `[${i}:v]scale=${ZP_INPUT_W}:${ZP_INPUT_H}:force_original_aspect_ratio=increase,crop=${ZP_INPUT_W}:${ZP_INPUT_H},setsar=1,${zp},scale=${resolution}:flags=bilinear,setpts=PTS-STARTPTS,format=yuv420p[v${i}]; `;
      }


      if (isNoneTransition) {
        let concatNodes = '';
        for (let i = 0; i < imageFiles.length; i++) {
          concatNodes += `[v${i}]`;
        }
        filterComplex += `${concatNodes}concat=n=${imageFiles.length}:v=1:a=0[vout]`;
      } else {
        let lastNode = '[v0]';
        let currentOffset = durationPerImage - transitionDuration;
        for (let i = 1; i < imageFiles.length; i++) {
          const outNode = (i === imageFiles.length - 1) ? '[vout]' : `[xf${i}]`;
          
          let effect = parsedTransitionTypes[Math.floor(Math.random() * parsedTransitionTypes.length)];
          
          // Safe fallback for effects that might be requested by UI but unsupported by installed FFmpeg version
          const fallbackMap = {
            'smoothleft': 'slideleft',
            'smoothright': 'slideright',
            'glitch': 'pixelize',
            'smoothpie': 'circlecrop',
            'zoomin': 'fade',
            'hlslice': 'fade',
            'dreamy': 'hblur',
            'radial': 'fade'
          };
          if (fallbackMap[effect]) effect = fallbackMap[effect];
          if (effect === 'none') effect = 'fade';
          
          const safeOffset = Math.max(0, currentOffset);
          
          filterComplex += `${lastNode}[v${i}]xfade=transition=${effect}:duration=${transitionDuration}:offset=${safeOffset}${outNode}; `;
          
          lastNode = outNode;
          currentOffset += (durationPerImage - transitionDuration);
        }
      }

      pass1Args.push(
        '-filter_complex', filterComplex,
        '-map', '[vout]',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-r', FPS.toString(),   // Explicit output framerate
        '-crf', '20',           // High quality, fast encode
        '-preset', 'veryfast',  // Fast encoding
        '-y', '-progress', 'pipe:1',
        slideshowPath
      );

      await runFFmpeg(pass1Args, {
        jobId, expectedDuration: slideshowDuration, progressOffset: 2, progressScale: 60
      });

      console.log(`[FFmpeg] ✅ Pass 1 done: slideshow clip (${slideshowDuration.toFixed(1)}s)`);

      // ── Pass 2: Loop the slideshow over the full audio or target duration ──
      if (jobId) progressMap.set(jobId, { progress: 65, status: 'Looping slideshow over audio...' });

      const loopCount = Math.max(0, Math.ceil(targetLength / slideshowDuration) - 1);
      
      const pass2Args = [
        '-stream_loop', loopCount.toString(), '-i', slideshowPath
      ];
      
      if (tTarget > 0) {
        pass2Args.push('-stream_loop', '-1');
      }
      const fadeOutStart = Math.max(0, targetLength - 2);

      pass2Args.push(
        '-i', audioPath,
        '-filter_complex', `[1:a]afade=t=out:st=${fadeOutStart}:d=2[aout]`,
        '-map', '0:v', '-map', '[aout]',
        '-c:v', 'copy',         // NO re-encoding! Preserves exact quality from Pass 1
        '-c:a', 'aac', '-b:a', '192k',
        '-t', targetLength.toString(),
        '-y', '-progress', 'pipe:1',
        outputPath
      );

      await runFFmpeg(pass2Args, { jobId, expectedDuration: targetLength, progressOffset: 65, progressScale: 34 });

      console.log(`[FFmpeg] ✅ Pass 2 done: looped over audio (${targetLength.toFixed(1)}s)`);
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
      setTimeout(() => {
        if (jobId) progressMap.delete(jobId);
      }, 5000);
      cleanup(req, imageFiles, audioPath, tmpFiles);
    });

  } catch (error) {
    console.error('[FFmpeg] Error:', error.message || error);
    if (req.body?.jobId) {
      progressMap.set(req.body.jobId, { progress: 0, status: 'Error: encoding failed' });
      setTimeout(() => progressMap.delete(req.body.jobId), 5000);
    }
    cleanup(req, imageFiles || [], audioPath || '', tmpFiles);
    if (!res.headersSent) {
      res.status(500).json({ error: error.message || 'Failed to generate video' });
    }
  }
};

export const cancelJob = (req, res) => {
  const { jobId } = req.body;
  if (!jobId) return res.status(400).json({ error: 'jobId is required' });
  
  const proc = activeJobsMap.get(jobId);
  if (proc) {
    proc.kill('SIGKILL');
    activeJobsMap.delete(jobId);
    progressMap.set(jobId, { progress: 0, status: 'Cancelled by user' });
    return res.json({ message: 'Job cancelled successfully' });
  } else {
    return res.status(404).json({ message: 'Job not found or already finished' });
  }
};

/**
 * Clean up all temporary files (uploaded images, audio, intermediate clips).
 */
function cleanup(req, imageFiles, audioPath, tmpFiles) {
  if (imageFiles) {
    for (const img of imageFiles) {
      try { fs.unlinkSync(path.resolve(img.path)); } catch (_) {}
    }
  }
  
  if (req.files && req.files['audio']) {
    for (const a of req.files['audio']) {
      try { fs.unlinkSync(path.resolve(a.path)); } catch (_) {}
    }
  } else if (audioPath && !tmpFiles.includes(audioPath)) {
    try { fs.unlinkSync(audioPath); } catch (_) {}
  }
  if (tmpFiles) {
    for (const f of tmpFiles) {
      try { fs.unlinkSync(f); } catch (_) {}
    }
  }
}
