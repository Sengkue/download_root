<template>
  <v-container class="py-6 px-4 song-generator-container" fluid>
    <div class="song-gen-wrapper mx-auto" style="max-width: 1360px;">
      
      <!-- Top Hero Banner -->
      <v-card class="hero-card pa-6 mb-6 rounded-2xl" elevation="10">
        <div class="d-flex flex-wrap align-center justify-space-between gap-4">
          <!-- Left: Title & Subtitle -->
          <div class="d-flex align-center">
            <div class="avatar-glow mr-4">
              <v-icon size="38" color="amber-accent-2">mdi-music-clef-treble</v-icon>
            </div>
            <div>
              <div class="d-flex align-center flex-wrap gap-2">
                <h1 class="text-h4 font-weight-black text-white brand-title">
                  Suno AI Song Studio
                </h1>
                <v-chip
                  :color="isServerOnline ? 'emerald-accent' : 'error'"
                  size="small"
                  variant="flat"
                  class="ml-2 font-weight-bold status-pill text-white"
                >
                  <span class="pulse-dot mr-1.5" :class="{ 'pulse-active': isServerOnline }"></span>
                  {{ isServerOnline ? 'Suno Server Online (Port 3008)' : 'Server Offline (Port 3008)' }}
                </v-chip>
              </div>
              <p class="subtitle-text text-body-2 mt-1 mb-0">
                ສະຕູດິໂອສ້າງເພງ AI ພາສາລາວ ແລະ ແຕ່ງດົນຕີຄຸນນະພາບສູງດ້ວຍ Suno AI & Gemini
              </p>
            </div>
          </div>

          <!-- Right: Credits Counter & Controls -->
          <div class="d-flex align-center flex-wrap gap-3">
            <div class="credits-badge d-flex align-center px-4 py-2 rounded-xl">
              <v-icon color="amber-accent-2" class="mr-2">mdi-lightning-bolt</v-icon>
              <div>
                <div class="credits-label">ເຄຣດິດຄົງເຫຼືອ (Credits)</div>
                <div class="credits-value font-weight-black text-white">
                  {{ creditsInfo?.credits_left ?? '60' }} <span class="credits-sub">/ {{ creditsInfo?.monthly_limit ?? '100' }}</span>
                </div>
              </div>
            </div>

            <v-btn
              variant="tonal"
              color="amber-accent-2"
              rounded="xl"
              prepend-icon="mdi-refresh"
              :loading="checkingCredits"
              @click="refreshAll"
              class="refresh-btn text-none font-weight-bold px-4"
            >
              Refresh
            </v-btn>
          </div>
        </div>

        <!-- Offline Server Alert -->
        <v-alert
          v-if="!isServerOnline && !checkingCredits"
          type="warning"
          variant="tonal"
          rounded="xl"
          class="mt-4 offline-alert"
          icon="mdi-alert-circle-outline"
        >
          <div class="font-weight-bold text-amber-lighten-1">Suno API Server ຍັງບໍ່ທັນເປີດ (Port 3008)</div>
          <div class="text-caption text-white mt-1">
            ກະລຸນາເປີດໄຟລ໌ <code>1_start_suno_server.bat</code> ໃນໂຟນເດີໂປຣເຈັກ ແລະ ກວດສອບ <code>SUNO_COOKIE</code> ໃນ <code>suno-api\.env</code>
          </div>
        </v-alert>
      </v-card>

      <!-- Main Workspace Grid -->
      <v-row class="workspace-row">
        <!-- LEFT COLUMN: Generator Controls -->
        <v-col cols="12" lg="6" xl="6">
          <v-card class="generator-panel pa-6 rounded-2xl h-100" elevation="8">
            
            <!-- Custom Styled Navigation Tabs -->
            <div class="tabs-header mb-5">
              <v-tabs
                v-model="activeTab"
                color="amber-accent-2"
                grow
                density="comfortable"
                class="custom-tabs rounded-xl pa-1"
              >
                <v-tab value="topic" class="tab-item font-weight-bold text-none">
                  <v-icon start size="20">mdi-auto-fix</v-icon>
                  ສ້າງເພງອັດຕະໂນມັດ (Auto AI)
                </v-tab>
                <v-tab value="custom" class="tab-item font-weight-bold text-none">
                  <v-icon start size="20">mdi-fountain-pen-tip</v-icon>
                  ໃສ່ເນື້ອເພງເອງ (Custom Lyrics)
                </v-tab>
              </v-tabs>
            </div>

            <v-window v-model="activeTab">
              <!-- ============================================== -->
              <!-- TAB 1: AUTO TOPIC TO LAO SONG                 -->
              <!-- ============================================== -->
              <v-window-item value="topic">
                <v-form @submit.prevent="generateFromTopic">
                  
                  <!-- Song Topic Input -->
                  <div class="form-group mb-4">
                    <label class="input-label d-flex align-center justify-space-between mb-2">
                      <span class="d-flex align-center">
                        <v-icon size="18" color="amber-accent-2" class="mr-1.5">mdi-lightbulb-on-outline</v-icon>
                        ຫົວຂໍ້ເພງ ຫຼື ເລື່ອງລາວທີ່ຕ້ອງການ (Song Topic) *
                      </span>
                      <span class="required-badge">ຈຳເປັນ</span>
                    </label>
                    <v-text-field
                      v-model="topicForm.topic"
                      placeholder="ຕົວຢ່າງ: ເພງຮັກສາວຫຼວງພະບາງ, ຄວາມຮັກຄິດຮອດບ້ານເກີດແຄມຂອງ..."
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      class="custom-input high-contrast-input"
                      hide-details="auto"
                      required
                      clearable
                    ></v-text-field>

                    <!-- Quick Topic Inspiration Chips -->
                    <div class="quick-chips-wrapper mt-2.5">
                      <div class="chips-title mb-1.5">
                        <v-icon size="14" color="amber-accent-3" class="mr-1">mdi-sparkles</v-icon>
                        ກົດເລືອກຫົວຂໍ້ຕົວຢ່າງ (Quick Ideas):
                      </div>
                      <div class="d-flex flex-wrap gap-1.5">
                        <v-chip
                          v-for="(idea, i) in sampleTopics"
                          :key="i"
                          size="small"
                          variant="tonal"
                          color="amber-accent-2"
                          class="preset-chip text-white"
                          @click="topicForm.topic = idea.text"
                        >
                          <span class="mr-1">{{ idea.icon }}</span> {{ idea.title }}
                        </v-chip>
                      </div>
                    </div>
                  </div>

                  <!-- Music Style / Tags Input -->
                  <div class="form-group mb-4">
                    <label class="input-label d-flex align-center justify-space-between mb-2">
                      <span class="d-flex align-center">
                        <v-icon size="18" color="cyan-accent-2" class="mr-1.5">mdi-music-circle-outline</v-icon>
                        ແນວເພງ ແລະ ເຄື່ອງດົນຕີ (Music Style & Tags)
                      </span>
                      <span class="optional-badge">ແນະນຳພາສາອັງກິດ</span>
                    </label>
                    <v-text-field
                      v-model="topicForm.style"
                      placeholder="e.g. Lao pop ballad, acoustic guitar, soft emotional male vocal, 90 bpm"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      class="custom-input high-contrast-input"
                      hide-details="auto"
                      clearable
                    ></v-text-field>

                    <!-- Style Preset Chips -->
                    <div class="quick-chips-wrapper mt-2.5">
                      <div class="chips-title mb-1.5">
                        <v-icon size="14" color="cyan-accent-3" class="mr-1">mdi-tag-multiple-outline</v-icon>
                        ແນວເພງຍອດນິຍົມ (Click to Apply Style):
                      </div>
                      <div class="d-flex flex-wrap gap-1.5">
                        <v-chip
                          v-for="(style, i) in sampleStyles"
                          :key="i"
                          size="small"
                          variant="tonal"
                          :color="topicForm.style === style.tags ? 'cyan-accent-2' : 'grey-lighten-2'"
                          class="preset-chip"
                          @click="topicForm.style = style.tags"
                        >
                          <span class="mr-1">{{ style.icon }}</span> {{ style.name }}
                        </v-chip>
                      </div>
                    </div>
                  </div>

                  <!-- Instrumental Toggle -->
                  <div class="toggle-card d-flex align-center justify-space-between pa-3 rounded-xl mb-5">
                    <div class="d-flex align-center">
                      <v-avatar size="34" color="deep-purple-darken-3" class="mr-3">
                        <v-icon size="18" color="amber-accent-2">mdi-violin</v-icon>
                      </v-avatar>
                      <div>
                        <div class="font-weight-bold text-white text-body-2">ເພງດົນຕີລ້ວນ (Instrumental Only)</div>
                        <div class="text-caption text-grey-lighten-1">ສ້າງສະເພາະສຽງດົນຕີ ບໍ່ມີສຽງຮ້ອງ</div>
                      </div>
                    </div>
                    <v-switch
                      v-model="topicForm.instrumental"
                      color="amber-accent-2"
                      hide-details
                      inset
                      density="compact"
                    ></v-switch>
                  </div>

                  <!-- Submit Action Button -->
                  <v-btn
                    type="submit"
                    color="amber-accent-3"
                    variant="flat"
                    block
                    size="x-large"
                    rounded="xl"
                    class="generate-btn font-weight-black text-black text-none"
                    :loading="generating"
                    :disabled="!topicForm.topic.trim() || !isServerOnline"
                  >
                    <v-icon start size="22">mdi-creation</v-icon>
                    ສ້າງເພງດ້ວຍ Suno AI (Generate Song)
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- ============================================== -->
              <!-- TAB 2: CUSTOM LAO LYRICS                       -->
              <!-- ============================================== -->
              <v-window-item value="custom">
                <v-form @submit.prevent="generateFromCustomLyrics">
                  
                  <!-- Song Title Input -->
                  <div class="form-group mb-4">
                    <label class="input-label d-flex align-center mb-2">
                      <v-icon size="18" color="amber-accent-2" class="mr-1.5">mdi-format-title</v-icon>
                      ຊື່ເພງ (Song Title)
                    </label>
                    <v-text-field
                      v-model="customForm.title"
                      placeholder="ຕົວຢ່າງ: ຫວັງຮັກເຈົ້າ, ຄິດຮອດສາວລາວ..."
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      class="custom-input high-contrast-input"
                      hide-details="auto"
                      clearable
                    ></v-text-field>
                  </div>

                  <!-- Style Tags Input -->
                  <div class="form-group mb-4">
                    <label class="input-label d-flex align-center justify-space-between mb-2">
                      <span class="d-flex align-center">
                        <v-icon size="18" color="cyan-accent-2" class="mr-1.5">mdi-music-box-outline</v-icon>
                        ແນວເພງ (Music Style Tags) *
                      </span>
                      <span class="required-badge">ຈຳເປັນ</span>
                    </label>
                    <v-text-field
                      v-model="customForm.style"
                      placeholder="e.g. lao morlam modern pop, female vocal, upbeat, synthesizer"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      class="custom-input high-contrast-input"
                      hide-details="auto"
                      required
                    ></v-text-field>

                    <!-- Style Preset Chips -->
                    <div class="quick-chips-wrapper mt-2">
                      <div class="d-flex flex-wrap gap-1.5">
                        <v-chip
                          v-for="(style, i) in sampleStyles"
                          :key="i"
                          size="small"
                          variant="tonal"
                          :color="customForm.style === style.tags ? 'cyan-accent-2' : 'grey-lighten-2'"
                          class="preset-chip"
                          @click="customForm.style = style.tags"
                        >
                          <span class="mr-1">{{ style.icon }}</span> {{ style.name }}
                        </v-chip>
                      </div>
                    </div>
                  </div>

                  <!-- Custom Lyrics Textarea -->
                  <div class="form-group mb-4">
                    <div class="d-flex align-center justify-space-between mb-2">
                      <label class="input-label d-flex align-center">
                        <v-icon size="18" color="purple-accent-2" class="mr-1.5">mdi-text-box-outline</v-icon>
                        ເນື້ອເພງພາສາລາວ (Lao Lyrics) *
                      </label>
                      <v-btn
                        size="x-small"
                        variant="tonal"
                        color="amber-accent-2"
                        rounded="pill"
                        prepend-icon="mdi-pencil-plus"
                        @click="insertSampleLyrics"
                        class="text-none font-weight-bold"
                      >
                        ໃສ່ເນື້ອເພງຕົວຢ່າງ (Sample)
                      </v-btn>
                    </div>

                    <!-- Structure helper buttons -->
                    <div class="lyrics-toolbar d-flex flex-wrap align-center gap-1.5 mb-2 pa-2 rounded-lg">
                      <span class="text-caption text-grey-lighten-1 mr-1">ເພີ່ມທ່ອນ:</span>
                      <v-btn size="x-small" variant="outlined" color="grey-lighten-1" class="text-none" @click="appendLyricTag('[Verse 1]\n')">+ [Verse 1]</v-btn>
                      <v-btn size="x-small" variant="outlined" color="amber-accent-2" class="text-none" @click="appendLyricTag('[Chorus]\n')">+ [Chorus]</v-btn>
                      <v-btn size="x-small" variant="outlined" color="grey-lighten-1" class="text-none" @click="appendLyricTag('[Verse 2]\n')">+ [Verse 2]</v-btn>
                      <v-btn size="x-small" variant="outlined" color="cyan-accent-2" class="text-none" @click="appendLyricTag('[Bridge]\n')">+ [Bridge]</v-btn>
                      <v-btn size="x-small" variant="outlined" color="grey-lighten-1" class="text-none" @click="appendLyricTag('[Outro]\n')">+ [Outro]</v-btn>
                    </div>

                    <v-textarea
                      v-model="customForm.lyrics"
                      placeholder="[Verse 1]&#10;ຍ່າງຜ່ານບ່ອນເກົ່າ ທີ່ເຮົາເຄີຍພົບກັນ...&#10;&#10;[Chorus]&#10;ຫຼົງຮັກເຈົ້າແລ້ວ ຮູ້ບໍ່ຄົນດີ...&#10;&#10;[Outro]&#10;ຮັກເຈົ້າຕະຫຼອດໄປ..."
                      variant="outlined"
                      rows="8"
                      rounded="lg"
                      class="custom-textarea high-contrast-input"
                      hide-details="auto"
                      required
                    ></v-textarea>
                  </div>

                  <!-- Instrumental Toggle -->
                  <div class="toggle-card d-flex align-center justify-space-between pa-3 rounded-xl mb-5">
                    <div class="d-flex align-center">
                      <v-avatar size="34" color="deep-purple-darken-3" class="mr-3">
                        <v-icon size="18" color="amber-accent-2">mdi-violin</v-icon>
                      </v-avatar>
                      <div>
                        <div class="font-weight-bold text-white text-body-2">ເພງດົນຕີລ້ວນ (Instrumental Only)</div>
                        <div class="text-caption text-grey-lighten-1">ສ້າງສະເພາະດົນຕີ ບໍ່ມີສຽງຮ້ອງ</div>
                      </div>
                    </div>
                    <v-switch
                      v-model="customForm.instrumental"
                      color="amber-accent-2"
                      hide-details
                      inset
                      density="compact"
                    ></v-switch>
                  </div>

                  <!-- Submit Custom Track Button -->
                  <v-btn
                    type="submit"
                    color="deep-purple-accent-2"
                    variant="flat"
                    block
                    size="x-large"
                    rounded="xl"
                    class="generate-btn font-weight-black text-white text-none"
                    :loading="generating"
                    :disabled="!customForm.lyrics.trim() || !isServerOnline"
                  >
                    <v-icon start size="22">mdi-play-circle</v-icon>
                    ສ້າງເພງຈາກເນື້ອຮ້ອງ (Generate Custom Track)
                  </v-btn>
                </v-form>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>

        <!-- RIGHT COLUMN: Generated Tracks & Player Library -->
        <v-col cols="12" lg="6" xl="6">
          <v-card class="results-panel pa-6 rounded-2xl h-100 d-flex flex-column" elevation="8">
            
            <!-- Panel Header -->
            <div class="d-flex flex-wrap align-center justify-space-between gap-3 mb-4">
              <div class="d-flex align-center">
                <v-icon color="pink-accent-2" size="26" class="mr-2">mdi-playlist-music</v-icon>
                <div>
                  <h2 class="text-h6 font-weight-bold text-white mb-0">
                    ລາຍການເພງ (Generated Tracks)
                  </h2>
                  <div class="text-caption text-grey-lighten-1">
                    ເພງທັງໝົດໃນບັນຊີ Suno ຂອງທ່ານ
                  </div>
                </div>
              </div>

              <div class="d-flex align-center gap-2">
                <v-chip size="small" color="purple-darken-2" variant="flat" class="font-weight-bold text-white">
                  {{ songList.length }} ເພງ
                </v-chip>
                <v-btn
                  size="small"
                  variant="text"
                  color="grey-lighten-2"
                  icon="mdi-refresh"
                  :loading="loadingTracks"
                  @click="fetchRecentTracks"
                  title="Refresh tracks"
                ></v-btn>
              </div>
            </div>

            <!-- Search Filter Bar if songs exist -->
            <div v-if="songList.length > 0" class="search-box mb-4">
              <v-text-field
                v-model="searchQuery"
                placeholder="🔍 ຄົ້ນຫາຕາມຊື່ເພງ ຫຼື ແນວເພງ..."
                density="compact"
                variant="outlined"
                rounded="lg"
                class="custom-search"
                hide-details
                clearable
              ></v-text-field>
            </div>

            <!-- State 1: Active Generation Progress Tracker -->
            <div v-if="generating" class="generating-box py-10 px-6 text-center rounded-2xl mb-4">
              <div class="sound-wave-container mb-4">
                <div class="wave-bar" v-for="n in 9" :key="n" :style="{ animationDelay: `${(n - 1) * 0.12}s` }"></div>
              </div>

              <div class="text-h6 font-weight-black text-amber-accent-2">
                AI ກຳລັງແຕ່ງ ແລະ ສ້າງເພງ...
              </div>
              <div class="text-body-2 text-white mt-1">
                Suno AI is composing melodies, vocals & audio mastering.
              </div>
              <div class="generation-timer text-caption text-grey-lighten-2 mt-2">
                ⏱️ ໃຊ້ເວລາປະມານ 60 - 90 ວິນາທີ (ກະລຸນາລໍຖ້າ...)
              </div>
            </div>

            <!-- State 2: Empty State -->
            <div v-else-if="filteredSongList.length === 0" class="empty-state py-12 text-center my-auto">
              <div class="empty-icon-wrap mx-auto mb-4">
                <v-icon size="48" color="grey-lighten-1">mdi-music-box-outline</v-icon>
              </div>
              <div class="text-subtitle-1 font-weight-bold text-white mb-1">
                {{ searchQuery ? 'ບໍ່ພົບເພງທີ່ກົງກັບຄຳຄົ້ນຫາ' : 'ຍັງບໍ່ມີເພງໃນລາຍການ' }}
              </div>
              <div class="text-caption text-grey-lighten-2 max-w-sm mx-auto">
                {{ searchQuery ? 'ລອງປ່ຽນຄຳຄົ້ນຫາໃໝ່' : 'ປ້ອນຫົວຂໍ້ເພງ ຫຼື ວາງເນື້ອເພງດ້ານຊ້າຍ ແລ້ວກົດປຸ່ມ Generate ເພື່ອເລີ່ມຕົ້ນ' }}
              </div>
            </div>

            <!-- State 3: Active Song List -->
            <div v-else class="song-list-scroll flex-grow-1 pr-1">
              <v-card
                v-for="(song, idx) in filteredSongList"
                :key="song.id || idx"
                class="song-card pa-4 mb-3.5 rounded-xl"
                elevation="3"
              >
                <div class="d-flex align-start gap-3">
                  <!-- Album Cover / Avatar -->
                  <div class="cover-art-wrapper flex-shrink-0">
                    <v-img
                      v-if="song.image_url"
                      :src="song.image_url"
                      cover
                      class="cover-img rounded-lg"
                      width="68"
                      height="68"
                    >
                      <template v-slot:placeholder>
                        <div class="d-flex align-center justify-center fill-height bg-grey-darken-3">
                          <v-icon color="grey">mdi-music</v-icon>
                        </div>
                      </template>
                    </v-img>
                    <div v-else class="cover-placeholder rounded-lg d-flex align-center justify-center">
                      <v-icon color="amber-accent-2" size="30">mdi-music-note</v-icon>
                    </div>
                  </div>

                  <!-- Song Details -->
                  <div class="flex-grow-1 overflow-hidden">
                    <div class="d-flex align-center justify-space-between mb-1">
                      <h3 class="song-title text-subtitle-1 font-weight-black text-white text-truncate">
                        {{ song.title || 'Untitled Song' }}
                      </h3>
                      <v-chip
                        size="x-small"
                        :color="song.status === 'complete' ? 'success' : 'info'"
                        variant="flat"
                        class="status-chip ml-2 font-weight-bold"
                      >
                        {{ song.status === 'complete' ? 'Ready' : (song.status || 'Processing') }}
                      </v-chip>
                    </div>

                    <!-- Tags & Meta -->
                    <div class="song-tags text-caption text-grey-lighten-1 text-truncate mb-2" :title="song.tags">
                      <v-icon size="12" class="mr-1" color="cyan-accent-2">mdi-tag-outline</v-icon>
                      {{ song.tags || 'Lao Modern Pop' }}
                    </div>

                    <!-- Audio Player Widget -->
                    <div v-if="song.audio_url" class="audio-player-box mb-2">
                      <audio
                        :src="song.audio_url"
                        controls
                        preload="metadata"
                        class="w-100 native-audio-player"
                      ></audio>
                    </div>

                    <!-- Song Action Buttons -->
                    <div class="d-flex flex-wrap align-center justify-space-between pt-2 border-t gap-2">
                      <span class="text-caption text-grey-lighten-2">
                        ID: <code class="id-tag">{{ song.id ? song.id.slice(0, 8) : 'N/A' }}</code>
                        <span v-if="song.duration" class="ml-2 font-weight-medium">⏱️ {{ Math.round(song.duration) }}s</span>
                      </span>

                      <div class="d-flex align-center gap-2">
                        <!-- View Lyrics Button -->
                        <v-btn
                          v-if="song.prompt || song.lyric"
                          size="small"
                          variant="tonal"
                          color="purple-accent-2"
                          rounded="lg"
                          prepend-icon="mdi-card-text-outline"
                          @click="openLyricsDialog(song)"
                          class="text-none font-weight-bold"
                        >
                          ເນື້ອເພງ
                        </v-btn>

                        <!-- Copy Audio Link -->
                        <v-btn
                          v-if="song.audio_url"
                          size="small"
                          variant="tonal"
                          color="grey-lighten-2"
                          rounded="lg"
                          icon="mdi-content-copy"
                          @click="copyAudioLink(song.audio_url)"
                          title="Copy Link"
                        ></v-btn>

                        <!-- Download Button -->
                        <v-btn
                          v-if="song.audio_url"
                          size="small"
                          color="amber-accent-3"
                          variant="flat"
                          rounded="lg"
                          prepend-icon="mdi-download"
                          :href="song.audio_url"
                          :download="`${song.title || 'suno_song'}_${song.id?.slice(0, 8)}.m4a`"
                          target="_blank"
                          class="text-none font-weight-bold text-black"
                        >
                          ດາວໂຫຼດ
                        </v-btn>
                      </div>
                    </div>
                  </div>
                </div>
              </v-card>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Lyrics Modal Dialog -->
    <v-dialog v-model="lyricsDialog" max-width="650px" rounded="2xl">
      <v-card class="lyrics-modal pa-6 rounded-2xl" elevation="16">
        <div class="d-flex align-center justify-space-between mb-4">
          <div class="d-flex align-center">
            <v-icon color="amber-accent-2" class="mr-2" size="26">mdi-music-note-eighth</v-icon>
            <div>
              <h3 class="text-h6 font-weight-black text-white">{{ currentLyricSong?.title || 'ເນື້ອເພງ (Lyrics)' }}</h3>
              <div class="text-caption text-grey-lighten-1">{{ currentLyricSong?.tags || 'Lao Song' }}</div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" color="grey-lighten-1" @click="lyricsDialog = false"></v-btn>
        </div>

        <v-divider class="mb-4 border-opacity-25"></v-divider>

        <div class="lyrics-content-scroll pa-4 rounded-xl mb-4">
          <pre class="lyrics-text text-white">{{ currentLyricSong?.prompt || currentLyricSong?.lyric || 'ບໍ່ພົບເນື້ອເພງ' }}</pre>
        </div>

        <div class="d-flex justify-end gap-2">
          <v-btn
            variant="tonal"
            color="grey-lighten-1"
            rounded="lg"
            class="text-none"
            @click="lyricsDialog = false"
          >
            ປິດ (Close)
          </v-btn>
          <v-btn
            color="amber-accent-2"
            variant="flat"
            rounded="lg"
            class="text-none text-black font-weight-bold"
            prepend-icon="mdi-content-copy"
            @click="copyLyricsText(currentLyricSong?.prompt || currentLyricSong?.lyric)"
          >
            ຄັດລອກເນື້ອເພງ (Copy)
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Global Snackbar Notification -->
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      timeout="3000"
      rounded="xl"
      location="top right"
      elevation="8"
    >
      <div class="d-flex align-center">
        <v-icon start class="mr-2">{{ snackbarIcon }}</v-icon>
        <span class="font-weight-medium text-white">{{ snackbarText }}</span>
      </div>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

