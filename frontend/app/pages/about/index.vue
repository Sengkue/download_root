<template>
  <div class="about-page">
    <v-container class="py-10">
      <div class="d-flex align-center justify-space-between mb-8">
        <div>
          <h1 class="text-h3 font-weight-black text-white mb-2 text-glow">Hello, I'm Seng Kue Vang</h1>
          <p class="text-h6 text-white opacity-80">Software Developer & Tech Enthusiast</p>
        </div>
      </div>

      <v-row>
        <!-- Profile Card -->
        <v-col cols="12" md="4">
          <v-card class="premium-glass-card h-100" elevation="10" rounded="xl">
            <div class="pa-6 text-center">
              <v-avatar size="150" class="elevation-6 mb-4 logo-circle">
                <img src="/images/seng_kue_vang_logo.jpg" alt="Logo" style="width: 100%; height: 100%; object-fit: cover;" />
              </v-avatar>
              <h2 class="text-h5 font-weight-bold text-white mb-1">Seng Kue Vang</h2>
              <v-chip color="blue-accent-2" variant="flat" class="font-weight-bold mb-4">
                Full-Stack Developer
              </v-chip>
              <div class="d-flex justify-center gap-3">
                <v-btn icon="mdi-github" variant="text" color="white" href="https://github.com" target="_blank"></v-btn>
                <v-btn icon="mdi-linkedin" variant="text" color="white" href="https://linkedin.com" target="_blank"></v-btn>
                <v-btn icon="mdi-email" variant="text" color="white" href="mailto:contact@example.com"></v-btn>
              </div>
            </div>
          </v-card>
        </v-col>

        <!-- Bio Content -->
        <v-col cols="12" md="8">
          <v-card class="premium-glass-card h-100" elevation="10" rounded="xl">
            <v-card-title class="text-h5 font-weight-bold text-white pa-6 pb-2">
              <v-icon start color="blue-accent-2" class="mr-2">mdi-account-details</v-icon>
              About Me
            </v-card-title>
            <v-card-text class="pa-6 pt-2">
              <p class="text-body-1 text-white opacity-90 mb-4 line-height-relaxed">
                Welcome to my personal corner of the web! I am a passionate developer focusing on building elegant, performant, and user-friendly applications.
              </p>
              <p class="text-body-1 text-white opacity-90 mb-4 line-height-relaxed">
                My journey in tech involves working with various modern technologies including Vue, Nuxt, Vuetify, and more. I love crafting seamless user experiences with a touch of glassmorphism and modern UI design.
              </p>
              
              <h3 class="text-h6 font-weight-bold text-white mt-6 mb-4 border-bottom-subtle pb-2">Technical Skills</h3>
              <div class="d-flex flex-wrap gap-2">
                <v-chip v-for="skill in skills" :key="skill" color="rgba(255,255,255,0.1)" class="text-white font-weight-medium">
                  {{ skill }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue';

definePageMeta({
  layout: 'about'
});

const skills = ref([
  'Vue.js', 'Nuxt 3', 'Vuetify', 'JavaScript', 'TypeScript', 
  'HTML/CSS', 'Node.js', 'Git', 'Responsive Design'
]);
</script>

<style scoped>
.about-page {
  width: 100%;
}

.text-glow {
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
}

.premium-glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.premium-glass-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3) !important;
  border-color: rgba(255, 255, 255, 0.2);
}

.logo-circle {
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.1);
}

.gap-3 {
  gap: 12px;
}

.gap-2 {
  gap: 8px;
}

.opacity-90 { opacity: 0.9; }
.opacity-80 { opacity: 0.8; }

.line-height-relaxed {
  line-height: 1.8;
}

.border-bottom-subtle {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
