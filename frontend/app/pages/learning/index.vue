<template>
  <div class="learning-wrapper">
    <!-- Hero Section -->
    <div class="hero-section bg-primary text-on-primary">
      <div class="animated-background"></div>
      <v-container class="position-relative z-10 text-center py-10">
        <h1 class="text-h3 font-weight-black text-on-primary mb-2 glowing-text">Learning Center</h1>
        <p class="text-h6 text-primary-fixed opacity-80">Expand your knowledge. Master new languages today.</p>
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
              :color="activeCategory === cat.id ? cat.color : 'surface-container'"
              :text-color="activeCategory === cat.id ? 'white' : 'on-surface-variant'"
              :variant="activeCategory === cat.id ? 'elevated' : 'flat'"
              @click="activeCategory = cat.id"
              class="font-weight-bold mx-1"
              size="large"
            >
              <v-icon start :icon="cat.icon" :color="activeCategory === cat.id ? 'white' : cat.color"></v-icon>
              {{ cat.title }}
            </v-chip>
          </div>

          <!-- Hmong Dashboard Intro -->
          <v-slide-y-transition>
            <div v-if="activeCategory === 'hmong'" class="mb-8">
              <v-card class="bg-surface-container-lowest pa-6 shadow-sm" elevation="0" border rounded="xl" style="border-left: 4px solid var(--v-theme-primary) !important;">
                <v-row align="center">
                  <v-col cols="12" md="7">
                    <h2 class="text-h4 font-weight-black text-primary mb-4" style="letter-spacing: -0.01em;">How to learn Hmong on this platform</h2>
                    <p class="text-body-1 text-on-surface-variant mb-4">
                      Welcome to the Hmong Learning Hub! This dashboard is designed to provide you with a variety of resources to master the language:
                    </p>
                    <v-list class="bg-transparent text-on-surface" density="compact">
                      <v-list-item prepend-icon="mdi-book-open-variant" class="mb-2">
                        <template v-slot:title>
                          <strong class="text-on-surface">Interactive Flipbook</strong>
                        </template>
                        <template v-slot:subtitle>
                          <span class="text-on-surface-variant">Read through our comprehensive digital book featuring rich, page-turning interactions.</span>
                        </template>
                      </v-list-item>
                      <v-list-item prepend-icon="mdi-youtube" class="mb-2">
                        <template v-slot:title>
                          <strong class="text-on-surface">Video Lessons</strong>
                        </template>
                        <template v-slot:subtitle>
                          <span class="text-on-surface-variant">Watch expert advice and pronunciation guides directly from YouTube.</span>
                        </template>
                      </v-list-item>
                      <v-list-item prepend-icon="mdi-play-circle" class="mb-2">
                        <template v-slot:title>
                          <strong class="text-on-surface">Video Learning</strong>
                        </template>
                        <template v-slot:subtitle>
                          <span class="text-on-surface-variant">Watch expert advice and pronunciation guides.</span>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-col>
                  <v-col cols="12" md="5">
                    <div class="video-wrapper rounded-xl overflow-hidden elevation-10" style="aspect-ratio: 16/9; background: #000;">
                      <iframe 
                        width="100%" 
                        height="100%" 
                        src="https://www.youtube.com/embed/s8pboIhSURc" 
                        title="YouTube video player" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        allowfullscreen
                      ></iframe>
                    </div>
                  </v-col>
                </v-row>
              </v-card>
            </div>
          </v-slide-y-transition>

          <TransitionGroup name="fade-slide" tag="div" class="v-row">
            <v-col 
              v-for="course in activeCourses" 
              :key="course.id"
              cols="12" sm="6" lg="4"
            >
              <div class="card-hover-wrapper h-100">
                <v-card class="bg-surface-container-lowest course-card h-100 d-flex flex-column shadow-sm" elevation="0" border rounded="xl">
                  <div 
                    class="course-image d-flex flex-column align-center justify-center position-relative overflow-hidden pa-4 text-center"
                    :style="{ 
                      background: course.thumbnailUrl 
                        ? `linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.8)), url(${course.thumbnailUrl}) center/cover no-repeat`
                        : `linear-gradient(135deg, ${course.color1} 0%, ${course.color2} 100%)` 
                    }"
                  >
                    <v-avatar size="64" class="mb-2 elevation-4" color="rgba(255,255,255,0.2)">
                      <span class="text-h4 font-weight-bold text-white">{{ course.flag }}</span>
                    </v-avatar>
                    <h3 class="text-h6 text-white font-weight-bold">{{ course.title }}</h3>
                  </div>
                  
                  <v-card-text class="pa-4 flex-grow-1 d-flex flex-column">
                    <p class="text-body-2 text-on-surface-variant mb-4">{{ course.description }}</p>
                    
                    <div class="mt-auto">
                      <div class="d-flex justify-space-between text-caption font-weight-bold text-on-surface-variant mb-1">
                        <span>Progress</span>
                        <span>{{ course.progress }}%</span>
                      </div>
                      <v-progress-linear
                        :model-value="course.progress"
                        :color="course.baseColor"
                        bg-color="surface-container"
                        height="6"
                        rounded
                        class="mb-4"
                      ></v-progress-linear>
                    </div>
                  </v-card-text>

                  <v-divider class="bg-surface-container-highest"></v-divider>
                  
                  <v-card-actions class="pa-3">
                    <v-btn
                      block
                      variant="elevated"
                      :color="course.baseColor"
                      class="text-none font-weight-bold rounded-pill action-btn"
                      @click="openCourse(course)"
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
            <v-icon size="64" color="outline-variant" class="mb-4">mdi-book-remove-multiple</v-icon>
            <h3 class="text-h5 text-on-surface-variant font-weight-medium">No courses available in this category</h3>
          </div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Flipbook Viewer Dialog -->
    <v-dialog v-model="flipbookDialog" fullscreen transition="dialog-bottom-transition">
      <v-card class="bg-grey-darken-4">
        <v-toolbar color="rgba(0,0,0,0.8)" theme="dark" class="border-b">
          <v-btn icon="mdi-close" @click="flipbookDialog = false"></v-btn>
          <v-toolbar-title class="font-weight-bold text-white">{{ currentFlipbookTitle }}</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <div class="iframe-container" style="height: calc(100vh - 64px); width: 100%; background: #222;">
          <iframe 
            v-if="flipbookDialog"
            :src="currentFlipbookUrl" 
            seamless="seamless" 
            scrolling="no" 
            frameborder="0" 
            allowtransparency="true" 
            allowfullscreen="true" 
            style="width: 100%; height: 100%;"
          ></iframe>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// Use the new learning layout!
