<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

const apiKey = ref('32033819-d1c055cd90058f2879aa55993'); // User's requested key
const searchQuery = ref('nature landscape');
const mediaType = ref('image');
const mediaOptions = [
  { title: 'Images', value: 'image' },
  { title: 'Videos', value: 'video' }
];

const results = ref<any[]>([]);
const selectedIds = ref<number[]>([]);
const isSearching = ref(false);
const isDownloading = ref(false);
const downloadProgress = ref(0);
const progressStatus = ref('');
const errorMessage = ref('');

// Pagination state
const currentPage = ref(1);
const totalPages = ref(1);
const totalHits = ref(0);

// Lightbox state
const isDialogVisible = ref(false);
const activeImage = ref<any>(null);
const zoomLevel = ref(1);

onMounted(() => {
  const savedKey = localStorage.getItem('pixabay_api_key');
  if (savedKey) apiKey.value = savedKey;
});

const fetchResults = async (page: number = 1) => {
  if (!apiKey.value.trim()) {
    errorMessage.value = "Please enter your free Pixabay API key first.";
    return;
  }
  
  localStorage.setItem('pixabay_api_key', apiKey.value.trim());
  errorMessage.value = '';
  isSearching.value = true;
  selectedIds.value = []; // Reset selections
  currentPage.value = page; // Set current page

  try {
    const isVideo = mediaType.value === 'video';
    const itemsPerPage = 30;
    
    // Request via the Node.js backend proxy to bypass browser security timeouts or ad-blockers
    const url = `http://localhost:3001/api/search?key=${apiKey.value}&q=${encodeURIComponent(searchQuery.value)}&per_page=${itemsPerPage}&page=${page}&video=${isVideo ? 'true' : 'false'}&image_type=photo`;

    const res = await fetch(url);
    if (!res.ok) {
       throw new Error(`Pixabay API Error: ${res.statusText}`);
    }
    const data = await res.json();
    
    totalHits.value = data.totalHits;
    totalPages.value = Math.ceil(data.totalHits / itemsPerPage);
    
    // Normalize the data objects so the template can easily read them without huge if/else blocks
    results.value = data.hits.map((hit: any) => {
       if (mediaType.value === 'video') {
          return {
             id: hit.id,
             previewUrl: hit.videos.medium?.thumbnail || hit.videos.small?.thumbnail,
             downloadUrl: hit.videos.large?.url || hit.videos.medium?.url,
             tags: hit.tags,
             resolution: `${hit.videos.large?.width || 0} x ${hit.videos.large?.height || 0}`,
             isVideo: true,
             duration: hit.duration
          };
       } else {
          return {
             id: hit.id,
             previewUrl: hit.webformatURL,
             downloadUrl: hit.largeImageURL,
             tags: hit.tags,
             resolution: `${hit.imageWidth} x ${hit.imageHeight}`,
             isVideo: false
          };
       }
    });

  } catch (err: any) {
    errorMessage.value = err.message || "Failed to fetch media.";
    results.value = [];
    totalPages.value = 1;
  } finally {
    isSearching.value = false;
  }
};

const handleSearch = () => {
  fetchResults(1); // Fresh search always starts at page 1
};

const handlePageChange = (newPage: number) => {
  if (newPage >= 1 && newPage <= totalPages.value) {
     fetchResults(newPage);
     // Scroll to the top of the window when paginating
     window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

const toggleSelectAll = (newValue: boolean | null) => {
   if (newValue) {
      selectedIds.value = results.value.map(img => img.id);
   } else {
      selectedIds.value = [];
   }
};

const isAllSelected = computed(() => {
   return results.value.length > 0 && selectedIds.value.length === results.value.length;
});

const openLightbox = (image: any) => {
   activeImage.value = image;
   zoomLevel.value = 1;
   isDialogVisible.value = true;
};

const zoomIn = () => zoomLevel.value += 0.25;
const zoomOut = () => zoomLevel.value = Math.max(0.25, zoomLevel.value - 0.25);

// Reuse the native fetch downloading from the previous forms
const executeDownload = async (targetUrl: string, isVideo: boolean = false) => {
  // We explicitly use type: 'image' for our backend endpoint because Pixabay provides 
  // DIRECT raw file URLs for both its Images and its MP4s. 
  // Our backend 'image' fetcher simply fetches any direct URL and pipes it back.
  // It doesn't use yt-dlp.
  const response = await fetch('http://localhost:3001/api/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      url: targetUrl,
      type: 'image'
    }),
  });

  if (!response.ok) {
      throw new Error(`Failed to download ${targetUrl}`);
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
      } else if (downloadProgress.value < 95) {
         downloadProgress.value += 1;
      }
  }

  const blob = new Blob(chunks);
  let fallbackFilename = isVideo 
      ? `stock-video-${Math.floor(Math.random()*10000)}.mp4`
      : `stock-image-${Math.floor(Math.random()*10000)}.jpg`;
  const blobUrl = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = blobUrl;
  a.download = fallbackFilename;
  
  document.body.appendChild(a);
  a.click();
  
  document.body.removeChild(a);
  URL.revokeObjectURL(blobUrl);
};

