<template>
  <div class="editor-container text-white">
    <div class="workspace">
      <!-- Upload Zones -->
      <div v-if="!videoUrl" class="upload-zones">
        
        <!-- Background Media Drop Zone -->
        <div
          class="drop-zone glass-card mb-6"
          :class="{
            'drag-over': isDraggingVideo,
            'has-file': videoFiles.length > 0,
          }"
          @dragover.prevent="isDraggingVideo = true"
          @dragleave.prevent="isDraggingVideo = false"
          @drop.prevent="onDropVideo"
          @click="$refs.videoInput.click()"
        >
          <input
            type="file"
            ref="videoInput"
            accept="image/*,video/*"
            multiple
            class="d-none"
            @change="onSelectVideo"
            @click.stop
          />

          <div v-if="videoFiles.length === 0" class="zone-placeholder">
            <v-icon
              icon="mdi-image-area"
              size="40"
              class="mb-2 floating-icon"
              color="rgba(255,255,255,0.8)"
            ></v-icon>
            <h3 class="text-subtitle-1 font-weight-bold">Background Media</h3>
            <p class="text-caption text-grey-lighten-1">Drag & Drop Multiple Images or Videos</p>
          </div>

          <div v-else class="zone-preview audio-preview">
            <div class="d-flex align-center justify-space-between w-100 px-4">
              <div class="d-flex align-center">
                <v-icon icon="mdi-image-multiple" color="info" size="32" class="mr-2"></v-icon>
                <div>
                  <div class="font-weight-bold">{{ videoFiles.length }} Backgrounds Added</div>
                  <div class="text-caption text-grey-lighten-1">Click to add more</div>
                </div>
              </div>
              <v-btn
                color="error"
                variant="tonal"
                size="small"
                @click.stop="clearVideo"
              >
                Clear All
              </v-btn>
            </div>
          </div>
        </div>

        <!-- Background Media Reordering -->
        <v-card v-if="videoFiles.length > 0" class="glass-card mb-6" elevation="0" theme="dark">
          <v-card-title class="text-subtitle-1 font-weight-bold pb-0">
            <v-icon icon="mdi-sort" class="mr-2"></v-icon>Background Order
          </v-card-title>
          <v-list bg-color="transparent" density="compact" class="px-2" theme="dark">
            <v-list-item
              v-for="(file, index) in videoFiles"
              :key="'vid'+index"
              class="rounded-lg mb-1 audio-list-item"
            >
              <template v-slot:prepend>
                <div class="index-badge mr-3">{{ index + 1 }}</div>
                <v-icon :icon="file.type.startsWith('image/') ? 'mdi-image' : 'mdi-video'" color="grey-lighten-1" class="mr-2"></v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ file.name }}</v-list-item-title>
              
              <template v-slot:append>
                <v-btn
                  icon="mdi-chevron-up"
                  variant="text"
                  size="small"
                  :disabled="index === 0"
                  @click.stop="moveVideoUp(index)"
                ></v-btn>
                <v-btn
                  icon="mdi-chevron-down"
                  variant="text"
                  size="small"
                  :disabled="index === videoFiles.length - 1"
                  @click.stop="moveVideoDown(index)"
                ></v-btn>
                <v-btn
                  icon="mdi-delete-outline"
                  color="error"
                  variant="text"
                  size="small"
                  @click.stop="removeVideo(index)"
                  class="ml-2"
                ></v-btn>
              </template>
            </v-list-item>
          </v-list>
          <div class="px-4 pb-4" v-if="videoFiles.length > 1">
            <p class="text-subtitle-2 font-weight-bold mb-2">Slideshow Settings</p>
            <v-row dense>
              <v-col cols="12" md="6">
                <v-text-field v-model.number="bgImageDuration" type="number" min="1" max="60" label="Image Duration (s)" density="compact" variant="outlined" hide-details bg-color="rgba(255,255,255,0.05)" color="primary"></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model.number="bgTransitionDuration" type="number" min="0" max="5" label="Crossfade Duration (s)" density="compact" variant="outlined" hide-details bg-color="rgba(255,255,255,0.05)" color="primary"></v-text-field>
              </v-col>
            </v-row>
          </div>
        </v-card>

        <!-- Audio Playlist Drop Zone -->
        <div
          class="drop-zone glass-card mb-6"
          :class="{ 'drag-over': isDraggingAudio, 'has-file': audioFiles.length > 0 }"
          @dragover.prevent="isDraggingAudio = true"
          @dragleave.prevent="isDraggingAudio = false"
          @drop.prevent="onDropAudio"
          @click="$refs.audioInput.click()"
        >
          <input
            type="file"
            ref="audioInput"
            accept="audio/*"
            multiple
            class="d-none"
            @change="onSelectAudio"
            @click.stop
          />

          <div v-if="audioFiles.length === 0" class="zone-placeholder">
            <v-icon
              icon="mdi-playlist-music"
              size="40"
              class="mb-2 floating-icon-audio"
              color="rgba(255,255,255,0.8)"
            ></v-icon>
            <h3 class="text-subtitle-1 font-weight-bold">Audio Playlist</h3>
            <p class="text-caption text-grey-lighten-1">Drag & Drop multiple songs here</p>
          </div>

          <div v-else class="zone-preview audio-preview">
             <div class="d-flex align-center justify-space-between w-100 px-4">
                <div class="d-flex align-center">
                  <v-icon icon="mdi-music-circle" color="info" size="32" class="mr-2"></v-icon>
                  <div>
                    <div class="font-weight-bold">{{ audioFiles.length }} Songs Added</div>
                    <div class="text-caption text-grey-lighten-1">Click to add more</div>
                  </div>
                </div>
                <v-btn
                  color="error"
                  variant="tonal"
                  size="small"
                  @click.stop="clearAudio"
                >
                  Clear All
                </v-btn>
             </div>
          </div>
        </div>

        <!-- Playlist Reordering -->
        <v-card v-if="audioFiles.length > 0" class="glass-card mb-6" elevation="0" theme="dark">
          <v-card-title class="text-subtitle-1 font-weight-bold pb-0">
            <v-icon icon="mdi-sort" class="mr-2"></v-icon>Playlist Order
          </v-card-title>
          <v-list bg-color="transparent" density="compact" class="px-2" theme="dark">
            <v-list-item
              v-for="(file, index) in audioFiles"
              :key="index"
              class="rounded-lg mb-1 audio-list-item"
            >
              <template v-slot:prepend>
                <div class="index-badge mr-3">{{ index + 1 }}</div>
                <v-icon icon="mdi-music-note" color="grey-lighten-1" class="mr-2"></v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ file.name }}</v-list-item-title>
              
              <template v-slot:append>
                <v-btn
                  icon="mdi-chevron-up"
                  variant="text"
                  size="small"
                  :disabled="index === 0"
                  @click.stop="moveAudioUp(index)"
                ></v-btn>
                <v-btn
                  icon="mdi-chevron-down"
                  variant="text"
                  size="small"
                  :disabled="index === audioFiles.length - 1"
                  @click.stop="moveAudioDown(index)"
                ></v-btn>
                <v-btn
                  icon="mdi-delete-outline"
                  color="error"
                  variant="text"
                  size="small"
                  @click.stop="removeAudio(index)"
                  class="ml-2"
                ></v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-card>

        <!-- Live Preview -->
        <div class="glass-card mb-6">
          <h3 class="text-h6 font-weight-bold mb-4 d-flex align-center justify-space-between">
            <div class="d-flex align-center"><v-icon icon="mdi-monitor-eye" class="mr-2"></v-icon> Live Preview</div>
            <v-btn size="small" variant="outlined" color="grey-lighten-1" @click="resetPositions">Reset Positions</v-btn>
          </h3>
          <p class="text-caption text-grey-lighten-1 mb-2">Drag and drop elements below to set their exact position in the video.</p>
          <div class="preview-box" ref="previewBoxRef" @mousemove="onMouseMove" @mouseup="onMouseUp" @mouseleave="onMouseUp">
            <img v-if="videoPreviewUrl && isBackgroundImg" :src="videoPreviewUrl" class="preview-bg" />
            <video v-else-if="videoPreviewUrl" :src="videoPreviewUrl" class="preview-bg" muted></video>
            
            <div v-if="showNowPlaying" class="preview-playlist draggable-element" :style="{ left: playlistPos.x + '%', top: playlistPos.y + '%', fontSize: (playlistFontSize * 0.4) + 'px', gridTemplateRows: `repeat(${playlistItemsPerCol}, auto)`, columnGap: (playlistColGap * 0.2) + 'px' }" @mousedown="onMouseDown($event, 'playlist')">
              <div v-for="(song, index) in previewPlaylist" :key="index" :class="['playlist-item', { active: index === 0 }]">
                <span class="icon">{{ index === 0 ? '▶' : '' }}</span>
                {{ index + 1 }}. {{ song.title }}
              </div>
            </div>
            
            <div v-if="overlayTimer.enabled" class="preview-timer draggable-element" :style="{ left: timerPos.x + '%', top: timerPos.y + '%', fontSize: (overlayTimer.fontSize * 0.6) + 'px' }" @mousedown="onMouseDown($event, 'timer')">
              {{ previewTimerText }}
            </div>
          </div>
        </div>

        <!-- Settings Panel -->
        <div class="settings-panel glass-card">
          <h3 class="text-h6 font-weight-bold mb-4 d-flex align-center">
            <v-icon icon="mdi-cog-outline" class="mr-2"></v-icon> Video Settings
          </h3>

          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="outputResolution"
                :items="resolutionOptions"
                label="Output Format (Resolution)"
                variant="outlined"
                density="comfortable"
                hide-details
                bg-color="rgba(0,0,0,0.2)"
                class="settings-input mb-4"
                theme="dark"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :prepend-icon="item.raw.icon">
                  </v-list-item>
                </template>
              </v-select>
            </v-col>
            <v-col cols="12" md="6" class="d-flex align-center mb-4">
              <v-switch
                v-model="showNowPlaying"
                color="primary"
                hide-details
                label="Show On-Screen Playlist"
                class="font-weight-medium mb-2"
              ></v-switch>
              <v-slider v-if="showNowPlaying" v-model="playlistFontSize" min="16" max="72" step="2" label="Text Size" thumb-label hide-details density="compact" color="primary"></v-slider>
            </v-col>
          </v-row>
          <v-row v-if="showNowPlaying" dense class="mb-4 pl-3">
            <v-col cols="12" md="6" class="d-flex align-center">
              <v-text-field v-model.number="playlistItemsPerCol" type="number" min="1" max="50" label="Songs per Column" density="compact" variant="outlined" hide-details bg-color="rgba(255,255,255,0.05)" color="primary" class="rounded-lg mr-4"></v-text-field>
              <v-slider v-model="playlistColGap" min="100" max="1000" step="10" label="Column Spacing" thumb-label hide-details density="compact" color="primary"></v-slider>
            </v-col>
          </v-row>

          <v-divider class="mb-4 border-opacity-25"></v-divider>

          <div class="d-flex align-center justify-space-between mb-2">
            <div class="d-flex align-center">
              <v-icon icon="mdi-timer-outline" color="purple-lighten-2" class="mr-3" size="24"></v-icon>
              <div>
                <p class="font-weight-bold mb-0 text-white">Timer Overlay</p>
                <p class="text-caption text-grey-lighten-1 mb-0">Countdown timer for study/focus videos</p>
              </div>
            </div>
            <v-switch
              v-model="overlayTimer.enabled"
              color="purple-lighten-2"
              inset
              hide-details
              density="compact"
            ></v-switch>
          </div>

          <v-expand-transition>
            <div v-if="overlayTimer.enabled" class="mt-4">
              <v-row dense>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="overlayTimer.mode"
                    :items="[{title:'Pomodoro Cycle', value:'pomodoro'}, {title:'Per-Song Countdown', value:'persong'}]"
                    label="Timer Mode"
                    density="compact"
                    hide-details
                    variant="outlined"
                    bg-color="rgba(255,255,255,0.05)"
                    color="purple-lighten-2"
                    class="rounded-lg mb-2"
                    theme="dark"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="4" v-if="overlayTimer.mode === 'pomodoro'">
                  <div class="d-flex align-center" style="gap: 8px">
                    <v-btn v-for="preset in [25, 50]" :key="preset"
                      :color="overlayTimer.minutes === preset ? 'purple-lighten-2' : 'grey-darken-3'"
                      :variant="overlayTimer.minutes === preset ? 'flat' : 'outlined'"
                      size="small" height="40" @click="overlayTimer.minutes = preset" class="timer-preset-btn">
                      {{ preset }}m
                    </v-btn>
                    <v-text-field v-model.number="overlayTimer.minutes" type="number" min="1" max="180"
                      density="compact" hide-details variant="outlined" bg-color="rgba(255,255,255,0.05)"
                      color="purple-lighten-2" class="rounded-lg" style="max-width: 90px" suffix="min">
                    </v-text-field>
                  </div>
                </v-col>
                <v-col cols="12" md="4" class="d-flex flex-column justify-center">
                  <v-slider v-model="overlayTimer.fontSize" min="24" max="96" step="4" label="Text Size" thumb-label hide-details density="compact" color="purple-lighten-2"></v-slider>
                  <p class="text-caption text-grey-lighten-1 mb-0 mt-2">Drag the timer in the Live Preview box above to position it.</p>
                </v-col>
              </v-row>
              <v-row dense class="mt-1" v-if="overlayTimer.mode === 'pomodoro'">
                 <v-col cols="12" class="d-flex align-center gap-4">
                    <v-switch v-model="overlayTimer.withBreak" label="Add Short Break" color="green-lighten-2" inset hide-details density="compact" class="text-white"></v-switch>
                    <v-text-field v-if="overlayTimer.withBreak" v-model.number="overlayTimer.breakMinutes" type="number" min="1" max="60" density="compact" hide-details variant="outlined" bg-color="rgba(255,255,255,0.05)" color="green-lighten-2" class="rounded-lg" style="max-width: 100px" label="Break Min"></v-text-field>
                 </v-col>
              </v-row>
            </div>
          </v-expand-transition>
          
          <div class="d-flex justify-center mt-6">
            <v-btn
              color="primary"
              size="x-large"
              class="generate-btn px-8 text-none font-weight-bold rounded-pill"
              :disabled="!canGenerate || isGenerating"
              :loading="isGenerating"
              @click="generateVideo"
              elevation="4"
            >
              <template v-slot:prepend>
                <v-icon>mdi-auto-fix</v-icon>
              </template>
              Create Compilation
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Result / Progress Area -->
      <div v-else-if="videoUrl" class="result-area glass-card">
        <div class="d-flex justify-space-between align-center mb-4">
          <h2 class="text-h5 font-weight-bold text-success d-flex align-center">
            <v-icon icon="mdi-check-decagram" class="mr-2"></v-icon> Mixing Complete!
          </h2>
          <v-btn icon="mdi-refresh" variant="tonal" @click="resetMixer" title="Start Over"></v-btn>
        </div>

        <div class="video-preview-container mb-6">
          <video :src="videoUrl" controls class="final-video" autoplay></video>
        </div>

        <div class="d-flex gap-4 justify-center">
          <v-btn
            color="primary"
            size="large"
            prepend-icon="mdi-download"
            @click="downloadVideo"
            class="text-none font-weight-bold px-8 rounded-pill"
            elevation="4"
          >
            Download MP4
          </v-btn>
        </div>
      </div>

      <!-- Processing Overlay -->
      <v-overlay
        :model-value="isGenerating"
        class="align-center justify-center"
        persistent
        scrim="black"
      >
        <v-card class="bg-grey-darken-4 text-center px-8 py-6 processing-card" elevation="24" width="400">
          <div class="processing-animation mb-6">
            <v-progress-circular
              :model-value="currentProgress"
              color="purple-lighten-2"
              size="120"
              width="8"
            >
              <span class="text-h4 font-weight-bold text-purple-lighten-2">{{ currentProgress }}%</span>
            </v-progress-circular>
          </div>
          
          <h3 class="text-h6 font-weight-bold mb-2">Creating Compilation</h3>
          <p class="text-body-2 text-grey-lighten-1 mb-6 status-text">{{ currentStatus }}</p>
          
          <v-btn
            color="error"
            variant="tonal"
            @click="cancelGeneration"
            prepend-icon="mdi-close-circle"
            class="text-none"
            :disabled="currentProgress >= 100"
          >
            Cancel Process
          </v-btn>
        </v-card>
      </v-overlay>

      <!-- Notifications -->
      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        :timeout="snackbar.timeout"
        location="top right"
        rounded="lg"
        elevation="12"
      >
        <div class="d-flex align-center">
          <v-icon :icon="snackbar.icon" class="mr-3" size="large"></v-icon>
          <div>
            <div class="font-weight-bold text-subtitle-1">{{ snackbar.title }}</div>
            <div class="text-body-2 opacity-90">{{ snackbar.message }}</div>
          </div>
        </div>
        <template v-slot:actions>
          <v-btn icon="mdi-close" variant="text" @click="snackbar.show = false"></v-btn>
        </template>
      </v-snackbar>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useMediaApi } from "~/composables/useMediaApi";

