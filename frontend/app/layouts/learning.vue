<template>
  <v-app class="learning-layout-root">
    <!-- Learning Sidebar Navigation -->
    <v-navigation-drawer
      v-model="drawer"
      class="learning-sidebar"
      elevation="0"
      width="280"
      permanent
      theme="dark"
    >
      <v-list-item
        prepend-icon="mdi-school"
        title="Learning Center"
        class="py-4 font-weight-bold text-white"
        to="/learning"
      >
        <template v-slot:append>
          <v-chip color="teal-accent-4" size="x-small" variant="flat" class="font-weight-black text-white">
            HUB
          </v-chip>
        </template>
      </v-list-item>

      <v-divider color="rgba(255,255,255,0.2)"></v-divider>

      <!-- Sidebar Navigation Menu -->
      <v-list density="compact" nav class="mt-3 bg-transparent">
        <v-list-subheader class="text-uppercase font-weight-bold text-white mb-2 opacity-70">Languages</v-list-subheader>
        
        <v-list-item
          to="/learning/hmong"
          prepend-icon="mdi-translate"
          title="Hmong Learning"
          rounded="lg"
          class="nav-item mb-1 text-white"
          color="blue-accent-2"
        ></v-list-item>

        <v-list-item
          to="/learning/lao"
          prepend-icon="mdi-earth"
          title="Lao Learning"
          rounded="lg"
          class="nav-item mb-1 text-white"
          color="red-accent-2"
        ></v-list-item>

        <v-list-item
          to="/learning/english"
          prepend-icon="mdi-alphabet-latin"
          title="English Learning"
          rounded="lg"
          class="nav-item mb-1 text-white"
          color="deep-purple-accent-2"
        ></v-list-item>

        <v-list-subheader class="text-uppercase font-weight-bold text-white mt-4 mb-2 opacity-70">Practice</v-list-subheader>
        
        <v-list-item
          to="/learning/vocabulary"
          prepend-icon="mdi-book-open-page-variant"
          title="Vocabulary"
          rounded="lg"
          class="nav-item mb-1 text-white"
          color="green-accent-4"
        ></v-list-item>

      </v-list>
      
      <template v-slot:append>
        <div class="pa-4">
          <v-btn 
            block 
            color="rgba(255,255,255,0.1)" 
            variant="flat" 
            prepend-icon="mdi-arrow-left" 
            to="/" 
            rounded="lg"
            class="text-none font-weight-bold text-white back-btn"
          >
            Back to Dashboard
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Main Content Area -->
    <v-main class="learning-main-bg">
      <div class="page-content-wrapper">
        <slot />
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';

const drawer = ref(true);
</script>

<style scoped>
.learning-layout-root {
  background: radial-gradient(circle at top right, #1a1a2e 0%, #0f0f1a 100%);
  min-height: 100vh;
}

.learning-sidebar {
  background: rgba(20, 20, 30, 0.6) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.learning-main-bg {
  background: transparent;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-content-wrapper {
  flex-grow: 1;
  position: relative;
  height: 100%;
}

.nav-item {
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05) !important;
  transform: translateX(4px);
}

.v-list-item--active {
  background: rgba(255, 255, 255, 0.1) !important;
  border-left: 3px solid currentColor;
}

.back-btn {
  border: 1px solid rgba(255,255,255,0.1);
  transition: all 0.3s;
}

.back-btn:hover {
  background: rgba(255,255,255,0.2) !important;
  transform: translateY(-2px);
}

.opacity-70 { opacity: 0.7; }
</style>
