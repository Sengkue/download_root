<template>
  <div class="dashboard-wrapper">
    <!-- Dark/Fire Environment Overlay -->
    <div class="fire-environment"></div>
    
    <!-- Realistic Embers -->
    <div class="embers-container">
      <div 
        v-for="ember in embers" 
        :key="ember.id" 
        class="ember"
        :style="{
          left: ember.left + '%',
          animationDuration: ember.duration + 's',
          animationDelay: ember.delay + 's',
          width: ember.size + 'px',
          height: ember.size + 'px',
          opacity: ember.opacity,
          filter: `blur(${ember.blur}px)`
        }"
      ></div>
    </div>

    <!-- Main Content -->
    <v-container class="py-4 py-md-8 position-relative z-10">
      <v-row justify="center" class="mb-4 mb-md-6">
        <v-col cols="12" class="text-center position-relative px-4">
          <h1 class="text-h5 text-md-h3 font-weight-black mb-2 realistic-fire-text">DASHBOARD</h1>
          <p class="text-body-2 text-md-subtitle-1 text-white text-opacity-80">Welcome to the ME System core. Select a module below.</p>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col
          v-for="module in modules"
          :key="module.title"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <div class="card-hover-wrapper h-100">
            <v-card
              class="premium-glass-card h-100 d-flex flex-column"
              elevation="16"
              rounded="lg"
              :to="module.route"
            >
              <v-card-text class="d-flex flex-column align-center text-center pa-4">
                <v-avatar :color="module.color" size="60" class="mb-4 elevation-6 avatar-glow">
                  <v-icon size="30" color="white">{{ module.icon }}</v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2 text-white">{{ module.title }}</h3>
                <p class="text-body-2 text-white text-opacity-70 flex-grow-1">
                  {{ module.description }}
                </p>
              </v-card-text>
              
              <v-spacer></v-spacer>
              <v-divider color="rgba(255,255,255,0.2)"></v-divider>
              
              <v-card-actions class="pa-3 justify-center">
                <v-btn
                  :color="module.color"
                  variant="elevated"
                  size="small"
                  class="text-none font-weight-bold px-4 rounded-pill action-btn"
                  append-icon="mdi-arrow-right"
                >
                  Launch {{ module.title }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

definePageMeta({
  layout: 'default'
});

const modules = ref([
  {
    title: 'Downloader',
    description: 'Download images and media from direct URLs seamlessly.',
    icon: 'mdi-cloud-download',
    color: 'orange-darken-3',
    route: '/downloader/image'
  },
  {
    title: 'Chat AI',
    description: 'Interact with the advanced Chat AI system.',
    icon: 'mdi-robot',
    color: 'deep-orange-darken-3',
    route: '/chatai'
  },
  {
    title: 'Typing',
    description: 'Practice and improve your typing skills.',
    icon: 'mdi-keyboard',
    color: 'red-darken-3',
    route: '/typing'
  },
  {
    title: 'Editor',
    description: 'Advanced code and text editor environment.',
    icon: 'mdi-code-braces',
    color: 'brown-darken-2',
    route: '/editor'
  },
  {
    title: 'Webview Manager',
    description: 'Manage and monitor all active webviews.',
    icon: 'mdi-web',
    color: 'orange-darken-4',
    route: '/webview-manager'
  }
]);

const embers = ref([]);

onMounted(() => {
  const emberArray = [];
  // Generate 80 random realistic embers
  for (let i = 0; i < 80; i++) {
    emberArray.push({
      id: i,
      left: Math.random() * 100,
      duration: Math.random() * 4 + 3, // 3 to 7 seconds
      delay: Math.random() * 5, // 0 to 5 seconds delay
      size: Math.random() * 6 + 2, // 2px to 8px
      opacity: Math.random() * 0.6 + 0.4, // 0.4 to 1
      blur: Math.random() * 2 // 0 to 2px blur for depth
    });
  }
  embers.value = emberArray;
});
</script>

<style scoped>
.dashboard-wrapper {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  padding-bottom: 32px;
  /* Dark backdrop to make fire visible */
  background: radial-gradient(circle at bottom, #2d1000 0%, #0a0a0a 100%);
}

/* Base environment overlay for realistic lighting */
.fire-environment {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 40vh;
  background: linear-gradient(to top, rgba(255, 60, 0, 0.15) 0%, transparent 100%);
  animation: pulse-light 3s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: 1;
}

@keyframes pulse-light {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

/* Particles Container */
.embers-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  pointer-events: none;
}

.ember {
  position: absolute;
  bottom: -20px;
  background: radial-gradient(circle, #fffbd6 0%, #ffb74d 40%, #e65100 80%, transparent 100%);
  border-radius: 50%;
  box-shadow: 0 0 10px #ff9800, 0 0 20px #e65100;
  animation-name: floatUpEmber;
  animation-timing-function: ease-in;
  animation-iteration-count: infinite;
}

@keyframes floatUpEmber {
  0% {
    transform: translateY(0) scale(1) rotate(0deg);
    opacity: 1;
  }
  50% {
    transform: translateY(-50vh) translateX(20px) scale(1.2) rotate(180deg);
    opacity: 0.8;
  }
  100% {
    transform: translateY(-100vh) translateX(-20px) scale(0.5) rotate(360deg);
    opacity: 0;
  }
}

.z-10 {
  z-index: 10;
}

.text-white {
  color: #ffffff !important;
}

.text-opacity-80 {
  opacity: 0.8;
}
.text-opacity-70 {
  opacity: 0.7;
}

.card-hover-wrapper {
  perspective: 1000px;
}

.premium-glass-card {
  background: rgba(30, 30, 30, 0.4) !important;
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 120, 0, 0.2);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.card-hover-wrapper:hover .premium-glass-card {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(255, 100, 0, 0.8);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5),
              0 0 30px rgba(255, 80, 0, 0.3) inset,
              0 0 40px rgba(255, 120, 0, 0.2) !important;
}

.avatar-glow {
  box-shadow: 0 0 20px rgba(255, 120, 0, 0.5) !important;
  transition: transform 0.4s ease;
}

.card-hover-wrapper:hover .avatar-glow {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 0 30px rgba(255, 160, 0, 0.8) !important;
}

.action-btn {
  transition: transform 0.2s;
}

.action-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px currentColor !important;
}

/* Hyper-realistic Fire Text Animation */
.realistic-fire-text {
  color: #fff;
  text-shadow: 
    0 -2px 4px #fff,
    0 -6px 10px #ff0,
    0 -14px 20px #ff8000,
    0 -24px 40px #f00;
  animation: intenseFlicker 0.1s infinite alternate;
}

@keyframes intenseFlicker {
  0% {
    text-shadow: 
      0 -2px 4px #fff,
      0 -6px 10px #ff0,
      0 -14px 20px #ff8000,
      0 -24px 40px #f00,
      0 -30px 60px #f00;
  }
  100% {
    text-shadow: 
      0 -1px 3px #fff,
      0 -4px 8px #ff0,
      0 -10px 18px #ff8000,
      0 -20px 35px #f00,
      0 -25px 50px #800000;
  }
}
</style>