definePageMeta({
  layout: "video",
});

const videoInput = ref(null);
const audioInput = ref(null);

const snackbar = ref({
  show: false,
  color: 'success',
  icon: 'mdi-check-circle',
  title: '',
  message: '',
  timeout: 6000,
});

const isDraggingVideo = ref(false);
const isDraggingAudio = ref(false);

const videoFiles = ref([]);
const videoPreviewUrl = ref(null);
const audioFiles = ref([]);

const outputResolution = ref("1280:720");
const resolutionOptions = [
  { title: "YouTube / TV (16:9 HD)", value: "1280:720", icon: "mdi-monitor" },
  { title: "YouTube / TV (16:9 FHD)", value: "1920:1080", icon: "mdi-monitor-screenshot" },
  { title: "TikTok / Reels (9:16 HD)", value: "720:1280", icon: "mdi-cellphone" },
  { title: "TikTok / Reels (9:16 FHD)", value: "1080:1920", icon: "mdi-cellphone-screenshot" },
  { title: "Instagram Square (1:1)", value: "1080:1080", icon: "mdi-crop-square" },
];

const isGenerating = ref(false);
const videoUrl = ref(null);
const videoPath = ref(null);

const showNowPlaying = ref(false);

const overlayTimer = ref({
  enabled: false,
  mode: 'pomodoro', // 'pomodoro' or 'persong'
  minutes: 25,
  withBreak: false,
  breakMinutes: 5,
  fontSize: 48
});

