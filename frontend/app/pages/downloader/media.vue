<script setup lang="ts">
import { ref } from 'vue';

const urlInput = ref('');
const isChecking = ref(false);
const isDownloading = ref(false);
const downloadProgress = ref(0);
const progressStatus = ref('');
const errorMessage = ref('');

const videoInfo = ref<any>(null);
const selectedFormat = ref<'video' | 'audio'>('video');
const selectedQuality = ref<number | null>(null);

const checkLink = async () => {
  if (!urlInput.value) {
    errorMessage.value = 'Please enter a valid video URL';
    return;
  }

  isChecking.value = true;
  errorMessage.value = '';
  videoInfo.value = null;

  try {
    const response = await fetch('http://localhost:3001/api/info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: urlInput.value }),
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || 'Failed to fetch video information.');
    }

    const data = await response.json();
    videoInfo.value = data;
    
    // Default to the highest quality if available
    if (data.qualities && data.qualities.length > 0) {
      selectedQuality.value = data.qualities[0];
    }
  } catch (error: any) {
    console.error('Info fetch error:', error);
    errorMessage.value = error.message || 'An unexpected error occurred while checking the link.';
  } finally {
    isChecking.value = false;
  }
};

const executeDownload = async () => {
  if (!videoInfo.value) return;

  isDownloading.value = true;
  downloadProgress.value = 0;
  progressStatus.value = 'Connecting to server...';
  errorMessage.value = '';

  const jobId = Math.random().toString(36).substring(2, 15);
  const eventSource = new EventSource(`http://localhost:3001/api/progress?jobId=${jobId}`);
  
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    downloadProgress.value = data.progress || 0;
    progressStatus.value = data.status || 'Processing...';
  };

  try {
    const response = await fetch('http://localhost:3001/api/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: urlInput.value,
        type: selectedFormat.value,
        quality: selectedFormat.value === 'video' ? selectedQuality.value : undefined,
        jobId
      }),
    });

    if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || 'Failed to connect to the backend server.');
    }

    eventSource.close();
    progressStatus.value = "Downloading to browser...";
    downloadProgress.value = 0;

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
    let defaultExt = selectedFormat.value === 'audio' ? '.mp3' : '.mp4';
    
    // Use the fetched title for the filename, fallback to generic name
    let cleanTitle = videoInfo.value.title ? videoInfo.value.title.replace(/[^a-zA-Z0-9 ]/g, "").substring(0, 50) : `media-${Math.floor(Math.random()*10000)}`;
    let filename = `${cleanTitle}${defaultExt}`;

    const blobUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = filename;
    
    document.body.appendChild(a);
    a.click();
    
    document.body.removeChild(a);
    URL.revokeObjectURL(blobUrl);
    downloadProgress.value = 100;
  } catch (error: any) {
    console.error('Download error:', error);
    errorMessage.value = error.message || 'An unexpected error occurred while downloading the file.';
  } finally {
    eventSource.close();
    setTimeout(() => {
        isDownloading.value = false;
        downloadProgress.value = 0;
    }, 1000);
  }
};

const formatQualityLabel = (q: number) => `${q}p`;
</script>

