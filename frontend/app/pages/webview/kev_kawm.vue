<template>
  <div class="iframe-container">
    <iframe src="https://pubhtml5.com/wjop/evyx/PB10_NTAWV_HMOOB/" frameborder="0" class="full-iframe"></iframe>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'webview',
  title: 'Kev Kawm'
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