const playlistPos = ref({ x: 5, y: 8 });
const playlistFontSize = ref(32);
const playlistItemsPerCol = ref(15);
const playlistColGap = ref(400);
const timerPos = ref({ x: 75, y: 8 });
const previewBoxRef = ref(null);
const draggingElement = ref(null);
const bgImageDuration = ref(10);
const bgTransitionDuration = ref(1);

const resetPositions = () => {
  playlistPos.value = { x: 5, y: 8 };
  timerPos.value = { x: 75, y: 8 };
};

const onMouseDown = (e, element) => {
  e.preventDefault();
  draggingElement.value = element;
};

const onMouseMove = (e) => {
  if (!draggingElement.value || !previewBoxRef.value) return;
  const rect = previewBoxRef.value.getBoundingClientRect();
  
  // Calculate relative percentage
  let x = ((e.clientX - rect.left) / rect.width) * 100;
  let y = ((e.clientY - rect.top) / rect.height) * 100;
  
  // Clamp between 0 and 95 so it doesn't go completely off-screen
  x = Math.max(0, Math.min(x, 95));
  y = Math.max(0, Math.min(y, 90));

  if (draggingElement.value === 'playlist') {
    playlistPos.value = { x, y };
  } else if (draggingElement.value === 'timer') {
    timerPos.value = { x, y };
  }
};

