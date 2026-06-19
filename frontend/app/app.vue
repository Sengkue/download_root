<script setup>
import { ref, onMounted } from 'vue';

const isAppLoading = ref(true);

onMounted(() => {
  setTimeout(() => {
    isAppLoading.value = false;
  }, 800);
});
</script>

<template>
  <v-app>
    <!-- Plain CSS Global Loader to avoid SSR Hydration errors -->
    <div v-if="isAppLoading" class="global-css-loader">
      <div class="loader-content">
        <div class="spinner"></div>
        <h2 class="loader-title">MeDownloader</h2>
        <p class="loader-subtitle">Preparing your experience...</p>
      </div>
    </div>

    <!-- Main App Content -->
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </v-app>
</template>

<style>
/* Global styles */
html, body {
  margin: 0;
  padding: 0;
}

/* Global CSS Loader */
.global-css-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: #ffffff;
  z-index: 99999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #4CAF50; /* Primary Green */
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 24px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loader-title {
  font-family: sans-serif;
  font-size: 28px;
  font-weight: 900;
  color: #1A237E; /* Primary color fallback */
  margin: 0 0 8px 0;
  letter-spacing: 2px;
}

.loader-subtitle {
  font-family: sans-serif;
  font-size: 16px;
  color: #757575;
  margin: 0;
}
</style>
