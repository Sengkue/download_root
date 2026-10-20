<template>
  <div class="studio-root text-white">
    <!-- Top Studio Header -->
    <header class="studio-header d-flex align-center justify-space-between px-6 py-3">
      <div class="d-flex align-center gap-3">
        <div class="studio-badge">
          <v-icon icon="mdi-music-box-multiple" color="white" size="20"></v-icon>
        </div>
        <div>
          <div class="d-flex align-center gap-2">
            <h1 class="text-subtitle-1 font-weight-black gradient-title mb-0">Music Video Studio</h1>
            <v-chip size="x-small" color="purple-accent-3" variant="flat" class="font-weight-bold">PRO LIVE</v-chip>
          </div>
          <p class="text-caption text-grey-lighten-1 mb-0 d-flex align-center gap-2">
            <span>{{ videoFiles.length }} Visual{{ videoFiles.length !== 1 ? 's' : '' }}</span>
            <span class="dot">•</span>
            <span>{{ audioFiles.length }} Track{{ audioFiles.length !== 1 ? 's' : '' }} ({{ formattedTotalDuration }})</span>
            <span class="dot">•</span>
            <span class="text-purple-lighten-3">{{ activeResolutionLabel }}</span>
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-3">
        <!-- In Compilation View: Clean Navigation Back to Studio -->
        <v-btn
          v-if="videoUrl"
          variant="tonal"
          color="purple-accent-2"
          size="small"
          prepend-icon="mdi-arrow-left"
          class="text-none rounded-pill font-weight-bold"
          @click="reCustomizeProject('media')"
        >
          Back to Studio
        </v-btn>

        <!-- In Studio Editor View: Reset & Export Compilation -->
        <v-btn
          v-if="!videoUrl"
          variant="tonal"
          color="grey-lighten-2"
          size="small"
          prepend-icon="mdi-refresh"
          class="text-none rounded-pill"
          @click="openNewProjectConfirm"
          title="Reset project"
        >
          Reset
        </v-btn>

        <v-btn
          v-if="!videoUrl"
          color="primary"
          size="default"
          class="export-btn px-6 text-none font-weight-bold rounded-pill"
          :disabled="!canGenerate || isGenerating"
          :loading="isGenerating"
          @click="generateVideo"
          elevation="4"
        >
          <template v-slot:prepend>
            <v-icon icon="mdi-auto-fix" class="mr-1"></v-icon>
          </template>
          Export Compilation
        </v-btn>
      </div>
    </header>

    <!-- Main Workspace (Editor Studio or Export Result) -->
    <div class="studio-body">
      <!-- 1. Active Editor View -->
      <div v-if="!videoUrl" class="editor-grid">
        <!-- LEFT: Inspector & Settings Panel with Smooth Scrolling and Sticky Header -->
        <aside class="inspector-panel glass-panel" ref="inspectorPanelRef" @scroll="onInspectorScroll">
          <!-- Sticky Segmented Navigation Header -->
          <div class="inspector-sticky-header">
            <v-tabs
              v-model="activeTab"
              density="compact"
              color="purple-accent-2"
              align-tabs="center"
              class="inspector-tabs"
            >
              <v-tab value="media" class="text-none font-weight-bold">
                <v-icon start icon="mdi-folder-music-outline" size="18"></v-icon>
                Media
              </v-tab>
              <v-tab value="timeline" class="text-none font-weight-bold">
                <v-icon start icon="mdi-chart-timeline-variant-shimmer" size="18"></v-icon>
                Timeline & Cut
              </v-tab>
              <v-tab value="overlays" class="text-none font-weight-bold">
                <v-icon start icon="mdi-layers-outline" size="18"></v-icon>
                Overlays & Style
              </v-tab>
              <v-tab value="settings" class="text-none font-weight-bold">
                <v-icon start icon="mdi-cog-outline" size="18"></v-icon>
                Format
              </v-tab>
            </v-tabs>

            <!-- Quick Jump / Sub Navigation (Visible when on Media tab) -->
            <div v-if="activeTab === 'media'" class="media-quick-nav d-flex align-center justify-space-between mt-2 pt-2 border-top-subtle">
              <div class="d-flex align-center gap-1">
                <v-chip
                  size="x-small"
                  :color="isNearAudioSection ? 'grey-darken-3' : 'purple-accent-2'"
                  :variant="isNearAudioSection ? 'tonal' : 'flat'"
                  class="cursor-pointer font-weight-bold"
                  @click="scrollToMediaSection('visuals')"
                >
                  <v-icon start icon="mdi-image-multiple" size="13"></v-icon>
                  Visuals ({{ videoFiles.length }})
                </v-chip>
                <v-chip
                  size="x-small"
                  :color="isNearAudioSection ? 'purple-accent-2' : 'grey-darken-3'"
                  :variant="isNearAudioSection ? 'flat' : 'tonal'"
                  class="cursor-pointer font-weight-bold"
                  @click="scrollToMediaSection('audio')"
                >
                  <v-icon start icon="mdi-playlist-music" size="13"></v-icon>
                  Audio Playlist ({{ audioFiles.length }})
                </v-chip>
              </div>

              <!-- Instant Scroll Up / Down button -->
              <v-btn
                size="x-small"
                variant="tonal"
                color="purple-accent-2"
                class="text-none font-weight-bold px-2"
                @click="toggleMediaScroll"
                :title="isNearAudioSection ? 'Scroll Up to Visuals' : 'Scroll Down to Audio Playlist'"
              >
                <v-icon :icon="isNearAudioSection ? 'mdi-arrow-up' : 'mdi-arrow-down'" size="13" class="mr-1"></v-icon>
                {{ isNearAudioSection ? 'Top ↑' : 'Audio ↓' }}
              </v-btn>
            </div>
          </div>

          <v-window v-model="activeTab" class="inspector-window">
            <!-- TAB 1: MEDIA TRACKS -->
            <v-window-item value="media" class="tab-content">
              <!-- Visuals Section -->
              <div class="section-card mb-4" id="visuals-section">
                <div class="d-flex align-center justify-space-between mb-2">
                  <span
                    class="text-subtitle-2 font-weight-bold d-flex align-center cursor-pointer"
                    @click="isVisualsCollapsed = !isVisualsCollapsed"
                    title="Click to collapse / expand Background Visuals"
                  >
                    <v-icon icon="mdi-image-multiple" color="purple-lighten-2" class="mr-2" size="18"></v-icon>
                    Background Visuals
                    <v-badge v-if="videoFiles.length > 0" :content="videoFiles.length" color="purple" inline class="ml-2"></v-badge>
                  </span>
                  <div class="d-flex align-center gap-1">
                    <v-btn
                      v-if="videoFiles.length > 0"
                      size="x-small"
                      variant="text"
                      color="error"
                      @click="clearVideo"
                    >
                      Clear All
                    </v-btn>
                    <v-btn
                      icon
                      size="x-small"
                      variant="text"
                      color="grey-lighten-1"
                      @click="isVisualsCollapsed = !isVisualsCollapsed"
                      :title="isVisualsCollapsed ? 'Expand Background Visuals' : 'Collapse Background Visuals'"
                    >
                      <v-icon :icon="isVisualsCollapsed ? 'mdi-chevron-down' : 'mdi-chevron-up'" size="18"></v-icon>
                    </v-btn>
                  </div>
                </div>

                <v-expand-transition>
                  <div v-show="!isVisualsCollapsed">

                <!-- Visuals Dropzone -->
                <div
                  class="dropzone-compact"
                  :class="{ 'drag-over': isDraggingVideo, 'has-files': videoFiles.length > 0 }"
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
                  <v-icon icon="mdi-cloud-upload-outline" size="24" color="purple-lighten-3" class="mb-1"></v-icon>
                  <div class="text-caption font-weight-medium">Drag & Drop Backgrounds or Click</div>
                  <div class="text-caption text-grey-lighten-1" style="font-size: 11px;">MP4, WebM, JPG, PNG</div>
                </div>

                <!-- Visuals List & Reorder -->
                <div v-if="videoFiles.length > 0" class="asset-list mt-3">
                  <div
                    v-for="(file, idx) in videoFiles"
                    :key="'bg-' + idx"
                    class="asset-card d-flex flex-column"
                  >
                    <div class="d-flex align-center justify-space-between w-100">
                      <div class="d-flex align-center overflow-hidden mr-2">
                        <div class="index-badge mr-2">{{ idx + 1 }}</div>
                        <v-icon
                          :icon="file.type.startsWith('image/') ? 'mdi-image' : 'mdi-video'"
                          size="18"
                          color="grey-lighten-2"
                          class="mr-2"
                        ></v-icon>
                        <div class="d-flex flex-column overflow-hidden">
                          <span class="text-caption text-truncate">{{ file.name }}</span>
                          <span
                            v-if="videoTrims[idx]?.start > 0 || videoTrims[idx]?.end > 0"
                            class="text-purple-accent-2"
                            style="font-size: 10px;"
                          >
                            ✂️ Cut Start: {{ videoTrims[idx].start }}s
                          </span>
                        </div>
                      </div>
                      <div class="d-flex align-center gap-1">
                        <v-btn
                          v-if="!file.type.startsWith('image/')"
                          icon="mdi-content-cut"
                          size="x-small"
                          :color="(videoTrims[idx]?.start > 0 || videoTrims[idx]?.end > 0) ? 'purple-accent-2' : 'grey-lighten-1'"
                          :variant="(videoTrims[idx]?.start > 0 || videoTrims[idx]?.end > 0 || videoTrims[idx]?.expanded) ? 'tonal' : 'text'"
                          @click.stop="toggleVideoTrim(idx)"
                          title="Trim video start/end"
                        ></v-btn>
                        <v-btn
                          icon="mdi-chevron-up"
                          size="x-small"
                          variant="text"
                          :disabled="idx === 0"
                          @click.stop="moveVideoUp(idx)"
                        ></v-btn>
                        <v-btn
                          icon="mdi-chevron-down"
                          size="x-small"
                          variant="text"
                          :disabled="idx === videoFiles.length - 1"
                          @click.stop="moveVideoDown(idx)"
                        ></v-btn>
                        <v-btn
                          icon="mdi-delete-outline"
                          size="x-small"
                          color="error"
                          variant="text"
                          @click.stop="removeVideo(idx)"
                        ></v-btn>
                      </div>
                    </div>

                    <!-- Video Trim Drawer -->
                    <v-expand-transition>
                      <div
                        v-if="videoTrims[idx]?.expanded"
                        class="p-2 mt-2 rounded-lg bg-black-25 border border-purple-20"
                        @click.stop
                      >
                        <div class="d-flex align-center justify-space-between mb-1">
                          <span class="text-caption font-weight-bold text-purple-lighten-2">
                            <v-icon icon="mdi-content-cut" size="14" class="mr-1"></v-icon> Trim Video Start / End
                          </span>
                          <v-btn size="x-small" variant="text" color="grey" @click.stop="resetVideoTrim(idx)">Reset</v-btn>
                        </div>
                        <div class="d-flex justify-space-between text-caption mb-1">
                          <span>Cut Start (Skip Intro):</span>
                          <span class="font-weight-bold text-white">{{ (videoTrims[idx]?.start || 0).toFixed(1) }}s</span>
                        </div>
                        <v-slider
                          v-if="videoTrims[idx]"
                          v-model="videoTrims[idx].start"
                          min="0"
                          max="60"
                          step="0.5"
                          density="compact"
                          hide-details
                          color="purple-accent-2"
                          class="mb-2"
                        ></v-slider>

                        <div class="d-flex align-center justify-space-between flex-wrap gap-1 mb-2">
                          <div class="d-flex gap-1">
                            <v-btn size="x-small" variant="tonal" @click.stop="videoTrims[idx].start = 0">0s</v-btn>
                            <v-btn size="x-small" variant="tonal" @click.stop="videoTrims[idx].start = Math.max(0, (videoTrims[idx].start || 0) + 1)">+1s</v-btn>
                            <v-btn size="x-small" variant="tonal" @click.stop="videoTrims[idx].start = Math.max(0, (videoTrims[idx].start || 0) + 5)">+5s</v-btn>
                          </div>
                          <v-btn
                            size="x-small"
                            variant="flat"
                            color="purple-darken-2"
                            class="text-none"
                            @click.stop="setVideoTrimToCurrentTime(idx)"
                            title="Cut at current video playhead"
                          >
                            <v-icon icon="mdi-clock-check-outline" size="12" class="mr-1"></v-icon>
                            Cut at Playhead
                          </v-btn>
                        </div>
                      </div>
                    </v-expand-transition>
                  </div>
                </div>

                <!-- Slide Transition Effects & Timing (Always visible outside the scrollable list) -->
                <div v-if="videoFiles.length > 1" class="transition-settings-card mt-3 p-3 rounded-lg bg-black-20">
                  <div class="d-flex justify-space-between align-center mb-2">
                      <div class="d-flex align-center">
                        <v-icon icon="mdi-transition" color="purple-lighten-2" size="18" class="mr-2"></v-icon>
                        <span class="text-caption font-weight-bold text-white">Slide Transition Effects</span>
                      </div>
                      <span class="text-caption text-purple-accent-2 font-weight-bold">
                        {{ selectedTransitions.length }} selected
                      </span>
                    </div>

                    <!-- Multi-select for Transitions -->
                    <v-select
                      v-model="selectedTransitions"
                      :items="transitionOptions"
                      item-title="title"
                      item-value="value"
                      multiple
                      variant="outlined"
                      density="compact"
                      bg-color="rgba(255,255,255,0.05)"
                      color="purple-accent-2"
                      hide-details
                      class="mb-3 rounded-lg"
                      theme="dark"
                    >
                      <template v-slot:prepend-item>
                        <v-list-item ripple @click="toggleAllTransitions">
                          <template v-slot:prepend>
                            <v-checkbox-btn
                              :model-value="likesAllTransitions"
                              :indeterminate="likesSomeTransitions"
                              color="purple-accent-2"
                            ></v-checkbox-btn>
                          </template>
                          <v-list-item-title :class="likesAllTransitions ? 'text-purple-accent-2 font-weight-bold' : 'text-white'">
                            Select All / Clear All
                          </v-list-item-title>
                        </v-list-item>
                        <v-divider class="my-1"></v-divider>
                      </template>

                      <template v-slot:selection="{ item, index }">
                        <v-chip v-if="index < 2" color="purple-accent-2" size="x-small" variant="flat" class="font-weight-bold mr-1">
                          {{ item.raw.title }}
                        </v-chip>
                        <span v-if="index === 2" class="text-caption text-grey-lighten-1" style="font-size: 10px;">
                          (+{{ selectedTransitions.length - 2 }} others)
                        </span>
                      </template>

                      <template v-slot:item="{ props, item }">
                        <v-list-item v-bind="props" title="">
                          <template v-slot:prepend="{ isActive }">
                            <v-checkbox-btn :model-value="isActive" color="purple-accent-2"></v-checkbox-btn>
                            <v-icon :icon="item.raw.icon" class="mr-2" size="18"></v-icon>
                          </template>
                          <v-list-item-title class="text-caption">{{ item.raw.title }}</v-list-item-title>
                        </v-list-item>
                      </template>
                    </v-select>

                    <!-- Transition Duration slider -->
                    <div class="mb-2">
                      <div class="d-flex justify-space-between text-caption mb-1">
                        <span class="text-grey-lighten-1">Transition Duration</span>
                        <span class="font-weight-bold text-purple-lighten-2">{{ bgTransitionDuration }}s</span>
                      </div>
                      <v-slider
                        v-model="bgTransitionDuration"
                        min="0.2"
                        max="3.0"
                        step="0.1"
                        density="compact"
                        hide-details
                        color="purple-accent-2"
                      ></v-slider>
                    </div>

                    <!-- Photo Duration (only if image files are present) -->
                    <div v-if="hasImageBackgrounds" class="mt-2 pt-2" style="border-top: 1px solid rgba(255,255,255,0.08);">
                      <div class="d-flex justify-space-between text-caption mb-1">
                        <span class="text-grey-lighten-1">Photo Hold Duration</span>
                        <span class="font-weight-bold text-purple-lighten-2">{{ bgImageDuration }}s</span>
                      </div>
                      <v-slider
                        v-model="bgImageDuration"
                        min="1"
                        max="60"
                        step="1"
                        density="compact"
                        hide-details
                        color="purple-accent-2"
                      ></v-slider>
                    </div>

                    <!-- Ken Burns Camera Motion (Only if image files are present) -->
                    <div v-if="hasImageBackgrounds" class="mt-3 pt-3" style="border-top: 1px solid rgba(255,255,255,0.08);">
                      <div class="d-flex align-center justify-space-between mb-2">
                        <span class="text-caption font-weight-bold d-flex align-center">
                          <v-icon icon="mdi-camera-iris" color="purple-accent-2" size="16" class="mr-1"></v-icon>
                          Ken Burns Photo Motion
                        </span>
                        <v-chip size="x-small" color="purple-accent-3" variant="tonal" class="text-caption font-weight-bold">
                          {{ photoMotion === 'alternate' ? 'Alternate In/Out' : photoMotion === 'in' ? 'Zoom In' : photoMotion === 'out' ? 'Zoom Out' : 'Static' }}
                        </v-chip>
                      </div>

                      <!-- Mode selection buttons -->
                      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px;" class="mb-2">
                        <v-btn
                          size="x-small"
                          :variant="photoMotion === 'alternate' ? 'flat' : 'tonal'"
                          :color="photoMotion === 'alternate' ? 'purple-accent-2' : 'grey-darken-3'"
                          class="text-none justify-start px-2 py-1"
                          @click="photoMotion = 'alternate'"
                        >
                          <v-icon start icon="mdi-swap-horizontal-bold" size="14"></v-icon>
                          <span style="font-size: 11px;">Alternate In/Out</span>
                        </v-btn>
                        <v-btn
                          size="x-small"
                          :variant="photoMotion === 'in' ? 'flat' : 'tonal'"
                          :color="photoMotion === 'in' ? 'purple-accent-2' : 'grey-darken-3'"
                          class="text-none justify-start px-2 py-1"
                          @click="photoMotion = 'in'"
                        >
                          <v-icon start icon="mdi-magnify-plus-outline" size="14"></v-icon>
                          <span style="font-size: 11px;">Zoom In Only</span>
                        </v-btn>
                        <v-btn
                          size="x-small"
                          :variant="photoMotion === 'out' ? 'flat' : 'tonal'"
                          :color="photoMotion === 'out' ? 'purple-accent-2' : 'grey-darken-3'"
                          class="text-none justify-start px-2 py-1"
                          @click="photoMotion = 'out'"
                        >
                          <v-icon start icon="mdi-magnify-minus-outline" size="14"></v-icon>
                          <span style="font-size: 11px;">Zoom Out Only</span>
                        </v-btn>
                        <v-btn
                          size="x-small"
                          :variant="photoMotion === 'none' ? 'flat' : 'tonal'"
                          :color="photoMotion === 'none' ? 'purple-accent-2' : 'grey-darken-3'"
                          class="text-none justify-start px-2 py-1"
                          @click="photoMotion = 'none'"
                        >
                          <v-icon start icon="mdi-image-off-outline" size="14"></v-icon>
                          <span style="font-size: 11px;">Static (No Zoom)</span>
                        </v-btn>
                      </div>

                      <!-- Motion Zoom Depth Intensity Slider -->
                      <div v-if="photoMotion !== 'none'" class="mt-2">
                        <div class="d-flex justify-space-between text-caption mb-1">
                          <span class="text-grey-lighten-1" style="font-size: 11px;">Zoom Depth</span>
                          <span class="font-weight-bold text-purple-lighten-2" style="font-size: 11px;">
                            +{{ Math.round(photoZoomIntensity * 100) }}% ({{ (1 + Number(photoZoomIntensity)).toFixed(2) }}x)
                          </span>
                        </div>
                        <v-slider
                          v-model="photoZoomIntensity"
                          min="0.05"
                          max="0.40"
                          step="0.01"
                          density="compact"
                          hide-details
                          color="purple-accent-2"
                        ></v-slider>
                        <div class="d-flex justify-space-between text-grey-darken-1 mt-1" style="font-size: 10px;">
                          <span>Subtle (5%)</span>
                          <span class="text-purple-accent-2 font-weight-medium">Natural (15%)</span>
                          <span>Cinematic (25%+)</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </v-expand-transition>
            </div>

            <!-- Audio Playlist Section -->
            <div class="section-card" id="audio-playlist-section">
              <div class="d-flex align-center justify-space-between mb-2">
                <span
                  class="text-subtitle-2 font-weight-bold d-flex align-center cursor-pointer"
                  @click="isAudioCollapsed = !isAudioCollapsed"
                  title="Click to collapse / expand Audio Playlist"
                >
                  <v-icon icon="mdi-playlist-music" color="purple-accent-2" class="mr-2" size="20"></v-icon>
                  Audio Playlist
                  <v-badge v-if="audioFiles.length > 0" :content="audioFiles.length" color="purple" inline class="ml-2"></v-badge>
                </span>
                <div class="d-flex align-center gap-1">
                  <v-btn
                    v-if="audioFiles.length > 0"
                    size="x-small"
                    variant="text"
                    color="error"
                    @click="clearAudio"
                  >
                    Clear All
                  </v-btn>
                  <v-btn
                    icon
                    size="x-small"
                    variant="text"
                    color="grey-lighten-1"
                    @click="isAudioCollapsed = !isAudioCollapsed"
                    :title="isAudioCollapsed ? 'Expand Audio Playlist' : 'Collapse Audio Playlist'"
                  >
                    <v-icon :icon="isAudioCollapsed ? 'mdi-chevron-down' : 'mdi-chevron-up'" size="18"></v-icon>
                  </v-btn>
                </div>
              </div>

              <v-expand-transition>
                <div v-show="!isAudioCollapsed">

                <!-- Audio Dropzone -->
                <div
                  class="dropzone-compact"
                  :class="{ 'drag-over': isDraggingAudio, 'has-files': audioFiles.length > 0 }"
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
                  <v-icon icon="mdi-music-note-plus" size="24" color="purple-accent-2" class="mb-1"></v-icon>
                  <div class="text-caption font-weight-medium">Drag & Drop Songs (MP3, WAV, AAC, FLAC)</div>
                  <div class="text-caption text-grey-lighten-1" style="font-size: 11px;">Add entire album or compilation playlist</div>
                </div>

                <!-- Playlist Track Cards with Live Audition Player -->
                <div v-if="audioFiles.length > 0" class="asset-list mt-3">
                  <div
                    v-for="(file, idx) in audioFiles"
                    :key="'audio-' + idx"
                    class="asset-card audio-track-card d-flex flex-column"
                    :class="{ 'playing-active': isPlaying && currentTrackIndex === idx }"
                  >
                    <div class="d-flex align-center justify-space-between w-100" @click="playTrack(idx)">
                      <div class="d-flex align-center overflow-hidden mr-2">
                        <v-btn
                          icon
                          size="x-small"
                          :color="isPlaying && currentTrackIndex === idx ? 'purple-accent-2' : 'grey-darken-2'"
                          variant="flat"
                          class="mr-2 track-play-btn"
                          @click.stop="toggleTrackPlayback(idx)"
                        >
                          <v-icon
                            :icon="isPlaying && currentTrackIndex === idx ? 'mdi-pause' : 'mdi-play'"
                            size="14"
                          ></v-icon>
                        </v-btn>
                        <div class="track-details overflow-hidden">
                          <div class="text-caption font-weight-medium text-truncate" :title="file.name">
                            {{ idx + 1 }}. {{ getCleanSongTitle(file.name) }}
                          </div>
                          <div class="d-flex align-center gap-2">
                            <span class="text-caption text-grey-lighten-1" style="font-size: 10px;">
                              {{ formatTrackDuration(getAudioEffectiveDuration(idx)) }}
                            </span>
                            <span
                              v-if="audioTrims[idx]?.start > 0 || audioTrims[idx]?.end > 0"
                              class="text-purple-accent-2 font-weight-bold"
                              style="font-size: 10px;"
                            >
                              ✂️ Cut: {{ (audioTrims[idx]?.start || 0).toFixed(1) }}s
                            </span>
                          </div>
                        </div>
                      </div>

                      <div class="d-flex align-center gap-1">
                        <v-btn
                          icon="mdi-content-cut"
                          size="x-small"
                          :color="(audioTrims[idx]?.start > 0 || audioTrims[idx]?.end > 0) ? 'purple-accent-2' : 'grey-lighten-1'"
                          :variant="(audioTrims[idx]?.start > 0 || audioTrims[idx]?.end > 0 || audioTrims[idx]?.expanded) ? 'tonal' : 'text'"
                          @click.stop="toggleAudioTrim(idx)"
                          title="Cut out intro/outro audio"
                        ></v-btn>
                        <v-btn
                          icon="mdi-chevron-up"
                          size="x-small"
                          variant="text"
                          :disabled="idx === 0"
                          @click.stop="moveAudioUp(idx)"
                        ></v-btn>
                        <v-btn
                          icon="mdi-chevron-down"
                          size="x-small"
                          variant="text"
                          :disabled="idx === audioFiles.length - 1"
                          @click.stop="moveAudioDown(idx)"
                        ></v-btn>
                        <v-btn
                          icon="mdi-delete-outline"
                          size="x-small"
                          color="error"
                          variant="text"
                          @click.stop="removeAudio(idx)"
                        ></v-btn>
                      </div>
                    </div>

                    <!-- Audio Trim Drawer -->
                    <v-expand-transition>
                      <div
                        v-if="audioTrims[idx]?.expanded"
                        class="p-2 mt-2 rounded-lg bg-black-25 border border-purple-20"
                        @click.stop
                      >
                        <div class="d-flex align-center justify-space-between mb-2">
                          <span class="text-caption font-weight-bold text-purple-lighten-2 d-flex align-center">
                            <v-icon icon="mdi-content-cut" size="14" class="mr-1"></v-icon> Cut Song Intro (e.g. 5s silence)
                          </span>
                          <v-btn size="x-small" variant="text" color="grey" @click.stop="resetAudioTrim(idx)">Reset</v-btn>
                        </div>

                        <!-- Cut Start Slider -->
                        <div class="d-flex justify-space-between text-caption mb-1">
                          <span class="text-grey-lighten-1">Cut Start (Skip Intro):</span>
                          <span class="font-weight-bold text-purple-accent-2">{{ (audioTrims[idx]?.start || 0).toFixed(1) }}s</span>
                        </div>
                        <v-slider
                          v-if="audioTrims[idx]"
                          v-model="audioTrims[idx].start"
                          min="0"
                          :max="Math.max(1, (trackDurations[idx] || 180) - 2)"
                          step="0.5"
                          density="compact"
                          hide-details
                          color="purple-accent-2"
                          class="mb-2"
                        ></v-slider>

                        <!-- Quick Presets -->
                        <div class="d-flex align-center justify-space-between flex-wrap gap-1 mb-2">
                          <div class="d-flex gap-1">
                            <v-btn size="x-small" variant="tonal" @click.stop="audioTrims[idx].start = 0">0s</v-btn>
                            <v-btn size="x-small" variant="tonal" @click.stop="audioTrims[idx].start = Math.max(0, (audioTrims[idx].start || 0) + 1)">+1s</v-btn>
                            <v-btn size="x-small" variant="tonal" @click.stop="audioTrims[idx].start = Math.max(0, (audioTrims[idx].start || 0) + 5)">+5s</v-btn>
                            <v-btn size="x-small" variant="tonal" @click.stop="audioTrims[idx].start = Math.max(0, (audioTrims[idx].start || 0) + 10)">+10s</v-btn>
                          </div>
                          <v-btn
                            size="x-small"
                            variant="flat"
                            color="purple-darken-2"
                            class="text-none"
                            :disabled="currentTrackIndex !== idx || currentTime <= 0"
                            @click.stop="setAudioTrimToCurrentTime(idx)"
                            title="Cut at current playhead position"
                          >
                            <v-icon icon="mdi-clock-check-outline" size="12" class="mr-1"></v-icon>
                            Cut at Playhead
                          </v-btn>
                        </div>

                        <div class="d-flex align-center justify-space-between pt-1" style="border-top: 1px solid rgba(255,255,255,0.06);">
                          <span class="text-caption text-grey-lighten-1" style="font-size: 11px;">
                            Remaining: {{ formatTrackDuration(getAudioEffectiveDuration(idx)) }}
                          </span>
                          <v-btn
                            size="x-small"
                            variant="tonal"
                            color="primary"
                            class="text-none"
                            @click.stop="auditionAudioTrim(idx)"
                          >
                            <v-icon icon="mdi-play" size="12" class="mr-1"></v-icon> Audition Cut
                          </v-btn>
                        </div>
                      </div>
                    </v-expand-transition>
                  </div>
                </div>
              </div>
            </v-expand-transition>
          </div>
        </v-window-item>

            <!-- TAB: TIMELINE & CUT CUSTOMIZER -->
            <v-window-item value="timeline" class="tab-content">
              <div class="section-card mb-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <div>
                    <div class="text-subtitle-2 font-weight-black d-flex align-center">
                      <v-icon icon="mdi-content-cut" color="purple-accent-2" class="mr-2" size="20"></v-icon>
                      CapCut Clip Trimmer & Split
                    </div>
                    <div class="text-caption text-grey-lighten-1" style="font-size: 11px;">
                      Trim intro/outro, split at playhead, and ripple-delete unwanted sections
                    </div>
                  </div>
                  <v-chip size="x-small" color="purple-darken-3" variant="flat" class="font-mono">
                    {{ selectedTimelineClip.type === 'audio' ? 'Audio Track' : 'Visual Clip' }}
                  </v-chip>
                </div>

                <!-- Toggle Audio vs Video selection -->
                <v-btn-toggle
                  v-model="selectedTimelineClip.type"
                  mandatory
                  density="compact"
                  color="purple-accent-2"
                  class="w-100 mb-3"
                  variant="outlined"
                >
                  <v-btn value="audio" class="flex-grow-1 text-none font-weight-bold">
                    <v-icon start icon="mdi-music-note" size="16"></v-icon>
                    Audio Tracks ({{ audioClips.length }})
                  </v-btn>
                  <v-btn value="video" class="flex-grow-1 text-none font-weight-bold">
                    <v-icon start icon="mdi-video-outline" size="16"></v-icon>
                    Visual Clips ({{ videoClips.length }})
                  </v-btn>
                </v-btn-toggle>

                <!-- If Audio Selected -->
                <div v-if="selectedTimelineClip.type === 'audio'">
                  <div v-if="audioClips.length === 0" class="text-center py-6 text-grey text-caption">
                    <v-icon icon="mdi-music-note-off" size="32" class="mb-2 text-grey-darken-1"></v-icon>
                    <div>No audio tracks added yet.</div>
                    <v-btn size="x-small" variant="tonal" color="purple-accent-2" class="mt-2 text-none" @click="activeTab = 'media'">
                      Go to Media Tab to Upload
                    </v-btn>
                  </div>
                  <div v-else>
                    <!-- Select Track Dropdown -->
                    <div class="text-caption font-weight-bold mb-1 text-purple-lighten-2 d-flex align-center justify-space-between">
                      <span>Select Track / Segment:</span>
                      <span class="text-caption text-grey">Clip {{ (selectedTimelineClip.index || 0) + 1 }} of {{ audioClips.length }}</span>
                    </div>
                    <v-select
                      v-model="selectedTimelineClip.index"
                      :items="audioClips.map((clip, i) => ({ title: `${i + 1}. ${clip.title}${clip.trimStart > 0 || (clip.trimEnd && clip.trimEnd < clip.originalDuration) ? ' (Trimmed)' : ''}`, value: i }))"
                      item-title="title"
                      item-value="value"
                      density="compact"
                      variant="outlined"
                      bg-color="rgba(255,255,255,0.05)"
                      hide-details
                      class="mb-3"
                    ></v-select>

                    <!-- Selected Audio Trimmer Details -->
                    <div class="p-3 rounded-lg bg-black-25 border border-purple-20 mb-3" v-if="audioClips[selectedTimelineClip.index]">
                      <div class="d-flex align-center justify-space-between mb-2">
                        <span class="text-caption font-weight-bold text-white text-truncate" style="max-width: 190px;" :title="audioClips[selectedTimelineClip.index].title">
                          {{ audioClips[selectedTimelineClip.index].title }}
                        </span>
                        <div class="d-flex align-center gap-1">
                          <v-chip size="x-small" color="purple-accent-2" variant="flat" class="font-mono">
                            {{ formatTrackDuration(getAudioEffectiveDuration(selectedTimelineClip.index)) }}
                          </v-chip>
                          <v-btn
                            icon="mdi-delete-sweep-outline"
                            size="x-small"
                            color="error"
                            variant="text"
                            @click="deleteClip('audio', selectedTimelineClip.index)"
                            title="Ripple Delete this segment"
                          ></v-btn>
                        </div>
                      </div>

                      <!-- CapCut Interactive Clip Waveform Bar -->
                      <div class="clip-waveform-trimmer-wrap mb-3">
                        <div class="waveform-scale-header d-flex justify-space-between text-caption text-grey font-mono" style="font-size: 10px;">
                          <span>0:00</span>
                          <span>Source: {{ formatTrackDuration(audioClips[selectedTimelineClip.index].originalDuration) }}</span>
                        </div>
                        <div class="clip-trimmer-track position-relative">
                          <!-- Dimmed region before trim start -->
                          <div
                            class="dimmed-overlay dimmed-start"
                            :style="{ width: `${((audioClips[selectedTimelineClip.index].trimStart || 0) / (audioClips[selectedTimelineClip.index].originalDuration || 180)) * 100}%` }"
                          ></div>

                          <!-- Active Segment (Draggable Region) -->
                          <div
                            class="active-segment-highlight"
                            :style="{
                              left: `${((audioClips[selectedTimelineClip.index].trimStart || 0) / (audioClips[selectedTimelineClip.index].originalDuration || 180)) * 100}%`,
                              width: `${(getAudioEffectiveDuration(selectedTimelineClip.index) / (audioClips[selectedTimelineClip.index].originalDuration || 180)) * 100}%`
                            }"
                          >
                            <!-- Mini Waveform Visual Stripes -->
                            <div class="mini-waveform-stripes"></div>

                            <!-- In Handle -->
                            <div
                              class="inspector-trim-handle handle-in"
                              title="Drag left edge to cut start"
                              @mousedown="onInspectorHandleMouseDown($event, 'audio', selectedTimelineClip.index, 'in')"
                              @touchstart="onInspectorHandleTouchStart($event, 'audio', selectedTimelineClip.index, 'in')"
                            >
                              <div class="handle-pill"></div>
                            </div>

                            <!-- Out Handle -->
                            <div
                              class="inspector-trim-handle handle-out"
                              title="Drag right edge to cut end"
                              @mousedown="onInspectorHandleMouseDown($event, 'audio', selectedTimelineClip.index, 'out')"
                              @touchstart="onInspectorHandleTouchStart($event, 'audio', selectedTimelineClip.index, 'out')"
                            >
                              <div class="handle-pill"></div>
                            </div>
                          </div>

                          <!-- Dimmed region after trim end -->
                          <div
                            class="dimmed-overlay dimmed-end"
                            :style="{
                              left: `${((audioClips[selectedTimelineClip.index].trimEnd || audioClips[selectedTimelineClip.index].originalDuration || 180) / (audioClips[selectedTimelineClip.index].originalDuration || 180)) * 100}%`,
                              right: 0
                            }"
                          ></div>
                        </div>
                      </div>

                      <!-- Cut Start (Skip Intro) -->
                      <div class="d-flex justify-space-between align-center text-caption mb-1">
                        <span class="text-grey-lighten-1">Cut Start (Skip Intro):</span>
                        <span class="font-weight-bold text-purple-accent-2 text-body-2 font-mono">
                          {{ (audioClips[selectedTimelineClip.index]?.trimStart || 0).toFixed(1) }}s
                        </span>
                      </div>

                      <v-slider
                        v-model="audioClips[selectedTimelineClip.index].trimStart"
                        min="0"
                        :max="Math.max(0.1, (audioClips[selectedTimelineClip.index].trimEnd || audioClips[selectedTimelineClip.index].originalDuration || 180) - 0.5)"
                        step="0.1"
                        density="compact"
                        hide-details
                        color="purple-accent-2"
                        class="mb-2"
                      ></v-slider>

                      <!-- Quick Presets Start -->
                      <div class="d-flex align-center justify-space-between flex-wrap gap-1 mb-3">
                        <div class="d-flex gap-1">
                          <v-btn size="x-small" variant="tonal" @click="setClipTrimStart('audio', selectedTimelineClip.index, 0)">0s</v-btn>
                          <v-btn size="x-small" variant="tonal" @click="setClipTrimStart('audio', selectedTimelineClip.index, Math.max(0, (audioClips[selectedTimelineClip.index].trimStart || 0) + 1))">+1s</v-btn>
                          <v-btn size="x-small" variant="tonal" @click="setClipTrimStart('audio', selectedTimelineClip.index, Math.max(0, (audioClips[selectedTimelineClip.index].trimStart || 0) + 5))">+5s</v-btn>
                          <v-btn size="x-small" variant="tonal" @click="setClipTrimStart('audio', selectedTimelineClip.index, Math.max(0, (audioClips[selectedTimelineClip.index].trimStart || 0) - 1))">-1s</v-btn>
                        </div>
                        <v-btn
                          size="x-small"
                          variant="tonal"
                          color="purple-accent-2"
                          class="text-none"
                          @click="setClipStartToPlayhead('audio', selectedTimelineClip.index)"
                          title="Cut start at current playhead"
                        >
                          <v-icon icon="mdi-content-cut" size="12" class="mr-1"></v-icon>
                          Start at Playhead
                        </v-btn>
                      </div>

                      <!-- Cut End (Trim Outro) -->
                      <div class="d-flex justify-space-between align-center text-caption mb-1">
                        <span class="text-grey-lighten-1">Cut End (Trim Outro):</span>
                        <span class="font-weight-bold text-cyan-accent-3 text-body-2 font-mono">
                          {{ (audioClips[selectedTimelineClip.index]?.trimEnd < audioClips[selectedTimelineClip.index]?.originalDuration) ? `${audioClips[selectedTimelineClip.index].trimEnd.toFixed(1)}s` : 'End of Track' }}
                        </span>
                      </div>

                      <v-slider
                        v-model="audioClips[selectedTimelineClip.index].trimEnd"
                        :min="(audioClips[selectedTimelineClip.index].trimStart || 0) + 0.5"
                        :max="audioClips[selectedTimelineClip.index].originalDuration || 180"
                        step="0.1"
                        density="compact"
                        hide-details
                        color="cyan-accent-3"
                        class="mb-2"
                      ></v-slider>

                      <!-- Quick Presets End -->
                      <div class="d-flex align-center justify-space-between flex-wrap gap-1 mb-3">
                        <div class="d-flex gap-1">
                          <v-btn size="x-small" variant="tonal" @click="setClipTrimEnd('audio', selectedTimelineClip.index, audioClips[selectedTimelineClip.index].originalDuration)">Full End</v-btn>
                          <v-btn size="x-small" variant="tonal" @click="setClipTrimEnd('audio', selectedTimelineClip.index, Math.max((audioClips[selectedTimelineClip.index].trimStart || 0) + 0.5, (audioClips[selectedTimelineClip.index].trimEnd || audioClips[selectedTimelineClip.index].originalDuration) - 5))">-5s</v-btn>
                          <v-btn size="x-small" variant="tonal" @click="setClipTrimEnd('audio', selectedTimelineClip.index, Math.max((audioClips[selectedTimelineClip.index].trimStart || 0) + 0.5, (audioClips[selectedTimelineClip.index].trimEnd || audioClips[selectedTimelineClip.index].originalDuration) - 1))">-1s</v-btn>
                        </div>
                        <v-btn
                          size="x-small"
                          variant="tonal"
                          color="cyan-accent-3"
                          class="text-none"
                          @click="setClipEndToPlayhead('audio', selectedTimelineClip.index)"
                          title="Cut end at current playhead"
                        >
                          <v-icon icon="mdi-content-cut" size="12" class="mr-1"></v-icon>
                          End at Playhead
                        </v-btn>
                      </div>

                      <!-- CapCut Split & Ripple Actions -->
                      <div class="d-flex align-center gap-2 pt-2 mb-2" style="border-top: 1px solid rgba(255,255,255,0.08);">
                        <v-btn
                          size="small"
                          variant="flat"
                          color="purple-accent-3"
                          class="flex-grow-1 text-none font-weight-bold"
                          @click="splitClipAtPlayhead('audio')"
                          title="Split this song into two segments at current playhead position"
                        >
                          <v-icon icon="mdi-content-cut" size="14" class="mr-1"></v-icon>
                          Split at Playhead (✂️)
                        </v-btn>

                        <v-btn
                          size="small"
                          variant="tonal"
                          color="error"
                          class="text-none"
                          @click="deleteClip('audio', selectedTimelineClip.index)"
                          title="Ripple delete: remove this segment and shift subsequent tracks"
                        >
                          <v-icon icon="mdi-delete-sweep" size="14" class="mr-1"></v-icon>
                          Ripple Delete
                        </v-btn>
                      </div>

                      <!-- Bottom Audition & Reset -->
                      <div class="d-flex align-center justify-space-between pt-2" style="border-top: 1px solid rgba(255,255,255,0.05);">
                        <v-btn
                          size="x-small"
                          variant="text"
                          color="grey"
                          @click="resetClipTrim('audio', selectedTimelineClip.index)"
                        >
                          Reset Trim
                        </v-btn>
                        <v-btn
                          size="x-small"
                          variant="tonal"
                          color="primary"
                          class="text-none font-weight-bold"
                          @click="auditionClip('audio', selectedTimelineClip.index)"
                        >
                          <v-icon icon="mdi-play" size="14" class="mr-1"></v-icon>
                          Audition Trimmed Track
                        </v-btn>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- If Visual Selected -->
                <div v-else>
                  <div v-if="videoClips.length === 0" class="text-center py-6 text-grey text-caption">
                    <v-icon icon="mdi-video-off" size="32" class="mb-2 text-grey-darken-1"></v-icon>
                    <div>No background visual files added yet.</div>
                    <v-btn size="x-small" variant="tonal" color="purple-accent-2" class="mt-2 text-none" @click="activeTab = 'media'">
                      Go to Media Tab to Upload
                    </v-btn>
                  </div>
                  <div v-else>
                    <div class="text-caption font-weight-bold mb-1 text-purple-lighten-2 d-flex align-center justify-space-between">
                      <span>Select Visual Clip / Segment:</span>
                      <span class="text-caption text-grey">Clip {{ (selectedTimelineClip.index || 0) + 1 }} of {{ videoClips.length }}</span>
                    </div>
                    <v-select
                      v-model="selectedTimelineClip.index"
                      :items="videoClips.map((clip, i) => ({ title: `${i + 1}. ${clip.name}${clip.isImage ? ' (Image)' : ''}`, value: i }))"
                      item-title="title"
                      item-value="value"
                      density="compact"
                      variant="outlined"
                      bg-color="rgba(255,255,255,0.05)"
                      hide-details
                      class="mb-3"
                    ></v-select>

                    <div class="p-3 rounded-lg bg-black-25 border border-purple-20" v-if="videoClips[selectedTimelineClip.index]">
                      <div v-if="videoClips[selectedTimelineClip.index].isImage" class="text-caption text-grey py-2">
                        <v-icon icon="mdi-image-outline" size="18" class="mr-1 text-purple-lighten-3"></v-icon>
                        Image file duration is configured in Format & Slideshow settings. Trimming applies directly to video clips.
                      </div>
                      <div v-else>
                        <div class="d-flex align-center justify-space-between mb-2">
                          <span class="text-caption font-weight-bold text-white text-truncate" style="max-width: 190px;">
                            {{ videoClips[selectedTimelineClip.index].name }}
                          </span>
                          <v-chip size="x-small" color="purple-accent-2" variant="flat" class="font-mono">
                            {{ formatTrackDuration(getVideoEffectiveDuration(selectedTimelineClip.index)) }}
                          </v-chip>
                        </div>

                        <!-- Cut Start (Skip Video Intro) -->
                        <div class="d-flex justify-space-between align-center text-caption mb-1">
                          <span class="text-grey-lighten-1">Cut Start:</span>
                          <span class="font-weight-bold text-purple-accent-2 text-body-2 font-mono">
                            {{ (videoClips[selectedTimelineClip.index]?.trimStart || 0).toFixed(1) }}s
                          </span>
                        </div>
                        <v-slider
                          v-model="videoClips[selectedTimelineClip.index].trimStart"
                          min="0"
                          :max="Math.max(0.1, (videoClips[selectedTimelineClip.index].trimEnd || videoClips[selectedTimelineClip.index].originalDuration || 60) - 0.5)"
                          step="0.1"
                          density="compact"
                          hide-details
                          color="purple-accent-2"
                          class="mb-2"
                        ></v-slider>

                        <!-- Cut End (Trim Video Outro) -->
                        <div class="d-flex justify-space-between align-center text-caption mb-1">
                          <span class="text-grey-lighten-1">Cut End:</span>
                          <span class="font-weight-bold text-cyan-accent-3 text-body-2 font-mono">
                            {{ (videoClips[selectedTimelineClip.index]?.trimEnd || videoClips[selectedTimelineClip.index].originalDuration || 60).toFixed(1) }}s
                          </span>
                        </div>
                        <v-slider
                          v-model="videoClips[selectedTimelineClip.index].trimEnd"
                          :min="(videoClips[selectedTimelineClip.index].trimStart || 0) + 0.5"
                          :max="videoClips[selectedTimelineClip.index].originalDuration || 60"
                          step="0.1"
                          density="compact"
                          hide-details
                          color="cyan-accent-3"
                          class="mb-3"
                        ></v-slider>

                        <div class="d-flex align-center gap-2 pt-2 mb-2" style="border-top: 1px solid rgba(255,255,255,0.08);">
                          <v-btn
                            size="small"
                            variant="flat"
                            color="purple-accent-3"
                            class="flex-grow-1 text-none font-weight-bold"
                            @click="splitClipAtPlayhead('video')"
                            title="Split visual clip into two segments"
                          >
                            <v-icon icon="mdi-content-cut" size="14" class="mr-1"></v-icon>
                            Split at Playhead (✂️)
                          </v-btn>

                          <v-btn
                            size="small"
                            variant="tonal"
                            color="error"
                            class="text-none"
                            @click="deleteClip('video', selectedTimelineClip.index)"
                            title="Ripple delete: remove visual clip and shift subsequent clips"
                          >
                            <v-icon icon="mdi-delete-sweep" size="14" class="mr-1"></v-icon>
                            Ripple Delete
                          </v-btn>
                        </div>

                        <div class="d-flex align-center justify-space-between pt-2" style="border-top: 1px solid rgba(255,255,255,0.05);">
                          <v-btn
                            size="x-small"
                            variant="text"
                            color="grey"
                            @click="resetClipTrim('video', selectedTimelineClip.index)"
                          >
                            Reset Cut
                          </v-btn>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </v-window-item>

            <!-- TAB 2: OVERLAYS & STYLE -->
            <v-window-item value="overlays" class="tab-content">
              <!-- Playlist Overlay Settings -->
              <div class="section-card mb-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="d-flex align-center">
                    <v-icon icon="mdi-format-list-numbered" color="cyan-accent-3" class="mr-2" size="20"></v-icon>
                    <div>
                      <div class="text-subtitle-2 font-weight-bold">Now Playing Playlist</div>
                      <div class="text-caption text-grey-lighten-1" style="font-size: 11px;">Interactive on-screen song list</div>
                    </div>
                  </div>
                  <v-switch
                    v-model="showNowPlaying"
                    color="cyan-accent-3"
                    inset
                    hide-details
                    density="compact"
                  ></v-switch>
                </div>

                <v-expand-transition>
                  <div v-if="showNowPlaying" class="overlay-sub-settings pt-2">
                    <div class="mb-3">
                      <div class="d-flex justify-space-between text-caption mb-1">
                        <span>Font Size</span>
                        <span class="text-grey-lighten-1">{{ playlistFontSize }}px</span>
                      </div>
                      <v-slider
                        v-model="playlistFontSize"
                        min="16"
                        max="72"
                        step="2"
                        hide-details
                        density="compact"
                        color="cyan-accent-3"
                      ></v-slider>
                    </div>

                    <div class="mb-3">
                      <div class="d-flex justify-space-between text-caption mb-1">
                        <span>Songs Per Column</span>
                        <span class="text-grey-lighten-1">{{ playlistItemsPerCol }} items</span>
                      </div>
                      <v-slider
                        v-model="playlistItemsPerCol"
                        min="1"
                        max="30"
                        step="1"
                        hide-details
                        density="compact"
                        color="cyan-accent-3"
                      ></v-slider>
                    </div>

                    <div class="mb-3">
                      <div class="d-flex justify-space-between text-caption mb-1">
                        <span>Column Spacing</span>
                        <span class="text-grey-lighten-1">{{ playlistColGap }}px</span>
                      </div>
                      <v-slider
                        v-model="playlistColGap"
                        min="50"
                        max="800"
                        step="25"
                        hide-details
                        density="compact"
                        color="cyan-accent-3"
                      ></v-slider>
                    </div>

                    <!-- Preset Positions -->
                    <div class="mt-2">
                      <div class="text-caption text-grey-lighten-1 mb-1">Quick Snap Position:</div>
                      <div class="d-flex flex-wrap gap-1">
                        <v-btn size="x-small" variant="tonal" color="cyan-lighten-3" @click="setPlaylistPosition(5, 7)">Top Left (95% Safe)</v-btn>
                        <v-btn size="x-small" variant="tonal" color="pink-lighten-3" @click="setPlaylistPosition(10, 10)">Top Left (Title Safe)</v-btn>
                        <v-btn size="x-small" variant="tonal" @click="setPlaylistPosition(aspectRatioMode === '9:16' ? 45 : 65, 7)">Top Right</v-btn>
                        <v-btn size="x-small" variant="tonal" @click="setPlaylistPosition(5, aspectRatioMode === '9:16' ? 75 : 60)">Bottom Left</v-btn>
                      </div>
                    </div>
                  </div>
                </v-expand-transition>
              </div>

              <!-- Timer Overlay Settings -->
              <div class="section-card">
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="d-flex align-center">
                    <v-icon icon="mdi-timer-outline" color="purple-lighten-2" class="mr-2" size="20"></v-icon>
                    <div>
                      <div class="text-subtitle-2 font-weight-bold">Timer Overlay</div>
                      <div class="text-caption text-grey-lighten-1" style="font-size: 11px;">Focus & countdown overlay</div>
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
                  <div v-if="overlayTimer.enabled" class="overlay-sub-settings pt-2">
                    <v-select
                      v-model="overlayTimer.mode"
                      :items="[
                        { title: 'Per-Song Countdown (Default)', value: 'persong' },
                        { title: 'Pomodoro Focus Cycle', value: 'pomodoro' }
                      ]"
                      label="Timer Mode"
                      density="compact"
                      hide-details
                      variant="outlined"
                      bg-color="rgba(255,255,255,0.05)"
                      class="mb-3"
                    ></v-select>

                    <div v-if="overlayTimer.mode === 'persong'" class="p-2 rounded bg-black-25 border border-purple-20 mb-3 text-caption">
                      <div class="d-flex align-center justify-space-between mb-1">
                        <span class="text-grey-lighten-1">Mode:</span>
                        <span class="text-purple-accent-2 font-weight-bold">Per-Song Countdown</span>
                      </div>
                      <div class="d-flex align-center justify-space-between mb-1">
                        <span class="text-grey-lighten-1">Active Track Duration:</span>
                        <span class="font-mono text-white font-weight-bold">{{ formatTrackDuration(getAudioEffectiveDuration(currentTrackIndex)) }}</span>
                      </div>
                      <div class="d-flex align-center justify-space-between">
                        <span class="text-grey-lighten-1">Live Countdown:</span>
                        <span class="font-mono text-purple-accent-2 font-weight-black text-body-2">{{ liveTimerFormattedText }}</span>
                      </div>
                      <div class="text-grey text-caption mt-1" style="font-size: 10px;">
                        Counts down from current track's edited duration to 00:00. Dynamically recalculates when trimmed or split.
                      </div>
                    </div>

                    <div v-if="overlayTimer.mode === 'pomodoro'" class="mb-3">
                      <div class="d-flex align-center gap-2 mb-2">
                        <v-btn
                          v-for="p in [25, 50]"
                          :key="p"
                          size="x-small"
                          :color="overlayTimer.minutes === p ? 'purple-lighten-2' : 'grey-darken-3'"
                          :variant="overlayTimer.minutes === p ? 'flat' : 'outlined'"
                          @click="overlayTimer.minutes = p"
                        >
                          {{ p }}m
                        </v-btn>
                        <v-text-field
                          v-model.number="overlayTimer.minutes"
                          type="number"
                          min="1"
                          max="180"
                          density="compact"
                          hide-details
                          variant="outlined"
                          label="Minutes"
                          bg-color="rgba(255,255,255,0.05)"
                          style="max-width: 100px"
                        ></v-text-field>
                      </div>

                      <div class="d-flex align-center justify-space-between">
                        <v-switch
                          v-model="overlayTimer.withBreak"
                          label="Add Short Break"
                          color="green-lighten-2"
                          inset
                          hide-details
                          density="compact"
                          class="text-caption"
                        ></v-switch>
                        <v-text-field
                          v-if="overlayTimer.withBreak"
                          v-model.number="overlayTimer.breakMinutes"
                          type="number"
                          min="1"
                          max="60"
                          density="compact"
                          hide-details
                          variant="outlined"
                          label="Break Min"
                          bg-color="rgba(255,255,255,0.05)"
                          style="max-width: 90px"
                        ></v-text-field>
                      </div>
                    </div>

                    <div class="mb-3">
                      <div class="d-flex justify-space-between text-caption mb-1">
                        <span>Timer Font Size</span>
                        <span class="text-grey-lighten-1">{{ overlayTimer.fontSize }}px</span>
                      </div>
                      <v-slider
                        v-model="overlayTimer.fontSize"
                        min="24"
                        max="96"
                        step="4"
                        hide-details
                        density="compact"
                        color="purple-lighten-2"
                      ></v-slider>
                    </div>

                    <!-- Preset Positions -->
                    <div class="mt-2">
                      <div class="text-caption text-grey-lighten-1 mb-1">Quick Snap Position:</div>
                      <div class="d-flex flex-wrap gap-1">
                        <v-btn size="x-small" variant="tonal" color="cyan-lighten-3" @click="setTimerPosition(aspectRatioMode === '9:16' ? 60 : (outputResolution.includes('1080:1080') ? 72 : 84), 7)">Top Right (95% Safe)</v-btn>
                        <v-btn size="x-small" variant="tonal" color="pink-lighten-3" @click="setTimerPosition(aspectRatioMode === '9:16' ? 52 : (outputResolution.includes('1080:1080') ? 65 : 78), 10)">Top Right (Title Safe)</v-btn>
                        <v-btn size="x-small" variant="tonal" @click="setTimerPosition(5, 7)">Top Left</v-btn>
                        <v-btn size="x-small" variant="tonal" @click="setTimerPosition(aspectRatioMode === '9:16' ? 32 : (outputResolution.includes('1080:1080') ? 40 : 44), 7)">Top Center</v-btn>
                        <v-btn size="x-small" variant="tonal" @click="setTimerPosition(aspectRatioMode === '9:16' ? 60 : (outputResolution.includes('1080:1080') ? 72 : 84), 82)">Bottom Right</v-btn>
                        <v-btn size="x-small" variant="tonal" @click="setTimerPosition(5, 82)">Bottom Left</v-btn>
                      </div>
                    </div>
                  </div>
                </v-expand-transition>
              </div>
            </v-window-item>

            <!-- TAB 3: FORMAT & SETTINGS -->
            <v-window-item value="settings" class="tab-content">
              <div class="section-card mb-4">
                <span class="text-subtitle-2 font-weight-bold d-block mb-3">Aspect Ratio & Output Format</span>
                
                <div class="format-grid mb-4">
                  <div
                    v-for="opt in resolutionOptions"
                    :key="opt.value"
                    class="format-card"
                    :class="{ active: outputResolution === opt.value }"
                    @click="selectOutputResolution(opt.value)"
                  >
                    <v-icon :icon="opt.icon" size="24" class="mb-1"></v-icon>
                    <div class="text-caption font-weight-bold">{{ opt.title }}</div>
                    <div class="format-res">{{ opt.value }}</div>
                  </div>
                </div>

                <v-divider class="my-3 border-opacity-25"></v-divider>

                <div class="d-flex align-center justify-space-between">
                  <div>
                    <div class="text-caption font-weight-bold">Keep Video Audio</div>
                    <div class="text-caption text-grey-lighten-1" style="font-size: 11px;">Mix original video audio with playlist</div>
                  </div>
                  <v-switch
                    v-model="keepOriginalAudio"
                    color="purple-lighten-2"
                    inset
                    hide-details
                    density="compact"
                  ></v-switch>
                </div>
              </div>
            </v-window-item>
          </v-window>
        </aside>

        <!-- RIGHT: LIVE CANVAS STUDIO & TIMELINE -->
        <main class="studio-viewport-area d-flex flex-column">
          <!-- Viewport Toolbar -->
          <div class="viewport-toolbar d-flex align-center justify-space-between px-4 py-2">
            <div class="d-flex align-center gap-2">
              <span class="text-caption font-weight-bold text-grey-lighten-1 d-flex align-center mr-1">
                <v-icon icon="mdi-crop" size="16" class="mr-1"></v-icon> Canvas:
              </span>
              <v-btn-toggle
                v-model="aspectRatioMode"
                mandatory
                density="compact"
                color="purple-accent-2"
                rounded="pill"
                class="ratio-toggle"
              >
                <v-btn value="16:9" size="x-small" @click="setAspectRatio('1280:720')">16:9</v-btn>
                <v-btn value="9:16" size="x-small" @click="setAspectRatio('720:1280')">9:16</v-btn>
                <v-btn value="1:1" size="x-small" @click="setAspectRatio('1080:1080')">1:1</v-btn>
              </v-btn-toggle>
            </div>

            <div class="d-flex align-center gap-1">
              <v-btn
                size="x-small"
                :variant="showSafeGuides ? 'flat' : 'text'"
                :color="showSafeGuides ? 'cyan-accent-3' : 'grey-lighten-1'"
                prepend-icon="mdi-grid"
                @click="showSafeGuides = !showSafeGuides"
                title="Toggle Safe Margins & Guides"
              >
                Guides
              </v-btn>
              <v-btn
                size="x-small"
                variant="tonal"
                color="cyan-lighten-3"
                @click="snapToSafeGuides('action')"
                title="Snap title song and timer to 95% Action Safe corner positions"
              >
                Snap 95% Safe
              </v-btn>
              <v-btn
                size="x-small"
                variant="tonal"
                color="pink-lighten-3"
                @click="snapToSafeGuides('title')"
                title="Snap title song and timer inside 90% Title Safe boundary"
              >
                Snap Title Safe
              </v-btn>
              <v-btn
                size="x-small"
                variant="text"
                color="grey-lighten-1"
                prepend-icon="mdi-arrow-expand-all"
                @click="resetPositions"
                title="Reset Overlays"
              >
                Reset
              </v-btn>
            </div>
          </div>

          <!-- The Live Interactive Stage -->
          <div class="canvas-stage d-flex align-center justify-center p-4">
            <div
              class="canvas-monitor"
              :class="canvasRatioClass"
              ref="previewBoxRef"
              @mousemove="onMouseMove"
              @mouseup="onMouseUp"
              @mouseleave="onMouseUp"
              @touchmove="onTouchMove"
              @touchend="onMouseUp"
            >
              <!-- 1. Background Video / Slideshow Layer -->
              <video
                v-if="videoPreviewUrl && !isBackgroundImg"
                ref="previewVideoRef"
                :src="videoPreviewUrl"
                class="canvas-media"
                loop
                muted
                playsinline
              ></video>
              <img
                v-else-if="videoPreviewUrl && isBackgroundImg"
                :key="`${currentBgImageIndex}_${photoMotion}_${photoZoomIntensity}`"
                :src="currentBgImageSrc"
                class="canvas-media"
                :class="previewMotionClass"
                :style="previewMotionStyle"
                alt="Background"
              />
              <div v-else class="canvas-placeholder d-flex flex-column align-center justify-center">
                <v-icon icon="mdi-movie-filter-outline" size="56" color="rgba(255,255,255,0.2)" class="mb-2"></v-icon>
                <div class="text-subtitle-2 font-weight-bold text-grey-lighten-1">No Background Media Selected</div>
                <div class="text-caption text-grey-darken-1">Drop an image or video in Media Tracks</div>
              </div>

              <!-- 2. Broadcast Safe Guides Overlay (Optional) -->
              <div v-if="showSafeGuides" class="safe-guides-overlay">
                <div class="action-safe-box">
                  <span class="guide-tag">90% Action Safe</span>
                </div>
                <div class="title-safe-box">
                  <span class="guide-tag">80% Title Safe</span>
                </div>
              </div>

              <!-- 3. Interactive Draggable Playlist Box -->
              <div
                v-if="showNowPlaying"
                class="canvas-overlay-item playlist-overlay draggable-element"
                :class="{ 'is-dragging': draggingElement === 'playlist' }"
                :style="playlistElementStyle"
                @mousedown="onMouseDown($event, 'playlist')"
                @touchstart="onTouchStart($event, 'playlist')"
              >
                <!-- Drag Handle & Coordinates Tooltip -->
                <div class="overlay-badge">
                  <v-icon icon="mdi-drag" size="12"></v-icon>
                  Playlist ({{ Math.round(playlistPos.x) }}%, {{ Math.round(playlistPos.y) }}%)
                </div>

                <div
                  class="playlist-grid"
                  :style="{
                    gridTemplateRows: `repeat(${playlistItemsPerCol}, auto)`,
                    columnGap: `${Math.round(playlistColGap * previewScale * 0.3)}px`
                  }"
                >
                  <div
                    v-for="(song, index) in previewPlaylist"
                    :key="'pl-' + index"
                    class="canvas-playlist-item"
                    :class="{ 'active-track': index === currentTrackIndex }"
                  >
                    <span class="play-indicator">
                      {{ index === currentTrackIndex ? '▶' : '' }}
                    </span>
                    <span class="song-num">{{ index + 1 }}.</span>
                    <span class="song-name">{{ song.title }}</span>
                  </div>
                </div>
              </div>

              <!-- 4. Interactive Draggable Timer Box -->
              <div
                v-if="overlayTimer.enabled"
                class="canvas-overlay-item timer-overlay draggable-element"
                :class="{ 'is-dragging': draggingElement === 'timer' }"
                :style="timerElementStyle"
                @mousedown="onMouseDown($event, 'timer')"
                @touchstart="onTouchStart($event, 'timer')"
              >
                <div class="overlay-badge">
                  <v-icon icon="mdi-drag" size="12"></v-icon>
                  Timer ({{ Math.round(timerPos.x) }}%, {{ Math.round(timerPos.y) }}%)
                </div>
                <div class="timer-digits">
                  {{ liveTimerFormattedText }}
                </div>
                <div v-if="overlayTimer.mode === 'pomodoro' && overlayTimer.withBreak" class="timer-tag">
                  FOCUS
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom Studio Transport Bar & CapCut Interactive Multi-Track Timeline -->
          <div class="studio-footer px-4 py-3">
            <!-- Transport Bar -->
            <div class="transport-bar d-flex align-center justify-space-between mb-2">
              <!-- Left: Timecode Display -->
              <div class="timecode-display d-flex align-center gap-2">
                <v-icon icon="mdi-clock-outline" size="18" color="purple-lighten-2"></v-icon>
                <span class="text-body-2 font-weight-black font-mono text-white">
                  {{ formattedCurrentTime }}
                </span>
                <span class="text-caption text-grey-lighten-1">/</span>
                <span class="text-caption text-grey-lighten-1 font-mono">
                  {{ formattedTotalDuration }}
                </span>
                <v-chip size="x-small" color="purple-darken-3" variant="flat" class="ml-2 font-mono" v-if="audioClips.length > 0">
                  Track {{ currentTrackIndex + 1 }}/{{ audioClips.length }}
                </v-chip>
                <v-chip
                  v-if="selectedTimelineClip.id || (selectedTimelineClip.type === 'audio' ? audioClips[selectedTimelineClip.index] : videoClips[selectedTimelineClip.index])"
                  size="x-small"
                  color="purple-accent-2"
                  variant="outlined"
                  class="ml-1 text-truncate"
                  style="max-width: 180px;"
                >
                  Selected: {{ (selectedTimelineClip.type === 'audio' ? audioClips[selectedTimelineClip.index]?.title : videoClips[selectedTimelineClip.index]?.name) || 'None' }}
                </v-chip>
              </div>

              <!-- Center: Playback Transport Buttons -->
              <div class="transport-controls d-flex align-center gap-2">
                <v-btn
                  icon="mdi-skip-previous"
                  variant="text"
                  size="small"
                  color="grey-lighten-1"
                  :disabled="audioClips.length === 0"
                  @click="prevTrack"
                  title="Previous Track"
                ></v-btn>

                <v-btn
                  icon
                  size="large"
                  class="master-play-btn"
                  color="primary"
                  :disabled="audioClips.length === 0 && videoClips.length === 0"
                  @click="toggleMasterPlayback"
                  title="Play / Pause Live Preview (Space)"
                >
                  <v-icon :icon="isPlaying ? 'mdi-pause' : 'mdi-play'" size="28"></v-icon>
                </v-btn>

                <v-btn
                  icon="mdi-stop"
                  variant="text"
                  size="small"
                  color="grey-lighten-1"
                  :disabled="!isPlaying && currentTime === 0"
                  @click="stopMasterPlayback"
                  title="Stop"
                ></v-btn>

                <v-btn
                  icon="mdi-skip-next"
                  variant="text"
                  size="small"
                  color="grey-lighten-1"
                  :disabled="audioClips.length === 0"
                  @click="nextTrack"
                  title="Next Track"
                ></v-btn>
              </div>

              <!-- Right: Volume & Audio Controls -->
              <div class="d-flex align-center gap-2 volume-controls" style="min-width: 140px;">
                <v-btn
                  icon
                  size="x-small"
                  variant="text"
                  color="grey-lighten-1"
                  @click="isMuted = !isMuted"
                >
                  <v-icon :icon="isMuted ? 'mdi-volume-off' : (volume > 0.5 ? 'mdi-volume-high' : 'mdi-volume-medium')"></v-icon>
                </v-btn>
                <v-slider
                  v-model="volume"
                  min="0"
                  max="1"
                  step="0.05"
                  hide-details
                  density="compact"
                  color="purple-accent-2"
                  class="volume-slider"
                ></v-slider>
              </div>
            </div>

            <!-- CapCut Timeline Toolbar: Split, Delete, Zoom & Info -->
            <div class="timeline-action-toolbar d-flex align-center justify-space-between px-2 py-1 mb-2">
              <div class="d-flex align-center gap-2">
                <v-btn
                  size="x-small"
                  variant="flat"
                  color="purple-accent-3"
                  class="capcut-tool-btn text-none font-weight-black"
                  :disabled="audioClips.length === 0 && videoClips.length === 0"
                  @click="splitClipAtPlayhead(selectedTimelineClip.type)"
                  title="Split active track at current playhead position (Shortcut: S)"
                >
                  <v-icon icon="mdi-content-cut" size="14" class="mr-1"></v-icon>
                  Split (✂️)
                </v-btn>

                <v-btn
                  size="x-small"
                  variant="tonal"
                  color="error"
                  class="capcut-tool-btn text-none font-weight-bold"
                  :disabled="!canDeleteSelectedClip"
                  @click="deleteSelectedClip"
                  title="Delete selected clip and ripple-shift remaining tracks (Shortcut: Del / Backspace)"
                >
                  <v-icon icon="mdi-delete-sweep" size="14" class="mr-1"></v-icon>
                  Ripple Delete
                </v-btn>

                <v-btn
                  size="x-small"
                  variant="text"
                  color="grey-lighten-1"
                  class="text-none"
                  @click="jumpToPrevCut"
                  title="Jump to previous clip boundary"
                >
                  <v-icon icon="mdi-arrow-collapse-left" size="14" class="mr-1"></v-icon>
                  Prev Cut
                </v-btn>

                <v-btn
                  size="x-small"
                  variant="text"
                  color="grey-lighten-1"
                  class="text-none"
                  @click="jumpToNextCut"
                  title="Jump to next clip boundary"
                >
                  <v-icon icon="mdi-arrow-collapse-right" size="14" class="mr-1"></v-icon>
                  Next Cut
                </v-btn>
              </div>

              <!-- Zoom Controls -->
              <div class="d-flex align-center gap-1 timeline-zoom-controls">
                <span class="text-caption text-grey mr-1" style="font-size: 10px;">Zoom:</span>
                <v-btn
                  icon="mdi-minus"
                  size="x-small"
                  variant="text"
                  :disabled="timelineZoom <= 1"
                  @click="timelineZoom = Math.max(1, timelineZoom - 0.5)"
                  title="Zoom Out"
                ></v-btn>
                <span class="text-caption font-mono text-purple-lighten-2">{{ timelineZoom }}x</span>
                <v-btn
                  icon="mdi-plus"
                  size="x-small"
                  variant="text"
                  :disabled="timelineZoom >= 3"
                  @click="timelineZoom = Math.min(3, timelineZoom + 0.5)"
                  title="Zoom In"
                ></v-btn>
              </div>
            </div>

            <!-- CapCut Interactive Multi-Track Timeline Area -->
            <div
              class="capcut-timeline-wrapper"
              ref="timelineContainerRef"
              @click="onTimelineClick"
              @mousedown="onTimelineContainerMouseDown"
            >
              <!-- Timeline Content Width Scaled by Zoom -->
              <div
                class="capcut-timeline-inner"
                :style="{ width: `${timelineZoom * 100}%` }"
              >
                <!-- 1. Timecode Ruler -->
                <div class="capcut-ruler" @mousedown.stop="onPlayheadMouseDown" @touchstart.stop="onPlayheadTouchStart">
                  <div
                    v-for="(tick, tIdx) in timelineRulerTicks"
                    :key="'ruler-tick-' + tIdx"
                    class="ruler-tick"
                    :style="{ left: `${tick.percent}%` }"
                  >
                    <span class="tick-label">{{ tick.label }}</span>
                    <div class="tick-mark"></div>
                  </div>
                </div>

                <!-- 2. Visuals Track -->
                <div class="capcut-track-row visual-track-row d-flex align-center">
                  <div class="track-header-badge">
                    <v-icon icon="mdi-filmstrip" size="13" class="mr-1 text-purple-lighten-3"></v-icon>
                    <span>Visual</span>
                  </div>
                  <div class="track-clips-lane d-flex flex-grow-1 position-relative">
                    <template v-if="videoClips.length > 0">
                      <div
                        v-for="(clip, idx) in videoClips"
                        :key="clip.id || ('vclip-' + idx)"
                        class="capcut-clip-block visual-clip-block"
                        :class="{
                          'is-selected': selectedTimelineClip.type === 'video' && selectedTimelineClip.index === idx,
                          'is-image': clip.isImage
                        }"
                        :style="{ flexGrow: Math.max(1, Math.round(getVideoEffectiveDuration(idx) * 10)) }"
                        @click.stop="selectAndInspectClip('video', idx)"
                        :title="clip.name + ` (${getVideoEffectiveDuration(idx).toFixed(1)}s)`"
                      >
                        <!-- In Handle (Trim Start) -->
                        <div
                          class="capcut-clip-handle handle-left"
                          title="Drag right to cut start (remove beginning seconds)"
                          @mousedown.stop="onHandleMouseDown($event, 'video', idx, 'in')"
                          @touchstart.stop="onHandleTouchStart($event, 'video', idx, 'in')"
                        >
                          <div class="handle-bar"></div>
                        </div>

                        <!-- Clip Content -->
                        <div class="clip-inner-content d-flex align-center justify-space-between px-2 overflow-hidden">
                          <span class="clip-name text-truncate">
                            {{ idx + 1 }}. {{ clip.name }}
                          </span>
                          <div class="d-flex align-center gap-1">
                            <span class="clip-duration-badge">
                              {{ getVideoEffectiveDuration(idx).toFixed(1) }}s
                            </span>
                            <v-btn
                              icon="mdi-close"
                              size="x-small"
                              variant="text"
                              class="clip-delete-btn"
                              @click.stop="deleteClip('video', idx)"
                              title="Delete clip"
                            ></v-btn>
                          </div>
                        </div>

                        <!-- Out Handle (Trim End) -->
                        <div
                          class="capcut-clip-handle handle-right"
                          title="Drag left to cut end (remove ending seconds)"
                          @mousedown.stop="onHandleMouseDown($event, 'video', idx, 'out')"
                          @touchstart.stop="onHandleTouchStart($event, 'video', idx, 'out')"
                        >
                          <div class="handle-bar"></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="empty-track-placeholder d-flex align-center px-3 text-caption text-grey cursor-pointer" @click="activeTab = 'media'; scrollToMediaSection('visuals');" title="Click to upload background visuals in Media tab">
                      <v-icon icon="mdi-plus" size="14" class="mr-1"></v-icon> No background media (Click to add in Media tab)
                    </div>
                  </div>
                </div>

                <!-- 3. Audio Playlist Track -->
                <div class="capcut-track-row audio-track-row d-flex align-center mt-1">
                  <div class="track-header-badge">
                    <v-icon icon="mdi-music-note" size="13" class="mr-1 text-cyan-lighten-3"></v-icon>
                    <span>Audio</span>
                  </div>
                  <div class="track-clips-lane d-flex flex-grow-1 position-relative">
                    <template v-if="audioClips.length > 0">
                      <div
                        v-for="(clip, idx) in audioClips"
                        :key="clip.id || ('aclip-' + idx)"
                        class="capcut-clip-block audio-clip-block"
                        :class="{
                          'is-selected': selectedTimelineClip.type === 'audio' && selectedTimelineClip.index === idx,
                          'is-playing': isPlaying && currentTrackIndex === idx
                        }"
                        :style="{ flexGrow: Math.max(1, Math.round(getAudioEffectiveDuration(idx) * 10)) }"
                        @click.stop="selectAndInspectClip('audio', idx)"
                        :title="clip.title + ` (${getAudioEffectiveDuration(idx).toFixed(1)}s)`"
                      >
                        <!-- In Handle (Trim Start) -->
                        <div
                          class="capcut-clip-handle handle-left"
                          title="Drag right to cut intro (remove first seconds)"
                          @mousedown.stop="onHandleMouseDown($event, 'audio', idx, 'in')"
                          @touchstart.stop="onHandleTouchStart($event, 'audio', idx, 'in')"
                        >
                          <div class="handle-bar"></div>
                        </div>

                        <!-- Clip Content -->
                        <div class="clip-inner-content d-flex align-center justify-space-between px-2 overflow-hidden">
                          <div class="d-flex align-center overflow-hidden mr-1">
                            <span v-if="isPlaying && currentTrackIndex === idx" class="playing-equalizer mr-1">
                              <span></span><span></span><span></span>
                            </span>
                            <span class="clip-name text-truncate">
                              {{ idx + 1 }}. {{ clip.title }}
                            </span>
                          </div>
                          <div class="d-flex align-center gap-1">
                            <span class="clip-duration-badge">
                              {{ getAudioEffectiveDuration(idx).toFixed(1) }}s
                            </span>
                            <v-btn
                              icon="mdi-close"
                              size="x-small"
                              variant="text"
                              class="clip-delete-btn"
                              @click.stop="deleteClip('audio', idx)"
                              title="Ripple delete clip"
                            ></v-btn>
                          </div>
                        </div>

                        <!-- Out Handle (Trim End) -->
                        <div
                          class="capcut-clip-handle handle-right"
                          title="Drag left to cut outro (remove ending seconds)"
                          @mousedown.stop="onHandleMouseDown($event, 'audio', idx, 'out')"
                          @touchstart.stop="onHandleTouchStart($event, 'audio', idx, 'out')"
                        >
                          <div class="handle-bar"></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="empty-track-placeholder d-flex align-center px-3 text-caption text-grey cursor-pointer" @click="activeTab = 'media'; scrollToMediaSection('audio');" title="Click to upload songs in Audio Playlist">
                      <v-icon icon="mdi-plus" size="14" class="mr-1"></v-icon> No audio tracks added yet (Click to add in Audio Playlist)
                    </div>
                  </div>
                </div>

                <!-- 4. Interactive CapCut Playhead & Scrubber Needle -->
                <div
                  v-if="masterDuration > 0"
                  class="capcut-playhead"
                  :style="{ left: `${playheadPercentage}%` }"
                  @mousedown.stop="onPlayheadMouseDown"
                  @touchstart.stop="onPlayheadTouchStart"
                >
                  <!-- Playhead Head / Pin -->
                  <div class="playhead-pin" title="Drag playhead to scrub anywhere">
                    <div class="pin-badge font-mono">{{ formattedCurrentTime }}</div>
                    <div class="pin-shape"></div>
                  </div>

                  <!-- Playhead Laser Line slicing across tracks -->
                  <div class="playhead-line"></div>
                </div>
              </div>
            </div>

            <!-- Keyboard Shortcuts & Editing Hint -->
            <div class="timeline-hints d-flex align-center justify-space-between mt-2 px-1 text-grey" style="font-size: 10px;">
              <div class="d-flex align-center gap-3">
                <span><kbd class="kbd-key">Space</kbd> Play / Pause</span>
                <span><kbd class="kbd-key">S</kbd> Split (✂️)</span>
                <span><kbd class="kbd-key">Del</kbd> Ripple Delete</span>
                <span><kbd class="kbd-key">←</kbd> <kbd class="kbd-key">→</kbd> Scrub 1s</span>
              </div>
              <div>
                <span class="text-purple-accent-2">Tip:</span> Drag clip left/right edges to trim start & end handles
              </div>
            </div>
          </div>
        </main>
      </div>

      <!-- 2. Exported Video Result Screen -->
      <div v-else class="result-container px-6 py-8">
        <div class="max-w-4xl mx-auto">
          <div class="mb-6">
            <h2 class="text-h4 font-weight-black gradient-title d-flex align-center">
              <v-icon icon="mdi-check-decagram" color="success" class="mr-3" size="36"></v-icon>
              Compilation Ready!
            </h2>
            <p class="text-body-2 text-grey-lighten-1 mb-0">Your high-definition music video is compiled and ready to download or publish.</p>
          </div>

          <div class="final-video-card glass-panel mb-6 overflow-hidden">
            <video :src="videoUrl" controls class="final-video-player" autoplay></video>
          </div>

          <!-- Bottom Action Buttons: Download MP4 + Re-Customize (3rd button) + New Project -->
          <div class="d-flex align-center justify-center flex-wrap gap-4 mb-8">
            <!-- 1. Download Video -->
            <v-btn
              color="primary"
              size="large"
              prepend-icon="mdi-download"
              class="export-btn px-8 rounded-pill font-weight-bold text-none"
              elevation="6"
              @click="downloadVideo"
            >
              Download MP4
            </v-btn>

            <!-- 2. The Requested 3rd Button: Re-Customize without clearing files -->
            <v-btn
              size="large"
              class="re-customize-btn px-8 rounded-pill font-weight-bold text-none"
              elevation="6"
              @click="reCustomizeProject('media')"
              title="Return to Studio keeping all video/audio files, slide transitions, and timeline cuts intact"
            >
              <v-icon icon="mdi-tune-vertical" class="mr-2"></v-icon>
              Re-Customize Project
            </v-btn>

            <!-- 3. New Project (with safety confirmation) -->
            <v-btn
              variant="outlined"
              color="grey-lighten-2"
              size="large"
              prepend-icon="mdi-plus-circle-outline"
              class="rounded-pill text-none"
              @click="openNewProjectConfirm"
              title="Clear all files and start a brand new project"
            >
              New Project
            </v-btn>
          </div>

          <!-- YouTube & TikTok Uploaders Directly Integrated -->
          <v-row v-if="videoPath">
            <v-col cols="12" md="6">
              <div class="glass-panel p-4 h-100">
                <YoutubeUploader :videoPath="videoPath" />
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="glass-panel p-4 h-100">
                <TiktokUploader :videoPath="videoPath" />
              </div>
            </v-col>
          </v-row>
        </div>
      </div>
    </div>

    <!-- Processing Overlay Modal -->
    <v-overlay
      :model-value="isGenerating"
      class="align-center justify-center"
      persistent
      scrim="black"
    >
      <v-card class="processing-card px-8 py-6 text-center" elevation="24" width="420">
        <div class="mb-4">
          <v-progress-circular
            :model-value="currentProgress"
            color="purple-accent-2"
            size="110"
            width="8"
          >
            <span class="text-h4 font-weight-bold text-white">{{ currentProgress }}%</span>
          </v-progress-circular>
        </div>
        
        <h3 class="text-h6 font-weight-bold text-white mb-1">Rendering Compilation</h3>
        <p class="text-caption text-purple-lighten-3 mb-6 status-text">{{ currentStatus || 'Processing media...' }}</p>
        
        <v-btn
          color="error"
          variant="tonal"
          @click="cancelGeneration"
          prepend-icon="mdi-close-circle"
          class="text-none rounded-pill"
          :disabled="currentProgress >= 100"
        >
          Cancel Rendering
        </v-btn>
      </v-card>
    </v-overlay>

    <!-- New Project Safety Confirmation Dialog -->
    <v-dialog v-model="confirmNewProjectDialog" max-width="500" persistent>
      <v-card class="glass-panel p-5 border-purple-20" rounded="xl" style="background: rgba(15, 23, 42, 0.96) !important; border: 1px solid rgba(192, 132, 252, 0.25);">
        <div class="d-flex align-center gap-3 mb-2">
          <v-avatar color="amber-darken-3" size="42" class="elevation-4">
            <v-icon icon="mdi-alert-circle-outline" color="white" size="26"></v-icon>
          </v-avatar>
          <div>
            <div class="text-h6 font-weight-bold text-white">Start New Project?</div>
            <div class="text-caption text-grey-lighten-1">Please confirm before resetting your workspace</div>
          </div>
        </div>

        <v-card-text class="px-0 py-3 text-body-2 text-grey-lighten-2">
          Starting a new project will <strong class="text-white">permanently clear all uploaded video/image files, audio tracks, and timeline cuts</strong>.
          
          <div class="mt-3 p-3 rounded-lg bg-black-25 border border-purple-20 text-caption">
            <div class="d-flex align-center gap-1 text-purple-accent-2 font-weight-bold mb-1">
              <v-icon icon="mdi-lightbulb-on-outline" size="16"></v-icon>
              Want to adjust slide transitions, timing, or audio?
            </div>
            <div class="text-grey-lighten-1">
              Click <strong class="text-white">"Re-Customize Instead"</strong>! All your uploaded media files, trims, transitions, and timer will stay 100% intact so you can tweak and re-export anytime.
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="px-0 pt-2 d-flex justify-space-between flex-wrap gap-2">
          <v-btn
            variant="flat"
            color="purple-accent-2"
            class="rounded-pill text-none font-weight-bold px-4"
            prepend-icon="mdi-movie-edit"
            @click="confirmNewProjectDialog = false; reCustomizeProject('media')"
          >
            Re-Customize Instead
          </v-btn>

          <div class="d-flex gap-2">
            <v-btn
              variant="text"
              color="grey-lighten-1"
              class="rounded-pill text-none"
              @click="confirmNewProjectDialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
              variant="tonal"
              color="error"
              class="rounded-pill text-none font-weight-bold"
              prepend-icon="mdi-delete-sweep-outline"
              @click="confirmNewProjectDialog = false; resetMixer()"
            >
              Clear & Start New
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar Notifications -->
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
          <div class="font-weight-bold text-subtitle-2">{{ snackbar.title }}</div>
          <div class="text-caption opacity-90">{{ snackbar.message }}</div>
        </div>
      </div>
      <template v-slot:actions>
        <v-btn icon="mdi-close" variant="text" size="small" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import { useMediaApi } from "~/composables/useMediaApi";

