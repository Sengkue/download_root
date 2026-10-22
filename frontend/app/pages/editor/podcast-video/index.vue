<template>
  <div class="podcast-studio-page">
    <v-container fluid class="pa-3 pa-md-6 pa-lg-8">
      
      <!-- Studio Header Banner -->
      <v-card class="studio-header-card pa-5 pa-md-6 rounded-2xl mb-6 elevation-10 border position-relative overflow-hidden">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>

        <div class="position-relative z-10 d-flex flex-column flex-lg-row align-lg-center justify-space-between gap-4">
          <div>
            <div class="d-flex align-center gap-2 mb-2 flex-wrap">
              <v-chip color="deep-purple-accent-2" variant="flat" size="small" class="font-weight-black">
                <v-icon start size="small">mdi-book-open-page-variant</v-icon>
                STORYBOOK & PODCAST VIDEO CREATOR
              </v-chip>
              <v-chip color="amber-accent-3" variant="tonal" size="small" class="font-weight-bold">
                📖 Episode Series (EP01, EP02...)
              </v-chip>
              <v-chip color="cyan-accent-3" variant="tonal" size="small" class="font-weight-bold">
                🇲🇼 Lus Hmoob RPA • 🇱🇦 ພາສາລາວ • 🇹🇭 ไทย
              </v-chip>
              <v-chip color="pink-accent-2" variant="tonal" size="small" class="font-weight-bold">
                <v-icon start size="small">mdi-youtube</v-icon>
                YouTube Podcast Ready
              </v-chip>
            </div>
            
            <h1 class="text-h4 text-md-h3 font-weight-black text-white mb-2 tracking-tight">
              ອັດວິດີໂອ / ຮູບພາບ • Storybook & Podcast Studio
            </h1>
            <p class="text-subtitle-1 text-grey-lighten-2 mb-0 max-w-3xl">
              Input illustration image + text (Page 1, Page 2... / EP01, EP02...) to generate natural Hmong & Lao voiceover with word-by-word reading, animated storybook layout, and export complete video episodes for YouTube.
            </p>
          </div>

          <!-- Top Episode Selector & Actions -->
          <div class="d-flex align-center flex-wrap gap-2">
            <!-- Episode Dropdown -->
            <v-menu location="bottom end">
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  color="rgba(255,255,255,0.12)"
                  variant="flat"
                  rounded="xl"
                  class="text-white font-weight-bold text-none px-4"
                  prepend-icon="mdi-format-list-bulleted"
                  append-icon="mdi-chevron-down"
                >
                  {{ currentEpisode.title }}
                </v-btn>
              </template>
              <v-list density="compact" rounded="xl" class="bg-grey-darken-4 text-white border" min-width="260">
                <v-list-subheader class="text-caption font-weight-bold text-uppercase text-grey-lighten-1">My Episodes</v-list-subheader>
                <v-list-item
                  v-for="(ep, idx) in allEpisodes"
                  :key="ep.id"
                  @click="switchEpisode(idx)"
                  :active="currentEpisodeIndex === idx"
                  color="deep-purple-accent-2"
                >
                  <template v-slot:prepend>
                    <v-icon size="small" color="deep-purple-accent-2">mdi-movie-open</v-icon>
                  </template>
                  <v-list-item-title class="font-weight-bold">{{ ep.title }}</v-list-item-title>
                  <v-list-item-subtitle class="text-caption">{{ ep.scenes?.length || 1 }} Pages / Scenes</v-list-item-subtitle>
                </v-list-item>
                <v-divider class="my-1"></v-divider>
                <v-list-item @click="createNewEpisode" color="cyan-accent-3">
                  <template v-slot:prepend>
                    <v-icon size="small" color="cyan-accent-3">mdi-plus-circle</v-icon>
                  </template>
                  <v-list-item-title class="font-weight-bold text-cyan-accent-3">+ Create New Episode</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>

            <v-btn
              color="deep-purple-accent-2"
              rounded="xl"
              class="font-weight-bold text-none px-5 shadow-lg"
              prepend-icon="mdi-movie-open-play"
              :disabled="!canGenerateVideo"
              :loading="isRecordingVideo"
              @click="startVideoRecording"
            >
              Export Episode Video (HD)
            </v-btn>
          </div>
        </div>
      </v-card>

      <!-- Episode Series Sub-bar: Scene / Page Thumbnails Bar -->
      <v-card class="scene-navigator-bar pa-3 rounded-2xl mb-6 bg-surface-container-low border elevation-4">
        <div class="d-flex align-center justify-space-between mb-2 px-2">
          <div class="d-flex align-center gap-2">
            <v-icon color="amber-accent-2" size="small">mdi-filmstrip</v-icon>
            <span class="text-subtitle-2 font-weight-black text-white text-uppercase tracking-wider">
              {{ currentEpisode.title }} — Story Scenes / Pages ({{ currentEpisode.scenes.length }})
            </span>
          </div>

          <div class="d-flex align-center gap-2">
            <span class="text-caption text-grey-lighten-2 d-none d-sm-inline">
              Total Duration: ~{{ formatTime(totalEpisodeDuration) }}
            </span>
            <v-btn
              size="small"
              color="deep-purple-accent-2"
              variant="flat"
              rounded="lg"
              class="font-weight-bold text-none px-3"
              prepend-icon="mdi-plus"
              @click="addNewScene"
            >
              Add Page / Scene
            </v-btn>
          </div>
        </div>

        <!-- Horizontal Scrollable Scene Pills -->
        <div class="scene-strip d-flex align-center gap-3 px-2 py-1 overflow-x-auto">
          <div
            v-for="(scene, idx) in currentEpisode.scenes"
            :key="scene.id"
            class="scene-card position-relative rounded-xl cursor-pointer transition-all border d-flex flex-column"
            :class="activeSceneIndex === idx ? 'scene-card-active' : 'scene-card-inactive'"
            @click="selectScene(idx)"
          >
            <!-- Badge Page Number -->
            <div class="scene-number-chip text-caption font-weight-black">
              Page {{ idx + 1 }}
            </div>

            <!-- Thumbnail Preview -->
            <div class="scene-thumb-wrapper rounded-lg overflow-hidden position-relative mb-1">
              <img
                v-if="scene.imageUrl"
                :src="scene.imageUrl"
                class="scene-thumb-img"
              />
              <div v-else class="scene-thumb-placeholder d-flex align-center justify-center">
                <v-icon size="24" color="grey">mdi-image-outline</v-icon>
              </div>
            </div>

            <!-- Scene Snippet Text -->
            <div class="scene-snippet text-truncate text-grey-lighten-2 px-1" style="font-size: 11px;">
              {{ scene.text || 'Empty script...' }}
            </div>

            <!-- Delete scene button (if more than 1) -->
            <v-btn
              v-if="currentEpisode.scenes.length > 1"
              icon="mdi-close"
              size="x-small"
              color="error"
              variant="flat"
              class="scene-del-btn"
              @click.stop="deleteScene(idx)"
              title="Delete page"
            ></v-btn>
          </div>

          <!-- Add Scene Ghost Button -->
          <div
            class="add-scene-ghost rounded-xl d-flex flex-column align-center justify-center border-dashed cursor-pointer"
            @click="addNewScene"
          >
            <v-icon color="deep-purple-lighten-2" size="24">mdi-plus-circle-outline</v-icon>
            <span class="text-caption text-grey-lighten-2 mt-1" style="font-size: 11px;">+ Page {{ currentEpisode.scenes.length + 1 }}</span>
          </div>
        </div>
      </v-card>

      <!-- Main Workspace Grid -->
      <v-row>
        
        <!-- ================= LEFT COLUMN: CURRENT SCENE / PAGE EDITOR ================= -->
        <v-col cols="12" lg="6">
          <v-card class="studio-controls-card rounded-2xl border pa-4 pa-md-6 bg-surface-container-low elevation-4">
            
            <!-- Tab Navigation for Current Page -->
            <v-tabs v-model="activeTab" color="deep-purple-accent-2" class="mb-4 studio-tabs" density="comfortable">
              <v-tab value="page_content" class="font-weight-bold text-none">
                <v-icon start size="small">mdi-book-edit</v-icon>
                Page {{ activeSceneIndex + 1 }} Content
              </v-tab>
              <v-tab value="layout_style" class="font-weight-bold text-none">
                <v-icon start size="small">mdi-palette-swatch-outline</v-icon>
                Layout & Style
              </v-tab>
              <v-tab value="voice_audio" class="font-weight-bold text-none">
                <v-icon start size="small">mdi-waveform</v-icon>
                Voice & Audio
              </v-tab>
            </v-tabs>

            <v-window v-model="activeTab">
              
              <!-- TAB 1: PAGE CONTENT (IMAGE + SCRIPT) -->
              <v-window-item value="page_content">
                <div class="space-y-4">
                  
                  <!-- Page Header Bar -->
                  <div class="d-flex align-center justify-space-between bg-surface-container-lowest pa-3 rounded-xl border">
                    <div class="d-flex align-center gap-2">
                      <v-chip color="deep-purple-accent-2" size="small" class="font-weight-black">
                        Page {{ activeSceneIndex + 1 }} of {{ currentEpisode.scenes.length }}
                      </v-chip>
                      <span class="text-caption text-grey-lighten-1">{{ currentScene.chapterTitle || 'Chapter Scene' }}</span>
                    </div>

                    <div class="d-flex align-center gap-2">
                      <v-btn
                        size="x-small"
                        variant="tonal"
                        color="cyan-accent-3"
                        class="text-none font-weight-bold"
                        prepend-icon="mdi-content-copy"
                        @click="duplicateScene(activeSceneIndex)"
                      >
                        Duplicate
                      </v-btn>
                    </div>
                  </div>

                  <!-- 1. Upload Page Image / Illustration -->
                  <div>
                    <div class="d-flex align-center justify-space-between mb-2">
                      <span class="text-caption font-weight-black text-uppercase text-grey-lighten-1">
                        1. Page Illustration / Painting (ຮູບພາບປະກອບ)
                      </span>
                      <span v-if="currentScene.imageUrl" class="text-caption text-success font-weight-bold">
                        <v-icon size="x-small" color="success">mdi-check-circle</v-icon> Image Loaded
                      </span>
                    </div>

                    <div
                      class="media-drop-zone pa-5 rounded-2xl text-center border-dashed cursor-pointer position-relative overflow-hidden"
                      @click="$refs.sceneImageInput.click()"
                      @dragover.prevent
                      @drop.prevent="onSceneImageDrop"
                    >
                      <input
                        type="file"
                        ref="sceneImageInput"
                        accept="image/*"
                        class="d-none"
                        @change="onSceneImageSelect"
                      />

                      <!-- Preview if image uploaded -->
                      <div v-if="currentScene.imageUrl" class="d-flex align-center justify-center gap-4">
                        <img :src="currentScene.imageUrl" class="uploaded-img-preview rounded-xl elevation-4 border" />
                        <div class="text-left">
                          <div class="text-body-2 font-weight-bold text-white mb-1">Illustration Active</div>
                          <div class="text-caption text-grey-lighten-2 mb-2">Click or drop new file to replace</div>
                          <v-btn size="x-small" color="error" variant="tonal" @click.stop="clearSceneImage">
                            Remove Image
                          </v-btn>
                        </div>
                      </div>

                      <!-- Placeholder -->
                      <div v-else>
                        <v-icon size="38" color="deep-purple-accent-2" class="mb-2">mdi-image-plus</v-icon>
                        <div class="text-subtitle-2 font-weight-bold text-white">
                          Upload Story Illustration for Page {{ activeSceneIndex + 1 }}
                        </div>
                        <div class="text-caption text-grey-lighten-1">
                          Drop your artwork, painting, character portrait or scene (JPG, PNG)
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 2. Language Selection & Quick Sample Templates -->
                  <div>
                    <div class="d-flex align-center justify-space-between mb-2">
                      <span class="text-caption font-weight-black text-uppercase text-grey-lighten-1">
                        2. Story Language
                      </span>
                      <div class="d-flex gap-1">
                        <v-chip
                          v-for="l in ['lo', 'hmn', 'th', 'en']"
                          :key="l"
                          size="x-small"
                          :color="currentEpisode.language === l ? 'deep-purple-accent-2' : 'surface-container'"
                          :variant="currentEpisode.language === l ? 'flat' : 'outlined'"
                          class="font-weight-bold cursor-pointer"
                          @click="changeEpisodeLanguage(l)"
                        >
                          {{ l.toUpperCase() }}
                        </v-chip>
                      </div>
                    </div>

                    <!-- Quick Sample Text Loader -->
                    <div class="bg-surface-container-lowest pa-3 rounded-xl border mb-2 d-flex align-center justify-space-between flex-wrap gap-2">
                      <span class="text-caption text-grey-lighten-1">Quick Sample Story:</span>
                      <div class="d-flex gap-2 flex-wrap">
                        <v-chip
                          size="x-small"
                          color="amber-accent-2"
                          variant="tonal"
                          class="cursor-pointer font-weight-bold"
                          @click="loadSampleSivaStory"
                        >
                          🇱🇦 ເລື່ອງ ສີວາ (From Your Image)
                        </v-chip>
                        <v-chip
                          size="x-small"
                          color="cyan-accent-2"
                          variant="tonal"
                          class="cursor-pointer font-weight-bold"
                          @click="loadSampleHmongStory"
                        >
                          🇲🇼 Dab Neeg Luav Ntse
                        </v-chip>
                      </div>
                    </div>

                    <!-- Textarea for Script -->
                    <div class="d-flex align-center justify-space-between mb-1">
                      <label class="text-caption font-weight-bold text-grey-lighten-1">
                        Page Text / Paragraph (ຂໍ້ຄວາມ / Lus Dab Neeg):
                      </label>
                      <span class="text-caption text-grey-lighten-2">
                        {{ currentScene.text.length }} chars • {{ countWords(currentScene.text) }} words
                      </span>
                    </div>

                    <v-textarea
                      v-model="currentScene.text"
                      rows="5"
                      variant="outlined"
                      bg-color="rgba(15, 23, 42, 0.7)"
                      color="deep-purple-accent-2"
                      placeholder="Enter the story text for this page in Lao or Hmong..."
                      class="rounded-xl font-script-area"
                      density="comfortable"
                      hide-details
                      @update:model-value="onSceneTextChange"
                    ></v-textarea>
                  </div>

                  <!-- Header Tag & Page Drop Cap Config -->
                  <v-row dense>
                    <v-col cols="6">
                      <v-text-field
                        v-model="currentScene.headerTag"
                        label="Top Header Title (e.g., KOT WANG)"
                        variant="outlined"
                        density="compact"
                        hide-details
                        bg-color="rgba(255,255,255,0.05)"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model="currentScene.dropCapLetter"
                        label="Drop Cap Initial (ຕົວເລີ່ມຕົ້ນ)"
                        variant="outlined"
                        density="compact"
                        hide-details
                        bg-color="rgba(255,255,255,0.05)"
                        placeholder="Automatic from first word"
                      ></v-text-field>
                    </v-col>
                  </v-row>

                  <!-- Audition Current Page Audio -->
                  <div class="d-flex align-center justify-space-between pt-2">
                    <v-btn
                      :color="isPlayingAudio ? 'amber-accent-4' : 'deep-purple-accent-2'"
                      variant="flat"
                      rounded="xl"
                      class="font-weight-bold text-none px-5"
                      :prepend-icon="isPlayingAudio ? 'mdi-pause' : 'mdi-volume-high'"
                      :loading="isLoadingTTS"
                      :disabled="!currentScene.text.trim()"
                      @click="toggleAudioPreview"
                    >
                      {{ isPlayingAudio ? 'Pause Page Audio' : 'Listen Page Voice (ຟັງສຽງໜ້ານີ້)' }}
                    </v-btn>

                    <span v-if="audioDuration > 0" class="text-caption text-grey-lighten-1">
                      Duration: {{ formatTime(audioDuration) }}
                    </span>
                  </div>

                </div>
              </v-window-item>

              <!-- TAB 2: LAYOUT & VISUAL STYLE -->
              <v-window-item value="layout_style">
                <div class="space-y-4">
                  
                  <!-- Layout Mode Selector -->
                  <div>
                    <span class="text-caption font-weight-black text-uppercase text-grey-lighten-1 mb-2 d-block">
                      Visual Presentation Layout
                    </span>
                    <v-row dense>
                      <!-- Storybook Split Mode (like reference image) -->
                      <v-col cols="4">
                        <v-card
                          class="pa-3 text-center rounded-xl cursor-pointer border"
                          :class="currentEpisode.layoutStyle === 'storybook' ? 'bg-deep-purple-darken-3 border-purple-accent' : 'bg-surface-container-lowest'"
                          @click="currentEpisode.layoutStyle = 'storybook'"
                        >
                          <v-icon size="24" color="amber-accent-2" class="mb-1">mdi-book-open-page-variant</v-icon>
                          <div class="font-weight-bold text-caption text-white">Storybook Spread</div>
                          <div class="text-grey-lighten-2" style="font-size: 10px;">Like Your Image</div>
                        </v-card>
                      </v-col>

                      <!-- Fullscreen Cinematic Podcast -->
                      <v-col cols="4">
                        <v-card
                          class="pa-3 text-center rounded-xl cursor-pointer border"
                          :class="currentEpisode.layoutStyle === 'cinematic' ? 'bg-deep-purple-darken-3 border-purple-accent' : 'bg-surface-container-lowest'"
                          @click="currentEpisode.layoutStyle = 'cinematic'"
                        >
                          <v-icon size="24" color="cyan-accent-3" class="mb-1">mdi-movie-open</v-icon>
                          <div class="font-weight-bold text-caption text-white">Full Cinematic</div>
                          <div class="text-grey-lighten-2" style="font-size: 10px;">Podcast Overlay</div>
                        </v-card>
                      </v-col>

                      <!-- YouTube Shorts / TikTok 9:16 -->
                      <v-col cols="4">
                        <v-card
                          class="pa-3 text-center rounded-xl cursor-pointer border"
                          :class="currentEpisode.layoutStyle === 'shorts' ? 'bg-deep-purple-darken-3 border-purple-accent' : 'bg-surface-container-lowest'"
                          @click="currentEpisode.layoutStyle = 'shorts'"
                        >
                          <v-icon size="24" color="pink-accent-2" class="mb-1">mdi-cellphone</v-icon>
                          <div class="font-weight-bold text-caption text-white">Shorts 9:16</div>
                          <div class="text-grey-lighten-2" style="font-size: 10px;">TikTok / Reels</div>
                        </v-card>
                      </v-col>
                    </v-row>
                  </div>

                  <!-- Book Page Customization (When Storybook Mode) -->
                  <div v-if="currentEpisode.layoutStyle === 'storybook'" class="space-y-3">
                    <span class="text-caption font-weight-black text-uppercase text-grey-lighten-1">
                      Storybook Page Settings
                    </span>

                    <v-row dense>
                      <v-col cols="6">
                        <span class="text-caption text-grey-lighten-2 mb-1 d-block">Paper Color Theme</span>
                        <v-select
                          v-model="paperTheme"
                          :items="[
                            { title: 'Parchment Cream (Classic Book)', value: 'cream' },
                            { title: 'Pure Clean White', value: 'white' },
                            { title: 'Warm Sand Vintage', value: 'sand' },
                            { title: 'Dark Midnight Reader', value: 'dark' }
                          ]"
                          item-title="title"
                          item-value="value"
                          variant="outlined"
                          density="compact"
                          hide-details
                          bg-color="rgba(255,255,255,0.05)"
                        ></v-select>
                      </v-col>

                      <v-col cols="6">
                        <span class="text-caption text-grey-lighten-2 mb-1 d-block">Drop Cap Initial Style</span>
                        <v-select
                          v-model="dropCapStyle"
                          :items="[
                            { title: 'Elegant Curly / Calligraphic', value: 'calligraphic' },
                            { title: 'Bold Modern Serif', value: 'serif' },
                            { title: 'Simple Sans', value: 'sans' }
                          ]"
                          item-title="title"
                          item-value="value"
                          variant="outlined"
                          density="compact"
                          hide-details
                          bg-color="rgba(255,255,255,0.05)"
                        ></v-select>
                      </v-col>
                    </v-row>

                    <v-row dense>
                      <v-col cols="6">
                        <span class="text-caption text-grey-lighten-2 mb-1 d-block">Story Font Size: {{ bookFontSize }}px</span>
                        <v-slider
                          v-model="bookFontSize"
                          min="24"
                          max="48"
                          step="2"
                          color="deep-purple-accent-2"
                          track-color="rgba(255,255,255,0.1)"
                          hide-details
                          density="compact"
                        ></v-slider>
                      </v-col>
                      <v-col cols="6">
                        <span class="text-caption text-grey-lighten-2 mb-1 d-block">Word Highlight Color</span>
                        <div class="d-flex gap-2 pt-1">
                          <v-chip
                            v-for="color in ['#d97706', '#2563eb', '#9333ea', '#059669', '#dc2626']"
                            :key="color"
                            size="small"
                            :style="{ backgroundColor: color, width: '24px', height: '24px' }"
                            class="cursor-pointer border"
                            :class="activeWordColor === color ? 'elevation-4 border-white' : ''"
                            @click="activeWordColor = color"
                          ></v-chip>
                        </div>
                      </v-col>
                    </v-row>

                    <!-- Ken Burns Zoom on illustration -->
                    <div class="bg-surface-container-lowest pa-3 rounded-xl border d-flex align-center justify-space-between">
                      <div>
                        <div class="text-body-2 font-weight-bold text-white">Cinematic Gentle Zoom</div>
                        <div class="text-caption text-grey-lighten-2">Slow zoom motion on left illustration</div>
                      </div>
                      <v-switch
                        v-model="kenBurnsEnabled"
                        color="deep-purple-accent-2"
                        inset
                        density="compact"
                        hide-details
                      ></v-switch>
                    </div>
                  </div>

                  <!-- Waveform & Title Overlays -->
                  <div class="bg-surface-container-lowest pa-3 rounded-xl border space-y-3">
                    <div class="d-flex align-center justify-space-between">
                      <div>
                        <div class="text-body-2 font-weight-bold text-white">Audio Waveform Visualizer</div>
                        <div class="text-caption text-grey-lighten-2">Animated sound wave pulses during voice</div>
                      </div>
                      <v-switch
                        v-model="waveformEnabled"
                        color="pink-accent-2"
                        inset
                        density="compact"
                        hide-details
                      ></v-switch>
                    </div>
                  </div>

                </div>
              </v-window-item>

              <!-- TAB 3: VOICE & AUDIO MIXER (ElevenLabs Powered) -->
              <v-window-item value="voice_audio">
                <div class="space-y-4">

                  <!-- ElevenLabs Plan & Credits Status Badge -->
                  <div class="pa-4 rounded-xl border bg-surface-container-lowest">
                    <div class="d-flex align-center justify-space-between mb-2">
                      <div class="d-flex align-center gap-2">
                        <v-avatar color="deep-purple-accent-2" size="30">
                          <v-icon size="small" color="white">mdi-waveform</v-icon>
                        </v-avatar>
                        <div>
                          <div class="text-subtitle-2 font-weight-black text-white">ElevenLabs AI Studio</div>
                          <div class="text-caption text-cyan-accent-3 font-weight-bold">
                            {{ elevenUserStatus?.tier ? `Plan: ${elevenUserStatus.tier.toUpperCase()}` : 'Starter Plan Connected' }}
                          </div>
                        </div>
                      </div>
                      <v-chip color="success" size="small" variant="flat" class="font-weight-bold">
                        {{ 40000 - (elevenUserStatus?.character_count || 594) }} / 40,000 Credits
                      </v-chip>
                    </div>

                    <!-- Engine Selector -->
                    <div class="mb-3">
                      <div class="text-caption text-grey-lighten-1 mb-1 font-weight-bold">Voice Engine:</div>
                      <v-btn-toggle
                        v-model="selectedEngine"
                        mandatory
                        density="compact"
                        color="deep-purple-accent-2"
                        variant="outlined"
                        class="w-100 rounded-lg"
                      >
                        <v-btn value="elevenlabs" class="flex-grow-1 text-none font-weight-bold">
                          ✨ ElevenLabs (Human AI)
                        </v-btn>
                        <v-btn value="edge_tts" class="flex-grow-1 text-none font-weight-bold">
                          ⚡ Neural Edge-TTS (Free)
                        </v-btn>
                      </v-btn-toggle>
                    </div>

                    <!-- Voice Dropdown Selection -->
                    <div v-if="selectedEngine === 'elevenlabs'" class="mb-3">
                      <v-select
                        v-model="selectedVoiceId"
                        :items="availableVoices"
                        item-title="title"
                        item-value="value"
                        label="Select ElevenLabs Voice"
                        variant="outlined"
                        density="compact"
                        hide-details
                        bg-color="rgba(255,255,255,0.05)"
                        prepend-inner-icon="mdi-account-voice"
                        @update:model-value="onSceneTextChange"
                      ></v-select>
                    </div>

                    <!-- Voice Gender -->
                    <div class="d-flex align-center justify-space-between mb-3">
                      <span class="text-caption font-weight-bold text-grey-lighten-2">Speaker Gender:</span>
                      <v-btn-toggle
                        v-model="voiceGender"
                        mandatory
                        density="compact"
                        color="cyan-accent-3"
                        variant="outlined"
                        class="rounded-lg"
                        @update:model-value="onSceneTextChange"
                      >
                        <v-btn value="male" size="small" class="text-none font-weight-bold">
                          👨 Male (ຊາຍ)
                        </v-btn>
                        <v-btn value="female" size="small" class="text-none font-weight-bold">
                          👩 Female (ຍິງ)
                        </v-btn>
                      </v-btn-toggle>
                    </div>

                    <!-- Master Volume -->
                    <div class="mb-1">
                      <div class="d-flex justify-space-between text-caption text-grey-lighten-1 mb-1">
                        <span>Voice Volume (ຄວາມດັງສຽງ):</span>
                        <span class="font-weight-bold text-amber-accent-3">{{ Math.round(masterVolume * 100) }}%</span>
                      </div>
                      <v-slider
                        v-model="masterVolume"
                        min="0.1"
                        max="1.0"
                        step="0.05"
                        color="amber-accent-3"
                        track-color="rgba(255,255,255,0.1)"
                        hide-details
                        density="compact"
                      ></v-slider>
                    </div>
                  </div>

                  <!-- Word Voice Reading Mode & Speed -->
                  <div class="bg-surface-container-lowest pa-4 rounded-xl border">
                    <div class="d-flex align-center justify-space-between mb-3">
                      <div>
                        <div class="text-subtitle-2 font-weight-black text-white d-flex align-center gap-2">
                          <v-icon size="small" color="cyan-accent-3">mdi-translate</v-icon>
                          Reading Cadence
                        </div>
                        <div class="text-caption text-grey-lighten-2">
                          Synchronized word voice reader
                        </div>
                      </div>
                      <v-btn-toggle
                        v-model="readingMode"
                        mandatory
                        density="compact"
                        color="cyan-accent-3"
                        variant="outlined"
                        class="rounded-lg"
                      >
                        <v-btn value="continuous" size="small" class="text-none font-weight-bold">
                          Narrative Flow
                        </v-btn>
                        <v-btn value="word" size="small" class="text-none font-weight-bold">
                          Word-by-Word
                        </v-btn>
                      </v-btn-toggle>
                    </div>

                    <v-row dense align="center">
                      <v-col cols="12" sm="6">
                        <div class="d-flex justify-space-between text-caption text-grey-lighten-1 mb-1">
                          <span>Reading Speed:</span>
                          <span class="font-weight-bold text-white">{{ voiceSpeed }}x</span>
                        </div>
                        <v-slider
                          v-model="voiceSpeed"
                          min="0.75"
                          max="1.3"
                          step="0.05"
                          color="deep-purple-accent-2"
                          track-color="rgba(255,255,255,0.1)"
                          hide-details
                          density="compact"
                        ></v-slider>
                      </v-col>

                      <v-col cols="12" sm="6">
                        <div class="d-flex justify-space-between text-caption text-grey-lighten-1 mb-1">
                          <span>Word Pause Duration:</span>
                          <span class="font-weight-bold text-white">{{ wordPauseMs }}ms</span>
                        </div>
                        <v-slider
                          v-model="wordPauseMs"
                          :disabled="readingMode !== 'word'"
                          min="80"
                          max="350"
                          step="20"
                          color="cyan-accent-3"
                          track-color="rgba(255,255,255,0.1)"
                          hide-details
                          density="compact"
                        ></v-slider>
                      </v-col>
                    </v-row>
                  </div>

                  <!-- Background Ambiance Music Mixer -->
                  <div class="bg-surface-container-lowest pa-4 rounded-xl border">
                    <div class="d-flex align-center justify-space-between mb-3">
                      <div class="d-flex align-center gap-2">
                        <v-icon size="small" color="pink-accent-2">mdi-music</v-icon>
                        <span class="text-subtitle-2 font-weight-black text-white">Background Acoustic Music</span>
                      </div>
                      <v-switch
                        v-model="bgMusicEnabled"
                        color="pink-accent-2"
                        inset
                        density="compact"
                        hide-details
                      ></v-switch>
                    </div>

                    <v-expand-transition>
                      <div v-if="bgMusicEnabled" class="space-y-3">
                        <v-select
                          v-model="selectedBgMusic"
                          :items="[
                            { title: 'Calm Acoustic Guitar (Soft Folk)', value: 'acoustic' },
                            { title: 'Gentle Storybook Piano (Warm & Nostalgic)', value: 'piano' },
                            { title: 'Lofi Chill Study Melody', value: 'lofi' },
                            { title: 'Forest Breeze & Nature Ambiance', value: 'rain' }
                          ]"
                          item-title="title"
                          item-value="value"
                          label="Select Background Music"
                          variant="outlined"
                          density="compact"
                          hide-details
                          bg-color="rgba(255,255,255,0.05)"
                        ></v-select>

                        <div class="d-flex justify-space-between text-caption text-grey-lighten-1 mb-1">
                          <span>Music Volume:</span>
                          <span class="font-weight-bold text-pink-accent-2">{{ Math.round(bgMusicVolume * 100) }}%</span>
                        </div>
                        <v-slider
                          v-model="bgMusicVolume"
                          min="0.05"
                          max="0.4"
                          step="0.05"
                          color="pink-accent-2"
                          track-color="rgba(255,255,255,0.1)"
                          hide-details
                          density="compact"
                        ></v-slider>
                      </div>
                    </v-expand-transition>
                  </div>

                </div>
              </v-window-item>

            </v-window>

          </v-card>
        </v-col>

        <!-- ================= RIGHT COLUMN: LIVE CANVAS & EPISODE COMPILER ================= -->
        <v-col cols="12" lg="6">
          <v-card class="studio-preview-card rounded-2xl border pa-4 pa-md-6 bg-surface-container-low elevation-4 sticky-top">
            
            <div class="d-flex align-center justify-space-between mb-3">
              <div class="d-flex align-center gap-2">
                <v-icon size="small" color="deep-purple-accent-2">mdi-monitor-play</v-icon>
                <h3 class="text-subtitle-1 font-weight-black text-white mb-0">
                  {{ currentEpisode.layoutStyle === 'storybook' ? 'Storybook Page Spread' : 'Video Canvas' }}
                </h3>
              </div>
              <div class="d-flex align-center gap-2">
                <v-chip size="x-small" color="amber-accent-3" variant="flat" class="font-weight-bold">
                  {{ currentEpisode.title.split(' - ')[0] || 'EP01' }} • Page {{ activeSceneIndex + 1 }}
                </v-chip>
                <v-chip size="x-small" color="success" variant="flat" class="font-weight-bold">
                  1080p
                </v-chip>
              </div>
            </div>

            <!-- Canvas Container -->
            <div
              class="canvas-wrapper rounded-2xl overflow-hidden position-relative border elevation-8 mb-4 d-flex align-center justify-center bg-black"
              :class="currentEpisode.layoutStyle === 'shorts' ? 'ratio-9-16' : 'ratio-16-9'"
            >
              <canvas ref="videoCanvas" class="w-100 h-100 object-contain"></canvas>

              <!-- Loading / Preparing Overlay -->
              <div v-if="isLoadingTTS" class="canvas-overlay d-flex flex-column align-center justify-center">
                <v-progress-circular indeterminate color="deep-purple-accent-2" size="48" class="mb-2"></v-progress-circular>
                <div class="text-body-2 font-weight-bold text-white">Synthesizing Voice Audio...</div>
                <div class="text-caption text-grey-lighten-2 font-lao">ກຳລັງສັງເຄາະສຽງອ່ານ...</div>
              </div>

              <!-- Recording Overlay Indicator -->
              <div v-if="isRecordingVideo" class="recording-badge d-flex align-center gap-2 pa-2 px-3 rounded-pill position-absolute top-4 right-4">
                <span class="recording-dot"></span>
                <span class="text-caption font-weight-black text-white">RECORDING EPISODE ({{ Math.round(recordingProgress) }}%)</span>
              </div>
            </div>

            <!-- Transport & Page Navigation Controls -->
            <div class="bg-surface-container-lowest pa-3 rounded-xl border mb-4">
              <div class="d-flex align-center justify-space-between mb-1">
                <div class="d-flex align-center gap-2">
                  <!-- Prev Page -->
                  <v-btn
                    icon="mdi-chevron-left"
                    size="small"
                    variant="tonal"
                    :disabled="activeSceneIndex === 0"
                    @click="selectScene(activeSceneIndex - 1)"
                    title="Previous page"
                  ></v-btn>

                  <!-- Play / Pause Current Page -->
                  <v-btn
                    :icon="isPlayingAudio ? 'mdi-pause' : 'mdi-play'"
                    size="small"
                    color="deep-purple-accent-2"
                    variant="flat"
                    :disabled="!currentScene.text.trim()"
                    @click="toggleAudioPreview"
                  ></v-btn>

                  <!-- Next Page -->
                  <v-btn
                    icon="mdi-chevron-right"
                    size="small"
                    variant="tonal"
                    :disabled="activeSceneIndex >= currentEpisode.scenes.length - 1"
                    @click="selectScene(activeSceneIndex + 1)"
                    title="Next page"
                  ></v-btn>

                  <span class="text-caption font-weight-bold text-white ml-2">
                    {{ formatTime(currentTime) }} / {{ formatTime(audioDuration) }}
                  </span>
                </div>

                <div class="d-flex align-center gap-2">
                  <v-chip size="x-small" color="grey-lighten-1" variant="outlined">
                    Word {{ activeWordIdx + 1 }} / {{ parsedWords.length || 1 }}
                  </v-chip>
                </div>
              </div>

              <!-- Scrubber Bar -->
              <v-slider
                :model-value="audioProgress"
                min="0"
                max="100"
                color="deep-purple-accent-2"
                track-color="rgba(255,255,255,0.1)"
                hide-details
                density="compact"
                @update:model-value="seekAudio"
              ></v-slider>
            </div>

            <!-- Word-by-Word Live Reading Stream -->
            <div class="current-word-box pa-3 rounded-xl border mb-4 bg-surface-container-lowest">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-caption font-weight-bold text-grey-lighten-2">Live Word Stream (ຄຳທີ່ກຳລັງອ່ານ):</span>
                <span class="text-caption text-amber-accent-3 font-weight-bold">
                  {{ parsedWords[activeWordIdx] || '' }}
                </span>
              </div>
              <div class="script-highlight-stream text-body-1" :class="currentEpisode.language === 'lo' ? 'font-lao' : ''">
                <span
                  v-for="(w, idx) in parsedWords"
                  :key="idx"
                  class="word-token mr-1"
                  :class="idx === activeWordIdx ? 'active-word font-weight-black' : 'inactive-word'"
                  @click="jumpToWord(idx)"
                >
                  {{ w }}
                </span>
              </div>
            </div>

            <!-- Video Ready View & Download / YouTube Publish -->
            <v-expand-transition>
              <div v-if="readyVideoUrl" class="video-ready-card pa-4 rounded-xl border mb-4 bg-gradient-ready">
                <div class="d-flex align-center justify-space-between mb-3">
                  <div class="d-flex align-center gap-2">
                    <v-icon color="success" size="small">mdi-check-circle</v-icon>
                    <span class="text-subtitle-2 font-weight-bold text-white">{{ currentEpisode.title }} is Ready!</span>
                  </div>
                  <v-chip size="x-small" color="success" variant="flat">HD 1080p</v-chip>
                </div>

                <div class="d-flex flex-wrap gap-2 mb-4">
                  <v-btn
                    color="success"
                    variant="flat"
                    rounded="lg"
                    size="large"
                    class="font-weight-bold text-none flex-grow-1"
                    prepend-icon="mdi-download"
                    @click="downloadVideo"
                  >
                    Download Episode Video (.webm / .mp4)
                  </v-btn>

                  <v-btn
                    color="white"
                    variant="outlined"
                    rounded="lg"
                    size="large"
                    class="font-weight-bold text-none"
                    prepend-icon="mdi-play-circle-outline"
                    @click="previewVideoModal = true"
                  >
                    Watch Preview
                  </v-btn>
                </div>

                <!-- Integrated YouTube Uploader Component -->
                <div v-if="serverVideoPath" class="mt-4 pt-4 border-t border-white-10">
                  <YoutubeUploader :videoPath="serverVideoPath" />
                </div>
              </div>
            </v-expand-transition>

            <!-- Export Buttons -->
            <div v-if="!readyVideoUrl" class="d-flex flex-column gap-2">
              <v-btn
                color="deep-purple-accent-2"
                size="x-large"
                rounded="xl"
                class="font-weight-black text-none shadow-lg py-6"
                prepend-icon="mdi-movie-open-play"
                :disabled="!canGenerateVideo"
                :loading="isRecordingVideo"
                @click="startVideoRecording"
              >
                {{ isRecordingVideo ? `Recording Episode... ${Math.round(recordingProgress)}%` : `Export Complete ${currentEpisode.title} Video for YouTube` }}
              </v-btn>

              <div class="d-flex align-center justify-center gap-3 text-caption text-grey-lighten-2 mt-1">
                <span><v-icon size="x-small" color="success">mdi-check</v-icon> Full Episode Compilation</span>
                <span>•</span>
                <span><v-icon size="x-small" color="success">mdi-check</v-icon> Word-by-Word Voice</span>
                <span>•</span>
                <span><v-icon size="x-small" color="success">mdi-check</v-icon> 1080p YouTube Ready</span>
              </div>
            </div>

          </v-card>
        </v-col>

      </v-row>

      <!-- Video Preview Dialog -->
      <v-dialog v-model="previewVideoModal" max-width="840">
        <v-card class="pa-4 bg-grey-darken-4 rounded-2xl border">
          <div class="d-flex align-center justify-space-between mb-3">
            <h3 class="text-h6 text-white font-weight-bold">{{ currentEpisode.title }} — Preview</h3>
            <v-btn icon="mdi-close" variant="text" size="small" @click="previewVideoModal = false"></v-btn>
          </div>
          <video v-if="readyVideoUrl" :src="readyVideoUrl" controls autoplay class="w-100 rounded-xl"></video>
        </v-card>
      </v-dialog>

    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue';

