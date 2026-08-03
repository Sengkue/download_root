<template>
  <div class="editor-container">
    <div class="glass-header">
      <div class="header-icon-box">
        <v-icon icon="mdi-video-plus-outline" size="32" color="white"></v-icon>
      </div>
      <div class="header-text">
        <h1 class="header-title">Magic Video Editor</h1>
        <p class="header-subtitle">Fuse images and audio into stunning videos instantly.</p>
      </div>
    </div>

    <div class="workspace">
      <!-- Upload Zones -->
      <div v-if="!videoUrl" class="upload-zones">
        
        <!-- Image Drop Zone -->
        <div 
          class="drop-zone glass-card"
          :class="{ 'drag-over': isDraggingImage, 'has-file': imageFiles.length > 0 }"
          @dragover.prevent="isDraggingImage = true"
          @dragleave.prevent="isDraggingImage = false"
          @drop.prevent="onDropImage"
          @click="$refs.imageInput.click()"
        >
          <input type="file" ref="imageInput" accept="image/*" multiple class="d-none" @change="onSelectImage" />
          
          <div v-if="imageFiles.length === 0" class="zone-placeholder">
            <v-icon icon="mdi-image-multiple-outline" size="48" class="mb-3" color="rgba(255,255,255,0.7)"></v-icon>
            <h3>Image Track</h3>
            <p>Drag & Drop multiple images or Click to browse</p>
          </div>
          
          <div v-else class="zone-preview multi-preview">
            <div class="gallery-grid">
              <div v-for="(url, index) in imagePreviewUrls.slice(0, 4)" :key="index" class="gallery-item">
                <img :src="url" alt="Preview" class="preview-img-small" />
              </div>
              <div v-if="imageFiles.length > 4" class="more-indicator">
                +{{ imageFiles.length - 4 }}
              </div>
            </div>
            <div class="file-overlay">
              <v-icon icon="mdi-check-circle" color="success" size="32"></v-icon>
              <span>{{ imageFiles.length }} Image(s) selected</span>
              <small>(Click to replace)</small>
            </div>
          </div>
        </div>

        <!-- Audio Drop Zone -->
        <div 
          class="drop-zone glass-card"
          :class="{ 'drag-over': isDraggingAudio, 'has-file': audioFile }"
          @dragover.prevent="isDraggingAudio = true"
          @dragleave.prevent="isDraggingAudio = false"
          @drop.prevent="onDropAudio"
          @click="$refs.audioInput.click()"
        >
          <input type="file" ref="audioInput" accept="audio/*" class="d-none" @change="onSelectAudio" />
          
          <div v-if="!audioFile" class="zone-placeholder">
            <v-icon icon="mdi-music-note-outline" size="48" class="mb-3" color="rgba(255,255,255,0.7)"></v-icon>
            <h3>Audio Track</h3>
            <p>Drag & Drop or Click to browse</p>
          </div>
          
          <div v-else class="zone-preview audio-preview">
            <v-icon icon="mdi-waveform" size="64" color="white" class="wave-icon"></v-icon>
            <div class="file-overlay">
              <v-icon icon="mdi-check-circle" color="success" size="32"></v-icon>
              <span>{{ audioFile.name }}</span>
              <small>(Click to replace)</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Effects Settings Panel -->
      <div v-if="!videoUrl" class="settings-panel glass-card mt-8">
        <h3 class="mb-4 d-flex align-center gap-2">
          <v-icon icon="mdi-movie-filter" color="primary"></v-icon>
          Cinematic Effects Settings
        </h3>
        
        <v-row>
          <v-col cols="12" md="6">
            <p class="font-weight-bold mb-2 text-white">Zoom Direction (Ken Burns)</p>
            <v-btn-toggle
              v-model="zoomDir"
              color="primary"
              mandatory
              class="w-100 btn-group-custom"
            >
              <v-btn value="in" class="flex-grow-1">
                <v-icon start>mdi-magnify-plus</v-icon> In
              </v-btn>
              <v-btn value="out" class="flex-grow-1">
                <v-icon start>mdi-magnify-minus</v-icon> Out
              </v-btn>
              <v-btn value="alternate" class="flex-grow-1">
                <v-icon start>mdi-swap-horizontal</v-icon> Switch
              </v-btn>
              <v-btn value="none" class="flex-grow-1">
                <v-icon start>mdi-cancel</v-icon> None
              </v-btn>
            </v-btn-toggle>
          </v-col>
          
          <v-col cols="12" md="6">
            <p class="font-weight-bold mb-2 text-white">Zoom Speed</p>
            <v-btn-toggle
              v-model="zoomSpeed"
              color="secondary"
              mandatory
              :disabled="zoomDir === 'none'"
              class="w-100 btn-group-custom"
            >
              <v-btn value="slow" class="flex-grow-1">Slow</v-btn>
              <v-btn value="normal" class="flex-grow-1">Normal</v-btn>
              <v-btn value="fast" class="flex-grow-1">Fast</v-btn>
            </v-btn-toggle>
          </v-col>
        </v-row>
      </div>

      <!-- Result View -->
      <div v-if="videoUrl" class="result-view glass-card">
        <h3 class="mb-4 d-flex align-center gap-2">
          <v-icon icon="mdi-movie-open-check" color="success"></v-icon>
          Your Video is Ready
        </h3>
        
        <video controls class="final-video">
          <source :src="videoUrl" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        
        <div class="action-buttons mt-6">
          <v-btn
            size="large"
            color="white"
            variant="outlined"
            prepend-icon="mdi-refresh"
            @click="resetEditor"
            class="action-btn"
          >
            Make Another
          </v-btn>
          <v-btn
            size="large"
            color="success"
            prepend-icon="mdi-download"
            @click="downloadVideo"
            class="action-btn download-btn"
          >
            Download Video
          </v-btn>
        </div>
      </div>

      <!-- Generate Action with Progress Bar -->
      <div v-if="!videoUrl" class="generate-section mt-8">
        <v-btn
          v-if="!isGenerating"
          size="x-large"
          class="generate-btn"
          :disabled="!canGenerate"
          @click="generateVideo"
        >
          <v-icon icon="mdi-magic-staff" class="mr-2" />
          Generate Video
        </v-btn>
        
        <div v-else class="progress-section glass-card pa-6">
          <div class="d-flex justify-space-between align-center mb-3">
            <span class="font-weight-bold text-white text-body-1">{{ currentStatus }}</span>
            <span class="progress-percent">{{ Math.round(currentProgress) }}%</span>
          </div>
          <v-progress-linear
            :model-value="currentProgress"
            color="primary"
            height="14"
            rounded
            striped
            animated
            class="progress-bar-smooth"
          ></v-progress-linear>
          <p class="text-caption text-grey-lighten-1 mt-3 mb-0 text-center">
            <v-icon icon="mdi-information-outline" size="14" class="mr-1"></v-icon>
            Applying cinematic effects — this may take a minute for many images.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const imageInput = ref(null);
