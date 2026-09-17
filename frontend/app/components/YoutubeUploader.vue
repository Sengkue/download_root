<template>
  <div class="youtube-uploader-card">
    <div class="d-flex align-center mb-4">
      <v-icon icon="mdi-youtube" color="red" size="32" class="mr-3"></v-icon>
      <h3 class="text-h6 text-white mb-0">Publish to YouTube</h3>
    </div>

    <!-- Connect State -->
    <div v-if="!connectedChannels.length && !loadingChannels">
      <p class="text-body-2 text-grey-lighten-1 mb-4">
        Connect your YouTube channel to upload generated videos directly from this editor.
      </p>
      <v-btn color="red-darken-1" variant="flat" block @click="connectYoutube">
        <v-icon start icon="mdi-youtube"></v-icon>
        Connect YouTube Account
      </v-btn>
    </div>

    <div v-else-if="loadingChannels" class="text-center py-4">
      <v-progress-circular indeterminate color="red"></v-progress-circular>
    </div>

    <!-- Upload State -->
    <div v-else>
      <!-- Channel Selector -->
      <v-select
        v-model="selectedChannel"
        :items="connectedChannels"
        item-title="channelTitle"
        item-value="channelId"
        label="Select Channel"
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

      <v-text-field
        v-model="videoTitle"
        label="Video Title"
        variant="outlined"
        density="compact"
        bg-color="#2a2a3b"
        class="mb-3"
      ></v-text-field>

      <v-textarea
        v-model="videoDescription"
        label="Description"
        variant="outlined"
        density="compact"
        bg-color="#2a2a3b"
        rows="3"
        class="mb-3"
      ></v-textarea>

      <v-text-field
        v-model="videoTags"
        label="Tags (comma separated)"
        variant="outlined"
        density="compact"
        bg-color="#2a2a3b"
        class="mb-4"
      ></v-text-field>
      
      <div class="d-flex justify-space-between align-center mb-4">
        <span class="text-body-2 text-grey-lighten-1">Privacy:</span>
        <v-btn-toggle v-model="privacyStatus" mandatory color="red-darken-1" density="compact">
          <v-btn value="private">Private</v-btn>
          <v-btn value="unlisted">Unlisted</v-btn>
          <v-btn value="public">Public</v-btn>
        </v-btn-toggle>
      </div>

      <v-btn
        color="red-darken-1"
        variant="flat"
        block
        size="large"
        :loading="isUploading"
        :disabled="!selectedChannel || !videoTitle"
        @click="uploadVideo"
      >
        <v-icon start icon="mdi-cloud-upload"></v-icon>
        Upload to YouTube
      </v-btn>
      
      <!-- Connect Another -->
      <v-btn variant="text" block size="small" class="mt-2 text-grey" @click="connectYoutube">
        Connect Another Channel
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
      <div v-if="uploadStatus.link" class="mt-2">
        <a :href="uploadStatus.link" target="_blank" class="text-white">View on YouTube</a>
      </div>
    </v-alert>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  videoPath: {
    type: String,
    required: true
  }
});

const connectedChannels = ref([]);
const loadingChannels = ref(true);
const selectedChannel = ref(null);

const videoTitle = ref('My Awesome Video');
const videoDescription = ref('Generated via Video Editor Studio.\n\nEnjoy the content!');
const videoTags = ref('video, editor, generated');
const privacyStatus = ref('private');

const isUploading = ref(false);
const uploadStatus = ref(null);

const fetchChannels = async () => {
  loadingChannels.value = true;
  try {
    const res = await fetch('http://localhost:3005/api/youtube/channels');
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

const connectYoutube = async () => {
  try {
    const res = await fetch('http://localhost:3005/api/youtube/auth');
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url;
    }
  } catch (error) {
    console.error('Failed to get auth URL:', error);
    uploadStatus.value = { type: 'error', message: 'Failed to connect to YouTube server.' };
  }
};

const uploadVideo = async () => {
  isUploading.value = true;
  uploadStatus.value = null;
  
  try {
    const res = await fetch('http://localhost:3005/api/youtube/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        channelId: selectedChannel.value,
        videoPath: props.videoPath,
        title: videoTitle.value,
        description: videoDescription.value,
        tags: videoTags.value,
        privacyStatus: privacyStatus.value
      })
    });
    
    const text = await res.text();
    
    if (res.ok) {
      const match = text.match(/https:\/\/youtu\.be\/[\w-]+/);
      uploadStatus.value = {
        type: 'success',
        message: 'Upload successful!',
        link: match ? match[0] : null
      };
    } else {
      uploadStatus.value = {
        type: 'error',
        message: 'Upload failed: ' + text
      };
    }
  } catch (error) {
    uploadStatus.value = { type: 'error', message: 'Upload failed: ' + error.message };
  } finally {
    isUploading.value = false;
  }
};

onMounted(() => {
  fetchChannels();
  
  // Check if we just returned from auth
  if (window.location.search.includes('youtube_auth=success')) {
    uploadStatus.value = { type: 'success', message: 'YouTube account connected successfully!' };
    // Clean URL
    const url = new URL(window.location);
    url.searchParams.delete('youtube_auth');
    window.history.replaceState({}, '', url);
  }
});
</script>

<style scoped>
.youtube-uploader-card {
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
</style>