const onMouseUp = () => {
  draggingElement.value = null;
};

const currentProgress = ref(0);
const currentStatus = ref("");
const currentJobId = ref(null);
let eventSource = null;

const isBackgroundImg = computed(() => {
  return videoFiles.value.length > 0 && videoFiles.value[0].type.startsWith('image/');
});

const previewPlaylist = computed(() => {
  if (audioFiles.value.length > 0) {
    // Show all songs in the preview
    return audioFiles.value.map(f => ({
      title: f.name.replace(/\.[^/.]+$/, "")
    }));
  }
  return [
    { title: "First Song Name" },
    { title: "Second Song Name" },
    { title: "Third Song Name" }
  ];
});

const previewTimerText = computed(() => {
  if (overlayTimer.value.mode === 'pomodoro') {
    const mins = overlayTimer.value.minutes;
    return `${mins < 10 ? '0'+mins : mins}:00`;
  } else {
    return "03:45"; // placeholder for per-song duration
  }
});

const canGenerate = computed(() => videoFiles.value.length > 0 && audioFiles.value.length > 0);

const handleVideoFiles = (files) => {
  const validFiles = files.filter((f) => f.type.startsWith("image/") || f.type.startsWith("video/"));
  if (validFiles.length > 0) {
    videoFiles.value = [...videoFiles.value, ...validFiles];
    if (!videoPreviewUrl.value && videoFiles.value.length > 0) {
      videoPreviewUrl.value = URL.createObjectURL(videoFiles.value[0]);
    }
  }
};