const handleBulkDownload = async () => {
    if (selectedIds.value.length === 0) return;
    
    isDownloading.value = true;
    downloadProgress.value = 0;
    errorMessage.value = '';

    const selectedImgObjects = results.value.filter(img => selectedIds.value.includes(img.id));
    
    try {
       for (let i = 0; i < selectedImgObjects.length; i++) {
          const img = selectedImgObjects[i];
          progressStatus.value = `Downloading file ${i + 1} of ${selectedImgObjects.length}...`;
          downloadProgress.value = 0; // reset bar for next image
          // Use our normalized downloadUrl and pass the isVideo flag
          await executeDownload(img.downloadUrl, img.isVideo);
          // Small pause between multiple file save triggers
          await new Promise(r => setTimeout(r, 600));
       }
    } catch (err: any) {
        errorMessage.value = err.message || "Error downloading images.";
    } finally {
        setTimeout(() => {
            isDownloading.value = false;
            downloadProgress.value = 0;
        }, 1000);
    }
};

</script>

<template>
  <v-container class="py-6">
    <!-- Header Controls -->
    <v-card class="pa-6 mb-6 rounded-xl elevation-3 border-md">
       <v-card-title class="text-h4 font-weight-black mb-4">
         <v-icon icon="mdi-image-search" size="40" class="mr-3 text-primary"></v-icon>
         Stock Image Search
       </v-card-title>
       
       <v-row>
         <v-col cols="12" md="4">
           <v-text-field
             v-model="apiKey"
             label="Pixabay API Key"
             variant="outlined"
             type="password"
             clearable
             hint="Get a free key at pixabay.com/api/docs"
             persistent-hint
             prepend-inner-icon="mdi-key"
           ></v-text-field>
         </v-col>
         <v-col cols="12" md="5">
           <v-text-field
             v-model="searchQuery"
             label="Search for images..."
             variant="outlined"
             clearable
             @keyup.enter="handleSearch"
             prepend-inner-icon="mdi-magnify"
           ></v-text-field>
         </v-col>
         <v-col cols="12" md="3">
           <v-select
             v-model="mediaType"
             :items="mediaOptions"
             item-title="title"
             item-value="value"
             label="Media Type"
             variant="outlined"
             prepend-inner-icon="mdi-filter"
           ></v-select>
         </v-col>
       </v-row>
       
       <v-btn
          color="primary"
          size="x-large"
          class="mt-4 px-8 text-none font-weight-bold"
          rounded="pill"
          :loading="isSearching"
          @click="handleSearch"
       >
          Search {{ mediaType === 'video' ? 'Videos' : 'Images' }}
       </v-btn>

       <v-alert v-if="errorMessage" type="error" variant="tonal" class="mt-4 rounded-lg">
          {{ errorMessage }}
       </v-alert>
    </v-card>

    <!-- Toolbar: Shows up when images exist -->
    <v-expand-transition>
      <v-card v-if="results.length > 0" class="mb-6 px-4 py-2 border-md d-flex align-center bg-white" rounded="lg" elevation="2">
        <v-checkbox
           :model-value="isAllSelected"
           @update:model-value="toggleSelectAll"
           label="Select All"
           hide-details
           class="mr-6 font-weight-bold"
           color="primary"
        ></v-checkbox>
        
        <span class="text-subtitle-1 font-weight-bold text-grey-darken-1 mr-4">
           {{ selectedIds.length }} selected
        </span>

        <v-spacer></v-spacer>
        
        <!-- Progress linear if downloading -->
        <div v-if="isDownloading" class="mr-4 flex-grow-1" style="max-width: 300px;">
           <div class="d-flex justify-space-between mb-1">
             <span class="text-caption font-weight-bold text-primary">{{ progressStatus || 'Downloading Selection...' }}</span>
             <span class="text-caption font-weight-bold">{{ downloadProgress }}%</span>
           </div>
           <v-progress-linear v-model="downloadProgress" color="primary" rounded="pill" striped height="8"></v-progress-linear>
        </div>

        <v-btn
           color="success"
           prepend-icon="mdi-cloud-download"
           variant="flat"
           class="text-none font-weight-bold"
           :disabled="selectedIds.length === 0 || isDownloading"
           :loading="isDownloading"
           @click="handleBulkDownload"
        >
           Download Selected ({{ selectedIds.length }})
        </v-btn>
      </v-card>
    </v-expand-transition>

    <!-- Results Grid -->
    <v-row v-if="results.length > 0">
      <v-col v-for="image in results" :key="image.id" cols="12" sm="6" md="4" lg="3">
        <!-- Card with hover elevation -->
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 8 : 2"
            class="transition-swing rounded-lg h-100 position-relative overflow-hidden"
            :class="{ 'border-primary border-md': selectedIds.includes(image.id) }"
          >
            <!-- High quality Image View -->
            <v-img
              :src="image.previewUrl"
              cover
              height="250"
              class="align-end bg-grey-lighten-2 cursor-pointer"
              @click="openLightbox(image)"
            >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </div>
              </template>
              
              <!-- Video play icon overlay if it's a video -->
              <div v-if="image.isVideo" class="position-absolute d-flex align-center justify-center w-100 h-100 top-0 left-0" style="pointer-events: none;">
                <v-icon icon="mdi-play-circle-outline" size="64" color="white" style="opacity: 0.8; text-shadow: 0 0 10px rgba(0,0,0,0.5);"></v-icon>
              </div>
              
              <!-- Gradient overlay on bottom for text -->
              <div class="px-3 py-2 text-white position-relative" style="background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); z-index: 2;">
                <span class="font-weight-bold text-caption text-truncate d-block">{{ image.tags }}</span>
                <span class="text-caption opacity-70">{{ image.resolution }} <span v-if="image.isVideo" class="ml-2">• {{ image.duration }}s</span></span>
              </div>
            </v-img>

            <!-- Absolute positioned checkbox -->
            <v-checkbox
              v-model="selectedIds"
              :value="image.id"
              hide-details
              color="primary"
              class="position-absolute top-0 right-0 ma-2 ml-auto"
              style="background: rgba(255,255,255,0.8); border-radius: 5px;"
            ></v-checkbox>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>

    <!-- Pagination Controls -->
    <v-row v-if="results.length > 0 && totalPages > 1" class="mt-8 mb-4">
      <v-col cols="12" class="d-flex justify-center align-center">
        <v-btn
          variant="tonal"
          prepend-icon="mdi-chevron-left"
          class="mr-4 text-none font-weight-bold"
          :disabled="currentPage === 1 || isSearching"
          @click="handlePageChange(currentPage - 1)"
        >
          Previous
        </v-btn>
        
        <span class="text-subtitle-1 font-weight-bold mx-4 text-grey-darken-2">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        
        <v-btn
          variant="tonal"
          append-icon="mdi-chevron-right"
          class="ml-4 text-none font-weight-bold"
          :disabled="currentPage >= totalPages || isSearching"
          @click="handlePageChange(currentPage + 1)"
        >
          Next Page
        </v-btn>
      </v-col>
    </v-row>
    
    <v-fade-transition>
      <div v-if="!isSearching && results.length === 0" class="text-center py-16 opacity-60">
        <v-icon icon="mdi-image-off-outline" size="64" class="mb-4 text-grey"></v-icon>
        <div class="text-h6 text-grey">No images to display. Enter an API key and search!</div>
      </div>
    </v-fade-transition>
    
    <!-- Zoomable Lightbox -->
    <v-dialog v-model="isDialogVisible" fullscreen transition="dialog-fade-transition">
      <v-card class="bg-black" rounded="0">
        <v-toolbar color="transparent" class="position-absolute w-100" style="z-index: 10;">
          <v-spacer></v-spacer>
          <v-btn icon="mdi-magnify-minus" color="white" variant="tonal" class="mx-2 bg-black bg-opacity-50" @click="zoomOut" :disabled="zoomLevel <= 0.25"></v-btn>
          <v-btn icon="mdi-magnify-plus" color="white" variant="tonal" class="mx-2 bg-black bg-opacity-50" @click="zoomIn" :disabled="zoomLevel >= 3"></v-btn>
          <v-btn icon="mdi-close" color="white" variant="tonal" class="mx-2 bg-black bg-opacity-50" @click="isDialogVisible = false"></v-btn>
        </v-toolbar>
        
        <div class="d-flex align-center justify-center fill-height overflow-hidden w-100">
           <!-- Video Player -->
           <video 
             v-if="activeImage?.isVideo"
             :src="activeImage.downloadUrl" 
             controls 
             autoplay
             class="transition-swing"
             :style="{ transform: `scale(${zoomLevel})`, maxHeight: '90vh', maxWidth: '100vw' }"
           ></video>

           <!-- Image Viewer -->
           <v-img
             v-else-if="activeImage && !activeImage.isVideo"
             :src="activeImage.downloadUrl"
             contain
             max-height="90vh"
             max-width="100vw"
             class="transition-swing"
             :style="{ transform: `scale(${zoomLevel})` }"
           >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-progress-circular indeterminate color="white"></v-progress-circular>
                </div>
              </template>
           </v-img>
        </div>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<style scoped>
.border-md {
  border-width: 2px !important;
  border-style: solid !important;
  border-color: rgba(0,0,0,0.12) !important;
}
.border-primary {
  border-color: rgb(var(--v-theme-primary)) !important;
}
</style>
