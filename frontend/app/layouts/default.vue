<template>
  <v-app>
    <!-- Sidebar Navigation -->
    <v-navigation-drawer
      v-if="!isFullscreenMode"
      v-model="drawer"
      class="sidebar-enhanced"
      theme="dark"
      elevation="3"
    >
      <!-- Sidebar Header with Gradient -->
      <div class="sidebar-header">
        <div class="header-content">
          <v-avatar size="90" class="elevation-4 bg-white mb-3 logo-circle">
            <img src="/images/seng_kue_vang_logo.jpg" alt="Logo" style="width: 100%; height: 100%; object-fit: cover;" />
          </v-avatar>
          <h3 class="header-title">Seng Kue Vang</h3>
          <h5 class="header-subtitle">System Group</h5>
        </div>
      </div>

      <v-divider class="ma-0 opacity-20"></v-divider>

      <v-list density="compact" nav class="mt-2" v-model:opened="openGroups">
        <v-list-item
          to="/"
          prepend-icon="mdi-view-dashboard"
          title="Dashboard"
          value="dashboard"
          color="primary"
          rounded="lg"
          class="nav-item mb-1"
        ></v-list-item>

        <!-- About Me Menu -->
        <v-list-item
          to="/about"
          prepend-icon="mdi-account"
          title="About Me"
          value="about"
          color="blue-accent-2"
          rounded="lg"
          class="nav-item mb-1"
        ></v-list-item>

        <v-list-item
          to="/downloader/image"
          prepend-icon="mdi-cloud-download"
          title="Downloader Suite"
          value="downloader"
          color="cyan"
          rounded="lg"
          class="nav-item mb-1"
        ></v-list-item>
        <v-list-item
          to="/webview-manager"
          prepend-icon="mdi-table-large"
          title="Webview Manager"
          value="webview"
          color="teal"
          rounded="lg"
          class="nav-item mb-1"
        ></v-list-item>
        <v-list-item
          to="/typing/typing-test"
          prepend-icon="mdi-keyboard"
          title="Typing Test"
          value="typing"
          color="purple"
          rounded="lg"
          class="nav-item mb-1"
        ></v-list-item>

        <!-- Learning Menu -->
        <v-list-item
          to="/learning"
          prepend-icon="mdi-school"
          title="Learning"
          value="learning"
          color="indigo"
          rounded="lg"
          class="nav-item mb-1"
        ></v-list-item>

        <!-- Editor Menu with Photo Mixer & Video Mixer -->
        <v-list-item
          to="/editor/photo-mixer"
          prepend-icon="mdi-movie-edit"
          title="Editor"
          value="photo-mixer"
          color="orange-accent-2"
          rounded="lg"
          class="nav-item mb-1"
        ></v-list-item>

        <!-- Chat AI -->
        <v-list-group value="Chat AI">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-robot"
              title="Chat AI"
              rounded="lg"
              class="nav-item mb-1"
            ></v-list-item>
          </template>

          <v-list-item
            to="/chatai/qwenai"
            prepend-icon="mdi-message-text"
            title="Qwen AI Chat"
            value="qwenai"
            color="amber"
            rounded="lg"
            class="nav-item sub-item mb-1"
          ></v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

      <AiChatBox />
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

      <v-app-bar-title class="font-weight-bold"> SKV-TOOLS </v-app-bar-title>
    </v-app-bar>

    <!-- Main Content Area with global background -->
    <v-main class="page-background">
      <!-- Renders the current page -->
      <slot />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useDisplay } from "vuetify";
import { useHead } from "#imports";

useHead({
  bodyAttrs: {
    class: 'default-layout-active'
  }
});

// Vuetify useDisplay helps us know if it's a mobile screen
const { mobile } = useDisplay();

// Initialize to true for server rendering to match the desktop default
const drawer = ref(true);
const openGroups = ref(["Editor", "Chat AI"]);

