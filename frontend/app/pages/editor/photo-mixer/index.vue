<template>
  <div class="editor-container">


    <div class="workspace">
      <!-- Upload Zones -->
      <div v-if="!videoUrl" class="upload-zones">
        
        <!-- Image Drop Zone -->
        <div 
          class="drop-zone glass-card"
          :class="{ 'drag-over': isDraggingImage, 'has-file': imageFiles.length > 0 }"
          @dragover.prevent="isDraggingImage = true"
          @dragleave.prevent="isDraggingImage = false"
          @drop.prevent="onDropImage"
          @click="$refs.imageInput.click()"
        >
          <input type="file" ref="imageInput" accept="image/*" multiple class="d-none" @change="onSelectImage" @click.stop />
          
          <div v-if="imageFiles.length === 0" class="zone-placeholder">
            <v-icon icon="mdi-image-multiple-outline" size="40" class="mb-2 floating-icon" color="rgba(255,255,255,0.8)"></v-icon>
            <h3 class="text-subtitle-1 font-weight-bold">Image Sequence</h3>
            <p class="text-caption">Drag & Drop or Click (Multiple allowed)</p>
          </div>
          
          <div v-else class="zone-preview multi-preview">
            <v-btn icon="mdi-close" size="x-small" color="error" variant="flat" class="clear-box-btn" @click.stop="clearImages" title="Clear Images"></v-btn>
            <div class="gallery-grid">
              <div v-for="(url, index) in imagePreviewUrls.slice(0, 4)" :key="index" class="gallery-item">
                <img :src="url" alt="Preview" class="preview-img-small" />
              </div>
              <div v-if="imageFiles.length > 4" class="more-indicator">
                +{{ imageFiles.length - 4 }}
              </div>
            </div>
            <div class="file-overlay">
              <v-icon icon="mdi-check-circle" color="success" size="24"></v-icon>
              <span>{{ imageFiles.length }} Image(s) selected</span>
              <small>(Click to replace)</small>
            </div>
          </div>
        </div>

        <!-- Audio Drop Zone -->
        <div 
          class="drop-zone glass-card"
          :class="{ 'drag-over': isDraggingAudio, 'has-file': audioFiles.length > 0 }"
          @dragover.prevent="isDraggingAudio = true"
          @dragleave.prevent="isDraggingAudio = false"
          @drop.prevent="onDropAudio"
          @click="$refs.audioInput.click()"
        >
          <input type="file" ref="audioInput" accept="audio/*" multiple class="d-none" @change="onSelectAudio" @click.stop />
          
          <div v-if="audioFiles.length === 0" class="zone-placeholder">
            <v-icon icon="mdi-music-note-outline" size="40" class="mb-2 floating-icon" color="rgba(255,255,255,0.8)"></v-icon>
            <h3 class="text-subtitle-1 font-weight-bold">Audio Track</h3>
            <p class="text-caption">Drag & Drop or Click (Multiple allowed)</p>
          </div>
          
          <div v-else class="zone-preview audio-preview">
            <v-btn icon="mdi-close" size="x-small" color="error" variant="flat" class="clear-box-btn" @click.stop="clearAudio" title="Clear Audio"></v-btn>
            <v-icon icon="mdi-waveform" size="40" color="white" class="wave-icon"></v-icon>
            <div class="file-overlay">
              <v-icon icon="mdi-check-circle" color="success" size="24"></v-icon>
              <span>{{ audioFiles.length === 1 ? audioFiles[0].name : audioFiles.length + ' tracks selected' }}</span>
              <small>(Click to add more/replace)</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Effects Settings Panel -->
      <div v-if="!videoUrl" class="settings-panel glass-card mt-10">
        <div class="d-flex align-center mb-8">
          <div class="icon-box bg-primary-lighten-1 rounded-xl pa-3 mr-4 d-flex align-center justify-center">
            <v-icon icon="mdi-movie-filter" color="primary" size="28"></v-icon>
          </div>
          <div>
            <h3 class="text-h5 font-weight-bold text-white mb-0">Cinematic Effects</h3>
            <p class="text-caption text-grey-lighten-1 mb-0">Fine-tune your masterpiece settings</p>
          </div>
        </div>
        
        <v-row>
          <v-col cols="12" md="6">
            <p class="font-weight-bold mb-2 text-white">Zoom Direction (Ken Burns)</p>
            <v-btn-toggle
              v-model="zoomDir"
              color="primary"
              mandatory
              density="compact"
              class="w-100 btn-group-custom"
            >
              <v-btn value="in" class="flex-grow-1" size="small">
                <v-icon start size="small">mdi-magnify-plus</v-icon> In
              </v-btn>
              <v-btn value="out" class="flex-grow-1" size="small">
                <v-icon start size="small">mdi-magnify-minus</v-icon> Out
              </v-btn>
              <v-btn value="alternate" class="flex-grow-1" size="small">
                <v-icon start size="small">mdi-swap-horizontal</v-icon> Switch
              </v-btn>
              <v-btn value="none" class="flex-grow-1" size="small">
                <v-icon start size="small">mdi-cancel</v-icon> None
              </v-btn>
            </v-btn-toggle>
          </v-col>
          
          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">Zoom Intensity</p>
              <span class="text-caption text-secondary font-weight-bold">{{ zoomSpeed }}%</span>
            </div>
            <v-slider
              v-model="zoomSpeed"
              :disabled="zoomDir === 'none'"
              color="secondary"
              track-color="rgba(255,255,255,0.1)"
              min="5"
              max="100"
              step="1"
              hide-details
              thumb-size="20"
              track-size="6"
              class="mt-2"
            >
              <template v-slot:prepend>
                <v-icon size="20" color="grey-lighten-1" @click="zoomSpeed = Math.max(5, zoomSpeed - 5)">mdi-minus</v-icon>
              </template>
              <template v-slot:append>
                <v-icon size="20" color="grey-lighten-1" @click="zoomSpeed = Math.min(100, zoomSpeed + 5)">mdi-plus</v-icon>
              </template>
            </v-slider>
          </v-col>
        </v-row>

        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">Time per Image</p>
              <span class="text-caption text-success font-weight-bold">{{ imageDuration }} seconds</span>
            </div>
            <v-slider
              v-model="imageDuration"
              color="success"
              track-color="rgba(255,255,255,0.1)"
              min="2"
              max="20"
              step="1"
              hide-details
              thumb-size="20"
              track-size="6"
              class="mt-2"
            >
              <template v-slot:prepend>
                <v-icon size="20" color="grey-lighten-1" @click="imageDuration = Math.max(2, imageDuration - 1)">mdi-minus</v-icon>
              </template>
              <template v-slot:append>
                <v-icon size="20" color="grey-lighten-1" @click="imageDuration = Math.min(20, imageDuration + 1)">mdi-plus</v-icon>
              </template>
            </v-slider>
          </v-col>

          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">Slide Transition Effects</p>
              <span class="text-caption text-primary font-weight-bold">{{ selectedTransitions.length }} selected</span>
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
                        density="compact"
                      ></v-checkbox-btn>
                    </v-list-item-action>
                    <v-icon icon="mdi-check-all" :color="likesAllTransitions ? 'primary' : 'grey-lighten-1'" class="mr-3"></v-icon>
                  </template>
                  <v-list-item-title :class="likesAllTransitions ? 'text-primary font-weight-bold' : 'text-white'">
                    Select All / Clear All
                  </v-list-item-title>
                </v-list-item>
                <v-divider class="my-1"></v-divider>
              </template>
              <template v-slot:selection="{ item, index }">
                <v-chip v-if="index < 2" color="primary" size="small" variant="flat" class="font-weight-bold mr-1">
                  {{ item.raw.title }}
                </v-chip>
                <span v-if="index === 2" class="text-caption text-grey-lighten-1 ml-1">
                  (+{{ selectedTransitions.length - 2 }} others)
                </span>
              </template>
              
              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  title=""
                  :class="{ 'selected-item': selectedTransitions.includes(item.raw.value) }"
                  class="transition-list-item"
                >
                  <template v-slot:prepend="{ isActive }">
                    <v-list-item-action start>
                      <v-checkbox-btn :model-value="isActive" color="primary" density="compact"></v-checkbox-btn>
                    </v-list-item-action>
                    <v-icon :icon="item.raw.icon" :color="isActive ? 'primary' : 'grey-lighten-1'" class="mr-3"></v-icon>
                  </template>
                  <v-list-item-title :class="isActive ? 'text-primary font-weight-bold' : 'text-white'">
                    {{ item.raw.title }}
                  </v-list-item-title>
                  <template v-slot:append>
                    <div class="transition-preview-box" :class="'preview-' + item.raw.value">
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
              <p class="font-weight-bold mb-0 text-white">Target Video Length</p>
              <span class="text-caption text-primary font-weight-bold">
                {{ targetDurationValue > 0 ? targetDurationValue + ' ' + targetDurationUnit : 'Auto (Shortest)' }}
              </span>
            </div>
            <div class="d-flex align-center mt-2" style="gap: 12px;">
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
                style="max-width: 140px;"
                theme="dark"
                :menu-props="{ contentClass: 'bg-grey-darken-4' }"
              ></v-select>
            </div>
          </v-col>

          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">Output Resolution</p>
              <span class="text-caption text-primary font-weight-bold">Select aspect ratio</span>
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
                <v-icon :icon="item.raw.icon" size="small" class="mr-2"></v-icon>
                {{ item.raw.title }}
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :title="item.raw.title">
                  <template v-slot:prepend>
                    <v-icon :icon="item.raw.icon" color="grey-lighten-1" class="mr-3"></v-icon>
                  </template>
                  <template v-slot:subtitle>
                    <span class="text-grey-lighten-1">{{ item.raw.value }}</span>
                  </template>
                </v-list-item>
              </template>
            </v-select>
          </v-col>
        </v-row>

        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <div class="d-flex justify-space-between align-center mb-2">
              <p class="font-weight-bold mb-0 text-white">Transition Duration</p>
              <span class="text-caption text-warning font-weight-bold">{{ transitionDuration }} seconds</span>
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
                <v-icon size="20" color="grey-lighten-1" @click="transitionDuration = Math.max(0.5, transitionDuration - 0.5)">mdi-minus</v-icon>
              </template>
              <template v-slot:append>
                <v-icon size="20" color="grey-lighten-1" @click="transitionDuration = Math.min(3, transitionDuration + 0.5)">mdi-plus</v-icon>
              </template>
            </v-slider>
          </v-col>
        </v-row>
      </div>

      <!-- YouTube Overlay Settings Panel -->
      <div v-if="!videoUrl" class="settings-panel glass-card mt-6 overlay-panel">
        <div class="d-flex align-center mb-8">
          <div
            class="icon-box rounded-xl pa-3 mr-4 d-flex align-center justify-center"
            style="background: linear-gradient(135deg, rgba(255,107,107,0.2), rgba(132,94,194,0.2))"
          >
            <v-icon icon="mdi-youtube" color="red" size="28"></v-icon>
          </div>
          <div>
            <h3 class="text-h5 font-weight-bold text-white mb-0">
              YouTube Overlay Settings
            </h3>
            <p class="text-caption text-grey-lighten-1 mb-0">
              Add visual overlays for Transformative Content
            </p>
          </div>
        </div>

        <!-- ============ 1. POMODORO TIMER ============ -->
        <div class="overlay-section">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="d-flex align-center">
              <v-icon icon="mdi-timer-outline" color="purple-lighten-2" class="mr-3" size="24"></v-icon>
              <div>
                <p class="font-weight-bold mb-0 text-white">Pomodoro Timer</p>
                <p class="text-caption text-grey-lighten-1 mb-0">Countdown timer with progress bar</p>
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
            <div v-if="overlayTimer.enabled">
              <v-row dense>
                <v-col cols="12" md="4">
                  <p class="text-caption text-grey-lighten-1 mb-1">Timer Duration</p>
                  <div class="d-flex align-center" style="gap: 8px">
                    <v-btn
                      v-for="preset in [25, 50, 90]"
                      :key="preset"
                      :color="overlayTimer.minutes === preset ? 'purple-lighten-2' : 'grey-darken-3'"
                      :variant="overlayTimer.minutes === preset ? 'flat' : 'outlined'"
                      size="small"
                      height="40"
                      @click="overlayTimer.minutes = preset"
                      class="timer-preset-btn"
                    >
                      {{ preset }}m
                    </v-btn>
                    <v-text-field
                      v-model.number="overlayTimer.minutes"
                      type="number"
                      min="1"
                      max="180"
                      density="compact"
                      hide-details
                      variant="outlined"
                      bg-color="rgba(255,255,255,0.05)"
                      color="purple-lighten-2"
                      class="rounded-lg"
                      style="max-width: 110px"
                      suffix="min"
                    ></v-text-field>
                  </div>
                </v-col>
                <v-col cols="12" md="4">
                  <p class="text-caption text-grey-lighten-1 mb-1">Position</p>
                  <v-select
                    v-model="overlayTimer.position"
                    :items="positionOptions"
                    item-title="title"
                    item-value="value"
                    density="compact"
                    hide-details
                    variant="outlined"
                    bg-color="rgba(255,255,255,0.05)"
                    color="purple-lighten-2"
                    class="rounded-lg"
                    theme="dark"
                    :menu-props="{ contentClass: 'bg-grey-darken-4' }"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="4" class="d-flex flex-column justify-center" style="gap: 4px">
                  <v-switch
                    v-model="overlayTimer.showProgress"
                    label="Show Progress Bar"
                    color="purple-lighten-2"
                    inset
                    hide-details
                    density="compact"
                    class="text-white"
                  ></v-switch>
                  <div class="d-flex align-center gap-4 mt-2">
                    <v-switch
                      v-model="overlayTimer.withBreak"
                      label="Add Short Break"
                      color="green-lighten-2"
                      inset
                      hide-details
                      density="compact"
                      class="text-white"
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
                      bg-color="rgba(0,0,0,0.4)"
                      class="timer-input"
                      style="max-width: 90px;"
                      suffix="m"
                    ></v-text-field>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-expand-transition>
        </div>

        <v-divider class="my-5" color="rgba(255,255,255,0.08)"></v-divider>

        <!-- ============ 2. WATERMARK / LOGO ============ -->
        <div class="overlay-section">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="d-flex align-center">
              <v-icon icon="mdi-watermark" color="amber-lighten-2" class="mr-3" size="24"></v-icon>
              <div>
                <p class="font-weight-bold mb-0 text-white">Watermark / Logo</p>
                <p class="text-caption text-grey-lighten-1 mb-0">Brand your content with a logo overlay</p>
              </div>
            </div>
            <v-switch
              v-model="overlayLogo.enabled"
              color="amber-lighten-2"
              inset
              hide-details
              density="compact"
            ></v-switch>
          </div>

          <v-expand-transition>
            <div v-if="overlayLogo.enabled">
              <v-row dense>
                <v-col cols="12" md="3">
                  <p class="text-caption text-grey-lighten-1 mb-1">Logo File (PNG)</p>
                  <div
                    class="logo-upload-zone"
                    :class="{ 'has-logo': overlayLogo.file }"
                    @click="$refs.logoInput.click()"
                  >
                    <input
                      type="file"
                      ref="logoInput"
                      accept="image/png,image/webp,image/svg+xml"
                      class="d-none"
                      @change="onSelectLogo"
                      @click.stop
                    />
                    <div v-if="!overlayLogo.file" class="text-center">
                      <v-icon icon="mdi-image-plus" size="28" color="amber-lighten-2" class="mb-1"></v-icon>
                      <p class="text-caption text-grey-lighten-1 mb-0">Click to upload</p>
                    </div>
                    <div v-else class="d-flex align-center" style="gap: 8px">
                      <v-icon icon="mdi-check-circle" color="success" size="20"></v-icon>
                      <span class="text-caption text-white text-truncate" style="max-width: 100px">{{ overlayLogo.file.name }}</span>
                      <v-btn icon="mdi-close" size="x-small" color="error" variant="text" @click.stop="clearLogo"></v-btn>
                    </div>
                  </div>
                </v-col>
                <v-col cols="12" md="3">
                  <p class="text-caption text-grey-lighten-1 mb-1">Position</p>
                  <v-select
                    v-model="overlayLogo.position"
                    :items="logoPositionOptions"
                    item-title="title"
                    item-value="value"
                    density="compact"
                    hide-details
                    variant="outlined"
                    bg-color="rgba(255,255,255,0.05)"
                    color="amber-lighten-2"
                    class="rounded-lg"
                    theme="dark"
                    :menu-props="{ contentClass: 'bg-grey-darken-4' }"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="3">
                  <p class="text-caption text-grey-lighten-1 mb-1">Opacity: {{ overlayLogo.opacity }}</p>
                  <v-slider
                    v-model="overlayLogo.opacity"
                    color="amber-lighten-2"
                    track-color="rgba(255,255,255,0.1)"
                    min="0.1"
                    max="1.0"
                    step="0.1"
                    hide-details
                    thumb-size="16"
                    track-size="4"
                  ></v-slider>
                </v-col>
                <v-col cols="12" md="3">
                  <p class="text-caption text-grey-lighten-1 mb-1">Size: {{ overlayLogo.size }}px</p>
                  <v-slider
                    v-model="overlayLogo.size"
                    color="amber-lighten-2"
                    track-color="rgba(255,255,255,0.1)"
                    min="50"
                    max="300"
                    step="10"
                    hide-details
                    thumb-size="16"
                    track-size="4"
                  ></v-slider>
                </v-col>
              </v-row>
            </div>
          </v-expand-transition>
        </div>

        <v-divider class="my-5" color="rgba(255,255,255,0.08)"></v-divider>

        <!-- ============ 3. DYNAMIC QUOTES ============ -->
        <div class="overlay-section">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="d-flex align-center">
              <v-icon icon="mdi-format-quote-close" color="cyan-lighten-2" class="mr-3" size="24"></v-icon>
              <div>
                <p class="font-weight-bold mb-0 text-white">Motivational Quotes</p>
                <p class="text-caption text-grey-lighten-1 mb-0">Auto-display timed motivational text</p>
              </div>
            </div>
            <v-switch
              v-model="overlayQuotes.enabled"
              color="cyan-lighten-2"
              inset
              hide-details
              density="compact"
            ></v-switch>
          </div>

          <v-expand-transition>
            <div v-if="overlayQuotes.enabled">
              <v-row dense>
                <v-col cols="12" md="3">
                  <p class="text-caption text-grey-lighten-1 mb-1">Show Every (min)</p>
                  <v-text-field
                    v-model.number="overlayQuotes.interval"
                    type="number"
                    min="1"
                    max="60"
                    density="compact"
                    hide-details
                    variant="outlined"
                    bg-color="rgba(255,255,255,0.05)"
                    color="cyan-lighten-2"
                    class="rounded-lg"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="3">
                  <p class="text-caption text-grey-lighten-1 mb-1">Display Duration (sec)</p>
                  <v-text-field
                    v-model.number="overlayQuotes.duration"
                    type="number"
                    min="5"
                    max="60"
                    density="compact"
                    hide-details
                    variant="outlined"
                    bg-color="rgba(255,255,255,0.05)"
                    color="cyan-lighten-2"
                    class="rounded-lg"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="3">
                  <p class="text-caption text-grey-lighten-1 mb-1">Position</p>
                  <v-select
                    v-model="overlayQuotes.position"
                    :items="quotePositionOptions"
                    item-title="title"
                    item-value="value"
                    density="compact"
                    hide-details
                    variant="outlined"
                    bg-color="rgba(255,255,255,0.05)"
                    color="cyan-lighten-2"
                    class="rounded-lg"
                    theme="dark"
                    :menu-props="{ contentClass: 'bg-grey-darken-4' }"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="3" class="d-flex align-center">
                  <v-chip
                    v-if="overlayQuotes.customQuotes.trim().length === 0"
                    color="cyan-lighten-2"
                    variant="outlined"
                    size="small"
                    prepend-icon="mdi-auto-fix"
                  >
                    Using 20 default quotes
                  </v-chip>
                  <v-chip
                    v-else
                    color="cyan-lighten-2"
                    variant="flat"
                    size="small"
                    prepend-icon="mdi-text-box-check"
                  >
                    {{ overlayQuotes.customQuotes.split('\n').filter(l => l.trim()).length }} custom quotes
                  </v-chip>
                </v-col>
              </v-row>
              <v-row dense class="mt-2">
                <v-col cols="12">
                  <p class="text-caption text-grey-lighten-1 mb-1">Custom Quotes (one per line, leave empty for defaults)</p>
                  <v-textarea
                    v-model="overlayQuotes.customQuotes"
                    rows="3"
                    density="compact"
                    hide-details
                    variant="outlined"
                    bg-color="rgba(255,255,255,0.05)"
                    color="cyan-lighten-2"
                    class="rounded-lg"
                    placeholder="Stay focused...&#10;Deep work in progress...&#10;You are doing amazing!"
                  ></v-textarea>
                </v-col>
              </v-row>
            </div>
          </v-expand-transition>
        </div>
      </div>



      <!-- Result View -->
      <div v-if="videoUrl" class="result-view glass-card">
        <h3 class="mb-4 d-flex align-center gap-2">
          <v-icon icon="mdi-movie-open-check" color="success"></v-icon>
          Your Video is Ready
        </h3>
        
        <video controls class="final-video">
          <source :src="videoUrl" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        
        <YoutubeUploader v-if="videoUrl" :videoPath="videoPath" />

        <div class="action-buttons mt-6">
          <v-btn
            size="large"
            color="white"
            variant="outlined"
            prepend-icon="mdi-refresh"
            @click="resetEditor"
            class="action-btn"
          >
            Make Another
          </v-btn>
          <v-btn
            size="large"
            color="success"
            prepend-icon="mdi-download"
            @click="downloadVideo"
            class="action-btn download-btn"
          >
            Download Video
          </v-btn>
        </div>
      </div>

      <!-- Generate Action with Progress Bar -->
      <div v-if="!videoUrl" class="generate-section mt-8">
        <div v-if="!isGenerating" class="d-flex justify-center" style="gap: 16px;">
          <v-btn
            size="x-large"
            class="generate-btn"
            :disabled="!canGenerate"
            @click="generateVideo"
          >
            <v-icon icon="mdi-magic-staff" class="mr-2" />
            Generate Video
          </v-btn>
        </div>
        
        <div v-else class="progress-section glass-card pa-6">
          <div class="d-flex justify-space-between align-center mb-3">
            <span class="font-weight-bold text-white text-body-1">{{ currentStatus }}</span>
            <div class="d-flex align-center" style="gap: 12px;">
              <span class="progress-percent">{{ Math.round(currentProgress) }}%</span>
              <v-btn size="small" color="error" variant="flat" @click="cancelGeneration">
                <v-icon icon="mdi-close" class="mr-1"></v-icon> Cancel
              </v-btn>
            </div>
          </div>
          <v-progress-linear
            :model-value="currentProgress"
            color="primary"
            height="14"
            rounded
            striped
            animated
            class="progress-bar-smooth"
          ></v-progress-linear>
          <p class="text-caption text-grey-lighten-1 mt-3 mb-0 text-center">
            <v-icon icon="mdi-information-outline" size="14" class="mr-1"></v-icon>
            Applying cinematic effects — this may take a minute for many images.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const videoPath = ref(null);
