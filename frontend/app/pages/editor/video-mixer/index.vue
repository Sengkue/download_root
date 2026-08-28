<template>
  <div class="editor-container">
    <div class="workspace">
      <!-- Upload Zones -->
      <div v-if="!videoUrl" class="upload-zones">
        <!-- Video Drop Zone -->
        <div
          class="drop-zone glass-card"
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
            accept="video/*"
            multiple
            class="d-none"
            @change="onSelectVideo"
            @click.stop
          />

          <div v-if="videoFiles.length === 0" class="zone-placeholder">
            <v-icon
              icon="mdi-video-outline"
              size="40"
              class="mb-2 floating-icon"
              color="rgba(255,255,255,0.8)"
            ></v-icon>
            <h3 class="text-subtitle-1 font-weight-bold">Video Track</h3>
            <p class="text-caption">Drag & Drop or Click (Multiple allowed)</p>
          </div>

          <div v-else class="zone-preview multi-preview">
            <v-btn
              icon="mdi-close"
              size="x-small"
              color="error"
              variant="flat"
              class="clear-box-btn"
              @click.stop="clearVideos"
              title="Clear Videos"
            ></v-btn>
            <div class="gallery-grid">
              <div
                v-for="(url, index) in videoPreviewUrls.slice(0, 4)"
                :key="index"
                class="gallery-item"
              >
                <video
                  :src="url"
                  class="preview-img-small"
                  muted
                  loop
                  autoplay
                ></video>
              </div>
              <div v-if="videoFiles.length > 4" class="more-indicator">
                +{{ videoFiles.length - 4 }}
              </div>
            </div>
            <div class="file-overlay">
              <v-icon
                icon="mdi-check-circle"
                color="success"
                size="24"
              ></v-icon>
              <span>{{ videoFiles.length }} Video(s) selected</span>
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
              icon="mdi-music-note-outline"
              size="40"
              class="mb-2 floating-icon"
              color="rgba(255,255,255,0.8)"
            ></v-icon>
            <h3 class="text-subtitle-1 font-weight-bold">New Audio Track</h3>
            <p class="text-caption">Drag & Drop or Click (Multiple allowed)</p>
          </div>

          <div v-else class="zone-preview audio-preview">
            <v-btn
              icon="mdi-close"
              size="x-small"
              color="error"
              variant="flat"
              class="clear-box-btn"
              @click.stop="clearAudio"
              title="Clear Audio"
            ></v-btn>
            <v-icon
              icon="mdi-waveform"
              size="40"
              color="white"
              class="wave-icon"
            ></v-icon>
            <div class="file-overlay">
              <v-icon
                icon="mdi-check-circle"
                color="success"
                size="24"
              ></v-icon>
              <span>{{
                audioFiles.length === 1
                  ? audioFiles[0].name
                  : audioFiles.length + " tracks selected"
              }}</span>
              <small>(Click to add more/replace)</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Effects Settings Panel -->
      <div v-if="!videoUrl" class="settings-panel glass-card mt-10">
        <div class="d-flex align-center mb-8">
          <div
            class="icon-box bg-primary-lighten-1 rounded-xl pa-3 mr-4 d-flex align-center justify-center"
          >
            <v-icon icon="mdi-movie-filter" color="primary" size="28"></v-icon>
          </div>
          <div>
            <h3 class="text-h5 font-weight-bold text-white mb-0">
              Montage Settings
            </h3>
            <p class="text-caption text-grey-lighten-1 mb-0">
              Fine-tune speed and transitions
            </p>
          </div>
        </div>

        <v-row>
          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">Video Speed</p>
              <span class="text-caption text-success font-weight-bold"
                >{{ videoSpeed }}x</span
              >
            </div>
            <v-slider
              v-model="videoSpeed"
              color="success"
              track-color="rgba(255,255,255,0.1)"
              min="0.1"
              max="10.0"
              step="0.1"
              hide-details
              thumb-size="20"
              track-size="6"
              class="mt-2"
            >
              <template v-slot:prepend>
                <v-icon
                  size="20"
                  color="grey-lighten-1"
                  @click="
                    videoSpeed = Math.max(
                      0.1,
                      Number((videoSpeed - 0.1).toFixed(1)),
                    )
                  "
                  >mdi-minus</v-icon
                >
              </template>
              <template v-slot:append>
                <v-icon
                  size="20"
                  color="grey-lighten-1"
                  @click="
                    videoSpeed = Math.min(
                      10.0,
                      Number((videoSpeed + 0.1).toFixed(1)),
                    )
                  "
                  >mdi-plus</v-icon
                >
              </template>
            </v-slider>
          </v-col>

          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">
                Slide Transition Effects
              </p>
              <span class="text-caption text-primary font-weight-bold"
                >{{ selectedTransitions.length }} selected</span
              >
            </div>
            <v-select
              v-model="selectedTransitions"
              :items="transitionOptions"
              item-title="title"
              item-value="value"
              multiple
              variant="outlined"
              bg-color="rgba(255,255,255,0.05)"
              color="primary"
              hide-details
              class="beautiful-select rounded-lg"
              menu-icon="mdi-chevron-down"
              theme="dark"
              :menu-props="{ contentClass: 'bg-grey-darken-4' }"
            >
              <template v-slot:prepend-item>
                <v-list-item
                  ripple
                  @click="toggleAllTransitions"
                  class="transition-list-item"
                >
                  <template v-slot:prepend>
                    <v-list-item-action start>
                      <v-checkbox-btn
                        :model-value="likesAllTransitions"
                        :indeterminate="likesSomeTransitions"
                        color="primary"
                      ></v-checkbox-btn>
                    </v-list-item-action>
                    <v-icon
                      icon="mdi-check-all"
                      :color="
                        likesAllTransitions ? 'primary' : 'grey-lighten-1'
                      "
                      class="mr-3"
                    ></v-icon>
                  </template>
                  <v-list-item-title
                    :class="
                      likesAllTransitions
                        ? 'text-primary font-weight-bold'
                        : 'text-white'
                    "
                  >
                    Select All / Clear All
                  </v-list-item-title>
                </v-list-item>
                <v-divider class="my-1"></v-divider>
              </template>

              <template v-slot:selection="{ item, index }">
                <v-chip
                  v-if="index < 2"
                  color="primary"
                  size="small"
                  variant="flat"
                  class="font-weight-bold mr-1"
                >
                  {{ item.raw.title }}
                </v-chip>
                <span
                  v-if="index === 2"
                  class="text-caption text-grey-lighten-1 ml-1"
                >
                  (+{{ selectedTransitions.length - 2 }} others)
                </span>
              </template>

              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  title=""
                  :class="{
                    'selected-item': selectedTransitions.includes(
                      item.raw.value,
                    ),
                  }"
                  class="transition-list-item"
                >
                  <template v-slot:prepend="{ isActive }">
                    <v-list-item-action start>
                      <v-checkbox-btn
                        :model-value="isActive"
                        color="primary"
                      ></v-checkbox-btn>
                    </v-list-item-action>
                    <v-icon
                      :icon="item.raw.icon"
                      :color="isActive ? 'primary' : 'grey-lighten-1'"
                      class="mr-3"
                    ></v-icon>
                  </template>
                  <v-list-item-title
                    :class="
                      isActive ? 'text-primary font-weight-bold' : 'text-white'
                    "
                  >
                    {{ item.raw.title }}
                  </v-list-item-title>
                  <template v-slot:append>
                    <div
                      class="transition-preview-box"
                      :class="'preview-' + item.raw.value"
                    >
                      <div class="preview-layer-1"></div>
                      <div class="preview-layer-2"></div>
                    </div>
                  </template>
                </v-list-item>
              </template>
            </v-select>
          </v-col>
        </v-row>

        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">
                Target Video Length
              </p>
              <span class="text-caption text-primary font-weight-bold">
                {{
                  targetDurationValue > 0
                    ? targetDurationValue + " " + targetDurationUnit
                    : "Auto (Shortest)"
                }}
              </span>
            </div>
            <div class="d-flex align-center mt-2" style="gap: 12px">
              <v-text-field
                v-model.number="targetDurationValue"
                type="number"
                min="0"
                density="compact"
                hide-details
                variant="outlined"
                bg-color="rgba(255,255,255,0.05)"
                color="primary"
                class="rounded-lg"
                placeholder="0 = Auto"
              ></v-text-field>
              <v-select
                v-model="targetDurationUnit"
                :items="['Seconds', 'Minutes', 'Hours']"
                density="compact"
                hide-details
                variant="outlined"
                bg-color="rgba(255,255,255,0.05)"
                color="primary"
                class="rounded-lg"
                style="max-width: 140px"
                theme="dark"
                :menu-props="{ contentClass: 'bg-grey-darken-4' }"
              ></v-select>
            </div>
          </v-col>

          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">
                Transition Duration
              </p>
              <span class="text-caption text-warning font-weight-bold"
                >{{ transitionDuration }} seconds</span
              >
            </div>
            <v-slider
              v-model="transitionDuration"
              color="warning"
              track-color="rgba(255,255,255,0.1)"
              min="0.5"
              max="3"
              step="0.5"
              hide-details
              thumb-size="20"
              track-size="6"
              class="mt-2"
            >
              <template v-slot:prepend>
                <v-icon
                  size="20"
                  color="grey-lighten-1"
                  @click="
                    transitionDuration = Math.max(0.5, transitionDuration - 0.5)
                  "
                  >mdi-minus</v-icon
                >
              </template>
              <template v-slot:append>
                <v-icon
                  size="20"
                  color="grey-lighten-1"
                  @click="
                    transitionDuration = Math.min(3, transitionDuration + 0.5)
                  "
                  >mdi-plus</v-icon
                >
              </template>
            </v-slider>
          </v-col>
        </v-row>

        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">Output Resolution</p>
              <span class="text-caption text-primary font-weight-bold"
                >Select aspect ratio</span
              >
            </div>
            <v-select
              v-model="outputResolution"
              :items="resolutionOptions"
              item-title="title"
              item-value="value"
              density="compact"
              hide-details
              variant="outlined"
              bg-color="rgba(255,255,255,0.05)"
              color="primary"
              class="rounded-lg"
              theme="dark"
              :menu-props="{ contentClass: 'bg-grey-darken-4' }"
            >
              <template v-slot:selection="{ item }">
                <v-icon
                  :icon="item.raw.icon"
                  size="small"
                  class="mr-2"
                ></v-icon>
                {{ item.raw.title }}
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :title="item.raw.title">
                  <template v-slot:prepend>
                    <v-icon
                      :icon="item.raw.icon"
                      color="grey-lighten-1"
                      class="mr-3"
                    ></v-icon>
                  </template>
                  <template v-slot:subtitle>
                    <span class="text-grey-lighten-1">{{
                      item.raw.value
                    }}</span>
                  </template>
                </v-list-item>
              </template>
            </v-select>
          </v-col>

          <v-col cols="12" md="6" class="d-flex align-center mt-6">
            <v-switch
              v-model="keepOriginalAudio"
              :disabled="videoFiles.length > 1"
              :label="
                videoFiles.length > 1
                  ? 'Original sound disabled (Multi-video)'
                  : 'Keep Original Video Sound'
              "
              color="success"
              inset
              hide-details
              class="font-weight-bold text-white"
            ></v-switch>
          </v-col>
        </v-row>
      </div>

      <!-- Result View -->
      <div v-if="videoUrl" class="result-view glass-card">
        <h3 class="mb-4 d-flex align-center gap-2">
          <v-icon icon="mdi-movie-open-check" color="success"></v-icon>
          Mixed Video is Ready
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
            @click="resetMixer"
            class="action-btn"
          >
            Mix Another
          </v-btn>
          <v-btn
            size="large"
            color="success"
            prepend-icon="mdi-download"
            @click="downloadVideo"
            class="action-btn download-btn"
          >
            Download Final Video
          </v-btn>
        </div>
      </div>

      <!-- Generate Section -->
      <div v-if="!videoUrl" class="generate-section mt-8">
        <div
          v-if="!isGenerating"
          class="d-flex justify-center"
          style="gap: 16px"
        >
          <v-btn
            size="x-large"
            color="primary"
            :disabled="!canGenerate"
            @click="generateVideo"
            class="generate-btn"
            elevation="8"
          >
            <template v-slot:prepend>
              <v-icon icon="mdi-magic-staff"></v-icon>
            </template>
            MIX VIDEO & AUDIO INSTANTLY
          </v-btn>
        </div>

        <div v-if="isGenerating" class="progress-section mt-8">
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="text-subtitle-1 text-white">{{ currentStatus }}</span>
            <div class="d-flex align-center" style="gap: 12px">
              <span class="progress-percent">{{ currentProgress }}%</span>
              <v-btn
                size="small"
                color="error"
                variant="flat"
                @click="cancelGeneration"
              >
                <v-icon icon="mdi-close" class="mr-1"></v-icon> Cancel
              </v-btn>
            </div>
          </div>
          <v-progress-linear
            v-model="currentProgress"
            color="primary"
            height="12"
            rounded
            class="progress-bar-smooth bg-grey-darken-3"
          ></v-progress-linear>
          <p class="text-caption text-grey-lighten-1 mt-2 text-center">
            Stream copying video data... (Ultra-fast processing)
          </p>
        </div>
      </div>
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

