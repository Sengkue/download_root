<template>
  <v-layout class="typing-layout-root">
    <!-- Typing Sidebar Navigation (Light Glassmorphic) -->
    <v-navigation-drawer
      v-if="!isFullscreenMode"
      v-model="drawer"
      class="typing-light-sidebar"
      elevation="0"
      width="280"
      permanent
    >
      <v-list-item
        prepend-icon="mdi-keyboard"
        title="Typing Master"
        subtitle="Practice & Compete"
        class="py-4 font-weight-bold"
      >
        <template v-slot:prepend>
          <div class="brand-icon-wrapper mr-3">
            <v-icon color="white" size="20">mdi-keyboard</v-icon>
          </div>
        </template>
        <template v-slot:append>
          <v-chip color="indigo-accent-3" size="x-small" variant="flat" class="font-weight-black text-white">
            PRO
          </v-chip>
        </template>
      </v-list-item>

      <v-divider class="border-opacity-25"></v-divider>

      <!-- Sidebar Navigation Groups -->
      <v-list density="compact" nav class="mt-3" :opened="['Exam', 'Learning']">
        
        <!-- Menu 1: Exam Test & Speed Competition -->
        <v-list-group value="Exam">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-speedometer"
              title="Fast Typing Exam"
              class="font-weight-bold mb-1 text-indigo-darken-3"
            ></v-list-item>
          </template>

          <v-list-item 
            to="/typing/typing-test" 
            prepend-icon="mdi-keyboard-outline" 
            title="Typing Test" 
            value="typing-test" 
            active-color="indigo-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/leaderboard" 
            prepend-icon="mdi-trophy-award" 
            title="Leaderboard (ອັນດັບ)" 
            value="typing-leaderboard" 
            active-color="indigo-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/manage-lessons" 
            prepend-icon="mdi-format-list-bulleted" 
            title="Manage Lessons" 
            value="manage-lessons" 
            active-color="indigo-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>
        </v-list-group>

        <!-- Menu 2: Learning Typing -->
        <v-list-group value="Learning">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-school"
              title="Learning Typing"
              class="font-weight-bold mb-1 text-teal-darken-3"
            ></v-list-item>
          </template>

          <v-list-item 
            to="/typing/learn/basics" 
            prepend-icon="mdi-hand-back-right-outline" 
            title="Fingers & Rules Guide" 
            value="learn-basics" 
            active-color="teal-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/home-row" 
            prepend-icon="mdi-keyboard-settings-outline" 
            title="Home Row (ASDF JKL;)" 
            value="learn-home-row" 
            active-color="teal-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/top-row" 
            prepend-icon="mdi-arrow-up-bold-box-outline" 
            title="Top Row (QWERTY)" 
            value="learn-top-row" 
            active-color="teal-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/bottom-row" 
            prepend-icon="mdi-arrow-down-bold-box-outline" 
            title="Bottom Row (ZXCVB)" 
            value="learn-bottom-row" 
            active-color="teal-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/numbers-symbols" 
            prepend-icon="mdi-numeric" 
            title="Numbers & Symbols" 
            value="learn-numbers" 
            active-color="teal-darken-2"
            class="pl-6 font-weight-medium"
          ></v-list-item>
        </v-list-group>

      </v-list>

      <template v-slot:append>
        <div class="pa-3">
          <v-btn
            block
            color="red-lighten-1"
            variant="tonal"
            prepend-icon="mdi-arrow-left"
            to="/"
            class="font-weight-bold"
          >
            Exit to Main
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Top Navigation Bar (Frosted Light Glass) -->
    <v-app-bar v-if="!isFullscreenMode" class="typing-light-app-bar" elevation="0" fixed>
      <!-- Hamburger menu to toggle sidebar -->
      <v-app-bar-nav-icon @click="drawer = !drawer" color="indigo-darken-3"></v-app-bar-nav-icon>

      <v-app-bar-title class="font-weight-black d-flex align-center">
        <span class="gradient-text">Touch Typing Master</span>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <!-- Logout / Exit Button -->
      <v-btn
        prepend-icon="mdi-logout"
        color="red-darken-1"
        variant="tonal"
        to="/"
        class="font-weight-bold mr-2 rounded-pill px-4"
        title="Exit to Main App"
      >
        Logout
      </v-btn>
    </v-app-bar>

    <!-- Main Content Area — ONLY this area scrolls -->
    <v-main class="typing-aurora-background typing-main-scroll">
      <slot />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useDisplay } from 'vuetify';

const { mobile } = useDisplay();
const drawer = ref(true);
const isFullscreenMode = useState('isFullscreenMode', () => false);

onMounted(() => {
  if (mobile.value) {
    drawer.value = false;
  }
});
</script>

<style>
/* Root layout fills viewport — no outer scroll */
.typing-layout-root {
  height: 100vh !important;
  overflow: hidden !important;
}

/* Only the main content area scrolls */
.typing-main-scroll {
  overflow-y: auto !important;
}

.typing-aurora-background {
  min-height: 100%;
  background: 
    radial-gradient(at 0% 0%, #e0e7ff 0px, transparent 50%), 
    radial-gradient(at 100% 0%, #fae8ff 0px, transparent 50%), 
    radial-gradient(at 100% 100%, #e0f2fe 0px, transparent 50%), 
    radial-gradient(at 0% 100%, #ede9fe 0px, transparent 50%), 
    #f8fafc !important;
}

.brand-icon-wrapper {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
}

.gradient-text {
  background: linear-gradient(135deg, #4338ca, #7e22ce);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  letter-spacing: -0.5px;
}

/* Light Glassmorphism App Bar */
.typing-light-app-bar {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
  box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.03) !important;
}

/* Light Glassmorphism Sidebar */
.typing-light-sidebar {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(226, 232, 240, 0.8) !important;
  box-shadow: 4px 0 24px -5px rgba(0, 0, 0, 0.04) !important;
}

.typing-light-sidebar .v-list-item {
  border-radius: 12px !important;
  transition: all 0.2s ease !important;
  color: #334155 !important;
}

.typing-light-sidebar .v-list-item:hover {
  transform: translateX(4px);
  background: rgba(99, 102, 241, 0.08) !important;
}

.typing-light-sidebar .v-list-item--active {
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.15) !important;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(168, 85, 247, 0.12)) !important;
  color: #4338ca !important;
  font-weight: 700 !important;
}
</style>
