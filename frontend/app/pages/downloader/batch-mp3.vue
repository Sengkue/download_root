<template>
  <v-container class="py-8" max-width="900">
    <!-- Header -->
    <div class="text-center mb-8">
      <v-avatar color="purple-accent-2" size="64" class="mb-4 glass-card elevation-4">
        <v-icon icon="mdi-music-box-multiple" size="36" color="white"></v-icon>
      </v-avatar>
      <h1 class="text-h4 font-weight-black mb-2 text-primary text-white">Batch MP3 Downloader</h1>
      <p class="text-subtitle-1 text-grey-lighten-1">Download multiple YouTube songs at once</p>
    </div>

    <!-- Input Section -->
    <v-card class="glass-card mb-6" elevation="0" theme="dark">
      <v-card-text>
        <v-textarea
          v-model="rawInput"
          label="Paste URLs here (one per line)"
          placeholder="https://youtu.be/...\nhttps://youtu.be/..."
          variant="outlined"
          color="purple-accent-2"
          bg-color="rgba(0,0,0,0.2)"
          rows="5"
          hide-details
          class="mb-4"
        ></v-textarea>
        
        <v-btn
          color="purple-accent-2"
          prepend-icon="mdi-format-list-bulleted"
          @click="loadLinks"
          :disabled="!rawInput.trim() || isProcessing"
          block
        >
          Load Links
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- Queue Section -->
    <v-card v-if="queue.length > 0" class="glass-card mb-6" elevation="0" theme="dark">
      <v-card-title class="d-flex align-center justify-space-between pb-0">
        <span>Download Queue ({{ queue.length }} items)</span>
        <v-btn
          color="error"
          variant="tonal"
          size="small"
          @click="clearQueue"
          :disabled="isProcessing"
        >
          Clear
        </v-btn>
      </v-card-title>
      
      <v-card-text class="mt-4">
        <v-list bg-color="transparent" density="compact" class="px-0">
          <v-list-item
            v-for="(item, index) in queue"
            :key="index"
            class="mb-2 rounded-lg"
            :class="{
              'bg-blue-grey-darken-4': item.status === 'pending',
              'bg-indigo-darken-4': item.status === 'downloading',
              'bg-green-darken-4': item.status === 'success',
              'bg-red-darken-4': item.status === 'error'
            }"
          >
            <template v-slot:prepend>
              <div class="font-weight-bold mr-4" style="min-width: 24px;">{{ index + 1 }}</div>
            </template>
            
            <v-list-item-title class="text-truncate" style="max-width: 400px;">
              {{ item.url }}
            </v-list-item-title>
            
            <v-list-item-subtitle v-if="item.status === 'downloading'" class="mt-1">
              <div class="d-flex align-center">
                <span class="mr-2 text-caption">{{ item.progressStatus }}</span>
                <v-progress-linear
                  :model-value="item.progress"
                  color="white"
                  height="4"
                  rounded
                  class="flex-grow-1"
                ></v-progress-linear>
                <span class="ml-2 text-caption font-weight-bold">{{ item.progress }}%</span>
              </div>
            </v-list-item-subtitle>
            
            <v-list-item-subtitle v-if="item.status === 'error'" class="text-red-lighten-2 mt-1 text-caption">
              {{ item.error }}
            </v-list-item-subtitle>
            
            <template v-slot:append>
              <v-icon v-if="item.status === 'pending'" icon="mdi-clock-outline" color="grey"></v-icon>
              <v-progress-circular v-else-if="item.status === 'downloading'" indeterminate size="20" width="2" color="white"></v-progress-circular>
              <v-icon v-else-if="item.status === 'success'" icon="mdi-check-circle" color="success"></v-icon>
              <v-icon v-else-if="item.status === 'error'" icon="mdi-alert-circle" color="error"></v-icon>
            </template>
          </v-list-item>
        </v-list>

        <v-btn
          class="mt-4"
          color="success"
          size="x-large"
          block
          prepend-icon="mdi-download-multiple"
          @click="startBatchDownload"
          :loading="isProcessing"
          :disabled="!hasPendingItems"
        >
          Download All MP3s
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

definePageMeta({
  layout: 'downloader'
});

interface QueueItem {
  url: string;
  status: 'pending' | 'downloading' | 'success' | 'error';
  progress: number;
  progressStatus: string;
  error?: string;
}