const isDraggingVideo = ref(false);
const isDraggingAudio = ref(false);

const videoFile = ref(null);
const videoFiles = ref([]);
const videoPreviewUrls = ref([]);
const audioFiles = ref([]);

const videoSpeed = ref(1.0);
const transitionDuration = ref(1.0);
const targetDurationValue = ref(0);
const targetDurationUnit = ref("Hours");
const keepOriginalAudio = ref(false);
const outputResolution = ref("1280:720");
const resolutionOptions = [
  { title: "YouTube / TV (16:9 HD)", value: "1280:720", icon: "mdi-monitor" },
  {
    title: "YouTube / TV (16:9 FHD)",
    value: "1920:1080",
    icon: "mdi-monitor-screenshot",
  },
  {
    title: "TikTok / Reels (9:16 HD)",
    value: "720:1280",
    icon: "mdi-cellphone",
  },
  {
    title: "TikTok / Reels (9:16 FHD)",
    value: "1080:1920",
    icon: "mdi-cellphone-screenshot",
  },
  {
    title: "Instagram Square (1:1)",
    value: "1080:1080",
    icon: "mdi-crop-square",
  },
];
const transitionOptions = [
  {
    title: "None (Hard Cut)",
    value: "none",
    icon: "mdi-format-horizontal-align-center",
  },
  { title: "Smooth Crossfade", value: "fade", icon: "mdi-blur" },
  {
    title: "Fade to Black",
    value: "fadeblack",
    icon: "mdi-moon-waning-crescent",
  },
  {
    title: "Fade to White",
    value: "fadewhite",
    icon: "mdi-white-balance-sunny",
  },
  {
    title: "Wipe Left",
    value: "wipeleft",
    icon: "mdi-format-horizontal-align-left",
  },
  {
    title: "Wipe Right",
    value: "wiperight",
    icon: "mdi-format-horizontal-align-right",
  },
  {
    title: "Iris Circle Crop",
    value: "circlecrop",
    icon: "mdi-record-circle-outline",
  },
  { title: "Square Box Crop", value: "rectcrop", icon: "mdi-square-outline" },
  {
    title: "Fly Away Warp 🚀",
    value: "distance",
    icon: "mdi-rocket-launch-outline",
  },
  { title: "Clock Sweep", value: "radial", icon: "mdi-clock-outline" },
  { title: "Retro Pixelize", value: "pixelize", icon: "mdi-checkerboard" },
  { title: "Horizontal Blur", value: "hblur", icon: "mdi-blur-linear" },
];

