import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import ffmpegPath from 'ffmpeg-static';
import { runFFmpeg, probeAudioDuration } from './editor.controller.js';
import { progressMap } from './download.controller.js';

// Default motivational quotes used when user doesn't supply custom ones
const DEFAULT_QUOTES = [
  'Stay focused. You are doing great!',
  'Deep Work Session in Progress...',
  'One task at a time. You got this!',
  'Discipline equals freedom.',
  'Small steps lead to big results.',
  'Focus on progress, not perfection.',
  'Your future self will thank you.',
  'Eliminate distractions. Stay sharp.',
  'Every minute counts. Keep going!',
  'The secret of getting ahead is getting started.',
  'Breathe. Focus. Execute.',
  'Hard work beats talent when talent doesn\'t work hard.',
  'Almost there! Keep pushing!',
  'Success is built one session at a time.',
  'You are stronger than your excuses.',
  'This is your time to shine.',
  'Embrace the grind.',
  'Break coming soon. Stay strong!',
  'Turn your can\'ts into cans.',
  'Consistency is the key to mastery.'
];

/**
 * Escape text for FFmpeg drawtext filter.
 * Since we pass args via spawn() (no shell), we only need one level of FFmpeg escaping.
 */
export function escapeDrawtext(text) {
  return text
    .replace(/\\/g, '\\\\')
    .replace(/:/g, '\\:')
    .replace(/'/g, '’')
    .replace(/;/g, '\\;')
    .replace(/%/g, '%%')
    .replace(/,/g, '\\,');
}

/**
 * Build the complex filter string for dynamic overlays (Pomodoro timer, Quotes, Logo).
 * Returns { filterString, nextInputIndex, hasOverlays }
 * All escaping uses single-backslash level since spawn() passes args directly (no shell).
 */
export function buildOverlayFilters(params, totalDuration, extraInputStartIndex) {
  const {
    timerEnabled, timerMinutes, timerBreakMinutes, timerPosition, timerShowProgress, timerWithBreak,
    logoEnabled, logoPath, logoPosition, logoOpacity, logoSize,
    quotesEnabled, quotesInterval, quotesDuration, quotesPosition, customQuotes
  } = params;

  let filters = '';
  let currentNode = 'vbase';
  let nextNodeId = 0;
  const extraInputs = [];
  let inputIdx = extraInputStartIndex;

  const getNextNode = (isFinal) => isFinal ? 'vout' : `ovl${nextNodeId++}`;

  const enabledOverlays = [];
  if (timerEnabled) enabledOverlays.push('timer');
  if (logoEnabled && logoPath) enabledOverlays.push('logo');
  if (quotesEnabled) enabledOverlays.push('quotes');

  if (enabledOverlays.length === 0) {
    return { filters: `[${currentNode}]null[vout]`, extraInputs: [], inputIndexOffset: 0 };
  }

  // ======== LOGO WATERMARK ========
  if (logoEnabled && logoPath) {
    const isLast = enabledOverlays[enabledOverlays.length - 1] === 'logo';
    const outNode = getNextNode(isLast);
    extraInputs.push('-i', logoPath);
    const logoInputIdx = inputIdx++;

    const size = parseInt(logoSize) || 120;
    const opacity = parseFloat(logoOpacity) || 0.7;

    let overlayX, overlayY;
    switch (logoPosition) {
      case 'top-left':     overlayX = '20'; overlayY = '20'; break;
      case 'top-right':    overlayX = 'W-w-20'; overlayY = '20'; break;
      case 'bottom-left':  overlayX = '20'; overlayY = 'H-h-20'; break;
      case 'bottom-right': default: overlayX = 'W-w-20'; overlayY = 'H-h-20'; break;
    }

    filters += `[${logoInputIdx}:v]scale=${size}:-1,format=rgba,colorchannelmixer=aa=${opacity}[logo_scaled]; `;
    filters += `[${currentNode}][logo_scaled]overlay=${overlayX}:${overlayY}[${outNode}]; `;
    currentNode = outNode;
  }

  // ======== POMODORO TIMER ========
  if (timerEnabled) {
    const isLast = enabledOverlays[enabledOverlays.length - 1] === 'timer';
    const minutes = parseInt(timerMinutes) || 25;
    const bMinutes = parseInt(timerBreakMinutes) || 5;
    const cycleSec = minutes * 60;
    const breakSec = timerWithBreak ? (bMinutes * 60) : 0;
    const totalCycleSec = cycleSec + breakSec;

    let timerX, timerY;
    switch (timerPosition) {
      case 'top-left':     timerX = '30'; timerY = '30'; break;
      case 'top-right':    timerX = 'w-tw-30'; timerY = '30'; break;
      case 'top-center':   timerX = '(w-tw)/2'; timerY = '30'; break;
      case 'bottom-left':  timerX = '30'; timerY = 'h-th-60'; break;
      case 'bottom-right': timerX = 'w-tw-30'; timerY = 'h-th-60'; break;
      default:             timerX = 'w-tw-30'; timerY = '30'; break;
    }

    let timerText;
    if (breakSec > 0) {
      timerText = `%{eif\\: if(lt(mod(t\\,${totalCycleSec})\\,${cycleSec})\\, floor((${cycleSec}-mod(t\\,${totalCycleSec}))/60)\\, floor((${totalCycleSec}-mod(t\\,${totalCycleSec}))/60) ) \\:d\\:2}\\:%{eif\\: if(lt(mod(t\\,${totalCycleSec})\\,${cycleSec})\\, mod(floor(${cycleSec}-mod(t\\,${totalCycleSec}))\\,60)\\, mod(floor(${totalCycleSec}-mod(t\\,${totalCycleSec}))\\,60) ) \\:d\\:2}`;
    } else {
      timerText = `%{eif\\: floor((${cycleSec}-mod(t\\,${cycleSec}))/60) \\:d\\:2}\\:%{eif\\: mod(floor(${cycleSec}-mod(t\\,${cycleSec}))\\,60) \\:d\\:2}`;
    }

    const timerNode1 = getNextNode(false);
    filters += `[${currentNode}]drawtext=text='${timerText}':`;
    filters += `fontsize=48:fontcolor=white:`;
    filters += `x=${timerX}:y=${timerY}:`;
    filters += `box=1:boxcolor=black@0.55:boxborderw=14:`;
    filters += `fontfile='C\\:/Windows/Fonts/consola.ttf'`;
    filters += `[${timerNode1}]; `;
    currentNode = timerNode1;

    if (breakSec > 0) {
      const breakNode = getNextNode(false);
      filters += `[${currentNode}]drawtext=text='BREAK':`;
      filters += `fontsize=28:fontcolor=0x7CFC00:`;
      filters += `x=${timerX}:y=${timerY}+60:`;
      filters += `box=1:boxcolor=black@0.5:boxborderw=8:`;
      filters += `fontfile='C\\:/Windows/Fonts/consola.ttf':`;
      filters += `enable='gte(mod(t\\,${totalCycleSec})\\,${cycleSec})'`;
      filters += `[${breakNode}]; `;
      currentNode = breakNode;
    }

    if (timerShowProgress) {
      const bgNode = getNextNode(false);
      const barY = timerPosition?.startsWith('bottom') ? 'ih-12' : (parseInt(timerY) || 30) + 75;
      filters += `[${currentNode}]drawbox=x=0:y=${barY}:w=iw:h=8:color=black@0.4:t=fill[${bgNode}]; `;
      currentNode = bgNode;

      if (breakSec > 0) {
        // Work phase: purple bar
        const workNode = getNextNode(false);
        filters += `[${currentNode}]drawbox=x=0:y=${barY}:w='mod(t\\,${totalCycleSec})/${cycleSec}*iw':h=8:color=0x845EC2@0.9:t=fill:enable='lt(mod(t\\,${totalCycleSec})\\,${cycleSec})'[${workNode}]; `;
        currentNode = workNode;

        // Break phase: green bar
        const breakBarNode = getNextNode(isLast);
        filters += `[${currentNode}]drawbox=x=0:y=${barY}:w='(mod(t\\,${totalCycleSec})-${cycleSec})/${breakSec}*iw':h=8:color=0x7CFC00@0.9:t=fill:enable='gte(mod(t\\,${totalCycleSec})\\,${cycleSec})'[${breakBarNode}]; `;
        currentNode = breakBarNode;
      } else {
        const progressNode = getNextNode(isLast);
        filters += `[${currentNode}]drawbox=x=0:y=${barY}:w='mod(t\\,${cycleSec})/${cycleSec}*iw':h=8:color=0x845EC2@0.9:t=fill[${progressNode}]; `;
        currentNode = progressNode;
      }
    } else if (isLast) {
      const finalNode = getNextNode(true);
      filters += `[${currentNode}]null[${finalNode}]; `;
      currentNode = finalNode;
    }
  }

  // ======== DYNAMIC QUOTES ========
  if (quotesEnabled) {
    const interval = (parseInt(quotesInterval) || 10) * 60;
    const duration = parseInt(quotesDuration) || 15;
    const fadeTime = 2;

    let quotes = DEFAULT_QUOTES;
    if (customQuotes) {
      try {
        const parsed = JSON.parse(customQuotes);
        if (Array.isArray(parsed) && parsed.length > 0) {
          quotes = parsed.filter(q => q && q.trim().length > 0);
        }
      } catch (e) {
        const lines = customQuotes.split('\n').filter(l => l.trim().length > 0);
        if (lines.length > 0) quotes = lines;
      }
    }

    let quoteY;
    switch (quotesPosition) {
      case 'top':    quoteY = 'h*0.15'; break;
      case 'center': quoteY = '(h-th)/2'; break;
      case 'bottom': default: quoteY = 'h*0.82'; break;
    }

    const maxQuotes = Math.floor(totalDuration / interval);
    const numQuotes = Math.min(maxQuotes, 60);

    for (let i = 0; i < numQuotes; i++) {
      const startTime = (i + 1) * interval - duration;
      const endTime = startTime + duration;
      if (startTime < 0) continue;

      const quote = quotes[i % quotes.length];
      const escapedQuote = escapeDrawtext(quote);
      const isLast = enabledOverlays[enabledOverlays.length - 1] === 'quotes' && i === numQuotes - 1;
      const outNode = getNextNode(isLast);

      const alphaExpr = `if(lt(t\\,${startTime + fadeTime})\\,(t-${startTime})/${fadeTime}\\,if(gt(t\\,${endTime - fadeTime})\\,(${endTime}-t)/${fadeTime}\\,1))`;

      filters += `[${currentNode}]drawtext=text='${escapedQuote}':`;
      filters += `fontsize=32:fontcolor=white:alpha='${alphaExpr}':`;
      filters += `x=(w-tw)/2:y=${quoteY}:`;
      filters += `box=1:boxcolor=black@0.45:boxborderw=12:`;
      filters += `fontfile='C\\:/Windows/Fonts/consola.ttf':`;
      filters += `enable='between(t\\,${startTime}\\,${endTime})'`;
      filters += `[${outNode}]; `;
      currentNode = outNode;
    }

    if (numQuotes === 0 && enabledOverlays[enabledOverlays.length - 1] === 'quotes') {
      const finalNode = 'vout';
      filters += `[${currentNode}]null[${finalNode}]; `;
      currentNode = finalNode;
    }
  }

  return { filters, extraInputs, inputIndexOffset: inputIdx - extraInputStartIndex };
}

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

    const { jobId, videoSpeed = 1.0, transitionDuration = 1.0, transitionTypes, keepOriginalAudio, targetDuration, resolution = '1280:720',
      // Overlay parameters
      overlayTimerEnabled, overlayTimerMinutes, overlayTimerBreakMinutes, overlayTimerPosition, overlayTimerShowProgress, overlayTimerWithBreak,
      overlayLogoEnabled, overlayLogoPosition, overlayLogoOpacity, overlayLogoSize,
      overlayQuotesEnabled, overlayQuotesInterval, overlayQuotesDuration, overlayQuotesPosition, overlayQuotesCustom
    } = req.body;
    const videoFiles = req.files['video'];

    // Logo file handling
    let logoPath = null;
    if (req.files['logo'] && req.files['logo'].length === 1) {
      logoPath = path.resolve(req.files['logo'][0].path);
      tmpFiles.push(logoPath);
    }

    // Build overlay params object
    const overlayParams = {
      timerEnabled: overlayTimerEnabled === 'true',
      timerMinutes: overlayTimerMinutes,
      timerBreakMinutes: overlayTimerBreakMinutes,
      timerPosition: overlayTimerPosition || 'top-right',
      timerShowProgress: overlayTimerShowProgress === 'true',
      timerWithBreak: overlayTimerWithBreak === 'true',
      logoEnabled: overlayLogoEnabled === 'true',
      logoPath: logoPath,
      logoPosition: overlayLogoPosition || 'bottom-right',
      logoOpacity: overlayLogoOpacity || '0.7',
      logoSize: overlayLogoSize || '120',
      quotesEnabled: overlayQuotesEnabled === 'true',
      quotesInterval: overlayQuotesInterval || '10',
      quotesDuration: overlayQuotesDuration || '15',
      quotesPosition: overlayQuotesPosition || 'bottom',
      customQuotes: overlayQuotesCustom || null
    };
    const hasAnyOverlay = overlayParams.timerEnabled || (overlayParams.logoEnabled && logoPath) || overlayParams.quotesEnabled;
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
        progressMap.set(jobId, { progress: 5, status: hasAnyOverlay ? 'Building overlay filter graph...' : 'Building montage filter graph...' });
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

      // Count existing inputs: video=0, audio=1 (if present)
      let inputCount = 1 + (audioPath ? 1 : 0);

      let filterComplex = '';
      const ptsMultiplier = 1 / speed;

      if (hasAnyOverlay) {
        // With overlays: pipe through vbase → overlay chain → vout
        filterComplex += `[0:v]scale=${resolution}:force_original_aspect_ratio=increase,crop=${resolution},setsar=1,fps=30,setpts=${ptsMultiplier}*PTS,format=yuv420p[vbase]; `;
        
        const effectiveDuration = targetLength || totalExpectedDuration || 600;
        const overlay = buildOverlayFilters(overlayParams, effectiveDuration, inputCount);
        filterComplex += overlay.filters + ' ';
        // Add extra inputs (logo) to ffmpegArgs
        for (const arg of overlay.extraInputs) {
          ffmpegArgs.push(arg);
        }
      } else {
        // No overlays: simple passthrough
        filterComplex += `[0:v]scale=${resolution}:force_original_aspect_ratio=increase,crop=${resolution},setsar=1,fps=30,setpts=${ptsMultiplier}*PTS,format=yuv420p[v0]; [v0]null[vout]; `;
      }
      
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

      // Audio fadeout
      const fadeOutDuration = 1.5;
      const fadeOutStart = Math.max(0, (targetLength || totalExpectedDuration || 10) - fadeOutDuration);

      if (audioOutputNode) {
        filterComplex += `; [${audioOutputNode}]afade=t=out:st=${fadeOutStart}:d=${fadeOutDuration}[aout_final]`;
      }

      const filterScriptPath = path.join(tmpDir, `filter-${tmpId}.txt`);
      fs.writeFileSync(filterScriptPath, filterComplex.replace(/;\s*;/g, ';').trim().replace(/;$/, ''));
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
      fs.writeFileSync(filterScriptPath, filterComplex.replace(/;\s*;/g, ';').trim().replace(/;$/, ''));
      tmpFiles.push(filterScriptPath);

      pass1Args.push(
        '-filter_complex_script', filterScriptPath,
        '-map', '[vout]',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
        '-y', '-progress', 'pipe:1', baseSequencePath
      );

      await runFFmpeg(pass1Args, { jobId, expectedDuration: baseSequenceDuration, progressOffset: 5, progressScale: 60 });

      // -- Pass 2: Loop Base Sequence, Add Audio & Overlays --
      if (jobId) {
        progressMap.set(jobId, { progress: 65, status: hasAnyOverlay ? 'Adding overlays & audio (Pass 2)...' : 'Looping sequence over audio (Pass 2)...' });
      }

      const loopCount = Math.max(0, Math.ceil(targetLength / baseSequenceDuration) - 1);
      
      const pass2Args = [];
      pass2Args.push('-stream_loop', loopCount.toString(), '-i', baseSequencePath);

      if (audioPath) {
        if (targetLength > 0) pass2Args.push('-stream_loop', '-1');
        pass2Args.push('-vn', '-i', audioPath);
      }

      // Count pass2 inputs: base_sequence=0, audio=1 (if present)
      let pass2InputCount = 1 + (audioPath ? 1 : 0);

      const fadeOutDuration = 1.5;
      const fadeOutStart = Math.max(0, (targetLength || baseSequenceDuration || 10) - fadeOutDuration);

      if (hasAnyOverlay) {
        // Build overlay filter chain for Pass 2
        const effectiveDuration = targetLength || baseSequenceDuration || 600;
        const overlay = buildOverlayFilters(overlayParams, effectiveDuration, pass2InputCount);
        
        // Add extra inputs (logo file)
        for (const arg of overlay.extraInputs) {
          pass2Args.push(arg);
        }

        let pass2Filter = `[0:v]null[vbase]; ${overlay.filters}`;
        if (audioPath) {
          pass2Filter += ` [1:a]afade=t=out:st=${fadeOutStart}:d=${fadeOutDuration}[aout]`;
        }
        
        const pass2FilterScript = path.join(tmpDir, `filter2-${tmpId}.txt`);
        fs.writeFileSync(pass2FilterScript, pass2Filter.trim().replace(/;$/, ''));
        tmpFiles.push(pass2FilterScript);
        pass2Args.push('-filter_complex_script', pass2FilterScript);
        
        if (audioPath) {
          pass2Args.push('-map', '[vout]', '-map', '[aout]');
        } else {
          pass2Args.push('-map', '[vout]');
        }
        // Must encode video since we're applying filters
        pass2Args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p');
      } else {
        // No overlays - use stream copy for speed
        if (audioPath) {
          pass2Args.push('-filter_complex', `[1:a]afade=t=out:st=${fadeOutStart}:d=${fadeOutDuration}[aout]`);
          pass2Args.push('-map', '0:v', '-map', '[aout]');
        } else {
          pass2Args.push('-map', '0:v');
        }
        pass2Args.push('-c:v', 'copy'); // EXTREMELY FAST when no overlays
      }

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

    res.setHeader('X-Video-Path', outputPath);
    res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition, Content-Length, X-Video-Path');

    res.download(outputPath, 'mixed_video.mp4', (err) => {
      if (err) console.error('Download error:', err);
      // Clean up (keep output video for potential YouTube upload)
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
