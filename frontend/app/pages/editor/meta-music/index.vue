<template>
  <v-container class="py-6 px-4 meta-music-container" fluid>
    <div class="meta-wrapper mx-auto" style="max-width: 1400px;">
      
      <!-- Top Hero Banner -->
      <v-card class="hero-card pa-6 mb-6 rounded-2xl" elevation="10">
        <div class="d-flex flex-wrap align-center justify-space-between gap-4">
          <!-- Left: Title & Subtitle -->
          <div class="d-flex align-center">
            <div class="meta-avatar-glow mr-4">
              <v-icon size="40" color="cyan-accent-2">mdi-waveform</v-icon>
            </div>
            <div>
              <div class="d-flex align-center flex-wrap gap-2">
                <h1 class="text-h4 font-weight-black text-white brand-title">
                  Meta AI Music Studio
                </h1>
                <v-chip
                  :color="isServerOnline ? 'emerald-accent' : 'error'"
                  size="small"
                  variant="flat"
                  class="ml-2 font-weight-bold status-pill text-white"
                >
                  <span class="pulse-dot mr-1.5" :class="{ 'pulse-active': isServerOnline }"></span>
                  {{ isServerOnline ? 'Python Server Online (Port 3005)' : 'Server Offline (Port 3005)' }}
                </v-chip>
                <v-chip
                  color="cyan-accent-4"
                  size="small"
                  variant="outlined"
                  class="font-weight-bold ml-1 text-white"
                >
                  <v-icon start size="14">mdi-shield-check</v-icon>
                  100% Free • ບໍ່ມີ Captcha
                </v-chip>
              </div>
              <p class="subtitle-text text-body-2 mt-1 mb-0">
                ສະຕູດິໂອສ້າງດົນຕີຄຸນນະພາບສູງດ້ວຍ Meta MusicGen AI ຂັບເຄື່ອນດ້ວຍ Python FastAPI Backend
              </p>
            </div>
          </div>

          <!-- Right: Controls & Navigation -->
          <div class="d-flex align-center flex-wrap gap-3">
            <v-btn
              variant="tonal"
              color="cyan-accent-2"
              rounded="xl"
              prepend-icon="mdi-refresh"
              :loading="checkingStatus"
              @click="checkStatus"
              class="refresh-btn text-none font-weight-bold px-4"
            >
              Refresh
            </v-btn>

            <v-btn
              variant="tonal"
              :color="hasToken ? 'emerald-accent' : 'purple-accent-2'"
              rounded="xl"
              prepend-icon="mdi-key-outline"
              @click="tokenDialog = true"
              class="text-none font-weight-bold px-4"
            >
              {{ hasToken ? '🔑 Token: ພ້ອມໃຊ້ງານ' : '🔑 ໃສ່ HF Token (ຟຣີ)' }}
            </v-btn>

            <v-btn
              variant="flat"
              color="amber-accent-3"
              rounded="xl"
              prepend-icon="mdi-music-clef-treble"
              to="/editor/song-generator"
              class="text-none font-weight-bold px-4 text-black"
            >
              🎵 ໄປທີ່ Suno Song Studio
            </v-btn>
          </div>
        </div>

        <!-- Offline Server Alert -->
        <v-alert
          v-if="!isServerOnline && !checkingStatus"
          type="warning"
          variant="tonal"
          rounded="xl"
          class="mt-4 offline-alert"
          icon="mdi-alert-circle-outline"
        >
          <div class="font-weight-bold text-amber-lighten-1">Python Backend ຍັງບໍ່ທັນເປີດ (Port 3005)</div>
          <div class="text-caption text-white mt-1">
            ກະລຸນາເປີດໄຟລ໌ <code>2_start_python_backend.bat</code> ໃນໂຟນເດີໂປຣເຈັກ ເພື່ອເລີ່ມຕົ້ນລະບົບ Meta MusicGen AI.
          </div>
        </v-alert>
      </v-card>

      <!-- Main Workspace Grid -->
      <v-row class="workspace-row">
        <!-- LEFT COLUMN: Generator Controls -->
        <v-col cols="12" lg="6" xl="6">
          <v-card class="generator-panel pa-6 rounded-2xl h-100" elevation="8">
            <div class="d-flex align-center justify-space-between mb-4">
              <div class="d-flex align-center">
                <v-icon color="cyan-accent-3" class="mr-2" size="24">mdi-music-note-plus</v-icon>
                <h2 class="text-h6 font-weight-bold text-white">ແຕ່ງດົນຕີໃໝ່ (AI Music Composer)</h2>
              </div>
              <v-chip size="small" color="purple-accent-2" variant="tonal" class="font-weight-bold">
                Meta MusicGen-Small
              </v-chip>
            </div>

            <v-form @submit.prevent="generateMusic">
              <!-- Hugging Face Token (Frontend Input) -->
              <div class="form-group mb-4 token-input-box pa-3 rounded-xl">
                <div class="d-flex align-center justify-space-between mb-1.5">
                  <label class="input-label d-flex align-center">
                    <v-icon size="18" color="cyan-accent-2" class="mr-1.5">mdi-key-variant</v-icon>
                    Hugging Face Token (ໃສ່ Token ຢູ່ບ່ອນນີ້)
                  </label>
                  <a
                    href="https://huggingface.co/settings/tokens"
                    target="_blank"
                    class="text-caption text-cyan-accent-2 text-decoration-none font-weight-bold d-flex align-center"
                  >
                    <span>ຮັບ Token ຟຣີ</span>
                    <v-icon size="12" class="ml-1">mdi-open-in-new</v-icon>
                  </a>
                </div>
                <v-text-field
                  v-model="form.hf_token"
                  :type="showToken ? 'text' : 'password'"
                  placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                  variant="outlined"
                  density="compact"
                  rounded="lg"
                  class="custom-input high-contrast-input"
                  hide-details="auto"
                  :append-inner-icon="showToken ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showToken = !showToken"
                  @update:model-value="onTokenInput"
                  clearable
                ></v-text-field>
                <div class="d-flex align-center justify-space-between mt-1.5">
                  <span class="text-caption text-grey-lighten-2">
                    💡 ພິມ ຫຼື Paste ໃສ່ບ່ອນນີ້ໄດ້ເລີຍ ລະບົບຈະຈື່ໄວ້ໃຫ້ອັດຕະໂນມັດ ບໍ່ຕ້ອງເຂົ້າໄປແປງໄຟລ໌ .env
                  </span>
                  <v-chip
                    v-if="form.hf_token"
                    size="x-small"
                    color="emerald-accent"
                    variant="flat"
                    class="font-weight-bold text-white ml-2 flex-shrink-0"
                  >
                    <v-icon start size="12">mdi-check</v-icon>
                    ພ້ອມໃຊ້ງານ
                  </v-chip>
                </div>
              </div>

              <!-- Song Title (Optional) -->
              <div class="form-group mb-4">
                <label class="input-label d-flex align-center justify-space-between mb-2">
                  <span class="d-flex align-center">
                    <v-icon size="18" color="cyan-accent-2" class="mr-1.5">mdi-format-title</v-icon>
                    ຊື່ເພງ / ຊື່ໂປຣເຈັກ (Track Title)
                  </span>
                  <span class="optional-badge">ບໍ່ບັງຄັບ</span>
                </label>
                <v-text-field
                  v-model="form.title"
                  placeholder="ຕົວຢ່າງ: ສຽງແຄນແຄມຂອງ, Lao Coffee Chill Lo-Fi..."
                  variant="outlined"
                  density="comfortable"
                  rounded="lg"
                  class="custom-input high-contrast-input"
                  hide-details="auto"
                  clearable
                ></v-text-field>
              </div>

              <!-- Music Description / Prompt -->
              <div class="form-group mb-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <label class="input-label d-flex align-center">
                    <v-icon size="18" color="cyan-accent-2" class="mr-1.5">mdi-text-box-outline</v-icon>
                    ຄຳອະທິບາຍດົນຕີ (Music Style Description) *
                  </label>
                  <v-btn
                    size="small"
                    variant="tonal"
                    color="purple-accent-2"
                    rounded="lg"
                    :loading="enhancingPrompt"
                    @click="enhancePrompt"
                    class="text-none font-weight-bold px-3 ai-enhance-btn"
                  >
                    <v-icon start size="16">mdi-auto-fix</v-icon>
                    ປັບປຸງດ້ວຍ Gemini AI
                  </v-btn>
                </div>
                <v-textarea
                  v-model="form.prompt"
                  placeholder="ຕົວຢ່າງ: Lao traditional acoustic guitar and melodic khaen flute, relaxing river atmosphere, 85 bpm, warm cinematic tones..."
                  variant="outlined"
                  rows="3"
                  rounded="lg"
                  class="custom-input high-contrast-input"
                  hide-details="auto"
                  required
                ></v-textarea>
              </div>

              <!-- Quick Style Presets Chips -->
              <div class="presets-section mb-5">
                <div class="text-caption text-grey-lighten-2 mb-2 d-flex align-center">
                  <v-icon size="14" color="cyan-accent-2" class="mr-1">mdi-tag-multiple-outline</v-icon>
                  ແນວດົນຕີຍອດນິຍົມ (Click to apply preset):
                </div>
                <div class="d-flex flex-wrap gap-2">
                  <v-chip
                    v-for="(preset, idx) in stylePresets"
                    :key="idx"
                    size="small"
                    variant="tonal"
                    :color="preset.color"
                    class="preset-chip font-weight-bold"
                    @click="applyPreset(preset)"
                  >
                    <v-icon start size="14">{{ preset.icon }}</v-icon>
                    {{ preset.name }}
                  </v-chip>
                </div>
              </div>

              <!-- Controls: Duration & Seed -->
              <v-row class="mb-4">
                <!-- Duration Selector -->
                <v-col cols="12" sm="7">
                  <div class="control-box pa-4 rounded-xl">
                    <div class="d-flex align-center justify-space-between mb-2">
                      <span class="text-body-2 font-weight-bold text-white d-flex align-center">
                        <v-icon size="18" color="cyan-accent-3" class="mr-1.5">mdi-timer-outline</v-icon>
                        ຄວາມຍາວ (Duration)
                      </span>
                      <v-chip size="x-small" color="cyan-accent-3" variant="flat" class="font-weight-black text-black">
                        {{ form.duration }} ວິນາທີ (Seconds)
                      </v-chip>
                    </div>

                    <div class="d-flex gap-1 mb-2">
                      <v-btn
                        v-for="d in [10, 15, 20, 30]"
                        :key="d"
                        size="x-small"
                        :variant="form.duration === d ? 'flat' : 'tonal'"
                        :color="form.duration === d ? 'cyan-accent-3' : 'grey-lighten-2'"
                        :class="form.duration === d ? 'text-black font-weight-black' : 'text-white'"
                        rounded="pill"
                        class="flex-grow-1"
                        @click="form.duration = d"
                      >
                        {{ d }}s
                      </v-btn>
                    </div>

                    <v-slider
                      v-model="form.duration"
                      :min="10"
                      :max="30"
                      :step="5"
                      color="cyan-accent-3"
                      track-color="rgba(255,255,255,0.15)"
                      hide-details
                      class="custom-slider"
                    ></v-slider>
                  </div>
                </v-col>

                <!-- Seed Selector -->
                <v-col cols="12" sm="5">
                  <div class="control-box pa-4 rounded-xl h-100 d-flex flex-column justify-space-between">
                    <div class="d-flex align-center justify-space-between mb-2">
                      <span class="text-body-2 font-weight-bold text-white d-flex align-center">
                        <v-icon size="18" color="purple-accent-2" class="mr-1.5">mdi-dice-multiple-outline</v-icon>
                        Seed (0 - 10)
                      </span>
                      <v-chip size="x-small" color="purple-accent-2" variant="flat" class="font-weight-black text-white">
                        #{{ form.seed }}
                      </v-chip>
                    </div>

                    <div class="d-flex align-center gap-2">
                      <v-slider
                        v-model="form.seed"
                        :min="0"
                        :max="10"
                        :step="1"
                        color="purple-accent-2"
                        track-color="rgba(255,255,255,0.15)"
                        hide-details
                        class="custom-slider flex-grow-1"
                      ></v-slider>
                      <v-btn
                        icon="mdi-dice-5-outline"
                        size="small"
                        variant="tonal"
                        color="purple-accent-2"
                        @click="randomizeSeed"
                        title="Randomize Seed"
                      ></v-btn>
                    </div>
                  </div>
                </v-col>
              </v-row>

              <!-- Generating Progress Box -->
              <div v-if="isGenerating" class="generating-progress-box pa-4 rounded-xl mb-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <span class="text-body-2 font-weight-bold text-white d-flex align-center">
                    <v-progress-circular indeterminate size="18" width="2" color="cyan-accent-3" class="mr-2"></v-progress-circular>
                    ກຳລັງສ້າງດົນຕີດ້ວຍ Meta MusicGen AI... ({{ elapsedSeconds }}s)
                  </span>
                  <span class="text-caption text-cyan-accent-2">ບໍ່ມີ Turnstile Captcha</span>
                </div>
                <v-progress-linear
                  indeterminate
                  color="cyan-accent-3"
                  height="6"
                  rounded
                  class="progress-pulse"
                ></v-progress-linear>
                <div class="text-caption text-grey-lighten-2 mt-2">
                  💡 ລະບົບກຳລັງດາວໂຫຼດ ແລະ ປະມວນຜົນສຽງດ້ວຍ Python Server (Port 3005)...
                </div>
              </div>

              <!-- Generate Button -->
              <v-btn
                type="submit"
                color="cyan-accent-3"
                size="large"
                block
                rounded="xl"
                :loading="isGenerating"
                :disabled="!isServerOnline || isGenerating || !form.prompt.trim()"
                class="generate-action-btn font-weight-black text-black text-none py-6"
                elevation="6"
              >
                <v-icon start size="22">mdi-lightning-bolt</v-icon>
                ສ້າງດົນຕີດຽວນີ້ (Generate Meta Music)
              </v-btn>
            </v-form>
          </v-card>
        </v-col>

        <!-- RIGHT COLUMN: Audio Player & Track Library -->
        <v-col cols="12" lg="6" xl="6">
          <!-- Active Player Card -->
          <v-card class="player-panel pa-6 rounded-2xl mb-6" elevation="8">
            <div class="d-flex align-center justify-space-between mb-4">
              <div class="d-flex align-center">
                <div class="equalizer-icon mr-2.5" :class="{ 'is-playing': isAudioPlaying }">
                  <span></span><span></span><span></span><span></span>
                </div>
                <h2 class="text-h6 font-weight-bold text-white">ເຄື່ອງຫຼິ້ນສຽງ (Audio Player)</h2>
              </div>
              <v-chip
                v-if="currentTrack"
                size="small"
                color="cyan-accent-3"
                variant="outlined"
                class="font-weight-bold text-white"
              >
                {{ currentTrack.duration }}s • 256 kbps
              </v-chip>
            </div>

            <!-- Current Track Display -->
            <div v-if="currentTrack" class="now-playing-card pa-4 rounded-xl mb-4">
              <div class="d-flex align-center mb-2">
                <div class="disc-spin mr-3" :class="{ 'spin-active': isAudioPlaying }">
                  <v-icon color="cyan-accent-3" size="28">mdi-record-player</v-icon>
                </div>
                <div class="flex-grow-1 overflow-hidden">
                  <div class="text-subtitle-1 font-weight-bold text-white text-truncate">
                    {{ currentTrack.title }}
                  </div>
                  <div class="text-caption text-grey-lighten-2 text-truncate">
                    {{ currentTrack.prompt }}
                  </div>
                </div>
              </div>

              <!-- Audio Timeline & Controls -->
              <div class="player-controls-wrapper pt-2">
                <!-- Time slider -->
                <div class="d-flex align-center gap-3 mb-1">
                  <span class="text-caption text-grey-lighten-1 time-display">{{ formatTime(currentTime) }}</span>
                  <v-slider
                    v-model="currentTime"
                    :max="audioDuration || 1"
                    :step="0.1"
                    color="cyan-accent-3"
                    track-color="rgba(255,255,255,0.2)"
                    hide-details
                    class="custom-slider flex-grow-1"
                    @update:model-value="seekAudio"
                  ></v-slider>
                  <span class="text-caption text-grey-lighten-1 time-display">{{ formatTime(audioDuration) }}</span>
                </div>

                <!-- Main Player Buttons -->
                <div class="d-flex align-center justify-space-between mt-2">
                  <!-- Volume Control -->
                  <div class="d-flex align-center" style="width: 140px;">
                    <v-btn
                      icon
                      size="small"
                      variant="text"
                      color="grey-lighten-2"
                      @click="toggleMute"
                    >
                      <v-icon size="20">{{ isMuted ? 'mdi-volume-off' : 'mdi-volume-high' }}</v-icon>
                    </v-btn>
                    <v-slider
                      v-model="volume"
                      :min="0"
                      :max="1"
                      :step="0.05"
                      color="cyan-accent-3"
                      track-color="rgba(255,255,255,0.15)"
                      hide-details
                      class="custom-slider"
                      @update:model-value="updateVolume"
                    ></v-slider>
                  </div>

                  <!-- Play/Pause Button -->
                  <div class="d-flex align-center gap-2">
                    <v-btn
                      icon="mdi-rewind-5"
                      size="small"
                      variant="tonal"
                      color="grey-lighten-2"
                      @click="skipAudio(-5)"
                    ></v-btn>

                    <v-btn
                      :icon="isAudioPlaying ? 'mdi-pause' : 'mdi-play'"
                      size="large"
                      color="cyan-accent-3"
                      class="text-black play-main-btn"
                      elevation="4"
                      @click="togglePlay"
                    ></v-btn>

                    <v-btn
                      icon="mdi-fast-forward-5"
                      size="small"
                      variant="tonal"
                      color="grey-lighten-2"
                      @click="skipAudio(5)"
                    ></v-btn>
                  </div>

                  <!-- Loop Toggle -->
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    :color="isLooping ? 'cyan-accent-3' : 'grey-lighten-2'"
                    @click="isLooping = !isLooping"
                    title="Loop Audio"
                  >
                    <v-icon size="20">mdi-repeat</v-icon>
                  </v-btn>
                </div>

                <!-- Download Options -->
                <v-divider class="my-4 border-opacity-25" color="grey-lighten-1"></v-divider>
                <div class="d-flex gap-2">
                  <v-btn
                    variant="flat"
                    color="cyan-accent-3"
                    rounded="lg"
                    prepend-icon="mdi-download"
                    class="flex-grow-1 font-weight-bold text-black text-none"
                    :href="getApiUrl(currentTrack.mp3_url)"
                    download
                  >
                    ດາວໂຫຼດ MP3
                  </v-btn>
                  <v-btn
                    variant="tonal"
                    color="purple-accent-2"
                    rounded="lg"
                    prepend-icon="mdi-music-box-outline"
                    class="flex-grow-1 font-weight-bold text-white text-none"
                    :href="getApiUrl(currentTrack.wav_url)"
                    download
                  >
                    ດາວໂຫຼດ WAV
                  </v-btn>
                </div>
              </div>

              <!-- Hidden native HTML5 Audio element -->
              <audio
                ref="audioRef"
                :src="getApiUrl(currentTrack.mp3_url)"
                :loop="isLooping"
                @timeupdate="onTimeUpdate"
                @loadedmetadata="onLoadedMetadata"
                @ended="onAudioEnded"
              ></audio>
            </div>

            <!-- Empty State for Player -->
            <div v-else class="text-center py-10 px-4 empty-player-box rounded-xl">
              <v-icon size="48" color="grey-darken-1" class="mb-2">mdi-music-note-off</v-icon>
              <div class="text-subtitle-1 font-weight-bold text-grey-lighten-1">ຍັງບໍ່ມີເພງທີ່ກຳລັງຫຼິ້ນ</div>
              <p class="text-caption text-grey-darken-1 mb-0">
                ກະລຸນາເລືອກເພງຈາກລາຍການຂ້າງລຸ່ມ ຫຼື ສ້າງເພງໃໝ່ດ້ວຍ Meta MusicGen AI
              </p>
            </div>
          </v-card>

          <!-- Generated Tracks Library -->
          <v-card class="library-panel pa-6 rounded-2xl" elevation="8">
            <div class="d-flex align-center justify-space-between mb-4">
              <div class="d-flex align-center">
                <v-icon color="cyan-accent-3" class="mr-2" size="24">mdi-playlist-music</v-icon>
                <h2 class="text-h6 font-weight-bold text-white">ປະຫວັດດົນຕີທີ່ສ້າງ (Generated Tracks)</h2>
              </div>
              <v-chip size="small" color="grey-darken-1" variant="tonal" class="text-white">
                {{ tracksList.length }} ເພງ
              </v-chip>
            </div>

            <!-- Track List -->
            <div v-if="tracksList.length > 0" class="tracks-scroll-wrapper">
              <div
                v-for="track in tracksList"
                :key="track.id"
                class="track-item pa-3 mb-2 rounded-xl d-flex align-center justify-space-between"
                :class="{ 'active-track': currentTrack?.id === track.id }"
              >
                <!-- Left: Play icon & Info -->
                <div class="d-flex align-center overflow-hidden mr-2" style="cursor: pointer;" @click="selectTrack(track)">
                  <v-btn
                    icon
                    size="small"
                    :color="currentTrack?.id === track.id && isAudioPlaying ? 'cyan-accent-3' : 'grey-darken-3'"
                    :class="currentTrack?.id === track.id && isAudioPlaying ? 'text-black' : 'text-cyan-accent-3'"
                    class="mr-3"
                  >
                    <v-icon size="18">
                      {{ currentTrack?.id === track.id && isAudioPlaying ? 'mdi-pause' : 'mdi-play' }}
                    </v-icon>
                  </v-btn>

                  <div class="overflow-hidden">
                    <div class="text-body-2 font-weight-bold text-white text-truncate">
                      {{ track.title }}
                    </div>
                    <div class="text-caption text-grey-lighten-2 text-truncate" style="max-width: 280px;">
                      {{ track.prompt }}
                    </div>
                    <div class="text-caption text-cyan-accent-2">
                      {{ track.duration }}s • {{ formatDate(track.created_at) }}
                    </div>
                  </div>
                </div>

                <!-- Right: Actions -->
                <div class="d-flex align-center gap-1">
                  <v-btn
                    icon="mdi-download"
                    size="x-small"
                    variant="tonal"
                    color="cyan-accent-3"
                    :href="getApiUrl(track.mp3_url)"
                    download
                    title="ດາວໂຫຼດ MP3"
                  ></v-btn>
                  <v-btn
                    icon="mdi-delete-outline"
                    size="x-small"
                    variant="tonal"
                    color="red-accent-2"
                    @click="deleteTrack(track.id)"
                    title="ລຶບເພງ"
                  ></v-btn>
                </div>
              </div>
            </div>

            <!-- Empty State for Library -->
            <div v-else class="text-center py-8 text-grey-darken-1">
              <v-icon size="36" class="mb-2">mdi-music-box-outline</v-icon>
              <div>ຍັງບໍ່ມີເພງໃນປະຫວັດ. ເລີ່ມສ້າງເພງທຳອິດຂອງທ່ານເລີຍ!</div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Hugging Face Token Dialog -->
      <v-dialog v-model="tokenDialog" max-width="560">
        <v-card class="pa-6 rounded-2xl token-dialog-card" elevation="16">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="d-flex align-center">
              <v-icon color="cyan-accent-3" size="28" class="mr-2">mdi-key-variant</v-icon>
              <h2 class="text-h6 font-weight-bold text-white">Hugging Face Token (ຟຣີ 100%)</h2>
            </div>
            <v-btn icon="mdi-close" variant="text" size="small" @click="tokenDialog = false"></v-btn>
          </div>

          <p class="text-body-2 text-grey-lighten-2 mb-4">
            Meta MusicGen ເຮັດວຽກຜ່ານ Hugging Face ZeroGPU. ເພື່ອໃຫ້ສ້າງເພງໄດ້ຢ່າງຕໍ່ເນື່ອງໂດຍບໍ່ຕິດໂຄຕ້າ, ທ່ານສາມາດນຳເອົາ Token ຟຣີມາໃສ່ໄດ້ (ບໍ່ຕ້ອງໃຊ້ບັດເຄຣດິດ):
          </p>

          <v-alert type="info" variant="tonal" rounded="xl" class="mb-4 text-caption" icon="mdi-information-outline">
            <div>1. ເຂົ້າໄປທີ່ <a href="https://huggingface.co/settings/tokens" target="_blank" class="text-cyan-accent-2 font-weight-bold">huggingface.co/settings/tokens</a></div>
            <div>2. ຄລິກປຸ່ມ <b>Create new token</b> (ເລືອກປະເພດ Read ຫຼື Write)</div>
            <div>3. Copy token ມາວາງໃສ່ຊ່ອງຂ້າງລຸ່ມ ແລ້ວກົດ "ບັນທຶກ"</div>
          </v-alert>

          <v-text-field
            v-model="tokenInput"
            label="Hugging Face Token (hf_...)"
            placeholder="hf_xxxxxxxxxxxxxxxxxxxx"
            variant="outlined"
            density="comfortable"
            rounded="lg"
            class="high-contrast-input mb-4"
            prepend-inner-icon="mdi-lock-outline"
            clearable
          ></v-text-field>

          <div class="d-flex gap-3">
            <v-btn
              variant="tonal"
              color="grey-lighten-1"
              rounded="xl"
              class="flex-grow-1 text-none font-weight-bold"
              @click="tokenDialog = false"
            >
              ຍົກເລີກ
            </v-btn>
            <v-btn
              color="cyan-accent-3"
              rounded="xl"
              class="flex-grow-1 text-none font-weight-bold text-black"
              :loading="savingToken"
              @click="saveToken"
            >
              💾 ບັນທຶກ Token
            </v-btn>
          </div>
        </v-card>
      </v-dialog>

      <!-- Snackbar Alerts -->
      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        :timeout="4500"
        rounded="xl"
        location="bottom right"
      >
        <div class="d-flex align-center">
          <v-icon class="mr-2">{{ snackbar.icon }}</v-icon>
          <span>{{ snackbar.text }}</span>
        </div>
      </v-snackbar>
    </div>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useApiBaseUrl } from '~/composables/api';