definePageMeta({
  layout: 'video'
});

// Navigation State
const activeTab = ref('topic');
const isServerOnline = ref(false);
const checkingCredits = ref(false);
const loadingTracks = ref(false);
const generating = ref(false);
const creditsInfo = ref(null);
const searchQuery = ref('');

// Lyrics Dialog State
const lyricsDialog = ref(false);
const currentLyricSong = ref(null);

// Toast Snackbar State
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('success');
const snackbarIcon = ref('mdi-check-circle');

function showToast(text, color = 'success', icon = 'mdi-check-circle') {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbarIcon.value = icon;
  snackbar.value = true;
}

// Preset Samples for Easy 1-Click Generation
const sampleTopics = [
  { icon: '🌸', title: 'ສາວຫຼວງພະບາງ', text: 'ເພງຮັກສາວຫຼວງພະບາງ ຄວາມຮັກທີ່ອ່ອນຫວານ ບັນຍາກາດເມືອງມໍລະດົກໂລກ' },
  { icon: '🌊', title: 'ຄິດຮອດແຄມຂອງ', text: 'ຄິດຮອດບ້ານເກີດແຄມແມ່ນ້ຳຂອງ ສຽງແຄນສຽງເພງຍາມແລງ' },
  { icon: '💔', title: 'ຄວາມຮັກທີ່ຜິດຫວັງ', text: 'ຄວາມຮັກທີ່ເຈັບປວດ ເສຍສະຫຼະໃຫ້ຄົນຮັກໄດ້ດີ' },
  { icon: '🎉', title: 'ບຸນປີໃໝ່ລາວ', text: 'ງານບຸນປີໃໝ່ລາວ ຫຼິ້ນນ້ຳມ່ວນຊື່ນ ສຽງດົນຕີໂຈ໊ະໆ' },
  { icon: '☕', title: 'ກາເຟຍາມເຊົ້າ', text: 'ຮ້ານກາເຟຍາມເຊົ້າ ກັບຄວາມຄິດຮອດຄົນທີ່ຢູ່ໄກ' },
  { icon: '🏔️', title: 'ລົມໜາວພູເບ້ຍ', text: 'ສາຍລົມໜາວເທິງຍອດພູເບ້ຍ ຫົວໃຈທີ່ໂດດດ່ຽວ' }
];

