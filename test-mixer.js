import fs from 'fs';
import FormData from 'form-data';
import http from 'http';
import path from 'path';

const test = async () => {
  const form = new FormData();
  
  // Add 2 video files
  form.append('video', fs.createReadStream('d:/sourse code/ME/download_root/tools/video/stock-video-1808.mp4'));
  form.append('video', fs.createReadStream('d:/sourse code/ME/download_root/tools/video/stock-video-4702.mp4'));
  
  // Add audio file
  form.append('audio', fs.createReadStream('d:/sourse code/ME/download_root/tools/audio/_  2026  .mp3'));
  
  // Add montage settings
  form.append('jobId', 'test-job-123');
  form.append('videoSpeed', '1.5');
  form.append('transitionDuration', '1.0');
  form.append('transitionTypes', JSON.stringify(['fade', 'wipeleft']));

  console.log('Sending request to Video Mixer API...');
  
  const request = http.request('http://localhost:3001/api/video-mixer', {
    method: 'POST',
    headers: form.getHeaders(),
  });

  form.pipe(request);

  request.on('response', (res) => {
    console.log(`STATUS: ${res.statusCode}`);
    if (res.statusCode === 200) {
      const outPath = path.join('d:/sourse code/ME/download_root/tools', 'test-output.mp4');
      const fileStream = fs.createWriteStream(outPath);
      res.pipe(fileStream);
      fileStream.on('finish', () => {
        console.log(`Success! Video saved to ${outPath}`);
      });
    } else {
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        console.log(`BODY: ${chunk}`);
      });
    }
  });

  request.on('error', (e) => {
    console.error(`Problem with request: ${e.message}`);
  });
};

test();
