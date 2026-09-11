<template>
  <slot />
</template>

<style lang="css">
/* Force scrolling on if Vuetify/Nuxt disabled it */
html, body {
  margin: 0;
  padding: 0;
  height: auto;
  min-height: 100vh;
  overflow-y: auto !important; 
}

/* Ensure Nuxt root doesn't restrict height/width */
#__nuxt {
  width: 100%;
  min-height: 100vh;
}

/* Force the wrapper to fit the full screen width instead of 1140px */
.wrapper {
  max-width: 100% !important;
}
</style>