import { ref, computed } from 'vue';
import { useMediaApi } from '~/composables/useMediaApi';

definePageMeta({
  layout: 'video'
});

const imageInput = ref(null);
const audioInput = ref(null);

const isDraggingImage = ref(false);
const isDraggingAudio = ref(false);

const imageFiles = ref([]);
const imagePreviewUrls = ref([]);
const audioFiles = ref([]);

// Settings State (Cinematic Best Practices)
const zoomDir = ref('alternate');
const zoomSpeed = ref(15); // Subtle, slow Ken Burns zoom
const imageDuration = ref(5); // Gives the viewer time to appreciate the image

const transitionDuration = ref(1.5); // Buttery smooth, slightly longer transition
const transitionOptions = [
  { title: 'None (Hard Cut)', value: 'none', icon: 'mdi-format-horizontal-align-center' },
  { title: 'Smooth Crossfade', value: 'fade', icon: 'mdi-blur' },
  { title: 'Fade to Black', value: 'fadeblack', icon: 'mdi-moon-waning-crescent' },
  { title: 'Fade to White', value: 'fadewhite', icon: 'mdi-white-balance-sunny' },
  { title: 'Wipe Left', value: 'wipeleft', icon: 'mdi-format-horizontal-align-left' },
  { title: 'Wipe Right', value: 'wiperight', icon: 'mdi-format-horizontal-align-right' },
  { title: 'Iris Circle Crop', value: 'circlecrop', icon: 'mdi-record-circle-outline' },
  { title: 'Square Box Crop', value: 'rectcrop', icon: 'mdi-square-outline' },
  { title: 'Fly Away Warp 🚀', value: 'distance', icon: 'mdi-rocket-launch-outline' },
  { title: 'Clock Sweep', value: 'radial', icon: 'mdi-clock-outline' },
  { title: 'Retro Pixelize', value: 'pixelize', icon: 'mdi-checkerboard' },
  { title: 'Horizontal Blur', value: 'hblur', icon: 'mdi-blur-linear' }
];

