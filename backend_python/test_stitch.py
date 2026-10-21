import os
import urllib.request
import ssl
import subprocess
import imageio_ffmpeg

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = 'https://sanchit-gandhi-musicgen-streaming.hf.space/gradio_api/stream/291c805a-eef5-45ca-a6d5-ebcbcb59ff8f/139773409418288/4/'
m3u8_url = base + 'playlist.m3u8'
req = urllib.request.Request(m3u8_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as r:
    content = r.read().decode('utf-8')

segments = [l.strip() for l in content.splitlines() if l.strip().endswith('.aac')]
temp_dir = r'd:\sourse code\ME\download_root\output_songs\temp_test'
os.makedirs(temp_dir, exist_ok=True)

concat_file = os.path.join(temp_dir, 'concat.txt')
with open(concat_file, 'w', encoding='utf-8') as cf:
    for seg in segments:
        seg_path = os.path.join(temp_dir, seg).replace('\\', '/')
        seg_url = base + seg
        sreq = urllib.request.Request(seg_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(sreq, context=ctx) as sr:
            with open(seg_path, 'wb') as sf:
                sf.write(sr.read())
        cf.write(f"file '{seg_path}'\n")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
out_mp3 = r'd:\sourse code\ME\download_root\output_songs\meta_musicgen_demo.mp3'
cmd = [ffmpeg_exe, '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c:a', 'libmp3lame', '-b:a', '256k', out_mp3]
res = subprocess.run(cmd, capture_output=True, text=True)
print('FFmpeg returncode:', res.returncode)
if res.returncode == 0:
    print('SUCCESS! Final MP3 created at:', out_mp3, 'Size:', os.path.getsize(out_mp3), 'bytes')
else:
    print('FFmpeg error:', res.stderr)