definePageMeta({
  layout: 'video'
});

const apiBase = useApiBaseUrl();

// Server & Generation States
const isServerOnline = ref(true);
const checkingStatus = ref(false);
const isGenerating = ref(false);
const enhancingPrompt = ref(false);
const elapsedSeconds = ref(0);
let timerInterval = null;

// Token Dialog States
const tokenDialog = ref(false);
const hasToken = ref(false);
const tokenInput = ref('');
const savingToken = ref(false);

// Audio Player States
const audioRef = ref(null);
const currentTrack = ref(null);
const isAudioPlaying = ref(false);
const currentTime = ref(0);
const audioDuration = ref(0);
const volume = ref(0.85);
const isMuted = ref(false);
const isLooping = ref(false);

// Library & Form States
const showToken = ref(false);
let tokenSaveTimeout = null;

const tracksList = ref([]);
const form = reactive({
  title: '',
  prompt: 'Lao traditional acoustic guitar and melodic khaen flute, relaxing river atmosphere, 85 bpm, warm cinematic tones',
  duration: 15,
  seed: 5,
  hf_token: ''
});

function onTokenInput(val) {
  const token = (val || '').trim();
  form.hf_token = token;
  tokenInput.value = token;
  hasToken.value = !!token;
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('meta_music_hf_token', token);
  }
  
  clearTimeout(tokenSaveTimeout);
  tokenSaveTimeout = setTimeout(async () => {
    if (token) {
      try {
        await $fetch(`${apiBase}/api/meta-music/token`, {
          method: 'POST',
          body: { token }
        });
      } catch (err) {
        console.error('Token auto-sync error:', err);
      }
    }
  }, 1000);
}