const onDropVideo = (e) => {
  isDraggingVideo.value = false;
  handleVideoFiles(Array.from(e.dataTransfer?.files || []));
};

const onSelectVideo = (e) => {
  handleVideoFiles(Array.from(e.target.files || []));
  e.target.value = '';
};

const onDropAudio = (e) => {
  isDraggingAudio.value = false;
  const files = Array.from(e.dataTransfer?.files || []);
  const validFiles = files.filter((f) => f.type.startsWith("audio/"));
  if (validFiles.length > 0) {
    audioFiles.value = [...audioFiles.value, ...validFiles];
  }
};

const moveVideoUp = (index) => {
  if (index > 0) {
    const temp = videoFiles.value[index];
    videoFiles.value[index] = videoFiles.value[index - 1];
    videoFiles.value[index - 1] = temp;
    updateVideoPreviewUrl();
  }
};

const moveVideoDown = (index) => {
  if (index < videoFiles.value.length - 1) {
    const temp = videoFiles.value[index];
    videoFiles.value[index] = videoFiles.value[index + 1];
    videoFiles.value[index + 1] = temp;
    updateVideoPreviewUrl();
  }
};

const removeVideo = (index) => {
  videoFiles.value.splice(index, 1);
  updateVideoPreviewUrl();
};