// Default to all selected so it behaves like a massive random mix
const selectedTransitions = ref(transitionOptions.map(t => t.value));

const likesAllTransitions = computed(() => selectedTransitions.value.length === transitionOptions.length);
const likesSomeTransitions = computed(() => selectedTransitions.value.length > 0 && !likesAllTransitions.value);

const toggleAllTransitions = () => {
  if (likesAllTransitions.value) {
    selectedTransitions.value = [];
  } else {
    selectedTransitions.value = transitionOptions.map(t => t.value);
  }
};

const targetDurationValue = ref(0);
const targetDurationUnit = ref('Hours');
const outputResolution = ref('1280:720');
const resolutionOptions = [
  { title: 'YouTube / TV (16:9 HD)', value: '1280:720', icon: 'mdi-monitor' },
  { title: 'YouTube / TV (16:9 FHD)', value: '1920:1080', icon: 'mdi-monitor-screenshot' },
  { title: 'TikTok / Reels (9:16 HD)', value: '720:1280', icon: 'mdi-cellphone' },
  { title: 'TikTok / Reels (9:16 FHD)', value: '1080:1920', icon: 'mdi-cellphone-screenshot' },
  { title: 'Instagram Square (1:1)', value: '1080:1080', icon: 'mdi-crop-square' }
];