definePageMeta({
  layout: 'video'
});

const apiBase = 'http://localhost:3005';

// Studio Active Tab
const activeTab = ref('page_content');

// ================= EPISODE & SCENE SERIES STRUCTURE =================
const defaultEpisodes = [
  {
    id: 'ep_01',
    title: 'EP01 - ເລື່ອງ ສີວາ ຜູ້ມີນ້ຳໃຈງົດງາມ',
    language: 'lo',
    layoutStyle: 'storybook', // 'storybook', 'cinematic', 'shorts'
    scenes: [
      {
        id: 1,
        pageNumber: 1,
        headerTag: 'KOT WANG',
        dropCapLetter: 'ໃ',
        imageUrl: '',
        imageObj: null,
        text: 'ໃນດິນແດນອັນແສນງຽບສະຫງົບຢູ່ຕີນເຂົາໃຫຍ່, ມີເດັກໜຸ່ມຈິດໃຈດີຄົນໜຶ່ງຊື່ວ່າ "ສີວາ". ເຂົາເປັນຄົນມັກຊ່ວຍເຫຼືອຜູ້ອື່ນ ແລະ ຮັກສາຄວາມສະຫງົບຂອງໝູ່ບ້ານສະເໝີ.',
        audioUrl: null,
        duration: 0
      },
      {
        id: 2,
        pageNumber: 2,
        headerTag: 'KOT WANG • EP01',
        dropCapLetter: 'ທ',
        imageUrl: '',
        imageObj: null,
        text: 'ທຸກໆເຊົ້າ ສີວາ ຈະຕື່ນແຕ່ເຊົ້າຕູ່ ເກັບໝາກໄມ້ສົດໆຈາກສວນມາແບ່ງປັນໃຫ້ຜູ້ເຖົ້າຜູ້ແກ່. ທຸກຄົນໃນໝູ່ບ້ານຕ່າງຮັກແພງ ແລະ ຍ້ອງຍໍໃນນ້ຳໃຈອັນບໍລິສຸດຂອງລາວ.',
        audioUrl: null,
        duration: 0
      }
    ]
  },
  {
    id: 'ep_02',
    title: 'EP02 - Dab Neeg Luav Ntse Thiab Tus Tsov',
    language: 'hmn',
    layoutStyle: 'storybook',
    scenes: [
      {
        id: 1,
        pageNumber: 1,
        headerTag: 'LUS DAB NEEG • EP02',
        dropCapLetter: 'T',
        imageUrl: '',
        imageObj: null,
        text: 'Thaum ub, muaj ib tug tsov loj heev nyob hauv hav zoov ntsuab. Txhua txhua hnub, cov tsiaj hauv hav zoov ntshai tus tsov ntawd heev vim nws nyiam ntes tsiaj noj.',
        audioUrl: null,
        duration: 0
      },
      {
        id: 2,
        pageNumber: 2,
        headerTag: 'LUS DAB NEEG • EP02',
        dropCapLetter: 'M',
        imageUrl: '',
        imageObj: null,
        text: 'Muaj ib hnub, tus tsov ntes tau ib tug luav me me yuav noj. Tus luav txawm hais tias: Thov tsis txhob noj kuv, muaj ib tug tsov loj dua koj nyob tom lub qhov dej tob!',
        audioUrl: null,
        duration: 0
      }
    ]
  }
];

