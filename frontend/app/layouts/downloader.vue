<template>
  <v-layout>
    <!-- Sidebar Navigation for Downloader -->
    <v-navigation-drawer
      v-if="!isFullscreenMode"
      v-model="drawer"
      class="glass-sidebar downloader-sidebar"
      theme="dark"
      elevation="0"
    >
      <v-list-item
        prepend-icon="mdi-cloud-download"
        title="MeDownloader"
        subtitle="Download Tools"
        class="py-4 font-weight-bold"
      ></v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav class="mt-2">
        <v-list-item
          to="/"
          prepend-icon="mdi-home"
          title="Home"
          value="home"
          color="primary"
        ></v-list-item>
        <v-list-item
          to="/downloader/image"
          prepend-icon="mdi-image"
          title="Image Download"
          value="image"
          color="cyan-accent-2"
        ></v-list-item>
        <v-list-item
          to="/downloader/media"
          prepend-icon="mdi-video"
          title="Media Downloader"
          value="media"
          color="red-accent-2"
        ></v-list-item>
        <v-list-item
          to="/downloader/batch-mp3"
          prepend-icon="mdi-music-box-multiple"
          title="Batch MP3"
          value="batch-mp3"
          color="purple-accent-2"
        ></v-list-item>
        <v-list-item
          to="/downloader/stock"
          prepend-icon="mdi-magnify"
          title="Stock Search"
          value="search"
          color="blue-accent-2"
        ></v-list-item>
      </v-list>
      
      <template v-slot:append>
        <div class="pa-4">
          <v-btn
            block
            variant="tonal"
            color="grey-lighten-1"
            prepend-icon="mdi-apps"
            to="/webview-manager"
            class="text-none font-weight-medium rounded-lg mb-2"
          >
            Webview Manager
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Top Navigation Bar -->
    <v-app-bar
      v-if="!isFullscreenMode"
      class="glass-app-bar"
      theme="dark"
      elevation="0"
      fixed
    >
      <!-- Hamburger menu to toggle sidebar -->
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-app-bar-title class="font-weight-bold"> Downloader Suite </v-app-bar-title>
      <v-spacer></v-spacer>
      
      <v-btn variant="tonal" color="white" class="mr-2 rounded-pill px-4 text-none" to="/webview-manager" prepend-icon="mdi-apps">
        Main Menu
      </v-btn>
    </v-app-bar>

    <!-- Main Content Area with global background -->
    <v-main class="page-background">
      <!-- Renders the current page -->
      <slot />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useDisplay } from "vuetify";

// Vuetify useDisplay helps us know if it's a mobile screen
const { mobile } = useDisplay();

// Initialize to true for server rendering to match the desktop default
const drawer = ref(true);

const isFullscreenMode = useState("isFullscreenMode", () => false);

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
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease !important;
}

.glass-sidebar .v-list-item:hover {
  transform: translateX(4px);
}

.glass-sidebar .v-list-item--active {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}
</style>