const isGenerating = ref(false);
const videoUrl = ref(null);

// Progress State
const currentProgress = ref(0);
const currentStatus = ref('Preparing media...');
const currentJobId = ref(null);
let eventSource = null;

const canGenerate = computed(() => imageFiles.value.length > 0 && audioFiles.value.length > 0);

// Image Handlers
const onDropImage = (e) => {
  isDraggingImage.value = false;
  const files = Array.from(e.dataTransfer?.files || []);
  const validFiles = files.filter(f => f.type.startsWith('image/'));
  if (validFiles.length > 0) {
    setImages(validFiles);
  }
};

const onSelectImage = (e) => {
  const files = Array.from(e.target.files || []);
  if (files.length > 0) setImages(files);
  e.target.value = ''; // Reset input to allow selecting same files again if desired
};

const setImages = (files) => {
  imagePreviewUrls.value.forEach(url => URL.revokeObjectURL(url));
  imageFiles.value = files;
  imagePreviewUrls.value = files.map(f => URL.createObjectURL(f));
};

// Audio Handlers
const onDropAudio = (e) => {
  isDraggingAudio.value = false;
  const files = Array.from(e.dataTransfer?.files || []);
  const validFiles = files.filter(f => f.type.startsWith('audio/'));
  if (validFiles.length > 0) {
    setAudio(validFiles);
  }
};

