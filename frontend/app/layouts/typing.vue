<template>
  <v-layout class="typing-layout-root">
    <!-- Typing Sidebar Navigation (Light Glassmorphic) -->
    <v-navigation-drawer
      v-if="!isFullscreenMode"
      v-model="drawer"
      class="typing-light-sidebar"
      elevation="0"
      width="320"
      permanent
    >
      <v-list-item
        prepend-icon="mdi-keyboard"
        title="Typing Master"
        class="py-4 font-weight-bold"
      >
        <template v-slot:prepend>
          <v-avatar size="36" class="mr-3 elevation-2" rounded="lg">
            <v-img :src="'/images/typing_icon.jpg'" cover></v-img>
          </v-avatar>
        </template>
        <template v-slot:append>
          <v-chip color="indigo-accent-3" size="x-small" variant="flat" class="font-weight-black text-white">
            PRO
          </v-chip>
        </template>
      </v-list-item>

      <v-divider class="border-opacity-25"></v-divider>

      <!-- Sidebar Navigation Groups -->
      <v-list density="compact" nav class="mt-3" :opened="openGroups">
        
        <!-- Menu 1: Exam Test & Speed Competition -->
        <v-list-group value="Exam">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-speedometer"
              title="Fast Typing Exam"
              rounded="lg"
              class="nav-item group-activator font-weight-bold mb-1 text-indigo-darken-3"
            ></v-list-item>
          </template>

          <v-list-item 
            to="/typing/typing-test" 
            prepend-icon="mdi-keyboard-outline" 
            title="Typing Test" 
            value="typing-test" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/leaderboard" 
            prepend-icon="mdi-trophy-award" 
            title="Leaderboard (ອັນດັບ)" 
            value="typing-leaderboard" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/profile" 
            prepend-icon="mdi-account-circle" 
            title="Profile & History" 
            value="typing-profile" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/manage-lessons" 
            prepend-icon="mdi-format-list-bulleted" 
            title="Manage Lessons" 
            value="manage-lessons" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>
        </v-list-group>

        <!-- Menu 2: Learning Typing -->
        <v-list-group value="Learning">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-school"
              title="Learning Typing"
              rounded="lg"
              class="nav-item group-activator font-weight-bold mb-1 text-teal-darken-3"
            ></v-list-item>
          </template>

          <v-list-item 
            to="/typing/learn/basics" 
            prepend-icon="mdi-hand-back-right-outline" 
            title="Fingers & Rules Guide" 
            value="learn-basics" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/home-row" 
            prepend-icon="mdi-keyboard-settings-outline" 
            title="Home Row (ASDF JKL;)" 
            value="learn-home-row" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/top-row" 
            prepend-icon="mdi-arrow-up-bold-box-outline" 
            title="Top Row (QWERTY)" 
            value="learn-top-row" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/bottom-row" 
            prepend-icon="mdi-arrow-down-bold-box-outline" 
            title="Bottom Row (ZXCVB)" 
            value="learn-bottom-row" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>

          <v-list-item 
            to="/typing/learn/numbers-symbols" 
            prepend-icon="mdi-numeric" 
            title="Numbers & Symbols" 
            value="learn-numbers" 
            rounded="lg"
            class="nav-item sub-item mb-1 font-weight-medium"
          ></v-list-item>
        </v-list-group>

      </v-list>

      <!-- AdSense Area -->
      <template v-slot:append>
        <div class="pa-3">
          <div class="adsense-slot elevation-2 rounded-lg overflow-hidden cursor-pointer" title="Upgrade to Premium!">
            <slot name="sidebar-ad">
              <!-- AdSense code goes here -->
              <v-carousel
                cycle
                height="300"
                hide-delimiter-background
                :show-arrows="false"
                interval="5000"
              >
                <v-carousel-item
                  v-for="(img, i) in adImages"
                  :key="i"
                  :src="img"
                  cover
                >
                  <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height bg-grey-lighten-4">
                      <v-progress-circular indeterminate color="indigo-lighten-3"></v-progress-circular>
                    </div>
                  </template>
                </v-carousel-item>
              </v-carousel>
            </slot>
          </div>
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

      <!-- User Dropdown Menu -->
      <v-menu offset-y transition="slide-y-transition">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            variant="tonal"
            color="indigo-darken-3"
            class="font-weight-bold mr-2 rounded-pill px-4"
            prepend-icon="mdi-account-circle"
            append-icon="mdi-chevron-down"
          >
            {{ user ? user.name : 'Menu' }}
          </v-btn>
        </template>

        <v-list density="compact" min-width="200" class="py-1" rounded="lg" elevation="4">
          <v-list-item
            prepend-icon="mdi-home-outline"
            title="Exit to Main"
            to="/"
            class="font-weight-medium"
          ></v-list-item>
          <v-divider class="my-1"></v-divider>
          <v-list-item
            prepend-icon="mdi-logout"
            title="Logout"
            @click="handleLogout"
            class="font-weight-medium text-red-darken-1"
          ></v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Main Content Area — ONLY this area scrolls -->
    <v-main class="typing-aurora-background typing-main-scroll">
      <slot />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useDisplay } from 'vuetify';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const { mobile } = useDisplay();
