<template>
  <v-layout>
    <!-- Sidebar Navigation -->
    <v-navigation-drawer
      v-model="drawer"
      color="grey-darken-4"
      theme="dark"
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
        <v-list-item to="/typing-test" prepend-icon="mdi-keyboard" title="Lao Typing Test" value="typing" color="purple"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Top Navigation Bar -->
    <v-app-bar color="primary" elevation="4">
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
import { ref } from 'vue';
import { useDisplay } from 'vuetify';

// Vuetify useDisplay helps us know if it's a mobile screen
const { mobile } = useDisplay();

// Initialize to true for server rendering to match the desktop default
const drawer = ref(true);

import { onMounted } from 'vue';

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
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
</style>