const allEpisodes = ref([...defaultEpisodes]);
const currentEpisodeIndex = ref(0);
const currentEpisode = computed(() => allEpisodes.value[currentEpisodeIndex.value] || allEpisodes.value[0]);

const activeSceneIndex = ref(0);
const currentScene = computed(() => {
  const ep = currentEpisode.value;
  if (!ep || !ep.scenes || ep.scenes.length === 0) {
    return { text: '', headerTag: '', imageUrl: '' };
  }
  return ep.scenes[activeSceneIndex.value] || ep.scenes[0];
});

// Scene management
const selectScene = (idx) => {
  stopAudio();
  activeSceneIndex.value = Math.max(0, Math.min(idx, currentEpisode.value.scenes.length - 1));
};

const addNewScene = () => {
  stopAudio();
  const nextNum = currentEpisode.value.scenes.length + 1;
  currentEpisode.value.scenes.push({
    id: Date.now(),
    pageNumber: nextNum,
    headerTag: currentScene.value.headerTag || 'STORY EPISODE',
    dropCapLetter: '',
    imageUrl: '',
    imageObj: null,
    text: '',
    audioUrl: null,
    duration: 0
  });
  activeSceneIndex.value = currentEpisode.value.scenes.length - 1;
};

const duplicateScene = (idx) => {
  const target = currentEpisode.value.scenes[idx];
  if (!target) return;
  const clone = {
    ...target,
    id: Date.now(),
    pageNumber: currentEpisode.value.scenes.length + 1
  };
  currentEpisode.value.scenes.splice(idx + 1, 0, clone);
  activeSceneIndex.value = idx + 1;
};