const onSelectAudio = (e) => {
  const files = Array.from(e.target.files || []);
  if (files.length > 0) setAudio(files);
  e.target.value = ''; // Reset input
};

const setAudio = (files) => {
  audioFiles.value = files;
};

const { createProgressStream, mixImageMontage } = useMediaApi();


const logoInput = ref(null);

const overlayTimer = ref({
  enabled: false,
  minutes: 25,
  breakMinutes: 5,
  position: 'top-right',
  showProgress: true,
  withBreak: false
});

const overlayLogo = ref({
  enabled: false,
  file: null,
  position: 'bottom-right',
  opacity: 0.7,
  size: 120
});

const overlayQuotes = ref({
  enabled: false,
  interval: 10,
  duration: 15,
  position: 'bottom',
  customQuotes: ''
});

const positionOptions = [
  { title: 'Top Left', value: 'top-left' },
  { title: 'Top Right', value: 'top-right' },
  { title: 'Bottom Left', value: 'bottom-left' },
  { title: 'Bottom Right', value: 'bottom-right' }
];

const logoPositionOptions = [
  { title: 'Top Left', value: 'top-left' },
  { title: 'Top Right', value: 'top-right' },
  { title: 'Bottom Left', value: 'bottom-left' },
  { title: 'Bottom Right', value: 'bottom-right' }
];