const updateVideoPreviewUrl = () => {
  if (videoPreviewUrl.value) URL.revokeObjectURL(videoPreviewUrl.value);
  if (videoFiles.value.length > 0) {
    videoPreviewUrl.value = URL.createObjectURL(videoFiles.value[0]);
  } else {
    videoPreviewUrl.value = null;
  }
};

const clearVideo = () => {
  videoFiles.value = [];
  updateVideoPreviewUrl();
};

const onSelectAudio = (e) => {
  const files = Array.from(e.target.files || []);
  if (files.length > 0) {
    audioFiles.value = [...audioFiles.value, ...files];
  }
};

const clearAudio = () => {
  audioFiles.value = [];
  if (audioInput.value) audioInput.value.value = "";
};

const removeAudio = (index) => {
  audioFiles.value.splice(index, 1);
};

const moveAudioUp = (index) => {
  if (index > 0) {
    const temp = audioFiles.value[index];
    audioFiles.value[index] = audioFiles.value[index - 1];
    audioFiles.value[index - 1] = temp;
  }
};

const moveAudioDown = (index) => {
  if (index < audioFiles.value.length - 1) {
    const temp = audioFiles.value[index];
    audioFiles.value[index] = audioFiles.value[index + 1];
    audioFiles.value[index + 1] = temp;
  }
};