const deleteScene = (idx) => {
  if (currentEpisode.value.scenes.length <= 1) return;
  currentEpisode.value.scenes.splice(idx, 1);
  activeSceneIndex.value = Math.max(0, idx - 1);
};

const createNewEpisode = () => {
  const epNumber = allEpisodes.value.length + 1;
  const epId = `ep_${String(epNumber).padStart(2, '0')}`;
  const newEp = {
    id: epId,
    title: `EP${String(epNumber).padStart(2, '0')} - New Story Episode`,
    language: 'lo',
    layoutStyle: 'storybook',
    scenes: [
      {
        id: Date.now(),
        pageNumber: 1,
        headerTag: `EPISODE ${String(epNumber).padStart(2, '0')}`,
        dropCapLetter: '',
        imageUrl: '',
        imageObj: null,
        text: '',
        audioUrl: null,
        duration: 0
      }
    ]
  };
  allEpisodes.value.push(newEp);
  currentEpisodeIndex.value = allEpisodes.value.length - 1;
  activeSceneIndex.value = 0;
};

const switchEpisode = (idx) => {
  stopAudio();
  currentEpisodeIndex.value = idx;
  activeSceneIndex.value = 0;
};

const changeEpisodeLanguage = (lang) => {
  currentEpisode.value.language = lang;
  stopAudio();
};