<template>
  <v-container class="py-10">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        
        <!-- Step 1: Input URL -->
        <v-card class="pa-6 rounded-xl elevation-4 mb-6" :loading="isChecking">
          <v-card-title class="text-h4 font-weight-black text-center text-red-darken-2 mb-2">
            <v-icon icon="mdi-video" size="48" class="mr-2"></v-icon>
            Media Downloader
          </v-card-title>
          <v-card-subtitle class="text-subtitle-1 text-center mb-6">
            Paste a video link below to check available formats and download options.
          </v-card-subtitle>
          
          <v-card-text class="px-0">
            <v-form @submit.prevent="checkLink">
              <v-text-field
                v-model="urlInput"
                label="Paste Video URL"
                variant="outlined"
                placeholder="https://www.youtube.com/watch?v=... or https://vt.tiktok.com/..."
                required
                clearable
                :disabled="isChecking || isDownloading"
                prepend-inner-icon="mdi-link"
                hide-details="auto"
                class="mb-4"
              ></v-text-field>
              
              <v-alert v-if="errorMessage && !videoInfo" type="error" variant="tonal" class="mb-4 rounded-lg">
                {{ errorMessage }}
              </v-alert>

              <v-btn
                type="submit"
                color="red-darken-2"
                block
                size="x-large"
                rounded="pill"
                elevation="2"
                :disabled="isChecking || isDownloading || !urlInput"
                :loading="isChecking"
                class="text-none font-weight-bold"
              >
                Check Link
                <template v-slot:append>
                  <v-icon icon="mdi-magnify"></v-icon>
                </template>
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <!-- Step 2: Display Video Info and Format Options -->
        <v-expand-transition>
          <v-card v-if="videoInfo" class="pa-6 rounded-xl elevation-4" color="grey-lighten-4">
            
            <div class="d-flex flex-column flex-sm-row mb-6">
              <v-img
                :src="videoInfo.thumbnail"
                width="100%"
                max-width="200"
                height="120"
                cover
                class="rounded-lg elevation-2 mr-0 mr-sm-4 mb-4 mb-sm-0"
              ></v-img>
              <div class="flex-grow-1 d-flex flex-column justify-center">
                <h3 class="text-h6 font-weight-bold mb-2 text-truncate-2" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                  {{ videoInfo.title }}
                </h3>
              </div>
            </div>

            <v-divider class="mb-6"></v-divider>

            <v-alert v-if="errorMessage && videoInfo" type="error" variant="tonal" class="mb-4 rounded-lg">
              {{ errorMessage }}
            </v-alert>

            <div class="text-subtitle-1 font-weight-bold mb-4">Select Format to Download:</div>
            
            <v-row class="mb-4">
              <v-col cols="6">
                <v-card 
                  variant="outlined" 
                  :color="selectedFormat === 'video' ? 'red-darken-2' : 'grey'"
                  :class="selectedFormat === 'video' ? 'bg-red-lighten-5' : ''"
                  class="h-100 pa-4 cursor-pointer text-center rounded-lg transition-swing"
                  @click="selectedFormat = 'video'"
                >
                  <v-icon icon="mdi-video" size="36" class="mb-2"></v-icon>
                  <div class="font-weight-bold">MP4 Video</div>
                </v-card>
              </v-col>
              <v-col cols="6">
                <v-card 
                  variant="outlined" 
                  :color="selectedFormat === 'audio' ? 'red-darken-2' : 'grey'"
                  :class="selectedFormat === 'audio' ? 'bg-red-lighten-5' : ''"
                  class="h-100 pa-4 cursor-pointer text-center rounded-lg transition-swing"
                  @click="selectedFormat = 'audio'"
                >
                  <v-icon icon="mdi-music" size="36" class="mb-2"></v-icon>
                  <div class="font-weight-bold">MP3 Audio</div>
                </v-card>
              </v-col>
            </v-row>

            <v-expand-transition>
              <div v-if="selectedFormat === 'video' && videoInfo.qualities && videoInfo.qualities.length > 0">
                <v-select
                  v-model="selectedQuality"
                  :items="videoInfo.qualities"
                  :item-title="formatQualityLabel"
                  label="Select Quality"
                  variant="outlined"
                  bg-color="white"
                  hide-details
                  class="mb-6"
                  prepend-inner-icon="mdi-high-definition"
                ></v-select>
              </div>
            </v-expand-transition>

            <v-expand-transition>
              <div v-if="isDownloading" class="mb-6">
                 <div class="d-flex justify-space-between mb-1">
                   <span class="text-caption font-weight-bold text-grey-darken-1">{{ progressStatus }}</span>
                   <span class="text-caption font-weight-bold text-red-darken-2">{{ downloadProgress }}%</span>
                 </div>
                 <v-progress-linear
                    v-model="downloadProgress"
                    color="red-darken-2"
                    height="12"
                    rounded="pill"
                    striped
                 ></v-progress-linear>
              </div>
            </v-expand-transition>

            <v-btn
              @click="executeDownload"
              color="red-darken-2"
              block
              size="x-large"
              rounded="pill"
              elevation="3"
              :disabled="isDownloading"
              :loading="isDownloading"
              class="text-none font-weight-bold"
            >
              Download {{ selectedFormat === 'video' ? 'Video' : 'Audio' }}
              <template v-slot:append>
                <v-icon icon="mdi-cloud-download"></v-icon>
              </template>
            </v-btn>

          </v-card>
        </v-expand-transition>
        
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
.text-truncate-2 {
  white-space: normal;
}
</style>