const sampleStyles = [
  { icon: '🎸', name: 'Lao Pop Ballad', tags: 'Lao pop ballad, acoustic guitar, soft emotional male vocal, 90 bpm' },
  { icon: '🪕', name: 'Morlam Sing (ໝໍລຳ)', tags: 'Lao morlam modern pop, fast tempo khaen, upbeat rhythm, female vocal' },
  { icon: '☕', name: 'Acoustic Chill', tags: 'Acoustic guitar, warm piano, soft gentle voice, slow relaxing' },
  { icon: '⚡', name: 'Lao DJ EDM Remix', tags: 'Lao club remix, heavy dance bass, synth leads, energetic 128 bpm' },
  { icon: '🥁', name: 'Lao Hip-Hop / R&B', tags: 'Lao melodic rap, smooth trap beat, 808 bass, chill vocal' },
  { icon: '🌧️', name: 'Sad Emotional', tags: 'Sad emotional strings, dramatic electric guitar, crying vocal' }
];

// Form States
const topicForm = ref({
  topic: '',
  style: 'Lao pop ballad, acoustic guitar, soft emotional male vocal, 90 bpm',
  instrumental: false
});

const customForm = ref({
  title: 'ຫວັງຮັກເຈົ້າ',
  style: 'Lao pop ballad, soft emotional vocals, acoustic',
  lyrics: '',
  instrumental: false
});