// Preset samples
const loadSampleSivaStory = () => {
  currentEpisode.value.language = 'lo';
  currentScene.value.headerTag = 'KOT WANG';
  currentScene.value.dropCapLetter = 'ໃ';
  currentScene.value.text = 'ໃນດິນແດນອັນແສນງຽບສະຫງົບຢູ່ຕີນເຂົາໃຫຍ່, ມີເດັກໜຸ່ມຈິດໃຈດີຄົນໜຶ່ງຊື່ວ່າ "ສີວາ". ເຂົາເປັນຄົນມັກຊ່ວຍເຫຼືອຜູ້ອື່ນ ແລະ ຮັກສາຄວາມສະຫງົບຂອງໝູ່ບ້ານສະເໝີ.';
  stopAudio();
};

const loadSampleHmongStory = () => {
  currentEpisode.value.language = 'hmn';
  currentScene.value.headerTag = 'LUS DAB NEEG';
  currentScene.value.dropCapLetter = 'T';
  currentScene.value.text = 'Thaum ub, muaj ib tug tsov loj heev nyob hauv hav zoov ntsuab. Txhua txhua hnub, cov tsiaj hauv hav zoov ntshai tus tsov ntawd heev vim nws nyiam ntes tsiaj noj.';
  stopAudio();
};

// Image Upload Handlers for Current Scene
const onSceneImageSelect = (e) => {
  const file = e.target.files?.[0];
  if (file) handleImageFile(file);
};

const onSceneImageDrop = (e) => {
  const file = e.dataTransfer.files?.[0];
  if (file && file.type.startsWith('image/')) handleImageFile(file);
};

const handleImageFile = (file) => {
  const reader = new FileReader();
  reader.onload = (ev) => {
    const img = new Image();
    img.src = ev.target.result;
    img.onload = () => {
      currentScene.value.imageUrl = ev.target.result;
      currentScene.value.imageObj = img;
    };
  };
  reader.readAsDataURL(file);
};

const clearSceneImage = () => {
  currentScene.value.imageUrl = '';
  currentScene.value.imageObj = null;
};

// Voice, Timing & Styles
const readingMode = ref('continuous'); // 'continuous' or 'word'
const voiceSpeed = ref(1.0);
const wordPauseMs = ref(180);
const activeWordColor = ref('#d97706'); // Warm Amber
const paperTheme = ref('cream'); // 'cream', 'white', 'sand', 'dark'
const dropCapStyle = ref('calligraphic');
const bookFontSize = ref(36);
const kenBurnsEnabled = ref(true);
const waveformEnabled = ref(true);

// Background Music
const bgMusicEnabled = ref(false);
const selectedBgMusic = ref('acoustic');
const bgMusicVolume = ref(0.15);

