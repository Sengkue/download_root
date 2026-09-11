<template>
  <v-app class="about-layout-root">
    <!-- Sidebar only, no navbar -->
    <v-navigation-drawer
      v-model="drawer"
      class="about-sidebar"
      elevation="0"
      width="280"
      permanent
      theme="dark"
    >
      <div class="sidebar-header pa-4 text-center">
        <v-avatar size="100" class="elevation-4 bg-white mb-3 logo-circle">
          <img src="/images/seng_kue_vang_logo.jpg" alt="Logo" style="width: 100%; height: 100%; object-fit: cover;" />
        </v-avatar>
        <h3 class="header-title text-white font-weight-bold">Seng Kue Vang</h3>
        <h5 class="header-subtitle text-white opacity-70">About Me</h5>
      </div>

      <v-divider color="rgba(255,255,255,0.2)"></v-divider>

      <v-list density="compact" nav class="mt-3 bg-transparent">
        <v-list-item
          to="/about"
          prepend-icon="mdi-account"
          title="Profile"
          rounded="lg"
          class="nav-item mb-1 text-white"
          color="blue-accent-2"
          exact
        ></v-list-item>
        
        <v-list-item
          to="/about/experience"
          prepend-icon="mdi-briefcase"
          title="Experience"
          rounded="lg"
          class="nav-item mb-1 text-white"
          color="teal-accent-4"
        ></v-list-item>
        
        <v-list-item
          to="/about/projects"
          prepend-icon="mdi-folder-multiple"
          title="Projects"
          rounded="lg"
          class="nav-item mb-1 text-white"
          color="purple-accent-2"
        ></v-list-item>
      </v-list>
      
      <template v-slot:append>
        <div class="pa-4">
          <v-btn 
            block 
            color="rgba(255,255,255,0.1)" 
            variant="flat" 
            prepend-icon="mdi-home" 
            to="/" 
            rounded="lg"
            class="text-none font-weight-bold text-white back-btn"
          >
            Home Dashboard
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Main Content Area -->
    <v-main class="about-main-bg">
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
.about-layout-root {
  background: radial-gradient(circle at center, #232526 0%, #414345 100%);
  min-height: 100vh;
}

.about-sidebar {
  background: rgba(30, 30, 35, 0.7) !important;
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.sidebar-header .logo-circle {
  border-radius: 50%;
  overflow: hidden;
  aspect-ratio: 1 / 1;
  object-fit: cover;
}

.about-main-bg {
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
  background: rgba(255, 255, 255, 0.1) !important;
  transform: translateX(4px);
}

.v-list-item--active {
  background: rgba(255, 255, 255, 0.15) !important;
  border-left: 3px solid currentColor;
}

.back-btn {
  border: 1px solid rgba(255,255,255,0.15);
  transition: all 0.3s;
}

.back-btn:hover {
  background: rgba(255,255,255,0.25) !important;
  transform: translateY(-2px);
}

.opacity-70 { opacity: 0.7; }
</style>