const resetMixer = () => {
  clearVideo();
  clearAudio();
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  videoUrl.value = null;
  videoPath.value = null;
  currentProgress.value = 0;
  currentStatus.value = "";
};

const { createProgressStream, mixMusicVideo } = useMediaApi();

const generateVideo = async () => {
  if (!canGenerate.value) return;

  isGenerating.value = true;
  currentProgress.value = 0;
  currentStatus.value = "Preparing media...";

  const jobId = "job_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6);
  currentJobId.value = jobId;
  eventSource = createProgressStream(jobId);
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.progress)
      currentProgress.value = Math.min(99, Math.round(data.progress));
    if (data.status) currentStatus.value = data.status;
  };
  eventSource.onerror = () => {
    eventSource.close();
  };

  const formData = new FormData();
  formData.append("jobId", jobId);
  // Default transition None (Hard Cut) because we only have 1 video, no need for transitions between videos
  formData.append("transitionTypes", JSON.stringify(["none"]));
  formData.append("resolution", outputResolution.value);
  formData.append("keepOriginalAudio", "false"); // We want the audio mix, not the original background audio
  formData.append("showNowPlaying", showNowPlaying.value.toString());
  if (showNowPlaying.value) {
    formData.append("playlistPosX", playlistPos.value.x);
    formData.append("playlistPosY", playlistPos.value.y);
    formData.append("playlistFontSize", playlistFontSize.value);
    formData.append("playlistItemsPerCol", playlistItemsPerCol.value);
    formData.append("playlistColGap", playlistColGap.value);
  }

  if (overlayTimer.value.enabled) {
    formData.append("overlayTimerEnabled", "true");
    formData.append("overlayTimerMode", overlayTimer.value.mode);
    formData.append("overlayTimerMinutes", overlayTimer.value.minutes);
    formData.append("overlayTimerBreakMinutes", overlayTimer.value.breakMinutes);
    formData.append("overlayTimerWithBreak", overlayTimer.value.withBreak.toString());
    formData.append("timerPosX", timerPos.value.x);
    formData.append("timerPosY", timerPos.value.y);
    formData.append("timerFontSize", overlayTimer.value.fontSize);
  }

  formData.append("bgImageDuration", bgImageDuration.value);
  formData.append("bgTransitionDuration", bgTransitionDuration.value);

  videoFiles.value.forEach((file) => {
    formData.append("video", file);
  });

  audioFiles.value.forEach((file) => {
    formData.append("audio", file);
  });

  try {
    const { blob, videoPath: path } = await mixMusicVideo(formData);
    videoPath.value = path;

    currentProgress.value = 100;
    currentStatus.value = "Compilation Complete!";

    setTimeout(() => {
      videoUrl.value = URL.createObjectURL(blob);
      isGenerating.value = false;
      snackbar.value = {
        show: true,
        color: '#2E7D32',
        icon: 'mdi-party-popper',
        title: '🎉 Compilation Complete!',
        message: 'Your music video is ready to download.',
        timeout: 8000,
      };
      try {
        const audio = new Audio('data:audio/wav;base64,UklGRl9vT19teleAFgABABAAEABAABAAEABAABAAIACAAIAAgACA');
        audio.volume = 0.3;
        audio.play().catch(() => {});
      } catch (e) {}
    }, 500);
  } catch (error) {
    console.error("Generation failed:", error);
    currentStatus.value = "Failed: " + (error.data?.error || error.message);
    isGenerating.value = false;
    snackbar.value = {
      show: true,
      color: '#C62828',
      icon: 'mdi-alert-circle',
      title: '❌ Compilation Failed',
      message: error.data?.error || error.message || 'An unexpected error occurred.',
      timeout: 10000,
    };
  } finally {
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
    currentJobId.value = null;
  }
};

