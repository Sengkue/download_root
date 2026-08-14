<template>
  <v-layout>
    <!-- Webview Top Navigation Bar -->
    <v-app-bar color="primary" elevation="4">
      <!-- Back button to return to the main app -->
      <v-btn icon="mdi-arrow-left" @click="$router.back()"></v-btn>
    </v-app-bar>

    <!-- Main Content Area: 100% full screen for webview -->
    <v-main class="webview-background">
      <slot />
    </v-main>
  </v-layout>
</template>

<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
</script>

<style>
/* Remove padding and margin for true full-screen webview */
.webview-background {
  height: 100vh;
  background-color: #f5f5f5;
  overflow: hidden;
}
</style>