const audioInput = ref(null);

const isDraggingImage = ref(false);
const isDraggingAudio = ref(false);

const imageFiles = ref([]);
const imagePreviewUrls = ref([]);
const audioFile = ref(null);

// Settings State
const zoomDir = ref('alternate');
const zoomSpeed = ref('normal');

const isGenerating = ref(false);
const videoUrl = ref(null);

// Progress State
const currentProgress = ref(0);
const currentStatus = ref('');
let eventSource = null;

const canGenerate = computed(() => imageFiles.value.length > 0 && audioFile.value);

// Image Handlers
const onDropImage = (e) => {
  isDraggingImage.value = false;
  const files = Array.from(e.dataTransfer?.files || []);
  const validFiles = files.filter(f => f.type.startsWith('image/'));
  if (validFiles.length > 0) {
    setImages(validFiles);
  }
};

const onSelectImage = (e) => {
  const files = Array.from(e.target.files || []);
  if (files.length > 0) setImages(files);
};

const setImages = (files) => {
  imagePreviewUrls.value.forEach(url => URL.revokeObjectURL(url));
  imageFiles.value = files;
  imagePreviewUrls.value = files.map(f => URL.createObjectURL(f));
};

// Audio Handlers
const onDropAudio = (e) => {
  isDraggingAudio.value = false;
  const file = e.dataTransfer?.files[0];
  if (file && file.type.startsWith('audio/')) {
    setAudio(file);
  }
};

const onSelectAudio = (e) => {
  const file = e.target.files[0];
  if (file) setAudio(file);
};

const setAudio = (file) => {
  audioFile.value = file;
};

// Generation
const generateVideo = async () => {
  if (!canGenerate.value) return;
  
  isGenerating.value = true;
  currentProgress.value = 0;
  currentStatus.value = 'Uploading files...';
  
  const jobId = 'job_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
  
  // Start SSE connection FIRST before uploading
  let sseActive = true;
  eventSource = new EventSource(`http://localhost:3001/api/progress?jobId=${jobId}`);
  
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.progress !== undefined && data.progress > currentProgress.value) {
        currentProgress.value = data.progress;
      }
      if (data.status) {
        currentStatus.value = data.status;
      }
    } catch (_) {}
  };
  
  eventSource.onerror = () => {
    // SSE errors are normal when the connection drops. Don't close immediately —
    // the browser will auto-reconnect. Only close when we're done.
  };
  
  const formData = new FormData();
  formData.append('jobId', jobId);
  formData.append('zoomDir', zoomDir.value);
  formData.append('zoomSpeed', zoomSpeed.value);
  
  imageFiles.value.forEach(file => {
    formData.append('image', file);
  });
  formData.append('audio', audioFile.value);
  
  try {
    currentStatus.value = 'Uploading to server...';
    currentProgress.value = 1;
    
    const res = await fetch('http://localhost:3001/api/editor/merge', {
      method: 'POST',
      body: formData
    });
    
    if (!res.ok) throw new Error('Failed to generate video');
    
    // Video is encoded! Now downloading the file to browser...
    currentProgress.value = 99;
    currentStatus.value = 'Downloading video to browser...';
    
    const blob = await res.blob();
    
    // Blob fully received!
    currentProgress.value = 100;
    currentStatus.value = '✅ Video Ready!';
    videoUrl.value = URL.createObjectURL(blob);
    
  } catch (err) {
    console.error('Video generation error:', err);
    currentStatus.value = '❌ Failed to generate video';
    currentProgress.value = 0;
    setTimeout(() => {
      isGenerating.value = false;
    }, 2000);
    return;
  } finally {
    sseActive = false;
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
    isGenerating.value = false;
  }
};

