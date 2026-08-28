<template>
  <div class="dashboard-wrapper">
    <!-- Dark/Fire Environment Overlay -->
    <div class="fire-environment"></div>
    
    <!-- Realistic Embers (Optimized) -->
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
          opacity: ember.opacity
        }"
      ></div>
    </div>

    <!-- Lightning Cursor Canvas -->
    <canvas ref="lightningCanvas" class="lightning-canvas"></canvas>

    <!-- Main Content -->
    <v-container class="py-4 py-md-8 position-relative z-10">
      <v-row justify="center" class="mb-4 mb-md-6">
        <v-col cols="12" class="text-center position-relative px-4">
          <h1 class="text-h5 text-md-h3 font-weight-black mb-2 dashboard-title">DASHBOARD</h1>
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
import { ref, onMounted, onUnmounted } from 'vue';

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
    route: '/chatai/qwenai'
  },
  {
    title: 'Typing',
    description: 'Practice and improve your typing skills.',
    icon: 'mdi-keyboard',
    color: 'red-darken-3',
    route: '/typing/typing-test'
  },
  {
    title: 'Editor',
    description: 'Advanced code and text editor environment.',
    icon: 'mdi-code-braces',
    color: 'brown-darken-2',
    route: '/editor'
  },
  {
    title: 'Learning',
    description: 'Master new languages including Hmong, Lao, and English.',
    icon: 'mdi-school',
    color: 'teal-darken-2',
    route: '/learning'
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

// Lightning Cursor Effect State
const lightningCanvas = ref(null);
let ctx = null;
let animationFrameId = null;
const trail = [];
let currentMouse = { x: -1000, y: -1000 };
let lastMoveTime = 0;

const onMouseMove = (e) => {
  currentMouse.x = e.clientX;
  currentMouse.y = e.clientY;
  lastMoveTime = Date.now();

  const jitterX = (Math.random() - 0.5) * 20;
  const jitterY = (Math.random() - 0.5) * 20;
  
  trail.push({ 
    x: currentMouse.x + jitterX, 
    y: currentMouse.y + jitterY, 
    age: 0 
  });
};

const resizeCanvas = () => {
  if (lightningCanvas.value && ctx) {
    const dpr = window.devicePixelRatio || 1;
    lightningCanvas.value.width = window.innerWidth * dpr;
    lightningCanvas.value.height = window.innerHeight * dpr;
    ctx.scale(dpr, dpr);
  }
};

const drawLightning = () => {
  if (!ctx || !lightningCanvas.value) return;
  
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

  // If mouse is perfectly still, generate stationary crackling electricity!
  if (currentMouse.x !== -1000 && (Date.now() - lastMoveTime > 30)) {
    if (Math.random() > 0.5) { // Create a dense plasma ball around the cursor
      const idleJitterX = (Math.random() - 0.5) * 30;
      const idleJitterY = (Math.random() - 0.5) * 30;
      trail.push({ 
        x: currentMouse.x + idleJitterX, 
        y: currentMouse.y + idleJitterY, 
        age: 0 
      });
    }
  }

  // Age all points in the trail
  for (let i = 0; i < trail.length; i++) {
    trail[i].age += 0.8; 
  }
  
  // Remove dead points
  while (trail.length > 0 && trail[0].age > 30) {
    trail.shift();
  }

  // Draw the lightning line if we have a trail
  if (trail.length > 1) {
    ctx.lineCap = 'round';
    ctx.lineJoin = 'miter';

    // 1. Draw the main thick cyan glow
    ctx.beginPath();
    for (let i = 0; i < trail.length; i++) {
      const p = trail[i];
      if (i === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    }
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.4)';
    ctx.lineWidth = 10;
    ctx.stroke();

    // 2. Draw a secondary wild crackling strand
    ctx.beginPath();
    for (let i = 0; i < trail.length; i++) {
      const p = trail[i];
      const wildX = (Math.random() - 0.5) * 25;
      const wildY = (Math.random() - 0.5) * 25;
      if (i === 0) ctx.moveTo(p.x + wildX, p.y + wildY);
      else ctx.lineTo(p.x + wildX, p.y + wildY);
    }
    ctx.strokeStyle = 'rgba(0, 200, 255, 0.6)';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // 3. Draw a tertiary smaller crackling strand
    ctx.beginPath();
    for (let i = 0; i < trail.length; i++) {
      const p = trail[i];
      const wildX = (Math.random() - 0.5) * 15;
      const wildY = (Math.random() - 0.5) * 15;
      if (i === 0) ctx.moveTo(p.x + wildX, p.y + wildY);
      else ctx.lineTo(p.x + wildX, p.y + wildY);
    }
    ctx.strokeStyle = 'rgba(200, 255, 255, 0.8)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // 4. Draw the stable white core
    ctx.beginPath();
    for (let i = 0; i < trail.length; i++) {
      const p = trail[i];
      if (i === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    }
    ctx.strokeStyle = 'rgba(255, 255, 255, 1)';
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  // Loop infinitely so stationary electricity works
  animationFrameId = requestAnimationFrame(drawLightning);
};

onMounted(() => {
  const emberArray = [];
  // Reduced embers from 80 to 40 to significantly improve GPU performance
  for (let i = 0; i < 40; i++) {
    emberArray.push({
      id: i,
      left: Math.random() * 100,
      duration: Math.random() * 4 + 4, // 4 to 8 seconds
      delay: Math.random() * 5, // 0 to 5 seconds delay
      size: Math.random() * 4 + 2, // 2px to 6px
      opacity: Math.random() * 0.5 + 0.3
    });
  }
  embers.value = emberArray;

  // Setup Lightning Canvas
  if (lightningCanvas.value) {
    ctx = lightningCanvas.value.getContext('2d');
    resizeCanvas();
    // Passive listeners improve scroll/mouse performance
    window.addEventListener('resize', resizeCanvas, { passive: true });
    window.addEventListener('mousemove', onMouseMove, { passive: true });
    drawLightning();
  }
});

onUnmounted(() => {
  if (animationFrameId) cancelAnimationFrame(animationFrameId);
  window.removeEventListener('resize', resizeCanvas);
  window.removeEventListener('mousemove', onMouseMove);
});
</script>

<style scoped>
.dashboard-wrapper {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  padding-bottom: 80px; /* Increased padding to prevent hover scale from triggering scrollbar */
  background: radial-gradient(circle at bottom, #2d1000 0%, #0a0a0a 100%);
}

.fire-environment {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 40vh;
  background: linear-gradient(to top, rgba(255, 60, 0, 0.15) 0%, transparent 100%);
  animation: pulse-light 4s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: 1;
}

@keyframes pulse-light {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

.lightning-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 3;
}

.embers-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  pointer-events: none;
  overflow: hidden; /* Crucial: Prevents embers at bottom: -20px from causing scrollbars */
}

.ember {
  position: absolute;
  bottom: -20px;
  background: radial-gradient(circle, #fffbd6 0%, #ffb74d 40%, #e65100 80%, transparent 100%);
  border-radius: 50%;
  animation-name: floatUpEmber;
  animation-timing-function: linear; /* Smoother performance than ease */
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
  transform-origin: center bottom; /* Ensures scaling up doesn't push the bottom edge down */
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

.dashboard-title {
  color: #ffffff;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
  letter-spacing: 2px;
}
</style>