const songList = ref([]);
const sunoBaseUrl = ref('http://localhost:3008');

// Filtered Song List by search query
const filteredSongList = computed(() => {
  if (!searchQuery.value.trim()) return songList.value;
  const q = searchQuery.value.toLowerCase().trim();
  return songList.value.filter(s => 
    (s.title && s.title.toLowerCase().includes(q)) ||
    (s.tags && s.tags.toLowerCase().includes(q)) ||
    (s.id && s.id.toLowerCase().includes(q))
  );
});

// Insert Ready-to-Test Sample Lao Lyrics
function insertSampleLyrics() {
  customForm.value.title = 'ຫຼົງຮັກສາວລາວ';
  customForm.value.style = 'Lao modern pop ballad, soft emotional male vocal, acoustic guitar';
  customForm.value.lyrics = `[Intro]
ໂອ້... ເດ... ໃຈເອີຍ...

[Verse 1]
ຍ່າງຜ່ານບ່ອນເກົ່າ ທີ່ເຮົາເຄີຍພົບກັນ
ຮອຍຍິ້ມຂອງເຈົ້າ ມັນຕິດຢູ່ໃນຄວາມຊົງຈຳ
ບໍ່ຮູ້ເປັນຫຍັງ ມື້ນີ້ໃຈມັນລອຍ
ຄິດຮອດແຕ່ໜ້າງາມໆ ຂອງເຈົ້າທຸກເວລາ

[Chorus]
ຫຼົງຮັກເຈົ້າແລ້ວ ຮູ້ບໍ່ຄົນດີ
ມອບໝົດທັງໃຈ ໃຫ້ເຈົ້າຄົນນີ້
ບໍ່ມີຄຳໃດ ຈະປຽບເໝືອນດັ່ງ
ວ່າຮັກເຈົ້າຫຼາຍສຳໃດ ແມ່ສາວລາວເອີຍ!

[Verse 2]
ເຫງົາມື້ໃດ ກໍເປີດເບິ່ງຮູບເຈົ້າ
ເຖິງເຮົາຈະຢູ່ໄກກັນສຳໃດ
ແຕ່ໃຈສອງດວງ ມັນບອກວ່າຮັກກັນ
ຖ້າຫາກເປັນໄປໄດ້ ຢາກມີເຈົ້າຄຽງຂ້າງ

[Chorus]
ຫຼົງຮັກເຈົ້າແລ້ວ ຮູ້ບໍ່ຄົນດີ
ມອບໝົດທັງໃຈ ໃຫ້ເຈົ້າຄົນນີ້
ບໍ່ມີຄຳໃດ ຈະປຽບເໝືອນດັ່ງ
ວ່າຮັກເຈົ້າຫຼາຍສຳໃດ ແມ່ສາວລາວເອີຍ!

[Outro]
ຫຼົງຮັກແລ້ວ... ຮູ້ບໍ່...
ຮັກເຈົ້າຕະຫຼອດໄປ...`;
  showToast('ໃສ່ເນື້ອເພງຕົວຢ່າງສຳເລັດແລ້ວ!', 'info', 'mdi-playlist-check');
}