const isFullscreenMode = useState("isFullscreenMode", () => false);

// Only after the browser has hydrated the page, we calculate the real screen size
onMounted(() => {
  if (mobile.value) {
    drawer.value = false;
  }
});
</script>

<style>
/* Strictly prevent body scrolling and force internal scrolling only for default layout */
body.default-layout-active, 
html:has(body.default-layout-active), 
body.default-layout-active #__nuxt {
  margin: 0;
  padding: 0;
  height: 100%;
  max-height: 100%;
  overflow: hidden !important;
}

/* Global background applied to the main wrapper */
.page-background {
  height: 100%;
  max-height: 100%;
  overflow-y: scroll !important;
  overflow-x: hidden !important;
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

/* Sidebar Enhanced Styling */
.sidebar-enhanced {
  border-right: 1px solid rgb(var(--v-theme-border)) !important;
  background-color: rgb(var(--v-theme-surface)) !important;
  --sidebar-accent: 176, 190, 197; /* Silver accent color */
}

/* Gradient Header */
.sidebar-header {
  background: linear-gradient(
    135deg,
    rgb(var(--sidebar-accent)) 0%,
    rgba(var(--sidebar-accent), 0.8) 100%
  );
  padding: 32px 16px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.sidebar-header::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.1) 0%,
    transparent 70%
  );
  animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.sidebar-title {
  color: white;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Fix Vuetify List Group Padding for clean hierarchy */
.v-list-group__items .v-list-item {
  padding-inline-start: 12px !important;
}

/* Navigation Items */
.nav-item {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  margin-bottom: 3px;
  border-left: 3px solid transparent;
  color: rgb(var(--v-theme-text-primary)) !important;
}

.nav-item:hover {
  background: rgba(var(--sidebar-accent), 0.08) !important;
  border-left-color: rgb(var(--sidebar-accent)) !important;
  color: rgb(var(--sidebar-accent)) !important;
}

.nav-item.v-list-item--active {
  background: rgba(var(--sidebar-accent), 0.12) !important;
  border-left-color: rgb(var(--sidebar-accent)) !important;
  font-weight: 600 !important;
  color: rgb(var(--sidebar-accent)) !important;
}

/* Level 1: Main Group Activator */
.group-activator {
  font-weight: 600 !important;
}

/* Level 2: Sub-Menu */
.sub-item {
  font-size: 0.85rem !important;
  margin-left: 8px !important;
  padding-left: 12px !important;
  border-left: 2px solid rgba(var(--v-theme-on-surface), 0.15) !important;
  border-radius: 0 8px 8px 0 !important;
  color: rgb(var(--v-theme-text-secondary)) !important;
  transition:
    background-color 0.25s ease,
    border-color 0.25s ease,
    color 0.25s ease !important;
}

.sub-item .v-icon {
  font-size: 18px !important;
  opacity: 0.75;
}

/* Hover & Active States for Level 2 */
.sub-item:hover {
  background: rgba(var(--sidebar-accent), 0.08) !important;
  border-left-color: rgb(var(--sidebar-accent)) !important;
  border-left-style: solid !important;
  color: rgb(var(--sidebar-accent)) !important;
}

.sub-item:hover .v-icon {
  opacity: 1;
  color: rgb(var(--sidebar-accent)) !important;
}

.sub-item.v-list-item--active {
  background: rgba(var(--sidebar-accent), 0.14) !important;
  border-left-color: rgb(var(--sidebar-accent)) !important;
  border-left-style: solid !important;
  font-weight: 600 !important;
  color: rgb(var(--sidebar-accent)) !important;
}

.sub-item.v-list-item--active .v-icon {
  opacity: 1;
  color: rgb(var(--sidebar-accent)) !important;
}

/* Logo circle styling */
.sidebar-header .logo-circle {
  border-radius: 50%;
  overflow: hidden;
  aspect-ratio: 1 / 1;
  object-fit: cover;
}
</style>