const snackbar = reactive({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
});

// Lao & Global Style Presets
const stylePresets = [
  {
    name: '🪕 ສຽງແຄນລາວດັ້ງເດີມ (Lao Khaen)',
    prompt: 'Traditional Lao acoustic music with soulful bamboo khaen melodies, delicate fingerpicked acoustic guitar, wooden percussion, 80 bpm, warm atmospheric acoustic space',
    color: 'amber-accent-3',
    icon: 'mdi-music-clef-treble'
  },
  {
    name: '☕ ໂລຟາຍຊິວໆ (Lao Café Lo-Fi)',
    prompt: 'Relaxing chill lo-fi hip hop beat, soft electric piano Rhodes chords, acoustic guitar licks, smooth sub bass, vinyl crackle, cozy coffee shop vibe, 78 bpm',
    color: 'teal-accent-3',
    icon: 'mdi-coffee'
  },
  {
    name: '🎸 ກີຕ້າໂປ່ງຟັງສະບາຍ (Acoustic Guitar)',
    prompt: 'Gentle acoustic fingerstyle guitar solo, peaceful country melody, emotional harmonies, clear studio acoustic recording, 90 bpm',
    color: 'deep-orange-accent-2',
    icon: 'mdi-guitar-acoustic'
  },
  {
    name: '🥁 ບີດປັອບສະໄໝໃໝ່ (Modern Lao Pop)',
    prompt: 'Modern upbeat Lao pop backing track, bouncy synth bass, catchy guitar hooks, crisp drums, modern radio production, 110 bpm',
    color: 'pink-accent-2',
    icon: 'mdi-music-circle-outline'
  },
  {
    name: '🌅 ບັນຍາກາດແຄມຂອງ (Mekong Sunset Ambient)',
    prompt: 'Serene atmospheric ambient music, gentle wooden flute, acoustic nylon guitar, peaceful water stream sounds, soothing meditative pads',
    color: 'cyan-accent-3',
    icon: 'mdi-weather-sunset'
  },
  {
    name: '🎹 ເປຍໂນໂຣແມນຕິກ (Cinematic Piano)',
    prompt: 'Romantic neoclassical piano melody accompanied by warm orchestral strings, emotional film soundtrack, lush cinematic reverb',
    color: 'indigo-accent-2',
    icon: 'mdi-piano'
  }
];