const rawInput = ref('');
const queue = ref<QueueItem[]>([]);
const isProcessing = ref(false);

const hasPendingItems = computed(() => {
  return queue.value.some(item => item.status === 'pending' || item.status === 'error');
});

const loadLinks = () => {
  if (!rawInput.value.trim()) return;
  
  // Split by newline, comma, or space and filter out empty strings
  const urls = rawInput.value
    .split(/[\n, ]+/)
    .map(url => url.trim())
    .filter(url => url.length > 0 && (url.includes('http://') || url.includes('https://')));
    
  // Add to queue avoiding strict duplicates in the current run (optional)
  urls.forEach(url => {
    queue.value.push({
      url,
      status: 'pending',
      progress: 0,
      progressStatus: 'Waiting...',
    });
  });
  
  rawInput.value = ''; // clear input after loading
};

const clearQueue = () => {
  queue.value = [];
};

const downloadSingle = async (item: QueueItem) => {
  const jobId = `batch-${Math.random().toString(36).substring(2, 9)}`;
  const eventSource = new EventSource(`http://localhost:3005/api/progress?jobId=${jobId}`);

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    item.progressStatus = data.status || 'Processing...';
    if (data.progress !== undefined) {
      item.progress = Math.round(data.progress);
    }
  };

  eventSource.onerror = () => {
    eventSource.close();
  };

  try {
    const response = await fetch('http://localhost:3005/api/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: item.url,
        type: 'audio',
        jobId
      }),
    });

    if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || 'Failed to connect to the backend server.');
    }

    eventSource.close();
    item.progressStatus = "Downloading to browser...";
    item.progress = 0;

    const contentLength = response.headers.get('content-length');
    const totalBytes = contentLength ? parseInt(contentLength, 10) : 0;
    
    let receivedBytes = 0;
    const reader = response.body?.getReader();
    const chunks = [];

    if (!reader) throw new Error("Unable to read streaming response.");

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        chunks.push(value);
        receivedBytes += value.length;
        
        if (totalBytes) {
           item.progress = Math.round((receivedBytes / totalBytes) * 100);
        } else {
           if (item.progress < 95) {
               item.progress += 1;
           }
        }
    }

    const blob = new Blob(chunks);
    let defaultExt = '.mp3';
    
    // We don't fetch info first to save time in batch, so we generate a generic name
    // or try to extract video ID from URL
    let videoId = 'audio';
    try {
      if (item.url.includes('v=')) {
        const parts = item.url.split('v=');
        if (parts[1]) videoId = parts[1].split('&')[0] || 'audio';
      } else if (item.url.includes('youtu.be/')) {
        const parts = item.url.split('youtu.be/');
        if (parts[1]) videoId = parts[1].split('?')[0] || 'audio';
      }
    } catch(e) {}
    
    // Check Content-Disposition header if available
    const disposition = response.headers.get('Content-Disposition');
    let filename = `youtube-${videoId}${defaultExt}`;
    if (disposition) {
        const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
        if (utf8Match && utf8Match[1]) {
            filename = decodeURIComponent(utf8Match[1]);
        } else {
            const filenameMatch = disposition.match(/filename="?([^"]+)"?/);
            if (filenameMatch && filenameMatch[1]) {
                filename = filenameMatch[1];
            }
        }
    }

    const blobUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = filename;
    
    document.body.appendChild(a);
    a.click();
    
    document.body.removeChild(a);
    URL.revokeObjectURL(blobUrl);
    item.progress = 100;
    item.progressStatus = "Complete";
    
  } catch (error: any) {
    throw error;
  } finally {
    eventSource.close();
  }
};

const startBatchDownload = async () => {
  isProcessing.value = true;
  
  for (const item of queue.value) {
    if (item.status === 'success') continue; // skip already downloaded
    
    item.status = 'downloading';
    item.error = undefined;
    
    try {
      await downloadSingle(item);
      item.status = 'success';
    } catch (e: any) {
      console.error('Failed to download:', item.url, e);
      item.status = 'error';
      item.error = e.message || 'Download failed';
    }
  }
  
  isProcessing.value = false;
};
</script>

<style scoped>
.glass-card {
  background: rgba(38, 50, 56, 0.7) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px !important;
}
</style>