// Append Lyric Tag Marker to textarea
function appendLyricTag(tag) {
  if (!customForm.value.lyrics) {
    customForm.value.lyrics = tag;
  } else {
    customForm.value.lyrics += (customForm.value.lyrics.endsWith('\n') ? '\n' : '\n\n') + tag;
  }
}

// Copy Audio Link
function copyAudioLink(url) {
  if (!url) return;
  navigator.clipboard.writeText(url);
  showToast('ຄັດລອກລິ້ງສຽງແລ້ວ!', 'success', 'mdi-content-copy');
}

// Copy Lyrics Text
function copyLyricsText(text) {
  if (!text) return;
  navigator.clipboard.writeText(text);
  showToast('ຄັດລອກເນື້ອເພງແລ້ວ!', 'success', 'mdi-content-copy');
}

// Open Lyrics Modal
function openLyricsDialog(song) {
  currentLyricSong.value = song;
  lyricsDialog.value = true;
}

// Check Server & Credits
async function checkCredits() {
  checkingCredits.value = true;
  const ports = ['http://localhost:3008', 'http://localhost:3000', 'http://localhost:3001'];
  let found = false;

  for (const url of ports) {
    try {
      const res = await fetch(`${url}/api/get_limit`);
      if (res.ok) {
        const data = await res.json();
        if (data && data.credits_left !== undefined) {
          creditsInfo.value = data;
          sunoBaseUrl.value = url;
          isServerOnline.value = true;
          found = true;
          break;
        }
      }
    } catch (err) {
      // try next port
    }
  }

  if (!found) {
    isServerOnline.value = false;
  }
  checkingCredits.value = false;
}