function notify(text, color = 'success', icon = 'mdi-check-circle') {
  snackbar.text = text;
  snackbar.color = color;
  snackbar.icon = icon;
  snackbar.show = true;
}

function getApiUrl(path) {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  return `${apiBase}${path}`;
}

function formatDate(isoStr) {
  if (!isoStr) return '';
  try {
    const d = new Date(isoStr);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' ' + d.toLocaleDateString();
  } catch {
    return isoStr;
  }
}

function formatTime(seconds) {
  if (!seconds || isNaN(seconds)) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

function applyPreset(preset) {
  form.prompt = preset.prompt;
  if (!form.title) {
    form.title = preset.name.replace(/^[^\s]+\s*/, '');
  }
  notify(`ເລືອກແນວດົນຕີ: ${preset.name}`, 'cyan-accent-3', 'mdi-check');
}

function randomizeSeed() {
  form.seed = Math.floor(Math.random() * 11);
  notify(`ສຸ່ມ Seed: #${form.seed}`, 'purple-accent-2', 'mdi-dice-5-outline');
}

// Check Backend Status
async function checkStatus() {
  checkingStatus.value = true;
  try {
    const res = await $fetch(`${apiBase}/api/meta-music/status`);
    isServerOnline.value = res?.status === 'online';
    await fetchTokenStatus();
    await fetchTracks();
  } catch (err) {
    isServerOnline.value = false;
  } finally {
    checkingStatus.value = false;
  }
}

// Token Status & Save
async function fetchTokenStatus() {
  if (typeof window !== 'undefined' && window.localStorage) {
    const cached = localStorage.getItem('meta_music_hf_token');
    if (cached) {
      form.hf_token = cached;
      tokenInput.value = cached;
      hasToken.value = true;
    }
  }

  try {
    const res = await $fetch(`${apiBase}/api/meta-music/token`);
    if (res?.token && !form.hf_token) {
      form.hf_token = res.token;
      tokenInput.value = res.token;
      hasToken.value = true;
      if (typeof window !== 'undefined' && window.localStorage) {
        localStorage.setItem('meta_music_hf_token', res.token);
      }
    } else if (res?.has_token) {
      hasToken.value = true;
    }
  } catch (err) {
    console.error('Failed to fetch token status:', err);
  }
}

async function saveToken() {
  if (!tokenInput.value.trim()) {
    notify('ກະລຸນາໃສ່ Token', 'warning', 'mdi-alert');
    return;
  }
  savingToken.value = true;
  try {
    await $fetch(`${apiBase}/api/meta-music/token`, {
      method: 'POST',
      body: { token: tokenInput.value.trim() }
    });
    hasToken.value = true;
    form.hf_token = tokenInput.value.trim();
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('meta_music_hf_token', form.hf_token);
    }
    tokenDialog.value = false;
    notify('ບັນທຶກ Hugging Face Token ສຳເລັດແລ້ວ!', 'success', 'mdi-check-circle');
  } catch (err) {
    notify('ບໍ່ສາມາດບັນທຶກ Token ໄດ້: ' + (err.data?.detail || err.message), 'error', 'mdi-alert');
  } finally {
    savingToken.value = false;
  }
}

