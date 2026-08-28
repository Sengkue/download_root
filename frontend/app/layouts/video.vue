<template>
  <v-layout class="video-layout-root">
    <!-- Sidebar Navigation -->
    <v-navigation-drawer
      v-model="drawer"
      class="video-sidebar bg-grey-darken-4"
      elevation="0"
      width="280"
      permanent
    >
      <v-list-item
        prepend-icon="mdi-movie-open"
        title="Editor Studio"
        subtitle="Multimedia Creator"
        class="py-4 font-weight-bold text-white"
      >
        <template v-slot:prepend>
          <div class="brand-icon-wrapper mr-3">
            <v-icon color="white" size="24">mdi-video-vintage</v-icon>
          </div>
        </template>
        <template v-slot:append>
          <v-chip color="deep-orange-accent-3" size="x-small" variant="flat" class="font-weight-black text-white">
            PRO
          </v-chip>
        </template>
      </v-list-item>

      <v-divider class="border-opacity-25" color="grey-lighten-1"></v-divider>

      <!-- Sidebar Navigation Links -->
      <v-list density="compact" nav class="mt-3 text-grey-lighten-2">
        <v-list-item 
          to="/editor/photo-mixer" 
          prepend-icon="mdi-image-multiple" 
          title="Photo Mixer" 
          subtitle="Photos to Video"
          rounded="lg"
          color="primary"
          class="nav-item mb-1"
        ></v-list-item>

        <v-list-item 
          to="/editor/video-mixer" 
          prepend-icon="mdi-movie-open-play" 
          title="Video Mixer" 
          subtitle="Merge & Speed Edit"
          rounded="lg"
          color="primary"
          class="nav-item mb-1"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Top Navigation Bar -->
    <v-app-bar class="video-app-bar bg-grey-darken-4 text-white" elevation="0" border="b">
      <!-- Hamburger menu to toggle sidebar -->
      <v-app-bar-nav-icon @click="drawer = !drawer" color="white"></v-app-bar-nav-icon>

      <v-toolbar-title class="font-weight-bold text-h6 d-flex align-center">
        <span class="gradient-text">Editor Studio</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn variant="tonal" color="white" class="mr-2 rounded-pill px-4 text-none" to="/" prepend-icon="mdi-home-outline">
        Exit to Main
      </v-btn>
    </v-app-bar>

    <!-- Main Content Area -->
    <v-main class="video-main-background">
      <slot />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref } from 'vue';

const drawer = ref(true);
</script>

<style>
/* Root layout */
.video-layout-root {
  height: 100vh !important;
  overflow: hidden !important;
}

.video-main-background {
  min-height: 100%;
  background-color: #0f172a !important; /* Dark slate background */
  overflow-y: auto !important;
}

.brand-icon-wrapper {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #f43f5e, #8b5cf6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(244, 63, 94, 0.4);
}

.gradient-text {
  background: linear-gradient(135deg, #f87171, #c084fc);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.video-sidebar .v-list-item {
  border-radius: 10px !important;
  transition: transform 0.2s ease, background 0.2s ease !important;
}

.video-sidebar .v-list-item:hover {
  transform: translateX(4px);
}

.video-sidebar .v-list-item--active {
  background: rgba(255, 255, 255, 0.12) !important;
  color: #fff !important;
  font-weight: bold;
}
</style>