definePageMeta({
  layout: "video",
});

// UI State
const activeTab = ref("media");
const isDraggingVideo = ref(false);
const isDraggingAudio = ref(false);
const showSafeGuides = ref(false);
const aspectRatioMode = ref("16:9");

// Layout & Inspector Scroll State
const inspectorPanelRef = ref(null);
const isVisualsCollapsed = ref(false);
const isAudioCollapsed = ref(false);
const isNearAudioSection = ref(false);

function onInspectorScroll(e) {
  const el = e?.target || inspectorPanelRef.value;
  if (!el) return;
  isNearAudioSection.value = el.scrollTop > 140;
}

function scrollToMediaSection(section) {
  if (!inspectorPanelRef.value) return;
  if (section === 'audio') {
    isAudioCollapsed.value = false;
    setTimeout(() => {
      const audioEl = inspectorPanelRef.value?.querySelector('#audio-playlist-section');
      if (audioEl) {
        audioEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        inspectorPanelRef.value?.scrollTo({ top: inspectorPanelRef.value.scrollHeight, behavior: 'smooth' });
      }
    }, 50);
  } else {
    isVisualsCollapsed.value = false;
    inspectorPanelRef.value.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function toggleMediaScroll() {
  if (isNearAudioSection.value) {
    scrollToMediaSection('visuals');
  } else {
    scrollToMediaSection('audio');
  }
}

// Inputs & DOM refs
const videoInput = ref(null);
const audioInput = ref(null);
const previewBoxRef = ref(null);
const previewVideoRef = ref(null);
const timelineContainerRef = ref(null);

// CapCut Multi-Track Clips State
// Each clip: { id, file, name, title, isImage, originalDuration, trimStart, trimEnd, expanded }
const audioClips = ref([]);
const videoClips = ref([]);
const selectedTimelineClip = ref({ type: "audio", index: 0, id: null });

// Global Scrubber & Timeline Navigation
const globalPlayheadTime = ref(0); // in seconds across whole project
const isScrubbing = ref(false);
const timelineZoom = ref(1); // 1x, 1.5x, 2x, 2.5x, 3x
const activeHandleDrag = ref(null); // bottom timeline handle drag state
const inspectorHandleDrag = ref(null); // inspector trimmer handle drag state

// Backward-compatible legacy refs (mirrored for any existing consumers)
const videoFiles = ref([]);
const videoPreviewUrl = ref(null);
const videoTrims = ref([]);
const audioFiles = ref([]);
const trackDurations = ref([]);
const audioTrims = ref([]);
const audioElements = ref([]);

// Playback Engine State
const isPlaying = ref(false);
const currentTrackIndex = ref(0);
const currentTime = ref(0); // internal timestamp in currently loaded audio source
const volume = ref(0.8);
const isMuted = ref(false);
let activeAudio = null;
let playbackTimer = null;
let currentBgImageIndex = ref(0);
let bgSlideInterval = null;

// Settings & Overlays State
const outputResolution = ref("1280:720");
const resolutionOptions = [
  { title: "16:9 Landscape (HD)", value: "1280:720", icon: "mdi-monitor" },
  { title: "16:9 Landscape (FHD)", value: "1920:1080", icon: "mdi-monitor-screenshot" },
  { title: "9:16 Portrait (TikTok/Reels)", value: "720:1280", icon: "mdi-cellphone" },
  { title: "9:16 Portrait (FHD)", value: "1080:1920", icon: "mdi-cellphone-screenshot" },
  { title: "1:1 Square (Instagram)", value: "1080:1080", icon: "mdi-crop-square" },
];

const keepOriginalAudio = ref(false);
const showNowPlaying = ref(true);
const playlistPos = ref({ x: 5, y: 7 });
const playlistFontSize = ref(28);
const playlistItemsPerCol = ref(15);
const playlistColGap = ref(380);

// Timer Overlay State: Default mode set to 'persong' (Per-Song Countdown)
const overlayTimer = ref({
  enabled: true,
  mode: "persong", // Requirement 1: Default to 'persong' (Per-Song Countdown)
  minutes: 25,
  withBreak: false,
  breakMinutes: 5,
  fontSize: 48,
});
const timerPos = ref({ x: 84, y: 7 });

const bgImageDuration = ref(10);
const bgTransitionDuration = ref(1);
const photoMotion = ref("alternate");
const photoZoomIntensity = ref(0.15);

// Transition Options & State
const transitionOptions = [
  { title: "Smooth Crossfade", value: "fade", icon: "mdi-blur" },
  { title: "Fade to Black", value: "fadeblack", icon: "mdi-moon-waning-crescent" },
  { title: "Fade to White", value: "fadewhite", icon: "mdi-white-balance-sunny" },
  { title: "Wipe Left", value: "wipeleft", icon: "mdi-format-horizontal-align-left" },
  { title: "Wipe Right", value: "wiperight", icon: "mdi-format-horizontal-align-right" },
  { title: "Iris Circle Crop", value: "circlecrop", icon: "mdi-record-circle-outline" },
  { title: "Square Box Crop", value: "rectcrop", icon: "mdi-square-outline" },
  { title: "Fly Away Warp", value: "distance", icon: "mdi-rocket-launch-outline" },
  { title: "Clock Sweep", value: "radial", icon: "mdi-clock-outline" },
  { title: "Retro Pixelize", value: "pixelize", icon: "mdi-checkerboard" },
  { title: "Horizontal Blur", value: "hblur", icon: "mdi-blur-linear" },
  { title: "None (Hard Cut)", value: "none", icon: "mdi-format-horizontal-align-center" },
];

const selectedTransitions = ref(["fade"]);
const likesAllTransitions = computed(() => selectedTransitions.value.length === transitionOptions.length);
const likesSomeTransitions = computed(() => selectedTransitions.value.length > 0 && !likesAllTransitions.value);

const toggleAllTransitions = () => {
  if (likesAllTransitions.value) {
    selectedTransitions.value = [];
  } else {
    selectedTransitions.value = transitionOptions.map((t) => t.value);
  }
};

// Drag State for Canvas Overlays
const draggingElement = ref(null);

// Generation / Export State
const isGenerating = ref(false);
const currentProgress = ref(0);
const currentStatus = ref("");
const currentJobId = ref(null);
const videoUrl = ref(null);
const videoPath = ref(null);
let eventSource = null;

const snackbar = ref({
  show: false,
  color: "success",
  icon: "mdi-check-circle",
  title: "",
  message: "",
  timeout: 6000,
});

// Helper: Synchronize legacy refs with clips array
function syncLegacyRefs() {
  audioFiles.value = audioClips.value.map((c) => c.file);
  trackDurations.value = audioClips.value.map((c) => c.originalDuration || 180);
  audioTrims.value = audioClips.value.map((c) => ({
    start: Number(c.trimStart || 0),
    end: Number(c.trimEnd || c.originalDuration || 0),
    expanded: !!c.expanded,
  }));

  videoFiles.value = videoClips.value.map((c) => c.file);
  videoTrims.value = videoClips.value.map((c) => ({
    start: Number(c.trimStart || 0),
    end: Number(c.trimEnd || c.originalDuration || 0),
    expanded: !!c.expanded,
  }));
}

// Effective Duration Calculations
function getAudioEffectiveDuration(idx) {
  if (idx === undefined || idx < 0 || idx >= audioClips.value.length) return 0;
  const clip = audioClips.value[idx];
  if (!clip) return 0;
  const orig = clip.originalDuration || 180;
  const start = Number(clip.trimStart || 0);
  const end = Number(clip.trimEnd !== undefined && clip.trimEnd !== null ? clip.trimEnd : orig);
  return Math.max(0.1, end - start);
}

function getVideoEffectiveDuration(idx) {
  if (idx === undefined || idx < 0 || idx >= videoClips.value.length) return 10;
  const clip = videoClips.value[idx];
  if (!clip) return 10;
  if (clip.isImage) return Number(bgImageDuration.value || 10);
  const orig = clip.originalDuration || 10;
  const start = Number(clip.trimStart || 0);
  const end = Number(clip.trimEnd !== undefined && clip.trimEnd !== null ? clip.trimEnd : orig);
  return Math.max(0.1, end - start);
}

// Master Playlist & Timeline Durations
const totalPlaylistDuration = computed(() => {
  if (audioClips.value.length === 0) return 0;
  let total = 0;
  for (let i = 0; i < audioClips.value.length; i++) {
    total += getAudioEffectiveDuration(i);
  }
  return total;
});

const totalVisualDuration = computed(() => {
  if (videoClips.value.length === 0) return 0;
  let total = 0;
  for (let i = 0; i < videoClips.value.length; i++) {
    total += getVideoEffectiveDuration(i);
  }
  return total;
});

const masterDuration = computed(() => {
  if (totalPlaylistDuration.value > 0) return totalPlaylistDuration.value;
  if (totalVisualDuration.value > 0) return totalVisualDuration.value;
  return 0;
});

const formattedTotalDuration = computed(() => {
  const totalSec = Math.round(masterDuration.value);
  const mins = Math.floor(totalSec / 60);
  const secs = totalSec % 60;
  return `${mins}m ${secs < 10 ? "0" + secs : secs}s`;
});

const formattedCurrentTime = computed(() => {
  const sec = Math.floor(globalPlayheadTime.value);
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m < 10 ? "0" + m : m}:${s < 10 ? "0" + s : s}`;
});

const formattedActiveTrackDuration = computed(() => {
  const dur = Math.round(getAudioEffectiveDuration(currentTrackIndex.value));
  const m = Math.floor(dur / 60);
  const s = dur % 60;
  return `${m < 10 ? "0" + m : m}:${s < 10 ? "0" + s : s}`;
});

// Playhead Needle Percentage along timeline
const playheadPercentage = computed(() => {
  if (masterDuration.value <= 0) return 0;
  return Math.min(100, Math.max(0, (globalPlayheadTime.value / masterDuration.value) * 100));
});

// REQUIREMENT 1: Dynamic Countdown Timer Overlay
// Counts down from the current active song's effective edited duration to 00:00.
// Whenever a song is trimmed (handles) or split, recalculates dynamically in real time!
const liveTimerFormattedText = computed(() => {
  if (overlayTimer.value.mode === "pomodoro") {
    const totalSec = overlayTimer.value.minutes * 60;
    const remaining = isPlaying.value ? Math.max(0, totalSec - Math.floor(globalPlayheadTime.value)) : totalSec;
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    return `${m < 10 ? "0" + m : m}:${s < 10 ? "0" + s : s}`;
  } else {
    // Per-Song Countdown mode (Default)
    if (audioClips.value.length === 0) return "00:00";
    const activeClip = audioClips.value[currentTrackIndex.value];
    if (!activeClip) return "00:00";

    const effDur = getAudioEffectiveDuration(currentTrackIndex.value);
    const trimStart = activeClip.trimStart || 0;
    const elapsedInClip = Math.max(0, currentTime.value - trimStart);
    const remaining = Math.max(0, Math.round(effDur - elapsedInClip));

    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    return `${m < 10 ? "0" + m : m}:${s < 10 ? "0" + s : s}`;
  }
});

// Dynamic Timeline Ruler Ticks
const timelineRulerTicks = computed(() => {
  const total = masterDuration.value;
  if (total <= 0) {
    return [{ percent: 0, label: "00:00" }, { percent: 100, label: "00:00" }];
  }

  // Choose interval based on duration and zoom
  let step = 10;
  if (total > 600) step = 60;
  else if (total > 300) step = 30;
  else if (total > 120) step = 15;
  else if (total > 60) step = 10;
  else step = 5;

  if (timelineZoom.value > 1.5) step = Math.max(2, Math.floor(step / 2));

  const ticks = [];
  for (let sec = 0; sec <= total; sec += step) {
    const pct = (sec / total) * 100;
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    const label = `${m < 10 ? "0" + m : m}:${s < 10 ? "0" + s : s}`;
    ticks.push({ percent: pct, label });
  }
  return ticks;
});

const canDeleteSelectedClip = computed(() => {
  const type = selectedTimelineClip.value.type || "audio";
  const list = type === "audio" ? audioClips.value : videoClips.value;
  return list.length > 0 && selectedTimelineClip.value.index >= 0 && selectedTimelineClip.value.index < list.length;
});

const activeResolutionLabel = computed(() => {
  const found = resolutionOptions.find((r) => r.value === outputResolution.value);
  return found ? found.title : outputResolution.value;
});

const isBackgroundImg = computed(() => {
  if (videoClips.value.length === 0) return false;
  const target = videoClips.value[currentBgImageIndex.value % videoClips.value.length];
  return target?.isImage ?? false;
});

const hasImageBackgrounds = computed(() => {
  return videoClips.value.some((c) => c.isImage);
});

const currentBgImageSrc = computed(() => {
  if (videoClips.value.length === 0) return null;
  const target = videoClips.value[currentBgImageIndex.value % videoClips.value.length];
  if (!target || !target.file) return null;
  return URL.createObjectURL(target.file);
});

const previewMotionClass = computed(() => {
  if (!isBackgroundImg.value || photoMotion.value === 'none') return '';
  if (videoClips.value.length === 1) {
    if (photoMotion.value === 'alternate') return 'ken-burns-breathe';
    if (photoMotion.value === 'in') return 'ken-burns-in';
    if (photoMotion.value === 'out') return 'ken-burns-out';
  }
  if (photoMotion.value === 'alternate') {
    return currentBgImageIndex.value % 2 === 0 ? 'ken-burns-in' : 'ken-burns-out';
  }
  return photoMotion.value === 'in' ? 'ken-burns-in' : 'ken-burns-out';
});

const previewMotionStyle = computed(() => {
  if (!isBackgroundImg.value || photoMotion.value === 'none') return {};
  const duration = videoClips.value.length === 1 && photoMotion.value === 'alternate'
    ? 12
    : Math.max(2, Number(bgImageDuration.value || 10));
  const scaleVal = (1 + Number(photoZoomIntensity.value || 0.15)).toFixed(2);
  return {
    '--kb-scale': scaleVal,
    '--kb-duration': `${duration}s`,
    'animationPlayState': isPlaying.value ? 'running' : 'paused'
  };
});

const previewPlaylist = computed(() => {
  if (audioClips.value.length > 0) {
    return audioClips.value.map((c) => ({
      title: c.title || getCleanSongTitle(c.name),
    }));
  }
  return [
    { title: "Lofi Study Beats - Chilled Afternoon" },
    { title: "Coffee & Code Session - Track 02" },
    { title: "Midnight Rainfall & Piano Chill" },
    { title: "Ambient Workspace Harmony" },
  ];
});

const canvasRatioClass = computed(() => {
  if (outputResolution.value.includes("720:1280") || outputResolution.value.includes("1080:1920")) {
    return "ratio-portrait";
  }
  if (outputResolution.value.includes("1080:1080")) {
    return "ratio-square";
  }
  return "ratio-landscape";
});

const previewScale = computed(() => {
  if (aspectRatioMode.value === "9:16") {
    return 270 / 720;
  } else if (aspectRatioMode.value === "1:1") {
    return 460 / 1080;
  } else {
    // 16:9 Landscape monitor: ~854px vs 1280px standard base
    return 854 / 1280;
  }
});

const playlistElementStyle = computed(() => {
  const s = previewScale.value;
  return {
    left: `${playlistPos.value.x}%`,
    top: `${playlistPos.value.y}%`,
    fontSize: `${Math.max(10, Math.round(playlistFontSize.value * s * 0.72))}px`,
  };
});

const timerElementStyle = computed(() => {
  const s = previewScale.value;
  return {
    left: `${timerPos.value.x}%`,
    top: `${timerPos.value.y}%`,
    fontSize: `${Math.max(12, Math.round(overlayTimer.value.fontSize * s * 0.75))}px`,
  };
});

const canGenerate = computed(() => videoClips.value.length > 0 && audioClips.value.length > 0);

// Helper Methods
function getCleanSongTitle(filename) {
  if (!filename) return "Track";
  return filename.replace(/\.[^/.]+$/, "").replace(/^[0-9]+[\s._-]*/, "");
}

function formatTrackDuration(sec) {
  if (!sec && sec !== 0) return "--:--";
  const s = Math.round(sec);
  const m = Math.floor(s / 60);
  const rem = s % 60;
  return `${m}:${rem < 10 ? "0" + rem : rem}`;
}

function setAspectRatio(res) {
  outputResolution.value = res;
  if (res === "720:1280" || res === "1080:1920") aspectRatioMode.value = "9:16";
  else if (res === "1080:1080") aspectRatioMode.value = "1:1";
  else aspectRatioMode.value = "16:9";
}

function selectOutputResolution(res) {
  outputResolution.value = res;
  setAspectRatio(res);
  clampOverlayPositions();
}

function clampOverlayPositions() {
  const isPortrait = aspectRatioMode.value === "9:16";
  const isSquare = aspectRatioMode.value === "1:1";
  const maxTimerX = isPortrait ? 60 : (isSquare ? 72 : 84);
  if (timerPos.value.x > maxTimerX) {
    timerPos.value.x = maxTimerX;
  }
  const maxPlaylistX = isPortrait ? 50 : 70;
  if (playlistPos.value.x > maxPlaylistX) {
    playlistPos.value.x = maxPlaylistX;
  }
}

function setPlaylistPosition(x, y) {
  playlistPos.value = { x, y };
}

function setTimerPosition(x, y) {
  timerPos.value = { x, y };
}

function resetPositions() {
  const isPortrait = aspectRatioMode.value === "9:16";
  const isSquare = aspectRatioMode.value === "1:1";
  playlistPos.value = { x: 5, y: 7 };
  timerPos.value = { x: isPortrait ? 60 : (isSquare ? 72 : 84), y: 7 };
}

function snapToSafeGuides(mode = "action") {
  const isPortrait = aspectRatioMode.value === "9:16";
  const isSquare = aspectRatioMode.value === "1:1";
  if (mode === "title") {
    playlistPos.value = { x: 10, y: 10 };
    timerPos.value = { x: isPortrait ? 52 : (isSquare ? 65 : 78), y: 10 };
  } else {
    playlistPos.value = { x: 5, y: 7 };
    timerPos.value = { x: isPortrait ? 60 : (isSquare ? 72 : 84), y: 7 };
  }
}

// Media Ingestion & Upload
const handleVideoFiles = (files) => {
  const valid = files.filter((f) => f.type.startsWith("image/") || f.type.startsWith("video/"));
  if (valid.length > 0) {
    valid.forEach((file) => {
      const isImg = file.type.startsWith("image/");
      const clipId = "vc_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6);
      const newClip = {
        id: clipId,
        file: file,
        name: file.name,
        title: file.name,
        isImage: isImg,
        originalDuration: isImg ? (bgImageDuration.value || 10) : 10,
        trimStart: 0,
        trimEnd: isImg ? (bgImageDuration.value || 10) : 10,
        expanded: false,
      };
      videoClips.value.push(newClip);

      if (!isImg) {
        const url = URL.createObjectURL(file);
        const tempVid = document.createElement("video");
        tempVid.src = url;
        tempVid.addEventListener("loadedmetadata", () => {
          const dur = tempVid.duration || 10;
          newClip.originalDuration = dur;
          if (newClip.trimEnd === 10 || newClip.trimEnd > dur) {
            newClip.trimEnd = dur;
          }
          URL.revokeObjectURL(url);
          syncLegacyRefs();
        });
      }
    });
    syncLegacyRefs();
    updateVideoPreviewUrl();
  }
};

const onDropVideo = (e) => {
  isDraggingVideo.value = false;
  const dropped = Array.from(e.dataTransfer?.files || []);
  const visualFiles = dropped.filter((f) => f.type.startsWith("image/") || f.type.startsWith("video/"));
  const audioFilesList = dropped.filter((f) => f.type.startsWith("audio/"));

  if (visualFiles.length > 0) {
    handleVideoFiles(visualFiles);
  }
  if (audioFilesList.length > 0) {
    handleAudioFiles(audioFilesList);
    snackbar.value = {
      show: true,
      color: "info",
      icon: "mdi-playlist-music",
      title: "Audio Auto-Routed",
      message: `Detected and added ${audioFilesList.length} song(s) to Audio Playlist.`,
      timeout: 3500,
    };
  }
};

const onSelectVideo = (e) => {
  handleVideoFiles(Array.from(e.target.files || []));
  e.target.value = "";
};

const handleAudioFiles = (files) => {
  const valid = files.filter((f) => f.type.startsWith("audio/"));
  if (valid.length > 0) {
    valid.forEach((file) => {
      const clipId = "ac_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6);
      const newClip = {
        id: clipId,
        file: file,
        name: file.name,
        title: getCleanSongTitle(file.name),
        originalDuration: 180,
        trimStart: 0,
        trimEnd: 180,
        expanded: false,
      };
      audioClips.value.push(newClip);

      const url = URL.createObjectURL(file);
      const tempAudio = new Audio(url);
      tempAudio.addEventListener("loadedmetadata", () => {
        const dur = tempAudio.duration || 180;
        newClip.originalDuration = dur;
        if (newClip.trimEnd === 180 || newClip.trimEnd > dur) {
          newClip.trimEnd = dur;
        }
        URL.revokeObjectURL(url);
        syncLegacyRefs();
      });
      tempAudio.addEventListener("error", () => {
        URL.revokeObjectURL(url);
      });
    });
    syncLegacyRefs();
    isAudioCollapsed.value = false;
    scrollToMediaSection('audio');
  }
};

const onDropAudio = (e) => {
  isDraggingAudio.value = false;
  const dropped = Array.from(e.dataTransfer?.files || []);
  const audioFilesList = dropped.filter((f) => f.type.startsWith("audio/"));
  const visualFiles = dropped.filter((f) => f.type.startsWith("image/") || f.type.startsWith("video/"));

  if (audioFilesList.length > 0) {
    handleAudioFiles(audioFilesList);
  }
  if (visualFiles.length > 0) {
    handleVideoFiles(visualFiles);
    snackbar.value = {
      show: true,
      color: "info",
      icon: "mdi-image-multiple",
      title: "Visuals Auto-Routed",
      message: `Detected and added ${visualFiles.length} visual(s) to Background Visuals.`,
      timeout: 3500,
    };
  }
};

const onSelectAudio = (e) => {
  handleAudioFiles(Array.from(e.target.files || []));
  e.target.value = "";
};

const updateVideoPreviewUrl = () => {
  if (videoPreviewUrl.value) URL.revokeObjectURL(videoPreviewUrl.value);
  if (videoClips.value.length > 0) {
    videoPreviewUrl.value = URL.createObjectURL(videoClips.value[0].file);
  } else {
    videoPreviewUrl.value = null;
  }
};

// Reordering Clips
const moveClipUp = (type, idx) => {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  if (idx > 0) {
    const temp = list[idx];
    list[idx] = list[idx - 1];
    list[idx - 1] = temp;
    syncLegacyRefs();
    if (type === "video") updateVideoPreviewUrl();
  }
};

const moveClipDown = (type, idx) => {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  if (idx < list.length - 1) {
    const temp = list[idx];
    list[idx] = list[idx + 1];
    list[idx + 1] = temp;
    syncLegacyRefs();
    if (type === "video") updateVideoPreviewUrl();
  }
};

const moveAudioUp = (idx) => moveClipUp("audio", idx);
const moveAudioDown = (idx) => moveClipDown("audio", idx);
const moveVideoUp = (idx) => moveClipUp("video", idx);
const moveVideoDown = (idx) => moveClipDown("video", idx);

const clearVideo = () => {
  videoClips.value = [];
  syncLegacyRefs();
  updateVideoPreviewUrl();
};

const clearAudio = () => {
  stopMasterPlayback();
  audioClips.value = [];
  syncLegacyRefs();
  currentTrackIndex.value = 0;
  globalPlayheadTime.value = 0;
  currentTime.value = 0;
};

// REQUIREMENT 2: CAPCUT-STYLE TIMELINE EDITING

// 1. Playhead Interactive Dragging & Seeking
function seekToGlobalTime(targetSec) {
  const bounded = Math.max(0, Math.min(masterDuration.value || 0, targetSec));
  globalPlayheadTime.value = bounded;

  // Sync Audio Track
  if (audioClips.value.length > 0) {
    let accumulated = 0;
    for (let i = 0; i < audioClips.value.length; i++) {
      const effDur = getAudioEffectiveDuration(i);
      if (accumulated + effDur >= bounded || i === audioClips.value.length - 1) {
        currentTrackIndex.value = i;
        const offsetInClip = Math.max(0, bounded - accumulated);
        const targetFileTime = (audioClips.value[i].trimStart || 0) + offsetInClip;
        currentTime.value = targetFileTime;

        if (activeAudio) {
          activeAudio.currentTime = targetFileTime;
          if (isPlaying.value) {
            activeAudio.play().catch(() => {});
          }
        }
        break;
      }
      accumulated += effDur;
    }
  }

  // Sync Video Track
  if (previewVideoRef.value && !isBackgroundImg.value && videoClips.value.length > 0) {
    let vAccum = 0;
    for (let i = 0; i < videoClips.value.length; i++) {
      const vEff = getVideoEffectiveDuration(i);
      if (vAccum + vEff >= bounded || i === videoClips.value.length - 1) {
        const vOffset = Math.max(0, bounded - vAccum);
        const vTarget = (videoClips.value[i].trimStart || 0) + vOffset;
        previewVideoRef.value.currentTime = vTarget;
        break;
      }
      vAccum += vEff;
    }
  }
}

function getTimelineTimeFromClientX(clientX) {
  if (!timelineContainerRef.value || masterDuration.value <= 0) return 0;
  const rect = timelineContainerRef.value.getBoundingClientRect();
  const ratio = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
  return ratio * masterDuration.value;
}

function onTimelineClick(e) {
  seekToGlobalTime(getTimelineTimeFromClientX(e.clientX));
}

function onTimelineContainerMouseDown(e) {
  // If clicked directly on the track background, start scrubbing
  if (e.target.closest(".capcut-clip-handle") || e.target.closest(".clip-delete-btn")) return;
  onPlayheadMouseDown(e);
}

function onPlayheadMouseDown(e) {
  e.preventDefault();
  isScrubbing.value = true;
  seekToGlobalTime(getTimelineTimeFromClientX(e.clientX));

  const onMouseMove = (ev) => {
    if (!isScrubbing.value) return;
    seekToGlobalTime(getTimelineTimeFromClientX(ev.clientX));
  };

  const onMouseUp = () => {
    isScrubbing.value = false;
    window.removeEventListener("mousemove", onMouseMove);
    window.removeEventListener("mouseup", onMouseUp);
  };

  window.addEventListener("mousemove", onMouseMove);
  window.addEventListener("mouseup", onMouseUp);
}

function onPlayheadTouchStart(e) {
  if (!e.touches.length) return;
  isScrubbing.value = true;
  seekToGlobalTime(getTimelineTimeFromClientX(e.touches[0].clientX));

  const onTouchMove = (ev) => {
    if (!isScrubbing.value || !ev.touches.length) return;
    seekToGlobalTime(getTimelineTimeFromClientX(ev.touches[0].clientX));
  };

  const onTouchEnd = () => {
    isScrubbing.value = false;
    window.removeEventListener("touchmove", onTouchMove);
    window.removeEventListener("touchend", onTouchEnd);
  };

  window.addEventListener("touchmove", onTouchMove);
  window.addEventListener("touchend", onTouchEnd);
}

// 2. Drag In/Out Handles on Bottom Timeline
function onHandleMouseDown(e, type, index, handle) {
  e.stopPropagation();
  e.preventDefault();

  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[index];
  if (!clip) return;

  const rect = timelineContainerRef.value ? timelineContainerRef.value.getBoundingClientRect() : { width: 800 };
  const effectiveWidth = rect.width * (timelineZoom.value || 1);
  const pixelsPerSec = effectiveWidth / (masterDuration.value || 1);

  activeHandleDrag.value = {
    type,
    index,
    handle,
    startX: e.clientX,
    startTrimStart: clip.trimStart || 0,
    startTrimEnd: clip.trimEnd !== undefined ? clip.trimEnd : (clip.originalDuration || 180),
    pixelsPerSec: Math.max(1, pixelsPerSec),
  };

  const onMouseMove = (ev) => {
    if (!activeHandleDrag.value) return;
    const deltaX = ev.clientX - activeHandleDrag.value.startX;
    const deltaSec = deltaX / activeHandleDrag.value.pixelsPerSec;

    if (activeHandleDrag.value.handle === "in") {
      const maxIn = activeHandleDrag.value.startTrimEnd - 0.5;
      const newStart = Math.max(0, Math.min(maxIn, activeHandleDrag.value.startTrimStart + deltaSec));
      clip.trimStart = Math.round(newStart * 10) / 10;
      if (type === "audio" && activeAudio && currentTrackIndex.value === index) {
        activeAudio.currentTime = clip.trimStart;
        currentTime.value = clip.trimStart;
      }
    } else {
      const origDur = clip.originalDuration || 180;
      const minOut = activeHandleDrag.value.startTrimStart + 0.5;
      const newEnd = Math.max(minOut, Math.min(origDur, activeHandleDrag.value.startTrimEnd + deltaSec));
      clip.trimEnd = Math.round(newEnd * 10) / 10;
      if (type === "audio" && activeAudio && currentTrackIndex.value === index) {
        activeAudio.currentTime = clip.trimEnd;
        currentTime.value = clip.trimEnd;
      }
    }
    syncLegacyRefs();
  };

  const onMouseUp = () => {
    activeHandleDrag.value = null;
    window.removeEventListener("mousemove", onMouseMove);
    window.removeEventListener("mouseup", onMouseUp);
  };

  window.addEventListener("mousemove", onMouseMove);
  window.addEventListener("mouseup", onMouseUp);
}

function onHandleTouchStart(e, type, index, handle) {
  if (!e.touches.length) return;
  e.stopPropagation();

  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[index];
  if (!clip) return;

  const rect = timelineContainerRef.value ? timelineContainerRef.value.getBoundingClientRect() : { width: 800 };
  const effectiveWidth = rect.width * (timelineZoom.value || 1);
  const pixelsPerSec = effectiveWidth / (masterDuration.value || 1);

  activeHandleDrag.value = {
    type,
    index,
    handle,
    startX: e.touches[0].clientX,
    startTrimStart: clip.trimStart || 0,
    startTrimEnd: clip.trimEnd !== undefined ? clip.trimEnd : (clip.originalDuration || 180),
    pixelsPerSec: Math.max(1, pixelsPerSec),
  };

  const onTouchMove = (ev) => {
    if (!activeHandleDrag.value || !ev.touches.length) return;
    const deltaX = ev.touches[0].clientX - activeHandleDrag.value.startX;
    const deltaSec = deltaX / activeHandleDrag.value.pixelsPerSec;

    if (activeHandleDrag.value.handle === "in") {
      const maxIn = activeHandleDrag.value.startTrimEnd - 0.5;
      const newStart = Math.max(0, Math.min(maxIn, activeHandleDrag.value.startTrimStart + deltaSec));
      clip.trimStart = Math.round(newStart * 10) / 10;
    } else {
      const origDur = clip.originalDuration || 180;
      const minOut = activeHandleDrag.value.startTrimStart + 0.5;
      const newEnd = Math.max(minOut, Math.min(origDur, activeHandleDrag.value.startTrimEnd + deltaSec));
      clip.trimEnd = Math.round(newEnd * 10) / 10;
    }
    syncLegacyRefs();
  };

  const onTouchEnd = () => {
    activeHandleDrag.value = null;
    window.removeEventListener("touchmove", onTouchMove);
    window.removeEventListener("touchend", onTouchEnd);
  };

  window.addEventListener("touchmove", onTouchMove);
  window.addEventListener("touchend", onTouchEnd);
}

// 3. Drag In/Out Handles in Inspector Waveform Bar
function onInspectorHandleMouseDown(e, type, index, handle) {
  e.stopPropagation();
  e.preventDefault();

  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[index];
  if (!clip) return;

  const targetTrack = e.currentTarget.closest(".clip-trimmer-track");
  const trackWidth = targetTrack ? targetTrack.clientWidth : 280;
  const origDur = clip.originalDuration || 180;
  const pixelsPerSec = trackWidth / origDur;

  inspectorHandleDrag.value = {
    type,
    index,
    handle,
    startX: e.clientX,
    startTrimStart: clip.trimStart || 0,
    startTrimEnd: clip.trimEnd !== undefined ? clip.trimEnd : origDur,
    pixelsPerSec: Math.max(1, pixelsPerSec),
  };

  const onMouseMove = (ev) => {
    if (!inspectorHandleDrag.value) return;
    const deltaSec = (ev.clientX - inspectorHandleDrag.value.startX) / inspectorHandleDrag.value.pixelsPerSec;

    if (inspectorHandleDrag.value.handle === "in") {
      const maxIn = inspectorHandleDrag.value.startTrimEnd - 0.5;
      const newStart = Math.max(0, Math.min(maxIn, inspectorHandleDrag.value.startTrimStart + deltaSec));
      clip.trimStart = Math.round(newStart * 10) / 10;
    } else {
      const minOut = inspectorHandleDrag.value.startTrimStart + 0.5;
      const newEnd = Math.max(minOut, Math.min(origDur, inspectorHandleDrag.value.startTrimEnd + deltaSec));
      clip.trimEnd = Math.round(newEnd * 10) / 10;
    }
    syncLegacyRefs();
  };

  const onMouseUp = () => {
    inspectorHandleDrag.value = null;
    window.removeEventListener("mousemove", onMouseMove);
    window.removeEventListener("mouseup", onMouseUp);
  };

  window.addEventListener("mousemove", onMouseMove);
  window.addEventListener("mouseup", onMouseUp);
}

function onInspectorHandleTouchStart(e, type, index, handle) {
  if (!e.touches.length) return;
  onInspectorHandleMouseDown(
    {
      clientX: e.touches[0].clientX,
      stopPropagation: () => e.stopPropagation(),
      preventDefault: () => e.preventDefault(),
      currentTarget: e.currentTarget,
    },
    type,
    index,
    handle
  );
}

// 4. Split Clip at Current Playhead (✂️)
function splitClipAtPlayhead(forceType = null) {
  const targetType = forceType || selectedTimelineClip.value.type || "audio";
  const list = targetType === "audio" ? audioClips.value : videoClips.value;

  if (list.length === 0) {
    snackbar.value = {
      show: true,
      color: "warning",
      icon: "mdi-alert-circle",
      title: "No Clip to Split",
      message: "Please add media tracks to the timeline first.",
      timeout: 3000,
    };
    return;
  }

  // Find which clip spans globalPlayheadTime
  let accumulated = 0;
  let targetIdx = -1;
  let offsetInClip = 0;

  for (let i = 0; i < list.length; i++) {
    const effDur = targetType === "audio" ? getAudioEffectiveDuration(i) : getVideoEffectiveDuration(i);
    if (globalPlayheadTime.value >= accumulated && globalPlayheadTime.value <= accumulated + effDur) {
      targetIdx = i;
      offsetInClip = globalPlayheadTime.value - accumulated;
      break;
    }
    accumulated += effDur;
  }

  if (targetIdx === -1) {
    targetIdx = list.length - 1;
    offsetInClip = targetType === "audio" ? getAudioEffectiveDuration(targetIdx) : getVideoEffectiveDuration(targetIdx);
  }

  const clip = list[targetIdx];
  const sourceSplitTime = (clip.trimStart || 0) + offsetInClip;
  const currentEnd = clip.trimEnd !== undefined ? clip.trimEnd : (clip.originalDuration || 180);

  // Check split boundary distance
  if (sourceSplitTime <= (clip.trimStart || 0) + 0.3 || sourceSplitTime >= currentEnd - 0.3) {
    snackbar.value = {
      show: true,
      color: "info",
      icon: "mdi-information-outline",
      title: "Cannot Split Here",
      message: "Move the playhead at least 0.5s inside the clip to split.",
      timeout: 3500,
    };
    return;
  }

  // Segment 2 (second half)
  const newClip = {
    id: (targetType === "audio" ? "aclip_" : "vclip_") + Date.now() + "_" + Math.random().toString(36).substr(2, 6),
    file: clip.file,
    name: clip.name,
    title: clip.title ? `${clip.title} (Part 2)` : clip.name,
    isImage: clip.isImage || false,
    originalDuration: clip.originalDuration,
    trimStart: Math.round(sourceSplitTime * 10) / 10,
    trimEnd: currentEnd,
    expanded: false,
  };

  // Truncate Segment 1 (first half)
  clip.trimEnd = Math.round(sourceSplitTime * 10) / 10;

  // Insert Segment 2 right after Segment 1 (Contiguous, zero gap)
  list.splice(targetIdx + 1, 0, newClip);

  // Auto-select Segment 2
  selectedTimelineClip.value = {
    type: targetType,
    index: targetIdx + 1,
    id: newClip.id,
  };

  syncLegacyRefs();

  snackbar.value = {
    show: true,
    color: "#8b5cf6",
    icon: "mdi-content-cut",
    title: "✂️ Clip Split Successfully",
    message: `Split at ${formatTrackDuration(globalPlayheadTime.value)}. You can now edit, trim, or delete either segment.`,
    timeout: 3500,
  };
}

// 5. Ripple Delete: Remove clip and automatically shift remaining segments
function deleteClip(type, index) {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  if (!list.length || index < 0 || index >= list.length) return;

  const deletedDur = type === "audio" ? getAudioEffectiveDuration(index) : getVideoEffectiveDuration(index);

  // Remove segment (Ripple delete: subsequent clips slide left automatically)
  list.splice(index, 1);
  syncLegacyRefs();

  // If deleted currently playing audio track, adjust playback
  if (type === "audio") {
    if (isPlaying.value) {
      if (list.length === 0) {
        stopMasterPlayback();
      } else {
        const nextIdx = Math.min(index, list.length - 1);
        currentTrackIndex.value = nextIdx;
        currentTime.value = list[nextIdx].trimStart || 0;
        loadAndPlayCurrentTrack();
      }
    } else {
      if (currentTrackIndex.value >= list.length) {
        currentTrackIndex.value = Math.max(0, list.length - 1);
      }
    }
  }

  // Update selected index
  if (list.length > 0) {
    const newIdx = Math.min(index, list.length - 1);
    selectedTimelineClip.value = {
      type,
      index: newIdx,
      id: list[newIdx].id,
    };
  } else {
    selectedTimelineClip.value = { type, index: 0, id: null };
  }

  // Adjust playhead bounds
  if (globalPlayheadTime.value > masterDuration.value) {
    globalPlayheadTime.value = masterDuration.value;
  }

  snackbar.value = {
    show: true,
    color: "#334155",
    icon: "mdi-delete-sweep",
    title: "Ripple Delete",
    message: `Segment removed (-${deletedDur.toFixed(1)}s). Timeline shifted automatically.`,
    timeout: 3000,
  };
}

function deleteSelectedClip() {
  const type = selectedTimelineClip.value.type || "audio";
  const idx = selectedTimelineClip.value.index ?? -1;
  deleteClip(type, idx);
}

// Cut Points Navigation
function jumpToPrevCut() {
  const list = audioClips.value;
  if (!list.length) return;

  let accum = 0;
  let target = 0;
  for (let i = 0; i < list.length; i++) {
    const dur = getAudioEffectiveDuration(i);
    if (accum + dur >= globalPlayheadTime.value - 0.2) {
      target = accum;
      break;
    }
    accum += dur;
  }
  seekToGlobalTime(target);
}

function jumpToNextCut() {
  const list = audioClips.value;
  if (!list.length) return;

  let accum = 0;
  let target = masterDuration.value;
  for (let i = 0; i < list.length; i++) {
    const dur = getAudioEffectiveDuration(i);
    accum += dur;
    if (accum > globalPlayheadTime.value + 0.2) {
      target = accum;
      break;
    }
  }
  seekToGlobalTime(target);
}

// Trimming Helpers (Inspector Panel)
function resetClipTrim(type, idx) {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[idx];
  if (clip) {
    clip.trimStart = 0;
    clip.trimEnd = clip.originalDuration || (clip.isImage ? bgImageDuration.value : 180);
    syncLegacyRefs();
  }
}

function setClipTrimStart(type, idx, val) {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[idx];
  if (clip) {
    const maxVal = (clip.trimEnd || clip.originalDuration || 180) - 0.5;
    clip.trimStart = Math.max(0, Math.min(maxVal, Math.round(val * 10) / 10));
    syncLegacyRefs();
  }
}

function setClipTrimEnd(type, idx, val) {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[idx];
  if (clip) {
    const minVal = (clip.trimStart || 0) + 0.5;
    const maxVal = clip.originalDuration || 180;
    clip.trimEnd = Math.max(minVal, Math.min(maxVal, Math.round(val * 10) / 10));
    syncLegacyRefs();
  }
}

function setClipStartToPlayhead(type, idx) {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[idx];
  if (!clip) return;

  // Find clip global start
  let accum = 0;
  for (let i = 0; i < idx; i++) {
    accum += type === "audio" ? getAudioEffectiveDuration(i) : getVideoEffectiveDuration(i);
  }
  const offset = Math.max(0, globalPlayheadTime.value - accum);
  const newStart = (clip.trimStart || 0) + offset;
  setClipTrimStart(type, idx, newStart);
}

function setClipEndToPlayhead(type, idx) {
  const list = type === "audio" ? audioClips.value : videoClips.value;
  const clip = list[idx];
  if (!clip) return;

  let accum = 0;
  for (let i = 0; i < idx; i++) {
    accum += type === "audio" ? getAudioEffectiveDuration(i) : getVideoEffectiveDuration(i);
  }
  const offset = Math.max(0.5, globalPlayheadTime.value - accum);
  const newEnd = (clip.trimStart || 0) + offset;
  setClipTrimEnd(type, idx, newEnd);
}

function auditionClip(type, idx) {
  if (type !== "audio" || idx < 0 || idx >= audioClips.value.length) return;
  currentTrackIndex.value = idx;
  const clip = audioClips.value[idx];
  currentTime.value = clip.trimStart || 0;

  // Compute global start
  let accum = 0;
  for (let i = 0; i < idx; i++) {
    accum += getAudioEffectiveDuration(i);
  }
  globalPlayheadTime.value = accum;

  isPlaying.value = true;
  loadAndPlayCurrentTrack();
}

function selectAndInspectClip(type, idx) {
  selectedTimelineClip.value = {
    type,
    index: idx,
    id: (type === "audio" ? audioClips.value[idx]?.id : videoClips.value[idx]?.id) || null,
  };
  activeTab.value = "timeline";
  if (type === "audio") {
    playTrack(idx);
  }
}

// Playback Engine Implementation
function toggleMasterPlayback() {
  if (isPlaying.value) {
    pausePlayback();
  } else {
    startPlayback();
  }
}

function startPlayback() {
  if (audioClips.value.length === 0 && videoClips.value.length === 0) return;
  isPlaying.value = true;

  // 1. Play Background Video
  if (previewVideoRef.value && !isBackgroundImg.value) {
    previewVideoRef.value.play().catch(() => {});
  }

  // 2. Start Image Slideshow
  if (isBackgroundImg.value && videoClips.value.length > 1) {
    if (bgSlideInterval) clearInterval(bgSlideInterval);
    bgSlideInterval = setInterval(() => {
      currentBgImageIndex.value = (currentBgImageIndex.value + 1) % videoClips.value.length;
    }, Math.max(2, bgImageDuration.value) * 1000);
  }

  // 3. Play Current Audio Track
  if (audioClips.value.length > 0) {
    loadAndPlayCurrentTrack();
  }
}

function pausePlayback() {
  isPlaying.value = false;
  if (previewVideoRef.value) previewVideoRef.value.pause();
  if (activeAudio) activeAudio.pause();
  if (bgSlideInterval) {
    clearInterval(bgSlideInterval);
    bgSlideInterval = null;
  }
}

function stopMasterPlayback() {
  pausePlayback();
  globalPlayheadTime.value = 0;
  currentTrackIndex.value = 0;
  currentTime.value = audioClips.value[0]?.trimStart || 0;
  if (activeAudio) {
    activeAudio.currentTime = currentTime.value;
  }
}

function playTrack(idx) {
  if (idx < 0 || idx >= audioClips.value.length) return;
  currentTrackIndex.value = idx;
  const clip = audioClips.value[idx];
  currentTime.value = clip.trimStart || 0;

  // Seek global playhead
  let accum = 0;
  for (let i = 0; i < idx; i++) {
    accum += getAudioEffectiveDuration(i);
  }
  globalPlayheadTime.value = accum;

  startPlayback();
}

function toggleTrackPlayback(idx) {
  if (currentTrackIndex.value === idx && isPlaying.value) {
    pausePlayback();
  } else {
    playTrack(idx);
  }
}

function prevTrack() {
  if (audioClips.value.length === 0) return;
  const newIdx = currentTrackIndex.value > 0 ? currentTrackIndex.value - 1 : audioClips.value.length - 1;
  playTrack(newIdx);
}

function nextTrack() {
  if (audioClips.value.length === 0) return;
  const newIdx = (currentTrackIndex.value + 1) % audioClips.value.length;
  playTrack(newIdx);
}

function loadAndPlayCurrentTrack() {
  if (activeAudio) {
    activeAudio.pause();
    activeAudio.removeEventListener("timeupdate", onAudioTimeUpdate);
    activeAudio.removeEventListener("ended", onAudioEnded);
  }

  const clip = audioClips.value[currentTrackIndex.value];
  if (!clip || !clip.file) return;

  const url = URL.createObjectURL(clip.file);
  activeAudio = new Audio(url);
  activeAudio.volume = isMuted.value ? 0 : volume.value;

  const trimStart = clip.trimStart || 0;
  if (currentTime.value < trimStart) {
    currentTime.value = trimStart;
  }
  activeAudio.currentTime = currentTime.value;

  activeAudio.addEventListener("timeupdate", onAudioTimeUpdate);
  activeAudio.addEventListener("ended", onAudioEnded);

  activeAudio.play().catch((e) => {
    console.warn("Audio autoplay prevented:", e);
  });
}

function onAudioTimeUpdate() {
  if (activeAudio) {
    currentTime.value = activeAudio.currentTime;

    // Update global playhead time
    let priorSec = 0;
    for (let i = 0; i < currentTrackIndex.value; i++) {
      priorSec += getAudioEffectiveDuration(i);
    }
    const clip = audioClips.value[currentTrackIndex.value];
    const trimStart = clip?.trimStart || 0;
    const elapsedInClip = Math.max(0, activeAudio.currentTime - trimStart);
    globalPlayheadTime.value = priorSec + elapsedInClip;

    // Check if reached trimEnd
    const trimEnd = clip?.trimEnd || clip?.originalDuration || 180;
    if (trimEnd > trimStart && activeAudio.currentTime >= trimEnd) {
      onAudioEnded();
    }
  }
}

function onAudioEnded() {
  // Automatically advance to next track starting at trimStart
  if (currentTrackIndex.value < audioClips.value.length - 1) {
    currentTrackIndex.value++;
    const nextClip = audioClips.value[currentTrackIndex.value];
    currentTime.value = nextClip.trimStart || 0;
    loadAndPlayCurrentTrack();
  } else {
    // Loop back to start
    currentTrackIndex.value = 0;
    const firstClip = audioClips.value[0];
    currentTime.value = firstClip ? (firstClip.trimStart || 0) : 0;
    globalPlayheadTime.value = 0;
    loadAndPlayCurrentTrack();
  }
}

watch(volume, (newVol) => {
  if (activeAudio) activeAudio.volume = isMuted.value ? 0 : newVol;
});

watch(isMuted, (muted) => {
  if (activeAudio) activeAudio.volume = muted ? 0 : volume.value;
});

// Interactive Drag Handling for Canvas Overlays
const dragOffset = ref({ x: 0, y: 0 });

function onMouseDown(e, element) {
  e.preventDefault();
  draggingElement.value = element;
  const target = e.currentTarget;
  if (target && previewBoxRef.value) {
    const boxRect = previewBoxRef.value.getBoundingClientRect();
    const elRect = target.getBoundingClientRect();
    dragOffset.value = {
      x: ((e.clientX - elRect.left) / boxRect.width) * 100,
      y: ((e.clientY - elRect.top) / boxRect.height) * 100,
    };
  }
}

function onTouchStart(e, element) {
  draggingElement.value = element;
  if (e.touches && e.touches[0] && previewBoxRef.value) {
    const target = e.currentTarget;
    const boxRect = previewBoxRef.value.getBoundingClientRect();
    const elRect = target.getBoundingClientRect();
    dragOffset.value = {
      x: ((e.touches[0].clientX - elRect.left) / boxRect.width) * 100,
      y: ((e.touches[0].clientY - elRect.top) / boxRect.height) * 100,
    };
  }
}

function updateElementDrag(clientX, clientY) {
  if (!draggingElement.value || !previewBoxRef.value) return;
  const rect = previewBoxRef.value.getBoundingClientRect();

  let x = ((clientX - rect.left) / rect.width) * 100 - (dragOffset.value.x || 0);
  let y = ((clientY - rect.top) / rect.height) * 100 - (dragOffset.value.y || 0);

  const isPortrait = aspectRatioMode.value === "9:16";
  const maxX = isPortrait ? 60 : 85;
  const maxY = 86;

  x = Math.max(1, Math.min(x, maxX));
  y = Math.max(1, Math.min(y, maxY));

  if (draggingElement.value === "playlist") {
    playlistPos.value = { x: Math.round(x), y: Math.round(y) };
  } else if (draggingElement.value === "timer") {
    timerPos.value = { x: Math.round(x), y: Math.round(y) };
  }
}

function onMouseMove(e) {
  if (!draggingElement.value) return;
  updateElementDrag(e.clientX, e.clientY);
}

function onTouchMove(e) {
  if (!draggingElement.value || !e.touches.length) return;
  updateElementDrag(e.touches[0].clientX, e.touches[0].clientY);
}

function onMouseUp() {
  draggingElement.value = null;
}

// Window Keyboard Shortcuts Listener
function handleGlobalKeyDown(e) {
  const target = e.target;
  const isInput = target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable);
  if (isInput) return;

  if (e.code === "Space") {
    e.preventDefault();
    toggleMasterPlayback();
  } else if (e.key === "s" || e.key === "S") {
    e.preventDefault();
    splitClipAtPlayhead();
  } else if (e.key === "Delete" || e.key === "Backspace") {
    e.preventDefault();
    deleteSelectedClip();
  } else if (e.key === "ArrowLeft") {
    e.preventDefault();
    seekToGlobalTime(globalPlayheadTime.value - (e.shiftKey ? 0.2 : 1));
  } else if (e.key === "ArrowRight") {
    e.preventDefault();
    seekToGlobalTime(globalPlayheadTime.value + (e.shiftKey ? 0.2 : 1));
  }
}

onMounted(() => {
  window.addEventListener("keydown", handleGlobalKeyDown);
});

// Export / Generation
const { createProgressStream, mixMusicVideo } = useMediaApi();

async function generateVideo() {
  if (!canGenerate.value) return;

  pausePlayback();

  isGenerating.value = true;
  currentProgress.value = 0;
  currentStatus.value = "Preparing media...";

  const jobId = "job_" + Date.now() + "_" + Math.random().toString(36).substr(2, 6);
  currentJobId.value = jobId;

  eventSource = createProgressStream(jobId);
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.progress) currentProgress.value = Math.min(99, Math.round(data.progress));
      if (data.status) currentStatus.value = data.status;
    } catch (e) {}
  };
  eventSource.onerror = () => {
    if (eventSource) eventSource.close();
  };

  const formData = new FormData();
  formData.append("jobId", jobId);
  formData.append(
    "transitionTypes",
    JSON.stringify(selectedTransitions.value.length > 0 ? selectedTransitions.value : ["none"])
  );
  formData.append("transitionDuration", bgTransitionDuration.value.toString());
  formData.append("resolution", outputResolution.value);
  formData.append("keepOriginalAudio", keepOriginalAudio.value.toString());
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
  formData.append("photoMotion", photoMotion.value);
  formData.append("photoZoomIntensity", photoZoomIntensity.value.toString());

  // Send accurate audio and video clip segments to backend FFmpeg
  const audioTrimsClean = audioClips.value.map((c) => ({
    start: Number(c.trimStart || 0),
    end: Number(c.trimEnd !== undefined ? c.trimEnd : (c.originalDuration || 0)),
  }));
  formData.append("audioTrimData", JSON.stringify(audioTrimsClean));

  const videoTrimsClean = videoClips.value.map((c) => ({
    start: Number(c.trimStart || 0),
    end: Number(c.trimEnd !== undefined ? c.trimEnd : (c.originalDuration || 0)),
  }));
  formData.append("videoTrimData", JSON.stringify(videoTrimsClean));

  videoClips.value.forEach((c) => {
    formData.append("video", c.file);
  });

  audioClips.value.forEach((c) => {
    formData.append("audio", c.file);
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
        color: "#2E7D32",
        icon: "mdi-party-popper",
        title: "🎉 Compilation Complete!",
        message: "Your music video is ready to download or publish.",
        timeout: 8000,
      };
    }, 400);
  } catch (error) {
    console.error("Compilation failed:", error);
    isGenerating.value = false;
    snackbar.value = {
      show: true,
      color: "#C62828",
      icon: "mdi-alert-circle",
      title: "❌ Compilation Failed",
      message: error.data?.error || error.message || "An unexpected error occurred.",
      timeout: 10000,
    };
  } finally {
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
  }
}

async function cancelGeneration() {
  if (!currentJobId.value) return;
  try {
    await fetch("/api/music-mixer/cancel", {
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
    console.error("Failed to cancel job:", err);
  }
}

function downloadVideo() {
  if (!videoUrl.value) return;
  const a = document.createElement("a");
  a.href = videoUrl.value;
  a.download = `Music_Compilation_${Date.now()}.mp4`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

const confirmNewProjectDialog = ref(false);

function openNewProjectConfirm() {
  if (videoClips.value.length === 0 && audioClips.value.length === 0) {
    resetMixer();
  } else {
    confirmNewProjectDialog.value = true;
  }
}

function reCustomizeProject(targetTab = "media") {
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  videoUrl.value = null;
  activeTab.value = targetTab;

  snackbar.value = {
    show: true,
    color: "purple-darken-3",
    icon: "mdi-movie-edit",
    title: "Project Retained for Customization",
    message: "All video clips, audio tracks, cuts, and transitions are preserved. You can tweak and re-export anytime!",
    timeout: 5000,
  };
}

function editAgain() {
  reCustomizeProject("media");
}

function resetMixer() {
  stopMasterPlayback();
  clearVideo();
  clearAudio();
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  videoUrl.value = null;
  videoPath.value = null;
  currentProgress.value = 0;
  currentStatus.value = "";
  selectedTransitions.value = ["fade"];
  bgTransitionDuration.value = 1;
  photoMotion.value = "alternate";
  photoZoomIntensity.value = 0.15;
  overlayTimer.value.mode = "persong";
  resetPositions();

  snackbar.value = {
    show: true,
    color: "info",
    icon: "mdi-refresh",
    title: "New Project Started",
    message: "Workspace cleared. You can now add new media files.",
    timeout: 3500,
  };
}

onUnmounted(() => {
  stopMasterPlayback();
  window.removeEventListener("keydown", handleGlobalKeyDown);
  if (eventSource) eventSource.close();
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  if (videoPreviewUrl.value) URL.revokeObjectURL(videoPreviewUrl.value);
  if (bgSlideInterval) clearInterval(bgSlideInterval);
});
</script>

<style scoped>
/* Studio Container Layout */
.studio-root {
  height: calc(100vh - 64px);
  max-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  background-color: #0b0f19;
  font-family: inherit;
  overflow: hidden;
}

.studio-header {
  flex-shrink: 0;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.studio-badge {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #f43f5e, #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(244, 63, 94, 0.35);
}

.gradient-title {
  background: linear-gradient(135deg, #f87171, #c084fc);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.dot {
  opacity: 0.4;
}

.studio-body {
  flex: 1;
  min-height: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 2-Column Responsive Studio Grid */
.editor-grid {
  flex: 1;
  min-height: 0;
  height: 100%;
  max-height: 100%;
  display: grid;
  grid-template-columns: 420px 1fr;
  grid-template-rows: minmax(0, 1fr);
  overflow: hidden;
}

@media (max-width: 1080px) {
  .editor-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
    height: auto;
    overflow-y: auto;
  }
}

/* Glass Panels */
.glass-panel {
  background: rgba(17, 24, 39, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.07);
}

/* Inspector Left Panel */
.inspector-panel {
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  padding: 16px;
  height: 100%;
  max-height: 100%;
  min-height: 0;
  overflow-y: auto !important;
  overflow-x: hidden;
  scroll-behavior: smooth;
  scrollbar-width: thin;
  scrollbar-color: rgba(168, 85, 247, 0.7) rgba(255, 255, 255, 0.04);
}

/* Custom sleek gradient scrollbar so the user clearly sees they can scroll up and down */
.inspector-panel::-webkit-scrollbar {
  width: 8px;
}

.inspector-panel::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 4px;
}

.inspector-panel::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #a855f7 0%, #ec4899 100%);
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.inspector-panel::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #c084fc 0%, #f43f5e 100%);
}

/* Sticky top navigation header in Inspector */
.inspector-sticky-header {
  position: sticky;
  top: -16px;
  z-index: 25;
  background: rgba(11, 15, 25, 0.96);
  backdrop-filter: blur(16px);
  margin: -16px -16px 12px -16px;
  padding: 12px 16px 8px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.media-quick-nav {
  user-select: none;
}

.border-top-subtle {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.inspector-tabs :deep(.v-tab) {
  border-radius: 8px;
  font-size: 12px;
}

.inspector-window {
  min-height: 0;
}

.tab-content {
  padding-bottom: 70px;
}

.section-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 14px;
}

.transition-settings-card {
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.25);
  border-radius: 12px;
}

.dropzone-compact {
  border: 1.5px dashed rgba(255, 255, 255, 0.18);
  border-radius: 12px;
  padding: 14px;
  text-align: center;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.02);
  transition: all 0.2s ease;
}

.dropzone-compact:hover {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.05);
}

.dropzone-compact.drag-over {
  border-color: #c084fc;
  background: rgba(139, 92, 246, 0.12);
  transform: scale(1.01);
}

.asset-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 240px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(168, 85, 247, 0.5) rgba(255, 255, 255, 0.03);
}

.asset-list::-webkit-scrollbar {
  width: 5px;
}

.asset-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 3px;
}

.asset-list::-webkit-scrollbar-thumb {
  background: rgba(168, 85, 247, 0.6);
  border-radius: 3px;
}

.asset-list::-webkit-scrollbar-thumb:hover {
  background: #c084fc;
}

.asset-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 12px;
}

.audio-track-card {
  cursor: pointer;
  transition: all 0.2s;
}

.audio-track-card:hover {
  background: rgba(255, 255, 255, 0.08);
}

.audio-track-card.playing-active {
  background: rgba(139, 92, 246, 0.18);
  border-color: #8b5cf6;
}

.track-play-btn {
  border-radius: 6px;
  min-width: 24px;
  width: 24px;
  height: 24px;
}

.index-badge {
  background: rgba(139, 92, 246, 0.3);
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
}

.bg-black-20 {
  background: rgba(0, 0, 0, 0.25);
}

.bg-black-25 {
  background: rgba(0, 0, 0, 0.35);
}

.border-purple-20 {
  border: 1px solid rgba(139, 92, 246, 0.25);
}

.cut-indicator {
  font-size: 9px;
  font-weight: 700;
  color: #c084fc;
  background: rgba(139, 92, 246, 0.2);
  border: 1px solid rgba(139, 92, 246, 0.4);
  padding: 1px 4px;
  border-radius: 4px;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

/* Format Cards */
.format-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 8px;
}

.format-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 10px 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.format-card:hover {
  background: rgba(255, 255, 255, 0.06);
}

.format-card.active {
  background: rgba(139, 92, 246, 0.15);
  border-color: #a855f7;
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.2);
}

.format-res {
  font-size: 10px;
  color: #94a3b8;
}

/* RIGHT: Live Canvas Studio */
.studio-viewport-area {
  background: #070a12;
  position: relative;
  overflow: hidden;
  height: 100%;
  max-height: 100%;
  min-height: 0;
}

.viewport-toolbar {
  background: rgba(15, 23, 42, 0.7);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.ratio-toggle {
  background: rgba(255, 255, 255, 0.05);
}

.canvas-stage {
  flex: 1;
  position: relative;
  overflow: hidden;
  background-image: radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* Live Canvas Monitor */
.canvas-monitor {
  background: #000;
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.1);
  transition: aspect-ratio 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.ratio-landscape {
  aspect-ratio: 16 / 9;
  width: 100%;
  max-width: 860px;
  max-height: 480px;
}

.ratio-portrait {
  aspect-ratio: 9 / 16;
  height: 480px;
  width: auto;
  max-width: 270px;
}

.ratio-square {
  aspect-ratio: 1 / 1;
  height: 460px;
  width: auto;
  max-width: 460px;
}

.canvas-media {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.6;
  transform-origin: center center;
}

.canvas-media.ken-burns-in {
  animation: kenBurnsZoomIn var(--kb-duration, 10s) cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
  will-change: transform;
}

.canvas-media.ken-burns-out {
  animation: kenBurnsZoomOut var(--kb-duration, 10s) cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
  will-change: transform;
}

.canvas-media.ken-burns-breathe {
  animation: kenBurnsBreathe var(--kb-duration, 12s) cubic-bezier(0.4, 0, 0.2, 1) infinite;
  will-change: transform;
}

@keyframes kenBurnsZoomIn {
  0% {
    transform: scale(1.0);
  }
  100% {
    transform: scale(var(--kb-scale, 1.15));
  }
}

@keyframes kenBurnsZoomOut {
  0% {
    transform: scale(var(--kb-scale, 1.15));
  }
  100% {
    transform: scale(1.0);
  }
}

@keyframes kenBurnsBreathe {
  0% {
    transform: scale(1.0);
  }
  50% {
    transform: scale(var(--kb-scale, 1.12));
  }
  100% {
    transform: scale(1.0);
  }
}

.canvas-placeholder {
  width: 100%;
  height: 100%;
  min-height: 300px;
  background: radial-gradient(circle at center, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.9) 100%);
}

/* Safe Area Guides */
.safe-guides-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.action-safe-box {
  position: absolute;
  top: 5%;
  left: 5%;
  right: 5%;
  bottom: 5%;
  border: 1px dashed rgba(6, 182, 212, 0.4);
}

.title-safe-box {
  position: absolute;
  top: 10%;
  left: 10%;
  right: 10%;
  bottom: 10%;
  border: 1px dashed rgba(244, 63, 94, 0.4);
}

.guide-tag {
  position: absolute;
  top: 2px;
  left: 4px;
  font-size: 9px;
  color: rgba(255, 255, 255, 0.5);
  font-family: monospace;
}

/* Canvas Draggable Overlays */
.canvas-overlay-item {
  position: absolute;
  border: 1px solid transparent;
  transition: border-color 0.15s;
}

.draggable-element {
  cursor: grab;
}

.draggable-element:hover,
.draggable-element.is-dragging {
  border: 1px dashed #c084fc;
  box-shadow: 0 0 10px rgba(192, 132, 252, 0.3);
}

.draggable-element.is-dragging {
  cursor: grabbing;
}

.overlay-badge {
  position: absolute;
  top: -18px;
  left: 0;
  background: rgba(139, 92, 246, 0.85);
  color: white;
  font-size: 9px;
  padding: 1px 6px;
  border-radius: 4px;
  display: none;
  align-items: center;
  gap: 2px;
  font-family: monospace;
  white-space: nowrap;
}

.draggable-element:hover .overlay-badge,
.draggable-element.is-dragging .overlay-badge {
  display: flex;
}

/* Playlist Layout on Canvas */
.playlist-overlay {
  display: flex;
  flex-direction: column;
}

.playlist-grid {
  display: grid;
  grid-auto-flow: column;
  row-gap: 6px;
}

.canvas-playlist-item {
  color: white;
  font-weight: bold;
  font-family: 'Courier New', Courier, monospace;
  text-shadow: -1.5px -1.5px 0 rgba(0,0,0,0.8), 1.5px -1.5px 0 rgba(0,0,0,0.8), -1.5px 1.5px 0 rgba(0,0,0,0.8), 1.5px 1.5px 0 rgba(0,0,0,0.8);
  display: flex;
  align-items: center;
  line-height: 1.2;
}

.canvas-playlist-item .play-indicator {
  width: 1.2em;
  display: inline-block;
  color: #c084fc;
  font-size: 0.9em;
}

.canvas-playlist-item.active-track {
  background: rgba(139, 92, 246, 0.7);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-shadow: none;
}

/* Timer Layout on Canvas */
.timer-overlay {
  background: rgba(0, 0, 0, 0.65);
  border: 1.5px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  padding: 4px 14px;
  text-align: center;
}

.timer-digits {
  color: white;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 900;
  letter-spacing: 1px;
}

.timer-tag {
  font-size: 9px;
  color: #a855f7;
  font-weight: bold;
  letter-spacing: 1px;
}

/* Transport Bar & Timeline */
.studio-footer {
  background: rgba(15, 23, 42, 0.9);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.master-play-btn {
  background: linear-gradient(135deg, #f43f5e 0%, #8b5cf6 100%) !important;
  color: white !important;
  box-shadow: 0 4px 16px rgba(244, 63, 94, 0.35);
  transition: transform 0.15s ease;
}

.master-play-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.volume-slider :deep(.v-slider-thumb) {
  width: 12px;
  height: 12px;
}

/* CapCut Inspector Mini-Trimmer Bar */
.clip-waveform-trimmer-wrap {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 8px 10px;
}

.clip-trimmer-track {
  height: 38px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
}

.dimmed-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.65);
  background-image: repeating-linear-gradient(45deg, transparent, transparent 4px, rgba(0, 0, 0, 0.4) 4px, rgba(0, 0, 0, 0.4) 8px);
  z-index: 2;
  pointer-events: none;
}

.dimmed-start {
  left: 0;
}

.dimmed-end {
  right: 0;
}

.active-segment-highlight {
  position: absolute;
  top: 0;
  bottom: 0;
  background: linear-gradient(90deg, rgba(168, 85, 247, 0.35), rgba(236, 72, 153, 0.35));
  border-top: 2px solid #c084fc;
  border-bottom: 2px solid #c084fc;
  z-index: 3;
  display: flex;
  align-items: center;
}

.mini-waveform-stripes {
  width: 100%;
  height: 60%;
  background-image: repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.35) 0, rgba(255, 255, 255, 0.35) 2px, transparent 2px, transparent 6px);
  opacity: 0.7;
}

.inspector-trim-handle {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 14px;
  cursor: col-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
  transition: transform 0.1s;
}

.inspector-trim-handle:hover {
  transform: scaleY(1.08);
}

.inspector-trim-handle.handle-in {
  left: 0;
  background: #a855f7;
  border-radius: 4px 0 0 4px;
}

.inspector-trim-handle.handle-out {
  right: 0;
  background: #ec4899;
  border-radius: 0 4px 4px 0;
}

.handle-pill {
  width: 3px;
  height: 16px;
  background: white;
  border-radius: 2px;
}

/* CapCut Multi-Track Timeline Stage */
.timeline-action-toolbar {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.capcut-tool-btn {
  border-radius: 6px;
  font-size: 11px;
}

.capcut-timeline-wrapper {
  background: rgba(5, 10, 20, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 8px;
  position: relative;
  overflow-x: auto;
  overflow-y: hidden;
  user-select: none;
  cursor: pointer;
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
}

.capcut-timeline-inner {
  position: relative;
  min-width: 100%;
  transition: width 0.15s ease-out;
}

/* Timecode Ruler */
.capcut-ruler {
  height: 22px;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  cursor: col-resize;
  border-radius: 6px 6px 0 0;
}

.ruler-tick {
  position: absolute;
  top: 0;
  bottom: 0;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
}

.tick-label {
  font-size: 9px;
  font-family: monospace;
  color: #64748b;
  line-height: 12px;
}

.tick-mark {
  width: 1px;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  margin-top: 2px;
}

/* Track Rows */
.capcut-track-row {
  height: 38px;
  position: relative;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.015);
}

.track-header-badge {
  width: 76px;
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  display: flex;
  align-items: center;
  padding-left: 6px;
}

.track-clips-lane {
  height: 100%;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.25);
  gap: 2px;
  padding: 2px;
  overflow: visible;
}

.empty-track-placeholder {
  width: 100%;
  height: 100%;
  border: 1px dashed rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.empty-track-placeholder:hover {
  background: rgba(168, 85, 247, 0.12);
  border-color: rgba(168, 85, 247, 0.5);
  color: #e9d5ff !important;
}

/* Clip Blocks */
.capcut-clip-block {
  height: 100%;
  border-radius: 5px;
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 0.15s ease, filter 0.15s ease;
  user-select: none;
  min-width: 32px;
}

.visual-clip-block {
  background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
  border: 1px solid rgba(139, 92, 246, 0.4);
  color: white;
}

.visual-clip-block.is-image {
  background: linear-gradient(90deg, #4338ca 0%, #6366f1 100%);
}

.audio-clip-block {
  background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
  border: 1px solid rgba(56, 189, 248, 0.4);
  color: white;
}

.capcut-clip-block:hover {
  filter: brightness(1.1);
}

.capcut-clip-block.is-selected {
  outline: 2px solid #f43f5e;
  box-shadow: 0 0 14px rgba(244, 63, 94, 0.6);
  z-index: 10;
}

.audio-clip-block.is-playing {
  background: linear-gradient(90deg, #a855f7 0%, #ec4899 100%);
  border-color: #ec4899;
}

/* Trim In/Out Handles */
.capcut-clip-handle {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 8px;
  z-index: 15;
  cursor: col-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.25);
  transition: background 0.15s, width 0.15s;
}

.capcut-clip-handle:hover {
  width: 12px;
  background: #f43f5e;
}

.capcut-clip-handle.handle-left {
  left: 0;
  border-radius: 4px 0 0 4px;
}

.capcut-clip-handle.handle-right {
  right: 0;
  border-radius: 0 4px 4px 0;
}

.handle-bar {
  width: 2px;
  height: 14px;
  background: white;
  border-radius: 1px;
}

/* Clip Inner Elements */
.clip-inner-content {
  width: 100%;
  pointer-events: none;
}

.clip-name {
  font-size: 11px;
  font-weight: 600;
  color: white;
}

.clip-duration-badge {
  font-size: 9px;
  font-family: monospace;
  background: rgba(0, 0, 0, 0.45);
  padding: 1px 4px;
  border-radius: 3px;
  color: rgba(255, 255, 255, 0.85);
  white-space: nowrap;
}

.clip-delete-btn {
  pointer-events: auto;
  opacity: 0.6;
  width: 16px;
  height: 16px;
}

.clip-delete-btn:hover {
  opacity: 1;
  color: #f43f5e !important;
}

/* Equalizer mini animation */
.playing-equalizer {
  display: inline-flex;
  align-items: flex-end;
  gap: 1.5px;
  height: 10px;
}

.playing-equalizer span {
  width: 2px;
  height: 100%;
  background: white;
  animation: eqBounce 0.7s infinite alternate ease-in-out;
}

.playing-equalizer span:nth-child(2) {
  animation-delay: 0.2s;
}

.playing-equalizer span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes eqBounce {
  0% {
    height: 2px;
  }
  100% {
    height: 10px;
  }
}

/* Interactive CapCut Playhead & Scrubber Needle */
.capcut-playhead {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 20px;
  transform: translateX(-50%);
  z-index: 30;
  cursor: ew-resize;
  pointer-events: auto;
}

.playhead-pin {
  position: absolute;
  top: -1px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: grab;
}

.playhead-pin:active {
  cursor: grabbing;
}

.pin-badge {
  background: #f43f5e;
  color: white;
  font-size: 9px;
  font-weight: 800;
  padding: 1px 4px;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(244, 63, 94, 0.6);
  white-space: nowrap;
}

.pin-shape {
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 6px solid #f43f5e;
}

.playhead-line {
  position: absolute;
  top: 20px;
  bottom: 0;
  left: 50%;
  width: 2px;
  background: #f43f5e;
  box-shadow: 0 0 8px rgba(244, 63, 94, 0.9);
  pointer-events: none;
}

/* Keyboard badge */
.kbd-key {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  padding: 1px 4px;
  font-family: monospace;
  font-size: 9px;
  color: white;
}

/* Export / Processing Card */
.export-btn {
  background: linear-gradient(135deg, #f43f5e 0%, #8b5cf6 100%) !important;
  color: white !important;
  transition: transform 0.2s, box-shadow 0.2s;
}

.export-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(244, 63, 94, 0.4);
}

.re-customize-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%) !important;
  color: white !important;
  box-shadow: 0 4px 18px rgba(139, 92, 246, 0.45);
  transition: transform 0.2s, box-shadow 0.2s;
}

.re-customize-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(6, 182, 212, 0.5);
}

.processing-card {
  border-radius: 28px !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.95) !important;
  backdrop-filter: blur(24px);
}

/* Result Screen */
.final-video-card {
  border-radius: 20px;
  background: #000;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
}

.final-video-player {
  width: 100%;
  max-height: 520px;
  display: block;
}
</style>