// Fetch Generated Tracks
async function fetchTracks() {
  try {
    const res = await $fetch(`${apiBase}/api/meta-music/tracks`);
    tracksList.value = res?.tracks || [];
    if (!currentTrack.value && tracksList.value.length > 0) {
      currentTrack.value = tracksList.value[0];
    }
  } catch (err) {
    console.error('Failed to load tracks:', err);
  }
}

// Enhance Prompt using Gemini
async function enhancePrompt() {
  if (!form.prompt.trim()) {
    notify('ກະລຸນາພິມຄຳອະທິບາຍດົນຕີກ່ອນ', 'warning', 'mdi-alert');
    return;
  }
  enhancingPrompt.value = true;
  try {
    const res = await $fetch(`${apiBase}/api/meta-music/enhance-prompt`, {
      method: 'POST',
      body: { prompt: form.prompt }
    });
    if (res?.enhanced_prompt) {
      form.prompt = res.enhanced_prompt;
      notify('ປັບປຸງ Prompt ສຳເລັດແລ້ວດ້ວຍ Gemini AI!', 'success', 'mdi-auto-fix');
    }
  } catch (err) {
    notify('ບໍ່ສາມາດປັບປຸງ Prompt ໄດ້: ' + (err.data?.detail || err.message), 'error', 'mdi-alert');
  } finally {
    enhancingPrompt.value = false;
  }
}