const quotePositionOptions = [
  { title: 'Top Center', value: 'top' },
  { title: 'Middle Center', value: 'center' },
  { title: 'Bottom Center', value: 'bottom' }
];

const onSelectLogo = (e) => {
  const file = e.target.files[0];
  if (file) overlayLogo.value.file = file;
};

const clearLogo = () => {
  overlayLogo.value.file = null;
  if (logoInput.value) logoInput.value.value = '';
};

// Generation
const generateVideo = async () => {
  if (!canGenerate.value || isGenerating.value) return;
  
  isGenerating.value = true;
  currentProgress.value = 0;
  currentStatus.value = 'Uploading files...';
  
  const jobId = 'job_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
  currentJobId.value = jobId;
  
  // Start SSE connection
  eventSource = createProgressStream(jobId);
  
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.progress !== undefined && data.progress > currentProgress.value) {
        currentProgress.value = data.progress;
      }
      if (data.status) {
        currentStatus.value = data.status;
      }
    } catch (_) {}
  };
  
  eventSource.onerror = () => {
    // SSE errors are normal when connection drops or server restarts
  };
  
  const formData = new FormData();
  formData.append('jobId', jobId);
  formData.append('zoomDir', zoomDir.value);
  formData.append('zoomSpeed', zoomSpeed.value);
  formData.append('imageDuration', imageDuration.value);
  formData.append('transitionTypes', JSON.stringify(selectedTransitions.value));
  formData.append('transitionDuration', transitionDuration.value);
  formData.append('resolution', outputResolution.value);
  
  let tDurationSeconds = 0;
  if (targetDurationValue.value > 0) {
    if (targetDurationUnit.value === 'Seconds') tDurationSeconds = targetDurationValue.value;
    else if (targetDurationUnit.value === 'Minutes') tDurationSeconds = targetDurationValue.value * 60;
    else if (targetDurationUnit.value === 'Hours') tDurationSeconds = targetDurationValue.value * 3600;
  }
  formData.append('targetDuration', tDurationSeconds);
  

  // Overlay: Pomodoro Timer
  formData.append('overlayTimerEnabled', overlayTimer.value.enabled);
  if (overlayTimer.value.enabled) {
    formData.append('overlayTimerMinutes', overlayTimer.value.minutes);
    formData.append('overlayTimerBreakMinutes', overlayTimer.value.breakMinutes);
    formData.append('overlayTimerPosition', overlayTimer.value.position);
    formData.append('overlayTimerShowProgress', overlayTimer.value.showProgress);
    formData.append('overlayTimerWithBreak', overlayTimer.value.withBreak);
  }

  // Overlay: Logo
  formData.append('overlayLogoEnabled', overlayLogo.value.enabled);
  if (overlayLogo.value.enabled && overlayLogo.value.file) {
    formData.append('logo', overlayLogo.value.file);
    formData.append('overlayLogoPosition', overlayLogo.value.position);
    formData.append('overlayLogoOpacity', overlayLogo.value.opacity);
    formData.append('overlayLogoSize', overlayLogo.value.size);
  }

  // Overlay: Quotes
  formData.append('overlayQuotesEnabled', overlayQuotes.value.enabled);
  if (overlayQuotes.value.enabled) {
    formData.append('overlayQuotesInterval', overlayQuotes.value.interval);
    formData.append('overlayQuotesDuration', overlayQuotes.value.duration);
    formData.append('overlayQuotesPosition', overlayQuotes.value.position);
    formData.append('overlayCustomQuotes', overlayQuotes.value.customQuotes);
  }

  imageFiles.value.forEach(file => {
    formData.append('image', file);
  });
  audioFiles.value.forEach(file => {
    formData.append('audio', file);
  });
  
  try {
    currentStatus.value = 'Uploading to server...';
    currentProgress.value = 1;
    
    const { blob, videoPath: path } = await mixImageMontage(formData);
      videoPath.value = path;
    
    currentProgress.value = 100;
    currentStatus.value = '✅ Video Ready!';
    videoUrl.value = URL.createObjectURL(blob);
    isGenerating.value = false;
  } catch (err) {
    console.error('Video generation error:', err);
    currentStatus.value = `❌ ${err.message || 'Failed to generate video'}`;
    currentProgress.value = 0;
    setTimeout(() => {
      isGenerating.value = false;
    }, 4000);
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
    await fetch('/api/editor/cancel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ jobId: currentJobId.value })
    });
    isGenerating.value = false;
    currentStatus.value = 'Cancelled';
    currentProgress.value = 0;
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
  } catch (err) {
    console.error('Failed to cancel:', err);
  }
};