const drawer = ref(true);
const route = useRoute();
const openGroups = ref(['Exam', 'Learning']);
const adImages = [
  '/images/typing_ad_1.jpg',
  '/images/typing_ad_2.jpg',
  '/images/typing_ad_3.jpg',
];
const isFullscreenMode = useState('isFullscreenMode', () => false);
const user = ref(null);

const handleLogout = () => {
  localStorage.removeItem('typing_token');
  localStorage.removeItem('typing_user');
  router.push('/typing/login');
};

onMounted(() => {
  if (mobile.value) {
    drawer.value = false;
  }
  const userData = localStorage.getItem('typing_user');
  if (userData) {
    user.value = JSON.parse(userData);
  }
});
watch(() => route.fullPath, (newPath) => {
  if (newPath.includes('/typing/login')) {
    drawer.value = false;
    openGroups.value = [];
  } else {
    if (!mobile.value) {
      drawer.value = true;
    }
    openGroups.value = ['Exam', 'Learning'];
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

/* Navigation Items */
.typing-light-sidebar .nav-item {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  border-left: 3px solid transparent;
}

.typing-light-sidebar .nav-item:hover {
  background: rgba(99, 102, 241, 0.08) !important;
  border-left-color: rgba(99, 102, 241, 1) !important;
  transform: translateX(4px);
}

.typing-light-sidebar .nav-item.v-list-item--active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(168, 85, 247, 0.12)) !important;
  border-left-color: rgba(99, 102, 241, 1) !important;
  font-weight: 700 !important;
  color: #4338ca !important;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.15) !important;
}

/* Level 1: Main Group Activator */
.typing-light-sidebar .group-activator {
  font-weight: 600 !important;
}

/* Level 2: Sub-Menu */
.typing-light-sidebar .sub-item {
  font-size: 0.85rem !important;
  margin-left: 8px !important;
  padding-left: 12px !important;
  border-left: 2px solid rgba(51, 65, 85, 0.15) !important;
  border-radius: 0 8px 8px 0 !important;
  transition: background-color 0.25s ease, border-color 0.25s ease, color 0.25s ease !important;
}

/* Level 2 Sub-Group Header */
.typing-light-sidebar .sub-item.level-2 {
  font-size: 0.85rem !important;
  font-weight: 600 !important;
  margin-left: 8px !important;
  border-left: 2px solid rgba(99, 102, 241, 0.4) !important;
}

.typing-light-sidebar .sub-item .v-icon {
  font-size: 18px !important;
  opacity: 0.75;
}

/* Level 3: Sub-Sub Menu */
.typing-light-sidebar .sub-item.level-3 {
  font-size: 0.82rem !important;
  margin-left: 16px !important;
  padding-left: 10px !important;
  border-left: 2px dashed rgba(99, 102, 241, 0.3) !important;
  border-radius: 0 8px 8px 0 !important;
}

.typing-light-sidebar .sub-item.level-3 .v-icon {
  font-size: 16px !important;
  opacity: 0.7;
}

/* Hover States for Level 2 & 3 */
.typing-light-sidebar .sub-item:hover,
.typing-light-sidebar .sub-item.level-2:hover,
.typing-light-sidebar .sub-item.level-3:hover {
  background: rgba(99, 102, 241, 0.08) !important;
  border-left-color: rgba(99, 102, 241, 1) !important;
  border-left-style: solid !important;
  color: #4338ca !important;
}

.typing-light-sidebar .sub-item:hover .v-icon,
.typing-light-sidebar .sub-item.level-3:hover .v-icon {
  opacity: 1;
  color: #4338ca !important;
}

/* Active States for Level 2 & 3 */
.typing-light-sidebar .sub-item.v-list-item--active,
.typing-light-sidebar .sub-item.level-3.v-list-item--active {
  background: rgba(99, 102, 241, 0.14) !important;
  border-left-color: rgba(99, 102, 241, 1) !important;
  border-left-style: solid !important;
  font-weight: 600 !important;
  color: #4338ca !important;
}

.typing-light-sidebar .sub-item.v-list-item--active .v-icon,
.typing-light-sidebar .sub-item.level-3.v-list-item--active .v-icon {
  opacity: 1;
  color: #4338ca !important;
}

/* Fix Vuetify List Group Padding */
.v-list-group__items .v-list-item {
  padding-inline-start: 12px !important;
}

/* AdSense Slot */
.adsense-slot {
  min-height: 250px;
  border-radius: 12px;
  overflow: hidden;
}

.ad-placeholder {
  min-height: 250px;
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
}
</style>
