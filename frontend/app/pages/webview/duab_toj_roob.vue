<template>
  <div class="iframe-container">
    <iframe src="https://duabtojsiab.app/" frameborder="0" class="full-iframe"></iframe>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'webview',
  title: 'Duab Toj Roob'
})
</script>

<style scoped>
.iframe-container {
  width: 100%;
  height: calc(100vh - 64px); /* Subtract app-bar height */
  overflow: hidden;
}

.full-iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>