// Generate Music with Meta MusicGen
async function generateMusic() {
  if (!form.prompt.trim()) {
    notify('ກະລຸນາໃສ່ຄຳອະທິບາຍດົນຕີ', 'warning', 'mdi-alert');
    return;
  }

  isGenerating.value = true;
  elapsedSeconds.value = 0;
  timerInterval = setInterval(() => {
    elapsedSeconds.value++;
  }, 1000);

  try {
    const res = await $fetch(`${apiBase}/api/meta-music/generate`, {
      method: 'POST',
      body: {
        title: form.title || undefined,
        prompt: form.prompt,
        duration: form.duration,
        seed: form.seed,
        hf_token: form.hf_token?.trim() || undefined
      }
    });

    if (res?.success && res?.track) {
      notify('ສ້າງດົນຕີສຳເລັດແລ້ວ!', 'success', 'mdi-check-circle');
      await fetchTracks();
      selectTrack(res.track, true);
    } else {
      throw new Error(res?.detail || 'Generation failed');
    }
  } catch (err) {
    const errorText = err.data?.detail || err.message;
    notify('ເກີດຂໍ້ຜິດພາດໃນການສ້າງເພງ: ' + errorText, 'error', 'mdi-alert-circle');
    if (errorText.includes('ZeroGPU') || errorText.includes('limit') || errorText.includes('Token')) {
      tokenDialog.value = true;
    }
  } finally {
    clearInterval(timerInterval);
    isGenerating.value = false;
  }
}