definePageMeta({
  layout: 'learning'
});

const route = useRoute();
const router = useRouter();

const activeCategory = ref(route.query.category || 'hmong');

// Watch for category changes in URL
watch(() => route.query.category, (newCat) => {
  if (newCat) {
    activeCategory.value = newCat;
  }
});

const flipbookDialog = ref(false);
const currentFlipbookUrl = ref('');
const currentFlipbookTitle = ref('');

const getEmbedUrl = (url) => {
  if (!url) return '';
  
  // Handle standard youtube URLs: watch?v=ID or youtu.be/ID
  const youtubeRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/i;
  const match = url.match(youtubeRegex);
  
  if (match && match[1]) {
    return `https://www.youtube.com/embed/${match[1]}`;
  }
  
  return url;
};

const openCourse = (course) => {
  if (course.flipbookUrl || course.videoUrl) {
    let url = course.flipbookUrl || course.videoUrl;
    currentFlipbookUrl.value = getEmbedUrl(url);
    currentFlipbookTitle.value = course.title;
    flipbookDialog.value = true;
  } else {
    alert('This course content is coming soon!');
  }
};

const categories = ref([
  { id: 'hmong', title: 'Hmong', icon: 'mdi-translate', color: 'blue-accent-2' },
  { id: 'hmong-video', title: 'Video EPs', icon: 'mdi-youtube', color: 'red-accent-4' },
  { id: 'lao', title: 'Lao', icon: 'mdi-earth', color: 'red-accent-2' },
  { id: 'english', title: 'English', icon: 'mdi-alphabet-latin', color: 'deep-purple-accent-2' },
  { id: 'vocab', title: 'Vocab', icon: 'mdi-book-open-page-variant', color: 'green-accent-4' },
]);

const allCourses = ref([]);

const fetchCourses = async () => {
  try {
    const config = useRuntimeConfig();
    const apiBase = config.public.apiBase || 'http://localhost:3005';
    const res = await fetch(`${apiBase}/api/learning-videos`);
    if (res.ok) {
      const data = await res.json();
      allCourses.value = data.map(v => {
        let baseColor = 'grey';
        let color1 = '#333';
        let color2 = '#555';
        
        if (v.category === 'hmong') { baseColor = 'blue-accent-2'; color1 = '#1E88E5'; color2 = '#42A5F5'; }
        else if (v.category === 'hmong-video') { baseColor = 'red-accent-4'; color1 = '#D50000'; color2 = '#FF1744'; }
        else if (v.category === 'lao') { baseColor = 'red-accent-2'; color1 = '#E53935'; color2 = '#EF5350'; }
        else if (v.category === 'english') { baseColor = 'deep-purple-accent-2'; color1 = '#5E35B1'; color2 = '#7E57C2'; }
        else if (v.category === 'vocab') { baseColor = 'green-accent-4'; color1 = '#43A047'; color2 = '#66BB6A'; }

        let thumbnailUrl = '';
        if (v.videoUrl) {
          const youtubeRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/i;
          const match = v.videoUrl.match(youtubeRegex);
          if (match && match[1]) {
            thumbnailUrl = `https://img.youtube.com/vi/${match[1]}/hqdefault.jpg`;
          }
        }

        return {
          id: v.id,
          category: v.category,
          title: v.title,
          flag: v.flag || '▶️',
          description: v.description,
          progress: v.progress || 0,
          videoUrl: v.videoUrl,
          flipbookUrl: v.flipbookUrl,
          thumbnailUrl,
          baseColor,
          color1,
          color2
        };
      });
      // Call checkAutoOpen after data is loaded so the course can be found
      checkAutoOpen();
    }
  } catch (err) {
    console.error('Failed to fetch learning videos:', err);
  }
};

const activeCourses = computed(() => {
  return allCourses.value.filter(c => c.category === activeCategory.value);
});

// Auto-open course if specified in URL query
const checkAutoOpen = () => {
  const courseId = route.query.open;
  if (courseId) {
    const course = allCourses.value.find(c => c.id === courseId);
    if (course) {
      activeCategory.value = course.category;
      // Slight delay to ensure UI updates before opening dialog
      setTimeout(() => openCourse(course), 300);
    }
  }
};

onMounted(() => {
  fetchCourses();
});

watch(() => route.query.open, () => {
  checkAutoOpen();
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