const downloadVideo = () => {
  if (!videoUrl.value) return;
  const a = document.createElement('a');
  a.href = videoUrl.value;
  a.download = `fused-slideshow-${Date.now()}.mp4`;
  a.click();
};

const resetEditor = () => {
  imageFiles.value = [];
  audioFile.value = null;
  imagePreviewUrls.value.forEach(url => URL.revokeObjectURL(url));
  imagePreviewUrls.value = [];
  
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  videoUrl.value = null;
  
  if (imageInput.value) imageInput.value.value = '';
  if (audioInput.value) audioInput.value.value = '';
};
</script>

<style scoped>
.editor-container {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
}

.glass-header {
  background: rgba(25, 25, 35, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 48px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.header-icon-box {
  background: linear-gradient(135deg, #FF6B6B 0%, #845EC2 100%);
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(132, 94, 194, 0.4);
}

.header-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0;
  line-height: 1.2;
}

.header-subtitle {
  color: rgba(255, 255, 255, 0.7);
  margin: 8px 0 0;
  font-size: 1.1rem;
}

.glass-card {
  background: rgba(25, 25, 35, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.settings-panel {
  padding: 24px 32px;
}

.btn-group-custom {
  border-radius: 12px;
  background: rgba(0,0,0,0.2) !important;
}
.btn-group-custom .v-btn {
  border: none !important;
}
.btn-group-custom .v-btn--active {
  background: rgba(132, 94, 194, 0.2) !important;
}

.upload-zones {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.drop-zone {
  aspect-ratio: 16/9;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  position: relative;
  border: 2px dashed rgba(255, 255, 255, 0.1);
}

.drop-zone:hover {
  border-color: rgba(132, 94, 194, 0.5);
  background: rgba(132, 94, 194, 0.05);
  transform: translateY(-4px);
}

.drop-zone.drag-over {
  border-color: #FF6B6B;
  background: rgba(255, 107, 107, 0.05);
  transform: scale(1.02);
}

.drop-zone.has-file {
  border-style: solid;
  border-color: rgba(255, 255, 255, 0.1);
}

.zone-placeholder {
  text-align: center;
  color: white;
}

.zone-placeholder h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.zone-placeholder p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.zone-preview {
  width: 100%;
  height: 100%;
  position: relative;
}

.multi-preview {
  padding: 16px;
  background: rgba(0,0,0,0.2);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 8px;
  width: 100%;
  height: 100%;
}

.gallery-item {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.preview-img-small {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.more-indicator {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0,0,0,0.7);
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.audio-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(132, 94, 194, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
}

.wave-icon {
  opacity: 0.5;
  animation: pulse 2s infinite ease-in-out;
}

.file-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.drop-zone:hover .file-overlay {
  opacity: 1;
}

.file-overlay small {
  font-weight: 400;
  font-size: 0.9rem;
  opacity: 0.8;
}

.generate-section {
  text-align: center;
  margin-top: 48px;
}

.generate-btn {
  background: linear-gradient(135deg, #FF6B6B 0%, #845EC2 100%) !important;
  color: white !important;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 0 48px !important;
  height: 64px !important;
  border-radius: 32px !important;
  transition: transform 0.2s, box-shadow 0.2s;
}

.generate-btn:not(:disabled):hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 24px rgba(132, 94, 194, 0.4);
}

.generate-btn:disabled {
  opacity: 0.5;
  background: rgba(255, 255, 255, 0.1) !important;
}

.progress-section {
  max-width: 600px;
  margin: 0 auto;
  animation: fadeIn 0.4s ease-out;
}

.progress-percent {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #FF6B6B, #845EC2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  min-width: 60px;
  text-align: right;
}

.progress-bar-smooth :deep(.v-progress-linear__determinate) {
  transition: width 0.6s ease-out !important;
}

.result-view {
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: slideUp 0.5s ease-out;
}

.final-video {
  width: 100%;
  max-width: 800px;
  border-radius: 16px;
  background: #000;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);
}

.action-buttons {
  display: flex;
  gap: 16px;
}

.action-btn {
  border-radius: 12px !important;
  text-transform: none !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
}

.download-btn {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
  color: white !important;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .upload-zones {
    grid-template-columns: 1fr;
  }
}
</style>
