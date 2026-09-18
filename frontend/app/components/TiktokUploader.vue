<template>
  <div class="tiktok-uploader-card">
    <div class="d-flex align-center mb-4">
      <!-- TikTok Icon -->
      <svg viewBox="0 0 448 512" class="tiktok-icon mr-3" width="32" height="32">
        <path fill="currentColor" d="M448,209.91a210.06,210.06,0,0,1-122.77-39.25V349.38A162.55,162.55,0,1,1,185,188.31V278.2a74.62,74.62,0,1,0,52.23,71.18V0l88,0a121.18,121.18,0,0,0,1.86,22.17h0A122.18,122.18,0,0,0,381,102.39a121.43,121.43,0,0,0,67,20.14Z"/>
      </svg>
      <h3 class="text-h6 text-white mb-0">Publish to TikTok</h3>
    </div>

    <!-- Connect State -->
    <div v-if="!connectedChannels.length && !loadingChannels">
      <p class="text-body-2 text-grey-lighten-1 mb-4">
        Connect your TikTok account to post generated videos directly from this editor.
      </p>
      <v-btn color="black" class="tiktok-btn" variant="flat" block @click="connectTiktok">
        Connect TikTok Account
      </v-btn>
    </div>

    <div v-else-if="loadingChannels" class="text-center py-4">
      <v-progress-circular indeterminate color="#fe2c55"></v-progress-circular>
    </div>

    <!-- Upload State -->
    <div v-else>
      <!-- Channel Selector -->
      <v-select
        v-model="selectedChannel"
        :items="connectedChannels"
        item-title="channelTitle"
        item-value="channelId"
        label="Select Account"
        variant="outlined"
        density="compact"
        class="mb-3 custom-select"
        bg-color="#2a2a3b"
      >
        <template v-slot:item="{ props, item }">
          <v-list-item v-bind="props" :prepend-avatar="item.raw.thumbnailUrl" :title="item.raw.channelTitle"></v-list-item>
        </template>
        <template v-slot:selection="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="24" class="mr-2">
              <v-img :src="item.raw.thumbnailUrl"></v-img>
            </v-avatar>
            <span>{{ item.raw.channelTitle }}</span>
          </div>
        </template>
      </v-select>

      <v-textarea
        v-model="videoTitle"
        label="Caption (e.g. My amazing video!)"
        variant="outlined"
        density="compact"
        bg-color="#2a2a3b"
        rows="2"
        class="mb-3"
      ></v-textarea>

      <v-text-field
        v-model="videoTags"
        label="Tags (comma separated, e.g. fyp, viral)"
        variant="outlined"
        density="compact"
        bg-color="#2a2a3b"
        class="mb-4"
      ></v-text-field>
      
      <div class="d-flex justify-space-between align-center mb-4">
        <span class="text-caption text-grey-lighten-1">* Videos are uploaded as Private by default for safety.</span>
      </div>

      <v-btn
        class="tiktok-btn"
        variant="flat"
        block
        size="large"
        :loading="isUploading"
        :disabled="!selectedChannel || !videoTitle"
        @click="uploadVideo"
      >
        <v-icon start icon="mdi-cloud-upload"></v-icon>
        Upload to TikTok
      </v-btn>

      <div v-if="isUploading" class="mt-4">
        <div class="d-flex justify-space-between mb-1">
          <span class="text-caption text-grey-lighten-1">{{ uploadStatusText }}</span>
          <span class="text-caption font-weight-bold">{{ roundedProgress }}%</span>
        </div>
        <v-progress-linear
          :model-value="uploadProgress"
          color="#fe2c55"
          height="8"
          rounded
          striped
        ></v-progress-linear>
      </div>
      
      <!-- Connect Another -->
      <v-btn variant="text" block size="small" class="mt-2 text-grey" @click="connectTiktok">
        Connect Another Account
      </v-btn>
    </div>
    
    <!-- Status Message -->
    <v-alert
      v-if="uploadStatus"
      :type="uploadStatus.type"
      variant="tonal"
      class="mt-4"
      density="compact"
    >
      {{ uploadStatus.message }}
    </v-alert>
  </div>
</template>

<script setup>
import { useMediaApi } from '~/composables/useMediaApi';
const { createProgressStream } = useMediaApi();
import { ref, onMounted, computed } from 'vue';

const props = defineProps({
  videoPath: {
    type: String,
    required: true
  }
});

const connectedChannels = ref([]);
const loadingChannels = ref(true);
const selectedChannel = ref(null);