// Audio Player Functions
function selectTrack(track, autoplay = false) {
  currentTrack.value = track;
  if (audioRef.value) {
    audioRef.value.src = getApiUrl(track.mp3_url);
    audioRef.value.load();
    if (autoplay) {
      audioRef.value.play().then(() => {
        isAudioPlaying.value = true;
      }).catch(() => {
        isAudioPlaying.value = false;
      });
    } else {
      isAudioPlaying.value = false;
    }
  }
}

function togglePlay() {
  if (!audioRef.value || !currentTrack.value) return;
  if (isAudioPlaying.value) {
    audioRef.value.pause();
    isAudioPlaying.value = false;
  } else {
    audioRef.value.play().then(() => {
      isAudioPlaying.value = true;
    }).catch(e => {
      console.error(e);
      isAudioPlaying.value = false;
    });
  }
}

function onTimeUpdate() {
  if (audioRef.value) {
    currentTime.value = audioRef.value.currentTime;
  }
}

function onLoadedMetadata() {
  if (audioRef.value) {
    audioDuration.value = audioRef.value.duration;
  }
}

function onAudioEnded() {
  isAudioPlaying.value = false;
}

function seekAudio(val) {
  if (audioRef.value) {
    audioRef.value.currentTime = val;
  }
}

function skipAudio(seconds) {
  if (audioRef.value) {
    audioRef.value.currentTime = Math.max(0, Math.min(audioDuration.value, audioRef.value.currentTime + seconds));
  }
}

