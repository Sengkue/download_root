import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import ffmpegPath from 'ffmpeg-static';
import { runFFmpeg, probeAudioDuration } from './editor.controller.js';
import { progressMap } from './download.controller.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const tmpDir = path.resolve(__dirname, '../../../tmp');

if (!fs.existsSync(tmpDir)) {
  fs.mkdirSync(tmpDir, { recursive: true });
}

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

// Helper to get video duration using ffmpeg-static (no ffprobe needed)
async function getVideoDuration(filePath) {
  return new Promise((resolve) => {
    const probe = spawn(ffmpegPath, ['-i', filePath, '-hide_banner', '-f', 'null', '-']);
    let output = '';
    probe.stderr.on('data', (d) => { output += d.toString(); });
    probe.on('close', () => {
      const match = output.match(/Duration:\s*(\d{2}:\d{2}:\d{2}(?:\.\d+)?)/i);
      if (match) {
        resolve(parseTimeToSeconds(match[1]));
      } else {
        resolve(5); // fallback
      }
    });
    probe.on('error', () => resolve(5));
  });
}

export const mixVideo = async (req, res) => {
  const tmpFiles = [];

  try {
    if (!req.files || !req.files['video']) {
      return res.status(400).json({ error: 'Video file is required' });
    }

    const { jobId, videoSpeed = 1.0, transitionDuration = 1.0, transitionTypes, keepOriginalAudio, targetDuration, resolution = '1280:720' } = req.body;
    const videoFiles = req.files['video'];
    let audioPath = null;
    if (req.files['audio'] && req.files['audio'].length === 1) {
      audioPath = path.resolve(req.files['audio'][0].path);
      tmpFiles.push(audioPath);
    } else if (req.files['audio'] && req.files['audio'].length > 1) {
      if (jobId) progressMap.set(jobId, { progress: 0, status: 'Merging audio tracks...' });
      const tmpIdMerge = Date.now().toString() + '-' + Math.round(Math.random() * 1000);
      const mergedAudioPath = path.join(tmpDir, `merged-audio-${tmpIdMerge}.aac`);
      tmpFiles.push(mergedAudioPath);
      
      const audioArgs = [];
      let filterComplex = '';
      
      let concatInputs = '';
      for (let i = 0; i < req.files['audio'].length; i++) {
        const p = path.resolve(req.files['audio'][i].path);
        tmpFiles.push(p);
        audioArgs.push('-i', p);
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
    
    const videoPaths = videoFiles.map(f => {
      const p = path.resolve(f.path);
      tmpFiles.push(p);
      return p;
    });

    const tmpId = Date.now().toString() + '-' + Math.round(Math.random() * 1000);
    if (!fs.existsSync(tmpDir)) {
      fs.mkdirSync(tmpDir, { recursive: true });
    }
    const outputPath = path.join(tmpDir, `mixed-${tmpId}.mp4`);
    
    if (jobId) {
      progressMap.set(jobId, { progress: 2, status: 'Analyzing durations...' });
    }

    const tDur = parseFloat(transitionDuration);
    const speed = parseFloat(videoSpeed);
    const audioDuration = audioPath ? await probeAudioDuration(audioPath) : 0;
    const tTarget = parseFloat(targetDuration) || 0;

    // 1. Get adjusted durations for the base uploaded videos
    const baseDurations = [];
    let baseSequenceDuration = 0;
    
    for (const vPath of videoPaths) {
      const originalDur = await getVideoDuration(vPath);
      const adjustedDur = originalDur / speed;
      baseDurations.push(adjustedDur);
      baseSequenceDuration += adjustedDur;
    }
    
    // We only process the videos ONCE (no array duplication!)
    const finalVideoPaths = [...videoPaths];
    const finalDurations = [...baseDurations];

    let totalExpectedDuration = finalDurations.reduce((a, b) => a + b, 0);

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

    const isNoneTransition = transitionDuration <= 0 || (parsedTransitionTypes.length === 1 && parsedTransitionTypes[0] === 'none');

    if (finalVideoPaths.length > 1 && !isNoneTransition) {
      totalExpectedDuration -= (finalVideoPaths.length - 1) * tDur;
      baseSequenceDuration = totalExpectedDuration;
    }

    let targetLength = tTarget > 0 ? tTarget : audioDuration;

    // =============== SINGLE VIDEO ===============
    if (finalVideoPaths.length === 1) {
      if (jobId) {
        progressMap.set(jobId, { progress: 5, status: 'Building montage filter graph...' });
      }

      const ffmpegArgs = [];
      if (audioPath || targetLength > 0) {
        ffmpegArgs.push('-stream_loop', '-1', '-fflags', '+genpts');
      }
      ffmpegArgs.push('-i', finalVideoPaths[0]);
      
      if (audioPath) {
        if (targetLength > 0) ffmpegArgs.push('-stream_loop', '-1');
        ffmpegArgs.push('-vn', '-i', audioPath);
      }

      let filterComplex = '';
      const ptsMultiplier = 1 / speed;
      filterComplex += `[0:v]scale=${resolution}:force_original_aspect_ratio=increase,crop=${resolution},setsar=1,fps=30,setpts=${ptsMultiplier}*PTS,format=yuv420p[v0]; [v0]null[vout]; `;
      
      const keepAudio = keepOriginalAudio === 'true';
      let audioOutputNode = '';
      if (keepAudio && audioPath) {
        filterComplex += `[0:a][1:a]amix=inputs=2:duration=longest[aout]`;
        audioOutputNode = 'aout';
      } else if (keepAudio && !audioPath) {
        audioOutputNode = '0:a';
      } else if (!keepAudio && audioPath) {
        audioOutputNode = '1:a:0';
      }

      // NO VIDEO FADEOUT for performance (so we can use -c:v copy if we wanted, but we encode here due to speed/fps changes)
      const fadeOutDuration = 1.5;
      const fadeOutStart = Math.max(0, (targetLength || totalExpectedDuration || 10) - fadeOutDuration);

      if (audioOutputNode) {
        filterComplex += `; [${audioOutputNode}]afade=t=out:st=${fadeOutStart}:d=${fadeOutDuration}[aout_final]`;
      }

      const filterScriptPath = path.join(tmpDir, `filter-${tmpId}.txt`);
      fs.writeFileSync(filterScriptPath, filterComplex.trim().replace(/;$/, ''));
      tmpFiles.push(filterScriptPath);

      ffmpegArgs.push('-filter_complex_script', filterScriptPath);
      ffmpegArgs.push('-map', '[vout]');
      if (audioOutputNode) {
        ffmpegArgs.push('-map', '[aout_final]');
      }

      ffmpegArgs.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p'); 
      if (audioPath || keepAudio) {
        ffmpegArgs.push('-c:a', 'aac', '-b:a', '192k');
      }
      
      if (targetLength > 0) {
        ffmpegArgs.push('-t', targetLength.toString());
      } else {
        ffmpegArgs.push('-shortest');
      }
      
      ffmpegArgs.push('-y', '-progress', 'pipe:1', outputPath);

      await runFFmpeg(ffmpegArgs, { jobId, expectedDuration: targetLength || totalExpectedDuration || 10, progressOffset: 5, progressScale: 90 });

    // =============== MULTIPLE VIDEOS (TWO-PASS) ===============
    } else {
      
      // -- Pass 1: Build Base Sequence (No Audio) --
      const baseSequencePath = path.join(tmpDir, `basesequence-${tmpId}.mp4`);
      tmpFiles.push(baseSequencePath);

      if (jobId) {
        progressMap.set(jobId, { progress: 5, status: 'Rendering base transitions (Pass 1)...' });
      }

      const pass1Args = [];
      for (const vPath of finalVideoPaths) {
        pass1Args.push('-i', vPath);
      }

      let filterComplex = '';
      const ptsMultiplier = 1 / speed;
      for (let i = 0; i < finalVideoPaths.length; i++) {
        filterComplex += `[${i}:v]scale=${resolution}:force_original_aspect_ratio=increase,crop=${resolution},setsar=1,fps=30,setpts=${ptsMultiplier}*PTS,format=yuv420p[v${i}]; `;
      }

      if (isNoneTransition) {
        let concatNodes = '';
        for (let i = 0; i < finalVideoPaths.length; i++) {
          concatNodes += `[v${i}]`;
        }
        filterComplex += `${concatNodes}concat=n=${finalVideoPaths.length}:v=1:a=0[vout]`;
      } else {
        let lastNode = '[v0]';
        let currentOffset = finalDurations[0] - tDur;
        
        for (let i = 1; i < finalVideoPaths.length; i++) {
          const outNode = (i === finalVideoPaths.length - 1) ? '[vout]' : `[xf${i}]`;
          
          let effect = parsedTransitionTypes[Math.floor(Math.random() * parsedTransitionTypes.length)];
          const fallbackMap = { 'smoothleft': 'slideleft', 'smoothright': 'slideright', 'glitch': 'pixelize', 'smoothpie': 'circlecrop', 'zoomin': 'fade', 'hlslice': 'fade', 'dreamy': 'hblur' };
          if (fallbackMap[effect]) effect = fallbackMap[effect];
          if (effect === 'none') effect = 'fade';
          
          const safeOffset = Math.max(0, currentOffset);
          filterComplex += `${lastNode}[v${i}]xfade=transition=${effect}:duration=${tDur}:offset=${safeOffset}${outNode}; `;
          
          lastNode = outNode;
          currentOffset += (finalDurations[i] - tDur);
        }
      }

      const filterScriptPath = path.join(tmpDir, `filter-${tmpId}.txt`);
      fs.writeFileSync(filterScriptPath, filterComplex.trim().replace(/;$/, ''));
      tmpFiles.push(filterScriptPath);

      pass1Args.push(
        '-filter_complex_script', filterScriptPath,
        '-map', '[vout]',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
        '-y', '-progress', 'pipe:1', baseSequencePath
      );

      await runFFmpeg(pass1Args, { jobId, expectedDuration: baseSequenceDuration, progressOffset: 5, progressScale: 60 });

      // -- Pass 2: Loop Base Sequence & Add Audio --
      if (jobId) {
        progressMap.set(jobId, { progress: 65, status: 'Looping sequence over audio (Pass 2)...' });
      }

      const loopCount = Math.max(0, Math.ceil(targetLength / baseSequenceDuration) - 1);
      
      const pass2Args = [];
      pass2Args.push('-stream_loop', loopCount.toString(), '-i', baseSequencePath);

      if (audioPath) {
        if (targetLength > 0) pass2Args.push('-stream_loop', '-1');
        pass2Args.push('-vn', '-i', audioPath);
      }

      const fadeOutDuration = 1.5;
      const fadeOutStart = Math.max(0, (targetLength || baseSequenceDuration || 10) - fadeOutDuration);

      if (audioPath) {
        pass2Args.push('-filter_complex', `[1:a]afade=t=out:st=${fadeOutStart}:d=${fadeOutDuration}[aout]`);
        pass2Args.push('-map', '0:v', '-map', '[aout]');
      } else {
        pass2Args.push('-map', '0:v');
      }

      pass2Args.push('-c:v', 'copy'); // EXTREMELY FAST
      if (audioPath) pass2Args.push('-c:a', 'aac', '-b:a', '192k');

      if (targetLength > 0) {
        pass2Args.push('-t', targetLength.toString());
      } else {
        pass2Args.push('-shortest');
      }

      pass2Args.push('-y', '-progress', 'pipe:1', outputPath);

      await runFFmpeg(pass2Args, { jobId, expectedDuration: targetLength || baseSequenceDuration, progressOffset: 65, progressScale: 30 });
    }

    if (jobId) {
      progressMap.set(jobId, { progress: 100, status: 'Complete' });
    }

    res.download(outputPath, 'mixed_video.mp4', (err) => {
      if (err) console.error('Download error:', err);
      // Clean up
      tmpFiles.push(outputPath);
      tmpFiles.forEach(file => {
        try { if (fs.existsSync(file)) fs.unlinkSync(file); } catch(e) {}
      });
    });

  } catch (error) {
    console.error('Video mix failed:', error);
    tmpFiles.forEach(file => {
      try { if (fs.existsSync(file)) fs.unlinkSync(file); } catch(e) {}
    });
    
    const { jobId } = req.body;
    if (jobId) {
      progressMap.set(jobId, { progress: 0, status: 'Error', error: error.message });
    }
    
    res.status(500).json({ error: 'Video mix failed: ' + error.message });
  }
};