const cancelGeneration = async () => {
  if (!currentJobId.value) return;
  try {
    await fetch("/api/video-mixer/cancel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jobId: currentJobId.value }),
    });
    isGenerating.value = false;
    currentStatus.value = "Cancelled";
    currentProgress.value = 0;
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
  } catch (err) {
    console.error("Failed to cancel:", err);
  }
};

const downloadVideo = () => {
  if (!videoUrl.value) return;
  const a = document.createElement("a");
  a.href = videoUrl.value;
  a.download = `Music_Compilation_${Date.now()}.mp4`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};

onUnmounted(() => {
  if (eventSource) eventSource.close();
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  if (videoPreviewUrl.value) URL.revokeObjectURL(videoPreviewUrl.value);
});
</script>

<style scoped>
.editor-container {
  padding: 10px;
  max-width: 900px;
  margin: 0 auto;
  padding: 10px 24px 10px;
}

.glass-card {
  background: rgba(20, 20, 25, 0.7);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  padding: 32px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.drop-zone {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 200px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drop-zone:hover {
  border-color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.03);
}

.drop-zone.drag-over {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.1);
  transform: scale(1.02);
}

.drop-zone.has-file {
  border-style: solid;
  border-color: rgba(255, 255, 255, 0.1);
  padding: 0;
}

.zone-placeholder {
  pointer-events: none;
}

.zone-preview {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  min-height: 200px;
}

.audio-preview {
  background: rgba(139, 92, 246, 0.15);
  min-height: 100px;
}

.preview-img {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}

.file-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
  padding: 24px 16px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-weight: 500;
}

.clear-box-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  opacity: 0.8;
  backdrop-filter: blur(4px);
}
.clear-box-btn:hover {
  opacity: 1;
}

.floating-icon {
  animation: float 3s ease-in-out infinite;
}

.floating-icon-audio {
  animation: float-pulse 3s ease-in-out infinite;
  color: #8b5cf6 !important;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

@keyframes float-pulse {
  0% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-8px) scale(1.1); color: #c084fc !important; }
  100% { transform: translateY(0px) scale(1); }
}

.audio-list-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: background 0.2s;
}

.audio-list-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.index-badge {
  background: rgba(139, 92, 246, 0.3);
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.generate-btn {
  background: linear-gradient(135deg, #f43f5e 0%, #8b5cf6 100%) !important;
  color: white !important;
  border: none;
  transition: transform 0.2s, box-shadow 0.2s;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(244, 63, 94, 0.4);
}

.processing-card {
  border-radius: 32px !important;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(20,20,25,0.95) !important;
  backdrop-filter: blur(20px);
}

.status-text {
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-area {
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.video-preview-container {
  border-radius: 16px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.1);
}

.final-video {
  width: 100%;
  max-height: 500px;
  display: block;
}

.settings-input :deep(.v-field) {
  border-radius: 12px;
}

/* Live Preview */
.preview-box {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #111;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.preview-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.4;
}
.preview-playlist {
  position: absolute;
  top: 8%;
  left: 5%;
  display: grid;
  grid-auto-flow: column;
  row-gap: 8px;
}
.playlist-item {
  color: rgba(255, 255, 255, 0.6);
  font-weight: bold;
  font-family: 'Courier New', Courier, monospace;
  text-shadow: 1px 1px 2px black;
  display: flex;
  align-items: center;
}
.playlist-item .icon {
  width: 1.2em;
  display: inline-block;
}
.playlist-item.active {
  color: white;
  background: rgba(132, 94, 194, 0.7);
  padding: 4px 12px 4px 4px;
  border-radius: 4px;
  border: 1px solid rgba(255,255,255,0.2);
}
.preview-timer {
  position: absolute;
  padding: 4px 12px;
  background: rgba(0, 0, 0, 0.6);
  border: 2px solid rgba(0, 0, 0, 0.8);
  color: white;
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
  text-align: center;
}
.preview-progress {
  width: 80%;
  height: 4px;
  background: #845ec2;
  margin: 4px auto 0;
  border-radius: 2px;
}
.draggable-element {
  cursor: grab;
  user-select: none;
}
.draggable-element:active {
  cursor: grabbing;
}
</style>
