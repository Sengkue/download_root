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
    
    let finalVideoPaths = [];
    let finalDurations = [];

    if (videoPaths.length === 1) {
      // Single video: We will use -stream_loop -1 so no duplication needed
      finalVideoPaths = [...videoPaths];
      finalDurations = [...baseDurations];
    } else {
      // Multiple videos: Adjust duration for overlapping transitions
      baseSequenceDuration -= (videoPaths.length - 1) * tDur;
      
      // Determine how many times to repeat the entire sequence to cover the target duration or audio length
      let repeatCount = 1;
      let targetLength = tTarget > 0 ? tTarget : audioDuration;
      
      if (targetLength > 0 && baseSequenceDuration > 0 && baseSequenceDuration < targetLength) {
        repeatCount = Math.ceil(targetLength / baseSequenceDuration);
        // Cap at 100 loops to prevent OS file limit errors (100 loops of a few videos = ~300 inputs)
        if (repeatCount > 100) repeatCount = 100;
      }
      
      // Rebuild the final sequence by duplicating the arrays
      for (let r = 0; r < repeatCount; r++) {
        finalVideoPaths.push(...videoPaths);
        finalDurations.push(...baseDurations);
      }
    }

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
    }

    if (tTarget > 0) {
       totalExpectedDuration = tTarget;
    } else if (audioDuration > 0) {
       totalExpectedDuration = audioDuration;
    }

    if (jobId) {
      progressMap.set(jobId, { progress: 5, status: 'Building montage filter graph...' });
    }

    // 2. Build FFmpeg arguments
    const ffmpegArgs = [];
    
    if (finalVideoPaths.length === 1) {
      // Loop the single video infinitely at the input level if audio is present OR targetDuration > 0
      if (audioPath || tTarget > 0) {
        ffmpegArgs.push('-stream_loop', '-1', '-fflags', '+genpts');
      }
      ffmpegArgs.push('-i', finalVideoPaths[0]);
    } else {
      // Multiple inputs, mapped to xfade
      for (const vPath of finalVideoPaths) {
        ffmpegArgs.push('-i', vPath);
      }
    }
    
    if (audioPath) {
      if (tTarget > 0) {
        // Loop audio if user explicitly set a target duration
        ffmpegArgs.push('-stream_loop', '-1');
      }
      ffmpegArgs.push('-vn', '-i', audioPath);
    }
    
    const audioInputIndex = finalVideoPaths.length; // The audio is the last input
    let filterComplex = '';
    const ptsMultiplier = 1 / speed;
    
    // Scale, crop, normalize framerate, and adjust speed for all inputs
    for (let i = 0; i < finalVideoPaths.length; i++) {
      filterComplex += `[${i}:v]scale=${resolution}:force_original_aspect_ratio=increase,crop=${resolution},setsar=1,fps=30,setpts=${ptsMultiplier}*PTS,format=yuv420p[v${i}]; `;
    }

    // 3. Transitions

    if (finalVideoPaths.length === 1) {
      // Single video, no transitions
      filterComplex += `[v0]null[vout]`;
    } else if (isNoneTransition) {
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
        
        const fallbackMap = {
          'smoothleft': 'slideleft', 'smoothright': 'slideright', 'glitch': 'pixelize',
          'smoothpie': 'circlecrop', 'zoomin': 'fade', 'hlslice': 'fade', 'dreamy': 'hblur'
        };
        if (fallbackMap[effect]) effect = fallbackMap[effect];
        if (effect === 'none') effect = 'fade'; // Fallback if random picker chooses none inside xfade logic
        
        const safeOffset = Math.max(0, currentOffset);
        
        filterComplex += `${lastNode}[v${i}]xfade=transition=${effect}:duration=${tDur}:offset=${safeOffset}${outNode}; `;
        
        lastNode = outNode;
        currentOffset += (finalDurations[i] - tDur);
      }
    }

    // Remove trailing semicolon/space
    filterComplex = filterComplex.trim().replace(/;$/, '');

    // Handle Audio Routing Logic
    const keepAudio = keepOriginalAudio === 'true';
    let hasAout = false;
    let audioOutputNode = '';

    if (finalVideoPaths.length === 1) {
      if (keepAudio && audioPath) {
        // Blend original video audio and new audio
        filterComplex += `; [0:a][1:a]amix=inputs=2:duration=longest[aout]`;
        hasAout = true;
        audioOutputNode = 'aout';
      } else if (keepAudio && !audioPath) {
        audioOutputNode = '0:a';
      } else if (!keepAudio && audioPath) {
        audioOutputNode = '1:a:0';
      }
    } else {
      if (audioPath) {
        audioOutputNode = `${audioInputIndex}:a:0`;
      }
    }

    // Fade out settings
    const fadeOutDuration = 1.5;
    const fadeOutStart = Math.max(0, (totalExpectedDuration || 10) - fadeOutDuration);

    // Apply video fade out
    filterComplex += `; [vout]fade=t=out:st=${fadeOutStart}:d=${fadeOutDuration}[vout_final]`;

    // Apply audio fade out if we have an audio output node
    if (audioOutputNode) {
      filterComplex += `; [${audioOutputNode}]afade=t=out:st=${fadeOutStart}:d=${fadeOutDuration}[aout_final]`;
    }

    ffmpegArgs.push('-filter_complex', filterComplex);
    ffmpegArgs.push('-map', '[vout_final]');
    
    if (audioOutputNode) {
      ffmpegArgs.push('-map', '[aout_final]');
    }

    ffmpegArgs.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p'); 
    
    if (audioPath || keepAudio) {
      ffmpegArgs.push('-c:a', 'aac', '-b:a', '192k');
    }
    
    if (tTarget > 0) {
      ffmpegArgs.push('-t', tTarget.toString());
    } else {
      ffmpegArgs.push('-shortest'); // End when the shortest stream (video montage or audio) ends
    }
    
    ffmpegArgs.push('-y', '-progress', 'pipe:1', outputPath);

    // Run the re-encode
    await runFFmpeg(ffmpegArgs, { jobId, expectedDuration: totalExpectedDuration || 10, progressOffset: 5, progressScale: 90 });

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