const videoTitle = ref('Generated via Video Editor Studio.');
const videoTags = ref('editor, generated, viral, fyp');

const isUploading = ref(false);
const uploadStatus = ref(null);
const uploadProgress = ref(0);
const uploadStatusText = ref('');
const roundedProgress = computed(() => Math.round(uploadProgress.value || 0));

const fetchChannels = async () => {
  loadingChannels.value = true;
  try {
    const res = await fetch('http://localhost:3005/api/tiktok/channels');
    const data = await res.json();
    connectedChannels.value = data;
    if (data.length > 0) {
      selectedChannel.value = data[0].channelId;
    }
  } catch (error) {
    console.error('Failed to fetch channels:', error);
  } finally {
    loadingChannels.value = false;
  }
};

const connectTiktok = async () => {
  try {
    const res = await fetch('http://localhost:3005/api/tiktok/auth');
    const data = await res.json();
    if (data.url) {
      // Open in a popup window to prevent losing current page state
      const width = 500;
      const height = 600;
      const left = window.screenX + (window.outerWidth - width) / 2;
      const top = window.screenY + (window.outerHeight - height) / 2;
      
      const popup = window.open(
        data.url, 
        'TikTokAuth', 
        `width=${width},height=${height},left=${left},top=${top},status=yes,scrollbars=yes`
      );

      // Listen for the success message from the popup
      const messageListener = (event) => {
        if (event.origin !== window.location.origin) return;
        
        if (event.data === 'tiktok_auth_success') {
          uploadStatus.value = { type: 'success', message: 'TikTok account connected successfully!' };
          fetchChannels(); // Refresh the list of connected accounts
          window.removeEventListener('message', messageListener);
          if (popup && !popup.closed) popup.close();
        }
      };
      
      window.addEventListener('message', messageListener);
    }
  } catch (error) {
    console.error('Failed to get auth URL:', error);
    uploadStatus.value = { type: 'error', message: 'Failed to connect to TikTok server.' };
  }
};

const uploadVideo = async () => {
  isUploading.value = true;
  uploadStatus.value = null;
  uploadProgress.value = 0;
  uploadStatusText.value = 'Preparing upload...';

  const jobId = "job_tk_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6);
  let eventSource = createProgressStream(jobId);
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.progress) uploadProgress.value = data.progress;
    if (data.status) uploadStatusText.value = data.status;
  };
  eventSource.onerror = () => eventSource.close();

  try {
    const res = await fetch('http://localhost:3005/api/tiktok/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jobId,
        channelId: selectedChannel.value,
        videoPath: props.videoPath,
        title: videoTitle.value,
        tags: videoTags.value
      })
    });
    
    const data = await res.json();
    if (res.ok) {
      uploadStatus.value = {
        type: 'success',
        message: 'Upload initiated successfully! Note: The video is set to Private on TikTok by default.',
      };
      uploadProgress.value = 100;
      uploadStatusText.value = 'Upload complete!';
    } else {
      uploadStatus.value = {
        type: 'error',
        message: 'Upload failed: ' + (data.error || 'Unknown error')
      };
    }
  } catch (error) {
    uploadStatus.value = { type: 'error', message: 'Upload failed: ' + error.message };
  } finally {
    if (eventSource) eventSource.close();
    isUploading.value = false;
  }
};

onMounted(() => {
  fetchChannels();
  
  // Check if we just returned from auth
  if (window.location.search.includes('tiktok_auth=success')) {
    if (window.opener && !window.opener.closed) {
      // If we are in a popup, tell the main window we succeeded and close
      window.opener.postMessage('tiktok_auth_success', window.location.origin);
      window.close();
    } else {
      // Fallback if not in popup
      uploadStatus.value = { type: 'success', message: 'TikTok account connected successfully!' };
      // Clean URL
      const url = new URL(window.location);
      url.searchParams.delete('tiktok_auth');
      window.history.replaceState({}, '', url);
    }
  }
});
</script>

<style scoped>
.tiktok-uploader-card {
  background-color: rgba(30, 30, 46, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 24px;
  margin-top: 24px;
}
.custom-select :deep(.v-field__input) {
  padding-top: 4px;
  padding-bottom: 4px;
}
.tiktok-icon {
  color: white;
  filter: drop-shadow(2px 2px 0px #fe2c55) drop-shadow(-2px -2px 0px #25f4ee);
}
.tiktok-btn {
  background-color: #000000 !important;
  color: white !important;
  border: 1px solid rgba(255,255,255,0.1);
}
.tiktok-btn:hover {
  background-color: #1a1a1a !important;
}
</style>