const selectedTransitions = ref(transitionOptions.map((t) => t.value));

const likesAllTransitions = computed(
  () => selectedTransitions.value.length === transitionOptions.length,
);
const likesSomeTransitions = computed(
  () => selectedTransitions.value.length > 0 && !likesAllTransitions.value,
);

const toggleAllTransitions = () => {
  if (likesAllTransitions.value) {
    selectedTransitions.value = [];
  } else {
    selectedTransitions.value = transitionOptions.map((t) => t.value);
  }
};

const isGenerating = ref(false);
const videoUrl = ref(null);

const currentProgress = ref(0);
const currentStatus = ref("");
const currentJobId = ref(null);
let eventSource = null;

const canGenerate = computed(() => videoFiles.value.length > 0);

const handleVideoFiles = (files) => {
  const validFiles = files.filter((f) => f.type.startsWith("video/"));
  if (validFiles.length > 0) {
    videoFiles.value = validFiles;
    videoPreviewUrls.value.forEach((url) => URL.revokeObjectURL(url));
    videoPreviewUrls.value = validFiles.map((file) =>
      URL.createObjectURL(file),
    );
  }
};

const onDropVideo = (e) => {
  isDraggingVideo.value = false;
  const files = Array.from(e.dataTransfer?.files || []);
  handleVideoFiles(files);
};

