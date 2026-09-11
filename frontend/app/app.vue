<script setup>
import { ref, onMounted } from "vue";

const isAppLoading = ref(true);

onMounted(() => {
  // Use a slight delay to ensure smooth transition and allow fonts/images to render
  setTimeout(() => {
    isAppLoading.value = false;
  }, 600);
});
</script>

<template>
  <div>
    <!-- Smooth Fade Out Transition -->
    <Transition name="fade">
      <div v-if="isAppLoading" class="global-css-loader">
        <div class="loader-content">
          <!-- Modern animated spinner -->
          <div class="modern-spinner">
            <div class="ring"></div>
            <div class="ring"></div>
            <div class="ring"></div>
          </div>

          <h2 class="loader-title">
            <span class="text-gradient">System </span>Group
          </h2>
          <p class="loader-subtitle">Preparing your experience</p>
        </div>
      </div>
    </Transition>

    <!-- Main App Content -->
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  
  </div>
</template>

<style>
/* Global styles */
html,
body {
  margin: 0;
  padding: 0;
  font-family:
    "Inter",
    "Roboto",
    system-ui,
    -apple-system,
    sans-serif;
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1),
    backdrop-filter 0.8s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

/* Global CSS Loader */
.global-css-loader {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 99999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Modern Spinner (3 intersecting rings) */
.modern-spinner {
  position: relative;
  width: 72px;
  height: 72px;
  margin-bottom: 32px;
}

.modern-spinner .ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 4px solid transparent;
  animation: spin-ring 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
}

.modern-spinner .ring:nth-child(1) {
  border-top-color: #4caf50; /* Primary Green */
  animation-delay: 0s;
}

.modern-spinner .ring:nth-child(2) {
  border-right-color: #1a237e; /* Deep Blue */
  animation-delay: 0.15s;
}

.modern-spinner .ring:nth-child(3) {
  border-bottom-color: #00bcd4; /* Cyan Accent */
  animation-delay: 0.3s;
}

@keyframes spin-ring {
  0% {
    transform: rotate(0deg) scale(0.8);
    opacity: 0.5;
  }
  50% {
    transform: rotate(180deg) scale(1.1);
    opacity: 1;
  }
  100% {
    transform: rotate(360deg) scale(0.8);
    opacity: 0.5;
  }
}

/* Typography */
.loader-title {
  font-size: 36px;
  font-weight: 800;
  color: #1a237e;
  margin: 0 0 12px 0;
  letter-spacing: -0.5px;
}

.text-gradient {
  background: linear-gradient(135deg, #4caf50, #00bcd4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.loader-subtitle {
  font-size: 16px;
  color: #64748b;
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
}

/* Animated dots for subtitle */
.loader-subtitle::after {
  content: "";
  width: 24px;
  text-align: left;
  animation: dots 2s infinite steps(4, end);
}

@keyframes dots {
  0%,
  20% {
    content: "";
  }
  40% {
    content: ".";
  }
  60% {
    content: "..";
  }
  80%,
  100% {
    content: "...";
  }
}
</style>
