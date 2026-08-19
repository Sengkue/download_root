<template>
  <v-layout>
    <!-- Sidebar Navigation -->
    <v-navigation-drawer
      v-if="!isFullscreenMode"
      v-model="drawer"
      class="glass-sidebar"
      theme="dark"
      elevation="0"
    >
      <v-list-item
        prepend-icon="mdi-cloud-download"
        title="MeDownloader"
        class="py-4 font-weight-bold"
      ></v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav class="mt-2">
        <v-list-item to="/" prepend-icon="mdi-image" title="Image Download" value="image"></v-list-item>
        <v-list-item to="/downloader/media" prepend-icon="mdi-video" title="Media Downloader" value="media" color="red"></v-list-item>
        <v-list-item to="/downloader/stock" prepend-icon="mdi-magnify" title="Stock Search" value="search" color="blue"></v-list-item>
        <v-list-item to="/webview-manager" prepend-icon="mdi-table-large" title="Webview Manager" value="webview" color="teal"></v-list-item>
        <v-list-item to="/typing/typing-test" prepend-icon="mdi-keyboard" title="Typing Test" value="typing" color="purple"></v-list-item>
        <v-list-item to="/editor" prepend-icon="mdi-video-plus-outline" title="Video Editor" value="editor" color="orange"></v-list-item>
        <v-list-item to="/video-mixer" prepend-icon="mdi-movie-open-plus" title="Video Mixer" value="video-mixer" color="success"></v-list-item>
        <v-list-group value="Chat AI">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-robot"
              title="Chat AI"
            ></v-list-item>
          </template>

          <v-list-item 
            to="/chatai/qwenai" 
            prepend-icon="mdi-message-text" 
            title="Qwen AI Chat" 
            value="qwenai" 
            color="amber"
            class="pl-8"
          ></v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <!-- Top Navigation Bar -->
    <v-app-bar v-if="!isFullscreenMode" class="glass-app-bar" theme="dark" elevation="0" fixed>
      <!-- Hamburger menu to toggle sidebar -->
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-app-bar-title class="font-weight-bold">
        MeDownloader
      </v-app-bar-title>
    </v-app-bar>

    <!-- Main Content Area with global background -->
    <v-main class="page-background">
      <!-- Renders the current page -->
      <slot />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useDisplay } from 'vuetify';

// Vuetify useDisplay helps us know if it's a mobile screen
const { mobile } = useDisplay();

// Initialize to true for server rendering to match the desktop default
const drawer = ref(true);

const isFullscreenMode = useState('isFullscreenMode', () => false);

// Only after the browser has hydrated the page, we calculate the real screen size
onMounted(() => {
  if (mobile.value) {
    drawer.value = false;
  }
});
</script>

<style>
/* Global background applied to the main wrapper */
.page-background {
  min-height: 100vh;
  /* A modern premium radial gradient (Silver/Slate) */
  background: radial-gradient(circle at top left, #ffffff 0%, #cfd8dc 100%);
}

/* Glassmorphism for App Bar */
.glass-app-bar {
  background: rgba(38, 50, 56, 0.75) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Glassmorphism for Sidebar */
.glass-sidebar {
  background: rgba(38, 50, 56, 0.85) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Modernize List Items */
.glass-sidebar .v-list-item {
  border-radius: 10px !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

.glass-sidebar .v-list-item:hover {
  transform: translateX(4px);
}

.glass-sidebar .v-list-item--active {
  box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
}
</style>