function updateVolume(val) {
  if (audioRef.value) {
    audioRef.value.volume = val;
    isMuted.value = val === 0;
  }
}

function toggleMute() {
  if (!audioRef.value) return;
  if (isMuted.value) {
    audioRef.value.volume = volume.value || 0.8;
    isMuted.value = false;
  } else {
    audioRef.value.volume = 0;
    isMuted.value = true;
  }
}

async function deleteTrack(trackId) {
  if (!confirm('ທ່ານແນ່ໃຈບໍ່ວ່າຕ້ອງການລຶບເພງນີ້?')) return;
  try {
    await $fetch(`${apiBase}/api/meta-music/tracks/${trackId}`, { method: 'DELETE' });
    notify('ລຶບເພງສຳເລັດແລ້ວ', 'info', 'mdi-delete');
    if (currentTrack.value?.id === trackId) {
      if (audioRef.value) audioRef.value.pause();
      isAudioPlaying.value = false;
      currentTrack.value = null;
    }
    await fetchTracks();
  } catch (err) {
    notify('ບໍ່ສາມາດລຶບເພງໄດ້: ' + (err.data?.detail || err.message), 'error', 'mdi-alert');
  }
}

onMounted(() => {
  checkStatus();
});
</script>

<style scoped>
.meta-music-container {
  min-height: 100vh;
  background: radial-gradient(circle at 15% 15%, rgba(6, 182, 212, 0.12) 0%, transparent 40%),
              radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.12) 0%, transparent 45%);
}

.hero-card {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9)) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(6, 182, 212, 0.25);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
}

.meta-avatar-glow {
  width: 58px;
  height: 58px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2));
  border: 1px solid rgba(6, 182, 212, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 24px rgba(6, 182, 212, 0.35);
}

.brand-title {
  background: linear-gradient(135deg, #ffffff, #67e8f9, #c084fc);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ef4444;
  display: inline-block;
}

.pulse-active {
  background-color: #10b981;
  box-shadow: 0 0 10px #10b981;
  animation: pulse-ring 1.8s infinite;
}

@keyframes pulse-ring {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.generator-panel, .player-panel, .library-panel {
  background: rgba(15, 23, 42, 0.85) !important;
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.generator-panel:hover, .player-panel:hover, .library-panel:hover {
  border-color: rgba(6, 182, 212, 0.25);
}

.input-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e2e8f0;
}

.optional-badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  color: #94a3b8;
}

.high-contrast-input :deep(.v-field) {
  background: rgba(30, 41, 59, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: #ffffff !important;
}

.high-contrast-input :deep(.v-field--focused) {
  border-color: #22d3ee !important;
  box-shadow: 0 0 14px rgba(34, 211, 238, 0.25) !important;
}

.token-input-box {
  background: rgba(6, 182, 212, 0.08);
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.control-box {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.07);
}

.preset-chip {
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.25);
}

.ai-enhance-btn {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(6, 182, 212, 0.2)) !important;
  border: 1px solid rgba(168, 85, 247, 0.4) !important;
}

.generating-progress-box {
  background: rgba(6, 182, 212, 0.08);
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.generate-action-btn {
  background: linear-gradient(135deg, #06b6d4, #22d3ee, #a855f7) !important;
  transition: all 0.3s ease;
  font-size: 1.05rem;
  letter-spacing: 0.3px;
}

.generate-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(6, 182, 212, 0.5) !important;
}

/* Audio Player Equalizer & Disc Styles */
.equalizer-icon {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 20px;
}

.equalizer-icon span {
  width: 3px;
  height: 6px;
  background-color: #22d3ee;
  border-radius: 2px;
  transition: height 0.2s;
}

.equalizer-icon.is-playing span:nth-child(1) { animation: eq-wave 0.8s infinite ease-in-out alternate; }
.equalizer-icon.is-playing span:nth-child(2) { animation: eq-wave 0.6s infinite ease-in-out alternate 0.2s; }
.equalizer-icon.is-playing span:nth-child(3) { animation: eq-wave 0.9s infinite ease-in-out alternate 0.4s; }
.equalizer-icon.is-playing span:nth-child(4) { animation: eq-wave 0.7s infinite ease-in-out alternate 0.1s; }

@keyframes eq-wave {
  from { height: 4px; }
  to { height: 18px; }
}

.now-playing-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
  border: 1px solid rgba(6, 182, 212, 0.25);
}

.disc-spin {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(6, 182, 212, 0.15);
  border: 1px dashed rgba(6, 182, 212, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.spin-active {
  animation: disc-rotate 4s linear infinite;
}

@keyframes disc-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.play-main-btn {
  transform: scale(1.15);
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
}

.empty-player-box {
  background: rgba(30, 41, 59, 0.3);
  border: 1px dashed rgba(255, 255, 255, 0.1);
}

.tracks-scroll-wrapper {
  max-height: 380px;
  overflow-y: auto;
  padding-right: 4px;
}

.track-item {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: all 0.2s ease;
}

.track-item:hover {
  background: rgba(30, 41, 59, 0.85);
  border-color: rgba(6, 182, 212, 0.3);
  transform: translateX(3px);
}

.active-track {
  background: rgba(6, 182, 212, 0.12) !important;
  border-color: rgba(6, 182, 212, 0.4) !important;
}

.time-display {
  font-variant-numeric: tabular-nums;
  min-width: 38px;
}
</style>