// ElevenLabs & Voice Engine State
const selectedEngine = ref('elevenlabs'); // 'elevenlabs' | 'edge_tts'
const voiceGender = ref('male');
const selectedVoiceId = ref('JBFqnCBsd6RMkjVDRZzb'); // George - Storyteller
const availableVoices = ref([
  { title: 'George (Warm Storyteller)', value: 'JBFqnCBsd6RMkjVDRZzb' },
  { title: 'Sarah (Mature & Reassuring)', value: 'EXAVITQu4vr4xnSDxMaL' },
  { title: 'Charlie (Deep & Confident)', value: 'IKne3meq5aSn9XLyUdCD' },
  { title: 'Laura (Enthusiastic & Quirky)', value: 'FGY2WhTYpPnrIDTdsKH5' },
  { title: 'Roger (Casual & Resonant)', value: 'CwhRBWXzGAHq8TQ4Fs17' }
]);
const elevenUserStatus = ref({
  configured: true,
  tier: 'starter',
  character_count: 594,
  character_limit: 40000
});
const masterVolume = ref(1.0);

// Audio State
const isPlayingAudio = ref(false);
const isLoadingTTS = ref(false);
const audioDuration = ref(0);
const currentTime = ref(0);
const activeWordIdx = ref(0);
let audioElement = null;
let audioContext = null;
let analyserNode = null;
let audioSourceNode = null;

const audioProgress = computed(() => {
  if (!audioDuration.value) return 0;
  return Math.min(100, (currentTime.value / audioDuration.value) * 100);
});

const parsedWords = computed(() => {
  const txt = currentScene.value?.text || '';
  return txt.trim().split(/\s+/).filter(Boolean);
});

const totalEpisodeDuration = computed(() => {
  return currentEpisode.value.scenes.reduce((acc, s) => {
    const words = (s.text || '').trim().split(/\s+/).filter(Boolean).length;
    return acc + Math.max(3, words * 0.45);
  }, 0);
});

const countWords = (t) => {
  if (!t) return 0;
  return t.trim().split(/\s+/).filter(Boolean).length;
};