// Fetch 20 Recent Tracks from Suno API
async function fetchRecentTracks() {
  loadingTracks.value = true;
  try {
    const res = await fetch(`${sunoBaseUrl.value}/api/get`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        // Sanitize audio url
        songList.value = data.map(song => {
          let audioUrl = song.audio_url;
          if (!audioUrl || audioUrl.includes('forbidden')) {
            audioUrl = `https://d2lwuy8qc234o3.cloudfront.net/1/clip/${song.id}.m4a`;
          }
          return {
            ...song,
            audio_url: audioUrl
          };
        });
      }
    }
  } catch (err) {
    console.error('Error fetching tracks:', err);
  } finally {
    loadingTracks.value = false;
  }
}

// Full Refresh
async function refreshAll() {
  await checkCredits();
  if (isServerOnline.value) {
    await fetchRecentTracks();
    showToast('ອັບເດດສະຖານະ ແລະ ລາຍການເພງແລ້ວ', 'success', 'mdi-check-circle');
  } else {
    showToast('ເຊີບເວີຍັງ Offline, ກະລຸນາເປີດ 1_start_suno_server.bat', 'warning', 'mdi-alert');
  }
}

// Generate from Topic (Gemini + Suno)
async function generateFromTopic() {
  if (!topicForm.value.topic.trim()) return;
  generating.value = true;
  try {
    const promptText = topicForm.value.style
      ? `${topicForm.value.topic}, Style: ${topicForm.value.style}`
      : topicForm.value.topic;

    const res = await fetch(`${sunoBaseUrl.value}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: promptText,
        make_instrumental: topicForm.value.instrumental,
        wait_audio: true
      })
    });

    const data = await res.json();
    handleNewTracks(data);
    showToast('🎉 ສ້າງເພງໃໝ່ສຳເລັດແລ້ວ!', 'success', 'mdi-music-note-plus');
  } catch (err) {
    console.error('Error generating song:', err);
    showToast('ເກີດຂໍ້ຜິດພາດໃນການສ້າງເພງ', 'error', 'mdi-alert');
  } finally {
    generating.value = false;
    checkCredits();
  }
}

// Generate from Custom Lyrics
async function generateFromCustomLyrics() {
  if (!customForm.value.lyrics.trim()) return;
  generating.value = true;
  try {
    const res = await fetch(`${sunoBaseUrl.value}/api/custom_generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: customForm.value.lyrics,
        tags: customForm.value.style,
        title: customForm.value.title || 'Lao Song',
        make_instrumental: customForm.value.instrumental,
        wait_audio: true
      })
    });

    const data = await res.json();
    handleNewTracks(data);
    showToast('🎉 ສ້າງເພງຈາກເນື້ອຮ້ອງສຳເລັດແລ້ວ!', 'success', 'mdi-music-note-plus');
  } catch (err) {
    console.error('Error generating custom song:', err);
    showToast('ເກີດຂໍ້ຜິດພາດໃນການສ້າງເພງ', 'error', 'mdi-alert');
  } finally {
    generating.value = false;
    checkCredits();
  }
}