const onSelectVideo = (e) => {
  const files = Array.from(e.target.files || []);
  handleVideoFiles(files);
};

const onDropAudio = (e) => {
  isDraggingAudio.value = false;
  const files = Array.from(e.dataTransfer?.files || []);
  const validFiles = files.filter((f) => f.type.startsWith("audio/"));
  if (validFiles.length > 0) {
    audioFiles.value = validFiles;
  }
};

const onSelectAudio = (e) => {
  const files = Array.from(e.target.files || []);
  if (files.length > 0) {
    audioFiles.value = files;
  }
};

const resetMixer = () => {
  videoFiles.value = [];
  videoPreviewUrls.value.forEach((url) => URL.revokeObjectURL(url));
  videoPreviewUrls.value = [];
  audioFiles.value = [];
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  videoUrl.value = null;
  currentProgress.value = 0;
  currentStatus.value = "";
  if (videoInput.value) videoInput.value.value = "";
  if (audioInput.value) audioInput.value.value = "";
};

const clearVideos = () => {
  videoFiles.value = [];
  videoPreviewUrls.value.forEach((url) => URL.revokeObjectURL(url));
  videoPreviewUrls.value = [];
  if (videoInput.value) videoInput.value.value = "";
};

const clearAudio = () => {
  audioFiles.value = [];
  if (audioInput.value) audioInput.value.value = "";
};

