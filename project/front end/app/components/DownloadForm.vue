<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  type: 'image' | 'video' | 'audio';
  title: string;
  subtitle: string;
  icon: string;
  iconColor: string;
}>();

const urlInput = ref('');
const isDownloading = ref(false);
const isDownloadingStock = ref(false);
const downloadProgress = ref(0); // Track progress from 0 to 100
const progressStatus = ref('');
const errorMessage = ref('');

const executeDownload = async (targetUrl: string, explicitExt: string = '') => {
  const response = await fetch('http://localhost:3001/api/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      url: targetUrl,
      type: props.type
    }),
  });

  if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to connect to the backend server.');
  }

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
         downloadProgress.value = Math.round((receivedBytes / totalBytes) * 100);
      } else {
         if (downloadProgress.value < 95) {
             downloadProgress.value += 1;
         }
      }
  }

  const blob = new Blob(chunks);
  let defaultExt = explicitExt;
  if (!defaultExt) {
    if (props.type === 'image') defaultExt = '.jpg';
    if (props.type === 'video') defaultExt = '.mp4';
    if (props.type === 'audio') defaultExt = '.mp3';
  }

  let fallbackFilename = `downloaded-${props.type}-${Math.floor(Math.random()*10000)}${defaultExt}`;
  const blobUrl = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = blobUrl;
  a.download = fallbackFilename;
  
  document.body.appendChild(a);
  a.click();
  
  document.body.removeChild(a);
  URL.revokeObjectURL(blobUrl);
  downloadProgress.value = 100;
};

const handleDownload = async () => {
  if (!urlInput.value) {
    errorMessage.value = 'Please enter a valid URL';
    return;
  }
  
  isDownloading.value = true;
  downloadProgress.value = 0;
  progressStatus.value = 'Downloading to browser...';
  errorMessage.value = '';

  try {
    await executeDownload(urlInput.value);
  } catch (error: any) {
    console.error('Frontend download error:', error);
    errorMessage.value = error.message || 'An unexpected error occurred while downloading the file.';
  } finally {
    setTimeout(() => {
        isDownloading.value = false;
        downloadProgress.value = 0;
    }, 1000);
  }
};

const handleStockDownload = async () => {
  isDownloadingStock.value = true;
  downloadProgress.value = 0;
  errorMessage.value = '';

  try {
    // 1. Fetch 3 random stock images from Picsum Photos free API
    const randomPage = Math.floor(Math.random() * 50) + 1;
    const stockApiResponse = await fetch(`https://picsum.photos/v2/list?page=${randomPage}&limit=3`);
    
    if (!stockApiResponse.ok) {
       throw new Error('Failed to fetch from free stock API.');
    }
    
    const stockImages = await stockApiResponse.json();

    // 2. Loop through the API results and sequentially download them
    for (let i = 0; i < stockImages.length; i++) {
        progressStatus.value = `Downloading image ${i + 1} of ${stockImages.length}...`;
        downloadProgress.value = 0; // reset bar for each image
        await executeDownload(stockImages[i].download_url, '.jpg');
        // Give browser a quick breather between rapid file save prompts
        await new Promise(r => setTimeout(r, 500)); 
    }

  } catch (error: any) {
    console.error('Frontend stock download error:', error);
    errorMessage.value = error.message || 'An unexpected error fetching stock images.';
  } finally {
    setTimeout(() => {
        isDownloadingStock.value = false;
        downloadProgress.value = 0;
    }, 1000);
  }
};
</script>

<template>
  <v-container class="d-flex align-center justify-center min-vh-100" style="min-height: calc(100vh - 64px);">
    <v-card class="pa-6 mx-auto text-center" width="100%" max-width="500" elevation="6" rounded="xl">
      <v-avatar :color="iconColor" size="64" class="mb-4 elevation-2 text-white">
        <v-icon :icon="icon" size="36"></v-icon>
      </v-avatar>
      <v-card-title class="text-h4 font-weight-black mb-2 px-0" :class="`text-${iconColor}`">
        {{ title }}
      </v-card-title>
      <v-card-subtitle class="text-subtitle-1 mb-6 px-0" style="white-space: normal;">
        {{ subtitle }}
      </v-card-subtitle>
      
      <v-card-text class="px-0">
        <v-form @submit.prevent="handleDownload">
          
          <v-text-field
            v-model="urlInput"
            label="Paste your URL here"
            variant="outlined"
            placeholder="https://..."
            required
            clearable
            :disabled="isDownloading"
            prepend-inner-icon="mdi-link"
            hide-details="auto"
            class="mb-4"
          ></v-text-field>
          
          <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4 rounded-lg text-left">
            {{ errorMessage }}
          </v-alert>

          <!-- Progress Bar Section -->
          <v-expand-transition>
            <div v-if="isDownloading || isDownloadingStock" class="mb-4">
               <div class="d-flex justify-space-between mb-1">
                 <span class="text-caption font-weight-bold text-grey-darken-1">{{ progressStatus || 'Downloading...' }}</span>
                 <span class="text-caption font-weight-bold" :class="`text-${iconColor}`">{{ downloadProgress }}%</span>
               </div>
               <v-progress-linear
                  v-model="downloadProgress"
                  :color="iconColor"
                  height="12"
                  rounded="pill"
                  striped
               ></v-progress-linear>
            </div>
          </v-expand-transition>

          <v-btn
            type="submit"
            :color="iconColor"
            block
            size="x-large"
            rounded="pill"
            elevation="4"
            :disabled="isDownloading || isDownloadingStock"
            :loading="isDownloading"
            class="mt-2 text-none font-weight-bold"
          >
            Download File
            <template v-slot:append>
              <v-icon icon="mdi-download"></v-icon>
            </template>
          </v-btn>

          <!-- Secondary Batch Download Button for Stock API -->
          <v-btn
            v-if="props.type === 'image'"
            @click="handleStockDownload"
            variant="tonal"
            color="secondary"
            block
            size="large"
            rounded="pill"
            elevation="2"
            :disabled="isDownloading || isDownloadingStock"
            :loading="isDownloadingStock"
            class="mt-4 text-none font-weight-bold"
          >
            Surprise Me: Get 3 Free Stock Images
            <template v-slot:append>
              <v-icon icon="mdi-gift"></v-icon>
            </template>
          </v-btn>
          
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>