// Add newly generated tracks to the top of list
function handleNewTracks(data) {
  if (!data) return;
  const items = Array.isArray(data) ? data : [data];
  for (const track of items) {
    if (track && (track.audio_url || track.id)) {
      if (!track.audio_url || track.audio_url.includes('forbidden')) {
        track.audio_url = `https://d2lwuy8qc234o3.cloudfront.net/1/clip/${track.id}.m4a`;
      }
      // Check if not already in list
      const existingIdx = songList.value.findIndex(s => s.id === track.id);
      if (existingIdx !== -1) {
        songList.value[existingIdx] = track;
      } else {
        songList.value.unshift(track);
      }
    }
  }
}

onMounted(async () => {
  await checkCredits();
  if (isServerOnline.value) {
    await fetchRecentTracks();
  }
});
</script>

<style scoped>
/* ======================================================== */
/* High Contrast, Modern Glassmorphism & Visual Aesthetics  */
/* ======================================================== */

.song-generator-container {
  color: #f8fafc;
}

/* Hero Header Card */
.hero-card {
  background: linear-gradient(135deg, rgba(30, 27, 75, 0.95) 0%, rgba(15, 23, 42, 0.95) 60%, rgba(30, 41, 59, 0.95) 100%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.brand-title {
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #ffffff 40%, #fef08a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle-text {
  color: #cbd5e1 !important;
}

.avatar-glow {
  width: 58px;
  height: 58px;
  border-radius: 16px;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.3), rgba(217, 119, 6, 0.08));
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(245, 158, 11, 0.4);
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
}