const { createProgressStream, mixVideoMontage } = useMediaApi();

const generateVideo = async () => {
  if (!canGenerate.value) return;

  isGenerating.value = true;
  currentProgress.value = 0;
  currentStatus.value = "Preparing media...";

  const jobId =
    "job_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6);
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
  formData.append("videoSpeed", videoSpeed.value);
  formData.append("transitionDuration", transitionDuration.value);
  formData.append("transitionTypes", JSON.stringify(selectedTransitions.value));
  formData.append("keepOriginalAudio", keepOriginalAudio.value);
  formData.append("resolution", outputResolution.value);

  let tDurationSeconds = 0;
  if (targetDurationValue.value > 0) {
    if (targetDurationUnit.value === "Seconds")
      tDurationSeconds = targetDurationValue.value;
    else if (targetDurationUnit.value === "Minutes")
      tDurationSeconds = targetDurationValue.value * 60;
    else if (targetDurationUnit.value === "Hours")
      tDurationSeconds = targetDurationValue.value * 3600;
  }
  formData.append("targetDuration", tDurationSeconds);

  videoFiles.value.forEach((file) => {
    formData.append("video", file);
  });

  audioFiles.value.forEach((file) => {
    formData.append("audio", file);
  });

  try {
    const blob = await mixVideoMontage(formData);

    currentProgress.value = 100;
    currentStatus.value = "Mixing Complete!";

    setTimeout(() => {
      videoUrl.value = URL.createObjectURL(blob);
      isGenerating.value = false;
    }, 500);
  } catch (error) {
    console.error("Generation failed:", error);
    currentStatus.value = "Failed: " + (error.data?.error || error.message);
    isGenerating.value = false;
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
  a.download = `Mixed_Video_${Date.now()}.mp4`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};

onUnmounted(() => {
  if (eventSource) eventSource.close();
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  videoPreviewUrls.value.forEach((url) => URL.revokeObjectURL(url));
});
</script>

<style scoped>
.editor-container {
  padding: 10px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 10px 24px 10px;
}

.glass-card {
  background: rgba(20, 20, 25, 0.7);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
  transition:
    transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 0.3s;
}

.glass-card:hover {
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.6);
}

