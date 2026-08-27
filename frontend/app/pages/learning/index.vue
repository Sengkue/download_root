<template>
  <div class="learning-wrapper">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="animated-background"></div>
      <v-container class="position-relative z-10 text-center py-10">
        <h1 class="text-h3 font-weight-black text-white mb-2 glowing-text">Learning Center</h1>
        <p class="text-h6 text-white opacity-80">Expand your knowledge. Master new languages today.</p>
      </v-container>
    </div>

    <!-- Main Content -->
    <v-container class="py-6">
      <v-row>
        <!-- Course Grid -->
        <v-col cols="12">
          <!-- Category Filter Chips -->
          <div class="d-flex flex-wrap gap-2 mb-6 justify-center">
            <v-chip
              v-for="cat in categories"
              :key="cat.id"
              :color="activeCategory === cat.id ? cat.color : 'white'"
              :variant="activeCategory === cat.id ? 'elevated' : 'outlined'"
              @click="activeCategory = cat.id"
              class="font-weight-bold mx-1"
              size="large"
            >
              <v-icon start :icon="cat.icon"></v-icon>
              {{ cat.title }}
            </v-chip>
          </div>

          <TransitionGroup name="fade-slide" tag="div" class="v-row">
            <v-col 
              v-for="course in activeCourses" 
              :key="course.id"
              cols="12" sm="6" lg="4"
            >
              <div class="card-hover-wrapper h-100">
                <v-card class="premium-glass-card course-card h-100 d-flex flex-column" elevation="10" rounded="xl">
                  <div class="course-header pa-4 text-center" :style="{ background: `linear-gradient(135deg, ${course.color1}, ${course.color2})` }">
                    <v-avatar size="64" class="mb-2 elevation-4" color="rgba(255,255,255,0.2)">
                      <span class="text-h4 font-weight-bold text-white">{{ course.flag }}</span>
                    </v-avatar>
                    <h3 class="text-h6 text-white font-weight-bold">{{ course.title }}</h3>
                  </div>
                  
                  <v-card-text class="pa-4 flex-grow-1 d-flex flex-column">
                    <p class="text-body-2 text-white opacity-80 mb-4">{{ course.description }}</p>
                    
                    <div class="mt-auto">
                      <div class="d-flex justify-space-between text-caption text-white opacity-60 mb-1">
                        <span>Progress</span>
                        <span>{{ course.progress }}%</span>
                      </div>
                      <v-progress-linear
                        :model-value="course.progress"
                        :color="course.baseColor"
                        height="6"
                        rounded
                        class="mb-4"
                      ></v-progress-linear>
                    </div>
                  </v-card-text>

                  <v-divider color="rgba(255,255,255,0.1)"></v-divider>
                  
                  <v-card-actions class="pa-3">
                    <v-btn
                      block
                      variant="elevated"
                      :color="course.baseColor"
                      class="text-none font-weight-bold rounded-pill action-btn"
                    >
                      Start Learning
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </div>
            </v-col>
          </TransitionGroup>

          <!-- Empty State if no courses -->
          <div v-if="activeCourses.length === 0" class="text-center py-10">
            <v-icon size="64" color="white" class="opacity-40 mb-4">mdi-book-remove-multiple</v-icon>
            <h3 class="text-h5 text-white opacity-60">No courses available in this category</h3>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Use the new learning layout!
definePageMeta({
  layout: 'learning'
});

const activeCategory = ref('hmong');

const categories = ref([
  { id: 'hmong', title: 'Hmong', icon: 'mdi-translate', color: 'blue-accent-2' },
  { id: 'lao', title: 'Lao', icon: 'mdi-earth', color: 'red-accent-2' },
  { id: 'english', title: 'English', icon: 'mdi-alphabet-latin', color: 'deep-purple-accent-2' },
  { id: 'vocab', title: 'Vocab', icon: 'mdi-book-open-page-variant', color: 'green-accent-4' },
]);