const formatTime = (secs) => {
  if (!secs || isNaN(secs)) return '00:00';
  const m = Math.floor(secs / 60);
  const s = Math.floor(secs % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
};

const onSceneTextChange = () => {
  stopAudio();
  if (currentScene.value) {
    currentScene.value.audioBlobUrl = null;
    currentScene.value.wordTimestamps = null;
  }
};

// Synthesize Audio with ElevenLabs & Word Timestamps
const prepareSceneTTSAudio = async () => {
  const text = currentScene.value?.text?.trim();
  if (!text) return null;
  isLoadingTTS.value = true;

  try {
    const res = await fetch(`${apiBase}/api/tts/synthesize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        lang: currentEpisode.value.language || 'lo',
        gender: voiceGender.value || 'male',
        voice_id: selectedVoiceId.value || 'JBFqnCBsd6RMkjVDRZzb',
        engine: selectedEngine.value || 'elevenlabs'
      })
    });

    if (!res.ok) {
      throw new Error(`TTS synthesis request failed: ${res.status}`);
    }

    const data = await res.json();
    currentScene.value.wordTimestamps = data.word_timestamps || [];
    currentScene.value.duration = data.duration || 5.0;
    audioDuration.value = currentScene.value.duration;

    // Convert data base64 to same-origin Blob URL
    const audioRes = await fetch(data.audio_base64);
    const audioBlob = await audioRes.blob();
    const blobUrl = URL.createObjectURL(audioBlob);
    currentScene.value.audioBlobUrl = blobUrl;

    if (!audioElement) {
      audioElement = new Audio();
      audioElement.crossOrigin = 'anonymous';
    }
    audioElement.src = blobUrl;
    audioElement.volume = masterVolume.value;
    audioElement.playbackRate = voiceSpeed.value;

    await new Promise((resolve) => {
      audioElement.onloadedmetadata = () => resolve();
      audioElement.onerror = () => resolve();
    });

    setupWebAudio();
    isLoadingTTS.value = false;
    return audioElement;
  } catch (err) {
    console.error('TTS synthesis error:', err);
    isLoadingTTS.value = false;
    return null;
  }
};

const setupWebAudio = () => {
  if (typeof window === 'undefined') return;
  if (!audioContext) {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    audioContext = new AudioCtx();
  }
  if (audioContext.state === 'suspended') {
    audioContext.resume();
  }

  if (audioElement && !audioSourceNode) {
    try {
      audioSourceNode = audioContext.createMediaElementSource(audioElement);
      analyserNode = audioContext.createAnalyser();
      analyserNode.fftSize = 128;
      audioSourceNode.connect(analyserNode);
      analyserNode.connect(audioContext.destination);
    } catch (e) {
      console.warn('Audio node already connected:', e);
    }
  }
};

const toggleAudioPreview = async () => {
  // Synchronously unlock AudioContext on user gesture
  if (typeof window !== 'undefined') {
    if (!audioContext) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      audioContext = new AudioCtx();
    }
    if (audioContext.state === 'suspended') {
      await audioContext.resume();
    }
  }

  if (isPlayingAudio.value) {
    pauseAudio();
  } else {
    await playAudio();
  }
};

const playAudio = async () => {
  if (!currentScene.value?.audioBlobUrl) {
    const ready = await prepareSceneTTSAudio();
    if (!ready) return;
  } else if (!audioElement || audioElement.src !== currentScene.value.audioBlobUrl) {
    if (!audioElement) {
      audioElement = new Audio();
      audioElement.crossOrigin = 'anonymous';
    }
    audioElement.src = currentScene.value.audioBlobUrl;
  }

  if (audioContext && audioContext.state === 'suspended') {
    await audioContext.resume();
  }

  setupWebAudio();

  audioElement.volume = masterVolume.value;
  audioElement.playbackRate = voiceSpeed.value;

  try {
    await audioElement.play();
    isPlayingAudio.value = true;
  } catch (err) {
    console.warn('Audio play error, attempting direct play:', err);
    try {
      await audioElement.play();
      isPlayingAudio.value = true;
    } catch (e) {
      console.error('Audio play failed:', e);
    }
  }

  audioElement.ontimeupdate = () => {
    const curr = audioElement.currentTime;
    currentTime.value = curr;
    const timestamps = currentScene.value?.wordTimestamps;
    if (timestamps && timestamps.length > 0) {
      const idx = timestamps.findIndex(w => curr >= w.start && curr <= w.end);
      if (idx !== -1) {
        activeWordIdx.value = idx;
      } else {
        const prevIdx = timestamps.findLastIndex(w => curr >= w.start);
        if (prevIdx !== -1) activeWordIdx.value = prevIdx;
      }
    } else {
      updateActiveWord(curr, audioDuration.value);
    }
  };

  audioElement.onended = () => {
    isPlayingAudio.value = false;
    currentTime.value = 0;
    activeWordIdx.value = 0;
  };
};

const pauseAudio = () => {
  if (audioElement) {
    audioElement.pause();
    isPlayingAudio.value = false;
  }
};

const stopAudio = () => {
  if (audioElement) {
    audioElement.pause();
    audioElement.currentTime = 0;
    isPlayingAudio.value = false;
    currentTime.value = 0;
    activeWordIdx.value = 0;
  }
};

const seekAudio = (percent) => {
  if (audioElement && audioDuration.value) {
    const target = (percent / 100) * audioDuration.value;
    audioElement.currentTime = target;
    currentTime.value = target;
    updateActiveWord(target, audioDuration.value);
  }
};

const updateActiveWord = (curr, total) => {
  if (!total || parsedWords.value.length === 0) return;
  const progressRatio = Math.max(0, Math.min(1, curr / total));
  const wordIdx = Math.floor(progressRatio * parsedWords.value.length);
  activeWordIdx.value = Math.min(parsedWords.value.length - 1, Math.max(0, wordIdx));
};

const jumpToWord = (idx) => {
  if (!audioDuration.value || parsedWords.value.length === 0) return;
  const timestamps = currentScene.value?.wordTimestamps;
  if (timestamps && timestamps[idx]) {
    const targetTime = timestamps[idx].start;
    if (audioElement) {
      audioElement.currentTime = targetTime;
      currentTime.value = targetTime;
    }
  } else {
    const ratio = idx / parsedWords.value.length;
    const targetTime = ratio * audioDuration.value;
    if (audioElement) {
      audioElement.currentTime = targetTime;
      currentTime.value = targetTime;
    }
  }
  activeWordIdx.value = idx;
};

// ================= LIVE STORYBOOK CANVAS RENDERING ENGINE =================
const videoCanvas = ref(null);
let animationFrameId = null;
let canvasStartTime = 0;

const startCanvasLoop = () => {
  if (!videoCanvas.value) return;
  const canvas = videoCanvas.value;
  const ctx = canvas.getContext('2d');

  // Set internal resolution
  if (currentEpisode.value.layoutStyle === 'shorts') {
    canvas.width = 1080;
    canvas.height = 1920;
  } else {
    canvas.width = 1920;
    canvas.height = 1080;
  }

  const render = (timestamp) => {
    if (!canvasStartTime) canvasStartTime = timestamp;
    const elapsed = (timestamp - canvasStartTime) / 1000;

    if (currentEpisode.value.layoutStyle === 'storybook') {
      renderStorybookSpread(ctx, canvas, elapsed);
    } else if (currentEpisode.value.layoutStyle === 'shorts') {
      renderShortsLayout(ctx, canvas, elapsed);
    } else {
      renderCinematicLayout(ctx, canvas, elapsed);
    }

    animationFrameId = requestAnimationFrame(render);
  };

  animationFrameId = requestAnimationFrame(render);
};

// Renders Storybook Spread (Matching user's exact uploaded image!)
const renderStorybookSpread = (ctx, canvas, elapsed) => {
  const w = canvas.width;
  const h = canvas.height;
  const halfW = w / 2;

  // Background Paper Color for Right Page
  let paperBg = '#FAF8F5';
  let textColor = '#262626';
  if (paperTheme.value === 'white') {
    paperBg = '#FFFFFF';
    textColor = '#1E1E1E';
  } else if (paperTheme.value === 'sand') {
    paperBg = '#F4EFE6';
    textColor = '#332920';
  } else if (paperTheme.value === 'dark') {
    paperBg = '#181824';
    textColor = '#E2E8F0';
  }

  ctx.fillStyle = paperBg;
  ctx.fillRect(0, 0, w, h);

  // LEFT HALF: Illustration Image
  const imgObj = currentScene.value.imageObj;
  if (imgObj && imgObj.complete) {
    ctx.save();
    ctx.beginPath();
    ctx.rect(0, 0, halfW, h);
    ctx.clip();

    if (kenBurnsEnabled.value) {
      const zoom = 1.0 + Math.sin(elapsed * 0.25) * 0.05;
      const panX = Math.cos(elapsed * 0.15) * 20;
      const panY = Math.sin(elapsed * 0.15) * 15;
      ctx.translate(halfW / 2 + panX, h / 2 + panY);
      ctx.scale(zoom, zoom);
      ctx.drawImage(imgObj, -halfW / 2, -h / 2, halfW, h);
    } else {
      ctx.drawImage(imgObj, 0, 0, halfW, h);
    }
    ctx.restore();
  } else {
    // Elegant left placeholder gradient
    const leftGrad = ctx.createLinearGradient(0, 0, halfW, h);
    leftGrad.addColorStop(0, '#312E81');
    leftGrad.addColorStop(1, '#0F172A');
    ctx.fillStyle = leftGrad;
    ctx.fillRect(0, 0, halfW, h);

    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.font = 'bold 32px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('🎨 Upload Illustration / ຮູບພາບປະກອບ', halfW / 2, h / 2 - 20);
    ctx.font = '500 20px Outfit, sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.fillText(`Page ${activeSceneIndex.value + 1} Artwork`, halfW / 2, h / 2 + 25);
  }

  // CENTER BOOK SPINE CREASE SHADOW
  const spineGrad = ctx.createLinearGradient(halfW - 35, 0, halfW + 35, 0);
  spineGrad.addColorStop(0, 'rgba(0,0,0,0)');
  spineGrad.addColorStop(0.45, 'rgba(0,0,0,0.25)');
  spineGrad.addColorStop(0.5, 'rgba(0,0,0,0.4)');
  spineGrad.addColorStop(0.55, 'rgba(0,0,0,0.25)');
  spineGrad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = spineGrad;
  ctx.fillRect(halfW - 35, 0, 70, h);

  // RIGHT HALF: STORYBOOK TEXT
  const textX = halfW + 100;
  const textW = halfW - 200;

  // Header Title (e.g. KOT WANG)
  ctx.save();
  ctx.font = '600 22px Outfit, sans-serif';
  ctx.fillStyle = '#64748B';
  ctx.textAlign = 'right';
  ctx.fillText(currentScene.value.headerTag || 'KOT WANG', w - 100, 80);

  // Drop Cap Letter
  const fullText = (currentScene.value.text || '').trim();
  let firstChar = currentScene.value.dropCapLetter || (fullText ? fullText[0] : 'ໃ');
  let remainingText = fullText;
  if (fullText && fullText.startsWith(firstChar)) {
    remainingText = fullText.slice(firstChar.length).trim();
  }

  // Draw Drop Cap
  const dropCapX = textX;
  const dropCapY = 280;
  ctx.font = 'italic 120px "Noto Sans Lao", Georgia, serif';
  ctx.fillStyle = textColor;
  ctx.textAlign = 'left';
  ctx.fillText(firstChar, dropCapX, dropCapY);

  // Draw Story Paragraph with Word-by-Word Active Highlighting
  const fontFam = currentEpisode.value.language === 'lo' ? 'Noto Sans Lao' : (currentEpisode.value.language === 'th' ? 'Noto Sans Thai' : 'Georgia, serif');
  const fontSize = bookFontSize.value;
  const lineHeight = fontSize * 1.85;

  ctx.font = `500 ${fontSize}px ${fontFam}`;
  ctx.textAlign = 'left';

  const words = parsedWords.value;
  let curX = textX + 110; // offset after drop cap
  let curY = 220;
  let lineIdx = 0;

  words.forEach((word, wIdx) => {
    // If we passed first two lines, wrap across full width
    const currentMaxW = lineIdx < 2 ? textW - 120 : textW;
    const startLeftX = lineIdx < 2 ? textX + 110 : textX;

    const wordMeasure = ctx.measureText(word + ' ');
    if (curX + wordMeasure.width > textX + textW) {
      lineIdx++;
      curX = lineIdx < 2 ? textX + 110 : textX;
      curY += lineHeight;
    }

    const isActive = wIdx === activeWordIdx.value;

    if (isActive) {
      // Golden / selected word highlight pill
      ctx.save();
      ctx.fillStyle = activeWordColor.value;
      ctx.font = `bold ${fontSize + 2}px ${fontFam}`;
      ctx.fillText(word, curX, curY);
      ctx.restore();
    } else {
      ctx.fillStyle = textColor;
      ctx.font = `500 ${fontSize}px ${fontFam}`;
      ctx.fillText(word, curX, curY);
    }

    curX += wordMeasure.width;
  });

  // Page Number Footer (e.g., "1" at bottom right)
  ctx.font = '500 24px Georgia, serif';
  ctx.fillStyle = '#64748B';
  ctx.textAlign = 'right';
  ctx.fillText(String(activeSceneIndex.value + 1), w - 100, h - 80);

  // Draw Waveform if enabled
  if (waveformEnabled.value) {
    drawMiniWaveform(ctx, halfW + 100, h - 110, textW - 80, 40);
  }

  ctx.restore();
};

const drawMiniWaveform = (ctx, x, y, width, height) => {
  let freqData = new Uint8Array(24);
  if (analyserNode && isPlayingAudio.value) {
    freqData = new Uint8Array(analyserNode.frequencyBinCount);
    analyserNode.getByteFrequencyData(freqData);
  } else {
    for (let i = 0; i < 24; i++) {
      freqData[i] = Math.sin(Date.now() * 0.003 + i * 0.4) * 12 + 12;
    }
  }

  const numBars = 24;
  const barW = width / numBars - 4;
  ctx.save();
  for (let i = 0; i < numBars; i++) {
    const val = (freqData[i] || 0) / 255;
    const bHeight = Math.max(4, val * height);
    const barX = x + i * (barW + 4);
    ctx.fillStyle = activeWordColor.value;
    ctx.fillRect(barX, y + height - bHeight, barW, bHeight);
  }
  ctx.restore();
};

// Cinematic Fullscreen Podcast Layout
const renderCinematicLayout = (ctx, canvas, elapsed) => {
  const w = canvas.width;
  const h = canvas.height;

  // Draw background image
  const imgObj = currentScene.value.imageObj;
  if (imgObj && imgObj.complete) {
    ctx.drawImage(imgObj, 0, 0, w, h);
  } else {
    const grad = ctx.createLinearGradient(0, 0, w, h);
    grad.addColorStop(0, '#2e0854');
    grad.addColorStop(1, '#0f172a');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);
  }

  // Dark overlay
  ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
  ctx.fillRect(0, 0, w, h);

  // Subtitles
  drawSubtitles(ctx, canvas);
};

// Shorts 9:16 Layout
const renderShortsLayout = (ctx, canvas, elapsed) => {
  const w = canvas.width;
  const h = canvas.height;

  // Top half: image
  const imgObj = currentScene.value.imageObj;
  if (imgObj && imgObj.complete) {
    ctx.drawImage(imgObj, 0, 0, w, h * 0.55);
  } else {
    ctx.fillStyle = '#1e1b4b';
    ctx.fillRect(0, 0, w, h * 0.55);
  }

  // Bottom half: parchment book text
  ctx.fillStyle = '#FAF8F5';
  ctx.fillRect(0, h * 0.55, w, h * 0.45);

  drawSubtitles(ctx, canvas);
};

const drawSubtitles = (ctx, canvas) => {
  const w = canvas.width;
  const h = canvas.height;
  const words = parsedWords.value;
  if (!words.length) return;

  const windowSize = 8;
  const start = Math.max(0, Math.floor(activeWordIdx.value / windowSize) * windowSize);
  const currentChunk = words.slice(start, start + windowSize);

  const posY = h * 0.82;
  const fontFam = currentEpisode.value.language === 'lo' ? 'Noto Sans Lao' : (currentEpisode.value.language === 'th' ? 'Noto Sans Thai' : 'Outfit, sans-serif');
  const fontSize = 42;

  ctx.save();
  ctx.font = `bold ${fontSize}px ${fontFam}`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  const fullSentence = currentChunk.join(' ');
  const metrics = ctx.measureText(fullSentence);

  // Draw pill
  ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
  ctx.beginPath();
  ctx.roundRect((w - metrics.width) / 2 - 30, posY - fontSize / 2 - 16, metrics.width + 60, fontSize + 32, 16);
  ctx.fill();

  let cursorX = (w - metrics.width) / 2;
  currentChunk.forEach((word, i) => {
    const globalIdx = start + i;
    const isCurrent = globalIdx === activeWordIdx.value;
    const wordWidth = ctx.measureText(word + ' ').width;

    if (isCurrent) {
      ctx.fillStyle = '#FACC15';
      ctx.shadowColor = '#FACC15';
      ctx.shadowBlur = 15;
    } else {
      ctx.fillStyle = '#FFFFFF';
      ctx.shadowBlur = 0;
    }

    ctx.textAlign = 'left';
    ctx.fillText(word, cursorX, posY);
    cursorX += wordWidth;
  });
  ctx.restore();
};

// ================= MULTI-PAGE EPISODE COMPILATION & VIDEO EXPORT =================
const isRecordingVideo = ref(false);
const recordingProgress = ref(0);
const readyVideoUrl = ref(null);
const serverVideoPath = ref(null);
const previewVideoModal = ref(false);
let mediaRecorder = null;
let recordedChunks = [];

const canGenerateVideo = computed(() => {
  return currentEpisode.value?.scenes?.some(s => s.text?.trim().length > 0) && !isRecordingVideo.value;
});

const startVideoRecording = async () => {
  if (isRecordingVideo.value) return;
  readyVideoUrl.value = null;
  serverVideoPath.value = null;

  isRecordingVideo.value = true;
  recordingProgress.value = 0;

  try {
    const canvas = videoCanvas.value;
    const canvasStream = canvas.captureStream(30);

    if (!audioContext) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      audioContext = new AudioCtx();
    }
    await audioContext.resume();

    const dest = audioContext.createMediaStreamDestination();
    if (audioSourceNode) {
      audioSourceNode.connect(dest);
    }

    const combinedStream = new MediaStream([
      ...canvasStream.getVideoTracks(),
      ...dest.stream.getAudioTracks()
    ]);

    recordedChunks = [];
    let mimeType = 'video/webm;codecs=vp9';
    if (!MediaRecorder.isTypeSupported(mimeType)) mimeType = 'video/webm';

    mediaRecorder = new MediaRecorder(combinedStream, {
      mimeType,
      videoBitsPerSecond: 4500000
    });

    mediaRecorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      readyVideoUrl.value = URL.createObjectURL(blob);
      isRecordingVideo.value = false;
      recordingProgress.value = 100;

      // Save to server to get serverVideoPath for YoutubeUploader
      await uploadEpisodeToServer(blob);
    };

    mediaRecorder.start(100);

    // Sequentially play through each page in the episode
    const scenes = currentEpisode.value.scenes;
    for (let i = 0; i < scenes.length; i++) {
      activeSceneIndex.value = i;
      recordingProgress.value = Math.round((i / scenes.length) * 100);

      const ready = await prepareSceneTTSAudio();
      if (ready) {
        await playAudio();
        // Wait for page audio to complete
        await new Promise((res) => {
          const checkEnd = setInterval(() => {
            if (!isPlayingAudio.value) {
              clearInterval(checkEnd);
              res();
            }
          }, 300);
        });
      }
      // Small pause between pages (600ms page flip pause)
      await new Promise(r => setTimeout(r, 600));
    }

    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }

  } catch (err) {
    console.error('Episode recording error:', err);
    alert('Recording error: ' + err.message);
    isRecordingVideo.value = false;
  }
};

const uploadEpisodeToServer = async (blob) => {
  try {
    const formData = new FormData();
    formData.append('video', blob, `${currentEpisode.value.title.replace(/[^a-zA-Z0-9]/g, '_')}_${Date.now()}.webm`);
    formData.append('title', currentEpisode.value.title);

    const res = await fetch(`${apiBase}/api/tts/save-video`, {
      method: 'POST',
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      serverVideoPath.value = data.videoPath;
    }
  } catch (e) {
    console.warn('Could not save video to server:', e);
  }
};

const downloadVideo = () => {
  if (!readyVideoUrl.value) return;
  const a = document.createElement('a');
  a.href = readyVideoUrl.value;
  a.download = `${currentEpisode.value.title.replace(/[^a-zA-Z0-9]/g, '_')}.webm`;
  a.click();
};

const resetStudio = () => {
  stopAudio();
  allEpisodes.value = [...defaultEpisodes];
  currentEpisodeIndex.value = 0;
  activeSceneIndex.value = 0;
  readyVideoUrl.value = null;
  serverVideoPath.value = null;
};

// Lifecycle
onMounted(async () => {
  // Load ElevenLabs voices and live quota
  try {
    const res = await fetch(`${apiBase}/api/tts/voices`);
    if (res.ok) {
      const data = await res.json();
      if (data.voices && data.voices.length > 0) {
        availableVoices.value = data.voices.map(v => ({
          title: `${v.name} (${v.category || 'voice'})`,
          value: v.voice_id
        }));
      }
    }
  } catch (e) {
    console.warn('Failed to load ElevenLabs voices:', e);
  }

  try {
    const statRes = await fetch(`${apiBase}/api/tts/user-status`);
    if (statRes.ok) {
      elevenUserStatus.value = await statRes.json();
    }
  } catch (e) {
    console.warn('Failed to load ElevenLabs status:', e);
  }

  nextTick(() => {
    startCanvasLoop();
  });
});

onUnmounted(() => {
  stopAudio();
  if (animationFrameId) cancelAnimationFrame(animationFrameId);
});

// Watch Layout Style to update canvas dimensions
watch(() => currentEpisode.value?.layoutStyle, (val) => {
  if (videoCanvas.value) {
    const canvas = videoCanvas.value;
    if (val === 'shorts') {
      canvas.width = 1080;
      canvas.height = 1920;
    } else {
      canvas.width = 1920;
      canvas.height = 1080;
    }
  }
});
</script>

<style scoped>
.podcast-studio-page {
  min-height: 100vh;
  color: #f8fafc;
}

.studio-header-card {
  background: linear-gradient(135deg, rgba(88, 28, 135, 0.85), rgba(15, 23, 42, 0.9)) !important;
  backdrop-filter: blur(24px);
  border-color: rgba(168, 85, 247, 0.35) !important;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}
.orb-1 {
  width: 320px;
  height: 320px;
  background: rgba(168, 85, 247, 0.3);
  top: -100px;
  left: -50px;
}
.orb-2 {
  width: 280px;
  height: 280px;
  background: rgba(236, 72, 153, 0.25);
  bottom: -100px;
  right: -50px;
}

.scene-navigator-bar {
  border-color: rgba(255, 255, 255, 0.08) !important;
}

.scene-card {
  width: 140px;
  min-width: 140px;
  padding: 8px;
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(255, 255, 255, 0.1) !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.scene-card:hover {
  transform: translateY(-2px);
  border-color: rgba(168, 85, 247, 0.4) !important;
}
.scene-card-active {
  background: rgba(88, 28, 135, 0.45) !important;
  border: 2px solid #a855f7 !important;
  box-shadow: 0 4px 16px rgba(168, 85, 247, 0.3);
}

.scene-thumb-wrapper {
  width: 100%;
  height: 70px;
  background: #000;
}
.scene-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.scene-thumb-placeholder {
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
}

.scene-number-chip {
  color: #e2e8f0;
  margin-bottom: 4px;
}

.scene-del-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 20px;
  height: 20px;
}

.add-scene-ghost {
  width: 120px;
  min-width: 120px;
  height: 105px;
  border: 2px dashed rgba(168, 85, 247, 0.4);
  background: rgba(15, 23, 42, 0.3);
  transition: all 0.2s ease;
}
.add-scene-ghost:hover {
  border-color: #a855f7;
  background: rgba(88, 28, 135, 0.2);
}

.studio-controls-card, .studio-preview-card {
  background: rgba(30, 41, 59, 0.7) !important;
  backdrop-filter: blur(16px);
  border-color: rgba(255, 255, 255, 0.08) !important;
}

.border-purple-accent {
  border: 2px solid #a855f7 !important;
}

.font-script-area :deep(textarea) {
  font-family: 'Outfit', 'Noto Sans Lao', 'Noto Sans Thai', sans-serif;
  font-size: 1.05rem;
  line-height: 1.6;
}

.font-lao {
  font-family: 'Noto Sans Lao', sans-serif;
}

.media-drop-zone {
  border: 2px dashed rgba(168, 85, 247, 0.4);
  background: rgba(15, 23, 42, 0.4);
  transition: all 0.2s ease;
}
.media-drop-zone:hover {
  border-color: #a855f7;
  background: rgba(15, 23, 42, 0.7);
}

.uploaded-img-preview {
  width: 90px;
  height: 90px;
  object-fit: cover;
}

.canvas-wrapper {
  position: relative;
  background: #000;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
}
.ratio-16-9 {
  aspect-ratio: 16 / 9;
}
.ratio-9-16 {
  aspect-ratio: 9 / 16;
  max-height: 520px;
}

.canvas-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  z-index: 20;
}

.recording-badge {
  background: rgba(239, 68, 68, 0.9);
  backdrop-filter: blur(8px);
  z-index: 10;
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.6);
}

.recording-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #fff;
  animation: pulse-dot 1s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(0.8); }
}

.current-word-box {
  max-height: 130px;
  overflow-y: auto;
}

.script-highlight-stream {
  line-height: 1.8;
}

.word-token {
  cursor: pointer;
  padding: 2px 4px;
  border-radius: 4px;
  transition: all 0.15s ease;
}

.word-token:hover {
  background: rgba(255, 255, 255, 0.15);
}

.active-word {
  background: rgba(245, 158, 11, 0.25);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.5);
}

.inactive-word {
  color: #94a3b8;
}

.video-ready-card {
  background: linear-gradient(135deg, rgba(22, 101, 52, 0.7), rgba(15, 23, 42, 0.85)) !important;
  border-color: rgba(34, 197, 94, 0.4) !important;
}

.border-t {
  border-top: 1px solid;
}
.border-white-10 {
  border-color: rgba(255, 255, 255, 0.1);
}

.sticky-top {
  position: sticky;
  top: 80px;
}

.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.space-y-2 > * + * { margin-top: 8px; }
.space-y-3 > * + * { margin-top: 12px; }
.space-y-4 > * + * { margin-top: 16px; }
</style>