.modern-header {
  text-align: center;
  padding: 40px 20px 50px;
  background: radial-gradient(
    circle at top,
    rgba(132, 94, 194, 0.15),
    transparent 60%
  );
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0 0 40px 40px;
  margin-bottom: 40px;
}

.gradient-text {
  background: linear-gradient(135deg, #ff6b6b, #845ec2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.floating-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

.upload-zones {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.drop-zone {
  height: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  position: relative;
  border: 2px dashed rgba(255, 255, 255, 0.15);
}

.drop-zone:hover {
  border-color: #845ec2;
  box-shadow: inset 0 0 30px rgba(132, 94, 194, 0.1);
}

.drop-zone.drag-over {
  border-color: #ff6b6b;
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
  margin-bottom: 2px;
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

.audio-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    135deg,
    rgba(132, 94, 194, 0.2) 0%,
    rgba(255, 107, 107, 0.2) 100%
  );
}

.clear-box-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 10;
  opacity: 0.8;
  transition: opacity 0.2s;
}
.clear-box-btn:hover {
  opacity: 1;
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
  background: linear-gradient(135deg, #ff6b6b 0%, #845ec2 100%) !important;
  color: white !important;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 0 48px !important;
  height: 64px !important;
  border-radius: 32px !important;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
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
}

.progress-percent {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ff6b6b, #845ec2);
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

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 0.5;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Transition Previews */
.transition-preview-box {
  width: 48px;
  height: 28px;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-left: 16px;
  background: #2a2a35;
}
.preview-layer-1,
.preview-layer-2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.preview-layer-1 {
  background: #ff6b6b;
}
.preview-layer-2 {
  background: #845ec2;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

/* None */
.preview-none .preview-layer-2 {
  animation-name: anim-none;
}
@keyframes anim-none {
  0%,
  49.9% {
    opacity: 0;
  }
  50%,
  100% {
    opacity: 1;
  }
}

/* Fade */
.preview-fade .preview-layer-2 {
  animation-name: anim-fade;
}
@keyframes anim-fade {
  0%,
  30% {
    opacity: 0;
  }
  50%,
  80% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

/* Fade Black / Fade White */
.preview-fadeblack {
  background: #000;
}
.preview-fadewhite {
  background: #fff;
}
.preview-fadeblack .preview-layer-1,
.preview-fadewhite .preview-layer-1 {
  animation: anim-fade1 3s infinite;
}
.preview-fadeblack .preview-layer-2,
.preview-fadewhite .preview-layer-2 {
  animation: anim-fade2 3s infinite;
}
@keyframes anim-fade1 {
  0%,
  30% {
    opacity: 1;
  }
  45%,
  55% {
    opacity: 0;
  }
  70%,
  100% {
    opacity: 1;
  }
}
@keyframes anim-fade2 {
  0%,
  45% {
    opacity: 0;
  }
  60%,
  100% {
    opacity: 1;
  }
}

/* Wipe Left */
.preview-wipeleft .preview-layer-2 {
  animation-name: anim-wipeleft;
}
@keyframes anim-wipeleft {
  0%,
  20% {
    clip-path: polygon(100% 0, 100% 0, 100% 100%, 100% 100%);
  }
  50%,
  80% {
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
  }
  100% {
    clip-path: polygon(100% 0, 100% 0, 100% 100%, 100% 100%);
  }
}

/* Wipe Right */
.preview-wiperight .preview-layer-2 {
  animation-name: anim-wiperight;
}
@keyframes anim-wiperight {
  0%,
  20% {
    clip-path: polygon(0 0, 0 0, 0 100%, 0 100%);
  }
  50%,
  80% {
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
  }
  100% {
    clip-path: polygon(0 0, 0 0, 0 100%, 0 100%);
  }
}

/* Circle Crop */
.preview-circlecrop .preview-layer-2 {
  animation-name: anim-circlecrop;
}
@keyframes anim-circlecrop {
  0%,
  20% {
    clip-path: circle(0% at 50% 50%);
  }
  50%,
  80% {
    clip-path: circle(100% at 50% 50%);
  }
  100% {
    clip-path: circle(0% at 50% 50%);
  }
}

/* Rect Crop */
.preview-rectcrop .preview-layer-2 {
  animation-name: anim-rectcrop;
}
@keyframes anim-rectcrop {
  0%,
  20% {
    clip-path: inset(50% 50% 50% 50%);
  }
  50%,
  80% {
    clip-path: inset(0% 0% 0% 0%);
  }
  100% {
    clip-path: inset(50% 50% 50% 50%);
  }
}

/* Distance (Zoom) */
.preview-distance .preview-layer-2 {
  animation-name: anim-distance;
  transform-origin: center;
}
@keyframes anim-distance {
  0%,
  20% {
    transform: scale(0.2);
    opacity: 0;
  }
  50%,
  80% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(0.2);
    opacity: 0;
  }
}

/* Blur */
.preview-hblur .preview-layer-2 {
  animation-name: anim-hblur;
}
@keyframes anim-hblur {
  0%,
  20% {
    opacity: 0;
    filter: blur(4px);
  }
  50%,
  80% {
    opacity: 1;
    filter: blur(0px);
  }
  100% {
    opacity: 0;
    filter: blur(4px);
  }
}

/* Pixelize */
.preview-pixelize .preview-layer-2 {
  animation-name: anim-pixelize;
}
@keyframes anim-pixelize {
  0%,
  20% {
    opacity: 0;
    transform: scale(1.1);
    filter: contrast(150%) brightness(120%);
  }
  50%,
  80% {
    opacity: 1;
    transform: scale(1);
    filter: contrast(100%) brightness(100%);
  }
  100% {
    opacity: 0;
    transform: scale(1.1);
    filter: contrast(150%) brightness(120%);
  }
}

/* Radial */
.preview-radial .preview-layer-2 {
  animation-name: anim-radial;
}
@keyframes anim-radial {
  0%,
  20% {
    clip-path: polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%);
  }
  50%,
  80% {
    clip-path: polygon(
      50% 50%,
      50% 0%,
      100% 0%,
      100% 100%,
      0% 100%,
      0% 0%,
      50% 0%
    );
  }
  100% {
    clip-path: polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%);
  }
}
</style>