const downloadVideo = () => {
  if (!videoUrl.value) return;
  const a = document.createElement('a');
  a.href = videoUrl.value;
  a.download = `fused-slideshow-${Date.now()}.mp4`;
  a.click();
};

const resetEditor = () => {
  imageFiles.value = [];
  audioFiles.value = [];
  imagePreviewUrls.value.forEach(url => URL.revokeObjectURL(url));
  imagePreviewUrls.value = [];
  
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value);
  videoUrl.value = null;
  videoPath.value = null;
  
  if (imageInput.value) imageInput.value.value = '';
  if (audioInput.value) audioInput.value.value = '';
};

const clearImages = () => {
  imageFiles.value = [];
  imagePreviewUrls.value.forEach(url => URL.revokeObjectURL(url));
  imagePreviewUrls.value = [];
  if (imageInput.value) imageInput.value.value = '';
};

const clearAudio = () => {
  audioFiles.value = [];
  if (audioInput.value) audioInput.value.value = '';
};
</script>

<style scoped>


.editor-container {
  padding: 10px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 10px 24px 10px;
}
.glass-header {
  background: rgba(25, 25, 35, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 48px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.header-icon-box {
  background: linear-gradient(135deg, #FF6B6B 0%, #845EC2 100%);
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(132, 94, 194, 0.4);
}

.header-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0;
  line-height: 1.2;
}

.header-subtitle {
  color: rgba(255, 255, 255, 0.7);
  margin: 8px 0 0;
  font-size: 1.1rem;
}

.glass-card {
  background: rgba(20, 20, 25, 0.7);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s;
}
.glass-card:hover {
  border-color: rgba(255,255,255,0.15);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.6);
}

.modern-header {
  text-align: center;
  padding: 40px 20px 50px;
  background: radial-gradient(circle at top, rgba(132, 94, 194, 0.15), transparent 60%);
  border-bottom: 1px solid rgba(255,255,255,0.05);
  border-radius: 0 0 40px 40px;
  margin-bottom: 40px;
}

.gradient-text {
  background: linear-gradient(135deg, #FF6B6B, #845EC2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.icon-box {
  background: rgba(132, 94, 194, 0.1) !important;
  border: 1px solid rgba(132, 94, 194, 0.3);
  box-shadow: 0 0 20px rgba(132, 94, 194, 0.2);
}

.floating-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.settings-panel {
  padding: 24px 32px;
}

.btn-group-custom {
  border-radius: 12px;
  background: rgba(0,0,0,0.2) !important;
}
.btn-group-custom .v-btn {
  border: none !important;
}
.btn-group-custom .v-btn--active {
  background: rgba(132, 94, 194, 0.2) !important;
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  position: relative;
  border: 2px dashed rgba(255, 255, 255, 0.1);
}

.drop-zone:hover {
  border-color: rgba(132, 94, 194, 0.5);
  background: rgba(132, 94, 194, 0.05);
  transform: translateY(-4px);
}

.drop-zone.drag-over {
  border-color: #FF6B6B;
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

.multi-preview {
  padding: 16px;
  background: rgba(0,0,0,0.2);
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

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 8px;
  width: 100%;
  height: 100%;
}

.gallery-item {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.preview-img-small {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.more-indicator {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0,0,0,0.7);
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.audio-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(132, 94, 194, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
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
  background: linear-gradient(135deg, #FF6B6B 0%, #845EC2 100%) !important;
  color: white !important;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 0 48px !important;
  height: 64px !important;
  border-radius: 32px !important;
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-buttons .v-btn {
  text-transform: none;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Beautiful Select Styles */
.beautiful-select {
  transition: all 0.3s ease;
}
.beautiful-select:hover {
  box-shadow: 0 0 15px rgba(var(--v-theme-primary), 0.15);
}
.transition-list-item {
  padding: 12px 16px !important;
  transition: background 0.2s ease;
}
.transition-list-item:hover {
  background: rgba(var(--v-theme-primary), 0.1) !important;
}
.selected-item {
  background: rgba(var(--v-theme-primary), 0.15) !important;
  border-left: 3px solid rgb(var(--v-theme-primary));
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
  animation: fadeIn 0.4s ease-out;
}

.progress-percent {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #FF6B6B, #845EC2);
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

.download-btn {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
  color: white !important;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Transition Previews */
.transition-preview-box {
  width: 48px;
  height: 28px;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.2);
  margin-left: 16px;
  background: #2a2a35;
}
.preview-layer-1, .preview-layer-2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.preview-layer-1 { background: #FF6B6B; }
.preview-layer-2 { background: #845EC2; animation-duration: 3s; animation-iteration-count: infinite; animation-timing-function: ease-in-out; }

/* None */
.preview-none .preview-layer-2 { animation-name: anim-none; }
@keyframes anim-none { 0%, 49.9% { opacity: 0; } 50%, 100% { opacity: 1; } }

/* Fade */
.preview-fade .preview-layer-2 { animation-name: anim-fade; }
@keyframes anim-fade { 0%, 30% { opacity: 0; } 50%, 80% { opacity: 1; } 100% { opacity: 0; } }

/* Fade Black / Fade White */
.preview-fadeblack { background: #000; }
.preview-fadewhite { background: #fff; }
.preview-fadeblack .preview-layer-1, .preview-fadewhite .preview-layer-1 { animation: anim-fade1 3s infinite; }
.preview-fadeblack .preview-layer-2, .preview-fadewhite .preview-layer-2 { animation: anim-fade2 3s infinite; }
@keyframes anim-fade1 { 0%, 30% { opacity: 1; } 45%, 55% { opacity: 0; } 70%, 100% { opacity: 1; } }
@keyframes anim-fade2 { 0%, 45% { opacity: 0; } 60%, 100% { opacity: 1; } }

/* Wipe Left */
.preview-wipeleft .preview-layer-2 { animation-name: anim-wipeleft; }
@keyframes anim-wipeleft {
  0%, 20% { clip-path: polygon(100% 0, 100% 0, 100% 100%, 100% 100%); }
  50%, 80% { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
  100% { clip-path: polygon(100% 0, 100% 0, 100% 100%, 100% 100%); }
}

/* Wipe Right */
.preview-wiperight .preview-layer-2 { animation-name: anim-wiperight; }
@keyframes anim-wiperight {
  0%, 20% { clip-path: polygon(0 0, 0 0, 0 100%, 0 100%); }
  50%, 80% { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
  100% { clip-path: polygon(0 0, 0 0, 0 100%, 0 100%); }
}

/* Circle Crop */
.preview-circlecrop .preview-layer-2 { animation-name: anim-circlecrop; }
@keyframes anim-circlecrop {
  0%, 20% { clip-path: circle(0% at 50% 50%); }
  50%, 80% { clip-path: circle(100% at 50% 50%); }
  100% { clip-path: circle(0% at 50% 50%); }
}

/* Rect Crop */
.preview-rectcrop .preview-layer-2 { animation-name: anim-rectcrop; }
@keyframes anim-rectcrop {
  0%, 20% { clip-path: inset(50% 50% 50% 50%); }
  50%, 80% { clip-path: inset(0% 0% 0% 0%); }
  100% { clip-path: inset(50% 50% 50% 50%); }
}

/* Distance (Zoom) */
.preview-distance .preview-layer-2 { animation-name: anim-distance; transform-origin: center; }
@keyframes anim-distance {
  0%, 20% { transform: scale(0.2); opacity: 0; }
  50%, 80% { transform: scale(1); opacity: 1; }
  100% { transform: scale(0.2); opacity: 0; }
}

/* Blur */
.preview-hblur .preview-layer-2 { animation-name: anim-hblur; }
@keyframes anim-hblur {
  0%, 20% { opacity: 0; filter: blur(4px); }
  50%, 80% { opacity: 1; filter: blur(0px); }
  100% { opacity: 0; filter: blur(4px); }
}

/* Pixelize */
.preview-pixelize .preview-layer-2 { animation-name: anim-pixelize; }
@keyframes anim-pixelize {
  0%, 20% { opacity: 0; transform: scale(1.1); filter: contrast(150%) brightness(120%); }
  50%, 80% { opacity: 1; transform: scale(1); filter: contrast(100%) brightness(100%); }
  100% { opacity: 0; transform: scale(1.1); filter: contrast(150%) brightness(120%); }
}

/* Radial */
.preview-radial .preview-layer-2 { animation-name: anim-radial; }
@keyframes anim-radial {
  0%, 20% { clip-path: polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%); }
  50%, 80% { clip-path: polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 0% 100%, 0% 0%, 50% 0%); }
  100% { clip-path: polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%); }
}

@media (max-width: 768px) {
  .upload-zones {
    grid-template-columns: 1fr;
  }
}
</style>