/* Pulsing Online Dot */
.pulse-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ef4444;
}

.pulse-active {
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: pulse-ring 2s infinite;
}

@keyframes pulse-ring {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Credits Badge */
.credits-badge {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(245, 158, 11, 0.35);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
}

.credits-label {
  font-size: 11px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.credits-value {
  font-size: 18px;
  line-height: 1.2;
}

.credits-sub {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

/* Panels */
.generator-panel, .results-panel {
  background: rgba(20, 27, 45, 0.88) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  backdrop-filter: blur(16px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

/* Tabs */
.custom-tabs {
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-item {
  color: #cbd5e1 !important;
  transition: all 0.2s ease;
  font-size: 14px;
}

.tab-item.v-tab--selected {
  color: #fbbf24 !important;
  background: rgba(251, 191, 36, 0.12) !important;
  border-radius: 8px;
}

/* Input Labels & Badges */
.input-label {
  font-size: 13.5px;
  font-weight: 700;
  color: #f1f5f9;
}

.required-badge {
  font-size: 10px;
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.4);
  padding: 1px 6px;
  border-radius: 6px;
  font-weight: 700;
}

.optional-badge {
  font-size: 10px;
  background: rgba(14, 165, 233, 0.15);
  color: #7dd3fc;
  border: 1px solid rgba(14, 165, 233, 0.3);
  padding: 1px 6px;
  border-radius: 6px;
  font-weight: 600;
}

/* High Contrast Input Styling Overrides */
:deep(.high-contrast-input .v-field) {
  background-color: rgba(15, 23, 42, 0.75) !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: #ffffff !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

:deep(.high-contrast-input .v-field--focused) {
  border-color: #f59e0b !important;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.3) !important;
}

:deep(.high-contrast-input input),
:deep(.high-contrast-input textarea) {
  color: #ffffff !important;
  font-weight: 500;
}

:deep(.high-contrast-input input::placeholder),
:deep(.high-contrast-input textarea::placeholder) {
  color: #94a3b8 !important;
  opacity: 1 !important;
}

/* Quick Chips */
.quick-chips-wrapper {
  background: rgba(15, 23, 42, 0.4);
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px dashed rgba(255, 255, 255, 0.1);
}

.chips-title {
  font-size: 11.5px;
  color: #94a3b8;
  font-weight: 600;
}

.preset-chip {
  cursor: pointer;
  transition: transform 0.15s ease, background 0.15s ease;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.preset-chip:hover {
  transform: translateY(-1px);
  background: rgba(245, 158, 11, 0.2) !important;
  border-color: #f59e0b !important;
  color: #ffffff !important;
}

/* Lyrics Helper Toolbar */
.lyrics-toolbar {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Toggle Card */
.toggle-card {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

/* Generate Big Button */
.generate-btn {
  letter-spacing: 0.3px;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.35);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(245, 158, 11, 0.5);
}

/* Sound Wave Animation Box */
.generating-box {
  background: linear-gradient(135deg, rgba(30, 27, 75, 0.8), rgba(15, 23, 42, 0.8));
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.sound-wave-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  height: 48px;
}

.wave-bar {
  width: 6px;
  height: 10px;
  background: linear-gradient(180deg, #f59e0b, #ec4899);
  border-radius: 99px;
  animation: wave 1.2s ease-in-out infinite alternate;
}

@keyframes wave {
  0% { height: 8px; opacity: 0.4; }
  100% { height: 42px; opacity: 1; }
}

/* Empty State */
.empty-icon-wrap {
  width: 80px;
  height: 80px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px dashed rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Song Item Card */
.song-card {
  background: rgba(15, 23, 42, 0.75) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.song-card:hover {
  transform: translateY(-2px);
  border-color: rgba(245, 158, 11, 0.4) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.cover-art-wrapper {
  width: 68px;
  height: 68px;
  position: relative;
}

.cover-placeholder {
  width: 68px;
  height: 68px;
  background: linear-gradient(135deg, #1e1b4b, #312e81);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.song-title {
  color: #ffffff;
  font-size: 15px;
}

.id-tag {
  background: rgba(255, 255, 255, 0.08);
  padding: 1px 5px;
  border-radius: 4px;
  color: #cbd5e1;
}

.native-audio-player {
  height: 38px;
  border-radius: 8px;
  outline: none;
}

.border-t {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

/* Scroll area */
.song-list-scroll {
  max-height: 650px;
  overflow-y: auto;
}

.song-list-scroll::-webkit-scrollbar {
  width: 6px;
}
.song-list-scroll::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.4);
  border-radius: 4px;
}
.song-list-scroll::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

/* Lyrics Modal */
.lyrics-modal {
  background: #0f172a !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.lyrics-content-scroll {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  max-height: 400px;
  overflow-y: auto;
}

.lyrics-text {
  font-family: inherit;
  font-size: 14px;
  line-height: 1.7;
  white-space: pre-wrap;
}
</style>