const allCourses = ref([
  { id: 'h1', category: 'hmong', title: 'Hmong Basics', flag: 'H', description: 'Learn the foundational alphabet, tones, and basic greetings in Hmong.', progress: 45, color1: '#1E88E5', color2: '#42A5F5', baseColor: 'blue-accent-2' },
  { id: 'h2', category: 'hmong', title: 'Everyday Phrases', flag: 'H', description: 'Practical sentences for daily conversations and interactions.', progress: 10, color1: '#1976D2', color2: '#1E88E5', baseColor: 'blue-darken-1' },
  { id: 'h3', category: 'hmong', title: 'Advanced Grammar', flag: 'H', description: 'Deep dive into sentence structures and complex modifiers.', progress: 0, color1: '#0D47A1', color2: '#1565C0', baseColor: 'blue-darken-3' },
  
  { id: 'l1', category: 'lao', title: 'Lao Consonants', flag: '🇱🇦', description: 'Master the Lao alphabet consonants and their classes.', progress: 80, color1: '#E53935', color2: '#EF5350', baseColor: 'red-accent-2' },
  { id: 'l2', category: 'lao', title: 'Vowels & Tones', flag: '🇱🇦', description: 'Understand how vowels interact with consonants and tone marks.', progress: 20, color1: '#D32F2F', color2: '#E53935', baseColor: 'red-darken-1' },
  
  { id: 'e1', category: 'english', title: 'Grammar Essentials', flag: '🇬🇧', description: 'Build a strong foundation with English tenses and parts of speech.', progress: 65, color1: '#5E35B1', color2: '#7E57C2', baseColor: 'deep-purple-accent-2' },
  { id: 'e2', category: 'english', title: 'Business English', flag: '🇺🇸', description: 'Professional communication skills for the modern workplace.', progress: 5, color1: '#4527A0', color2: '#5E35B1', baseColor: 'deep-purple-darken-1' },
  { id: 'e3', category: 'english', title: 'IELTS Preparation', flag: '🎓', description: 'Comprehensive training for reading, writing, listening, and speaking.', progress: 0, color1: '#311B92', color2: '#4527A0', baseColor: 'deep-purple-darken-3' },

  { id: 'v1', category: 'vocab', title: 'Daily Top 500', flag: '📚', description: 'The 500 most frequently used words across multiple languages.', progress: 100, color1: '#43A047', color2: '#66BB6A', baseColor: 'green-accent-4' },
]);

const activeCourses = computed(() => {
  return allCourses.value.filter(c => c.category === activeCategory.value);
});
</script>

<style scoped>
.learning-wrapper {
  /* Using transparent because layout handles background */
  background: transparent;
  width: 100%;
}

.hero-section {
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0 0 24px 24px;
}

.animated-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(30,136,229,0.1), rgba(229,57,53,0.1), rgba(94,53,177,0.1));
  background-size: 400% 400%;
  animation: gradientBG 10s ease infinite;
  z-index: 1;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.glowing-text {
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
}

.z-10 {
  z-index: 10;
}

.opacity-80 { opacity: 0.8; }
.opacity-70 { opacity: 0.7; }
.opacity-60 { opacity: 0.6; }
.opacity-40 { opacity: 0.4; }

/* Premium Glass Card */
.premium-glass-card {
  background: rgba(30, 30, 40, 0.4) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Course Card Hover Effects */
.card-hover-wrapper {
  perspective: 1000px;
}

.course-card {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
}

.card-hover-wrapper:hover .course-card {
  transform: translateY(-8px);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4),
              0 0 20px rgba(255, 255, 255, 0.05) inset !important;
}

.course-header {
  position: relative;
  overflow: hidden;
}

.course-header::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.3));
}

.course-header > * {
  position: relative;
  z-index: 2;
}

.action-btn {
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-btn:hover {
  transform: scale(1.02);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
}

/* Animations */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
.fade-slide-move {
  transition: transform 0.4s ease;
}
</style>
