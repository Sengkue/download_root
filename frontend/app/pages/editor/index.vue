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

        <!-- Suno Song Studio Card -->
        <v-col cols="12" md="6">
          <v-card
            class="hub-card pa-6 rounded-xl h-100 d-flex flex-column"
            elevation="10"
            to="/editor/song-generator"
            style="border: 1px solid rgba(245, 158, 11, 0.35); background: linear-gradient(135deg, rgba(30, 27, 75, 0.7), rgba(15, 23, 42, 0.7));"
          >
            <div class="d-flex align-center mb-4">
              <div class="icon-avatar mr-4" style="background: linear-gradient(135deg, #f59e0b, #d97706); width: 56px; height: 56px; border-radius: 16px; display: flex; align-items: center; justify-content: center;">
                <v-icon size="32" color="white">mdi-music-clef-treble</v-icon>
              </div>
              <div>
                <h2 class="text-h5 font-weight-bold text-white mb-1">Suno Song Studio</h2>
                <span class="badge-tag" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">AI Lao & Suno Music Generator</span>
              </div>
            </div>

            <p class="text-grey-lighten-2 flex-grow-1 mb-6 text-body-1">
              Create complete original Lao songs and background soundtracks using local Suno AI integration and Gemini Lao lyrics generator.
            </p>

            <v-btn
              color="amber-accent-3"
              variant="flat"
              rounded="lg"
              size="large"
              block
              append-icon="mdi-arrow-right"
              class="font-weight-bold text-none text-black"
            >
              Open Suno Song Studio
            </v-btn>
          </v-card>
        </v-col>

        <!-- Meta AI Music Studio Card -->
        <v-col cols="12" md="6">
          <v-card
            class="hub-card pa-6 rounded-xl h-100 d-flex flex-column"
            elevation="10"
            to="/editor/meta-music"
            style="border: 1px solid rgba(6, 182, 212, 0.35); background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));"
          >
            <div class="d-flex align-center mb-4">
              <div class="icon-avatar mr-4" style="background: linear-gradient(135deg, #06b6d4, #8b5cf6); width: 56px; height: 56px; border-radius: 16px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);">
                <v-icon size="32" color="white">mdi-waveform</v-icon>
              </div>
              <div>
                <h2 class="text-h5 font-weight-bold text-white mb-1">Meta AI Music</h2>
                <span class="badge-tag" style="background: rgba(6, 182, 212, 0.2); color: #67e8f9; border: 1px solid rgba(6, 182, 212, 0.4); padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">Python Backend • 100% Free • No Captcha</span>
              </div>
            </div>

            <p class="text-grey-lighten-2 flex-grow-1 mb-6 text-body-1">
              Generate instrumental melodies and music tracks using Meta MusicGen AI running on the dedicated Python FastAPI server. Direct MP3/WAV download.
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
              Open Meta AI Music Studio
            </v-btn>
          </v-card>
        </v-col>

        <!-- Podcast & Story Video Studio Card -->
        <v-col cols="12">
          <v-card
            class="hub-card pa-6 rounded-xl h-100 d-flex flex-column"
            elevation="10"
            to="/editor/podcast-video"
            style="border: 1px solid rgba(168, 85, 247, 0.4); background: linear-gradient(135deg, rgba(88, 28, 135, 0.7), rgba(15, 23, 42, 0.85));"
          >
            <div class="d-flex flex-column flex-sm-row align-sm-center justify-space-between mb-4">
              <div class="d-flex align-center">
                <div class="icon-avatar mr-4" style="background: linear-gradient(135deg, #a855f7, #ec4899); width: 60px; height: 60px; border-radius: 18px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 20px rgba(168, 85, 247, 0.5);">
                  <v-icon size="34" color="white">mdi-podcast</v-icon>
                </div>
                <div>
                  <div class="d-flex align-center gap-2 mb-1 flex-wrap">
                    <h2 class="text-h5 font-weight-black text-white mb-0">Podcast & Story Video Studio</h2>
                    <span class="badge-tag" style="background: rgba(168, 85, 247, 0.25); color: #e9d5ff; border: 1px solid rgba(168, 85, 247, 0.5); padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: bold;">
                      NEW • Hmong & Lao Voice • YouTube Ready
                    </span>
                  </div>
                  <span class="text-subtitle-2 text-grey-lighten-2">ອັດວິດີໂອ / ຮູບພາບ • ສ້າງສຽງອ່ານຄຳສອນໃຈ, ພອດແຄສ ແລະ ນິທານ • ໂພສລົງ YouTube</span>
                </div>
              </div>

              <v-btn
                color="deep-purple-accent-2"
                variant="flat"
                rounded="lg"
                size="large"
                append-icon="mdi-arrow-right"
                class="font-weight-bold text-none mt-4 mt-sm-0"
              >
                Launch Studio
              </v-btn>
            </div>

            <p class="text-grey-lighten-2 mb-4 text-body-1">
              Upload photos or videos, record webcam/screen, type or select Hmong / Lao / Thai / English scripts (encouragement quotes, folklore, podcast episodes), generate word-by-word or narrative voiceover with synchronized animated captions and audio waveforms, then export HD MP4/WebM video files directly for your YouTube podcasts!
            </p>

            <div class="d-flex flex-wrap" style="gap: 8px;">
              <v-chip size="small" color="purple-lighten-3" variant="tonal" prepend-icon="mdi-translate">
                🇲🇼 Lus Hmoob RPA & 🇱🇦 Lao TTS
              </v-chip>
              <v-chip size="small" color="cyan-lighten-3" variant="tonal" prepend-icon="mdi-subtitles-outline">
                Word-by-Word Highlight Captions
              </v-chip>
              <v-chip size="small" color="pink-lighten-3" variant="tonal" prepend-icon="mdi-waveform">
                Live Audio Waveform
              </v-chip>
              <v-chip size="small" color="red-lighten-3" variant="tonal" prepend-icon="mdi-youtube">
                1-Click YouTube Upload
              </v-chip>
            </div>
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
