<template>
  <v-container class="py-10 px-4 fill-height align-center justify-center" fluid>
    <div class="editor-hub-wrapper w-100" style="max-width: 950px;">
      <div class="text-center mb-10">
        <div class="d-inline-flex align-center justify-center pa-3 rounded-circle mb-3 studio-badge">
          <v-icon size="36" color="amber-accent-2">mdi-movie-open</v-icon>
        </div>
        <h1 class="text-h4 font-weight-black text-white mb-2">
          Editor Studio Hub
        </h1>
        <p class="text-grey-lighten-1 text-subtitle-1">
          Select a creator tool below to begin producing your video projects.
        </p>
      </div>

      <v-row justify="center" align="stretch">
        <!-- Photo Mixer Card -->
        <v-col cols="12" md="6">
          <v-card
            class="hub-card pa-6 rounded-xl h-100 d-flex flex-column"
            elevation="10"
            to="/editor/photo-mixer"
          >
            <div class="d-flex align-center mb-4">
              <div class="icon-avatar photo-avatar mr-4">
                <v-icon size="32" color="white">mdi-image-multiple</v-icon>
              </div>
              <div>
                <h2 class="text-h5 font-weight-bold text-white mb-1">Photo Mixer</h2>
                <span class="badge-tag">Photos to Video</span>
              </div>
            </div>

            <p class="text-grey-lighten-2 flex-grow-1 mb-6 text-body-1">
              Transform multiple still images into seamless video slideshows with smooth Ken Burns zoom effects, cinematic transitions, and background soundtrack music.
            </p>

            <v-btn
              color="deep-purple-accent-2"
              variant="flat"
              rounded="lg"
              size="large"
              block
              append-icon="mdi-arrow-right"
              class="font-weight-bold text-none"
            >
              Open Photo Mixer
            </v-btn>
          </v-card>
        </v-col>

        <!-- Video Mixer Card -->
        <v-col cols="12" md="6">
          <v-card
            class="hub-card pa-6 rounded-xl h-100 d-flex flex-column"
            elevation="10"
            to="/editor/video-mixer"
          >
            <div class="d-flex align-center mb-4">
              <div class="icon-avatar video-avatar mr-4">
                <v-icon size="32" color="white">mdi-movie-open-play</v-icon>
              </div>
              <div>
                <h2 class="text-h5 font-weight-bold text-white mb-1">Video Mixer</h2>
                <span class="badge-tag">Merge & Effects</span>
              </div>
            </div>

            <p class="text-grey-lighten-2 flex-grow-1 mb-6 text-body-1">
              Stitch and merge multiple video clips, adjust playback speed, customize video transitions, and replace or add background audio tracks with ease.
            </p>

            <v-btn
              color="cyan-accent-3"
              variant="flat"
              rounded="lg"
              size="large"
              block
              append-icon="mdi-arrow-right"
              class="font-weight-bold text-none text-black"
            >
              Open Video Mixer
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
definePageMeta({
  layout: 'video'
});
</script>

<style scoped>
.studio-badge {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.hub-card {
  background: rgba(30, 41, 59, 0.75) !important;
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.hub-card:hover {
  transform: translateY(-6px);
  border-color: rgba(255, 255, 255, 0.35);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5) !important;
}

.icon-avatar {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-avatar {
  background: linear-gradient(135deg, #ec4899, #8b5cf6);
  box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
}

.video-avatar {
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
}

.badge-tag {
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  font-weight: 600;
}
</style>
