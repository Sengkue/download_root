<template>
  <div v-if="!isAuthChecked" class="d-flex justify-center align-center" style="min-height: 80vh;">
    <v-progress-circular indeterminate color="indigo-accent-3" size="64"></v-progress-circular>
  </div>
  <v-container v-else class="py-8" max-width="1000">
    <div class="d-flex align-center justify-space-between mb-8">
      <div>
        <h1 class="text-h4 font-weight-black gradient-text mb-1">My Profile</h1>
        <p class="text-subtitle-1 text-medium-emphasis">View your typing history and statistics</p>
      </div>
      <v-avatar size="64" color="indigo-lighten-4">
        <span class="text-h5 font-weight-bold text-indigo-darken-4">{{ userInitials }}</span>
      </v-avatar>
    </div>

    <!-- Stats Overview -->
    <v-row class="mb-8">
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="0">
          <v-card-text>
            <div class="d-flex align-center mb-2">
              <v-icon color="indigo-accent-3" class="mr-2">mdi-keyboard</v-icon>
              <span class="text-overline font-weight-bold">Total Tests</span>
            </div>
            <div class="text-h3 font-weight-black text-indigo-darken-4">{{ totalTests }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="0">
          <v-card-text>
            <div class="d-flex align-center mb-2">
              <v-icon color="green-accent-4" class="mr-2">mdi-speedometer</v-icon>
              <span class="text-overline font-weight-bold">Avg WPM</span>
            </div>
            <div class="text-h3 font-weight-black text-green-darken-4">{{ avgWpm }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="0">
          <v-card-text>
            <div class="d-flex align-center mb-2">
              <v-icon color="amber-darken-2" class="mr-2">mdi-target</v-icon>
              <span class="text-overline font-weight-bold">Avg Accuracy</span>
            </div>
            <div class="text-h3 font-weight-black text-amber-darken-4">{{ avgAccuracy }}%</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card" elevation="0">
          <v-card-text>
            <div class="d-flex align-center mb-2">
              <v-icon color="pink-accent-3" class="mr-2">mdi-trophy</v-icon>
              <span class="text-overline font-weight-bold">Best WPM</span>
            </div>
            <div class="text-h3 font-weight-black text-pink-darken-4">{{ bestWpm }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- History Table -->
    <v-card class="glass-table-card rounded-xl" elevation="0">
      <v-card-title class="pa-6 pb-2 d-flex align-center">
        <v-icon class="mr-3" color="indigo-darken-2">mdi-history</v-icon>
        <span class="text-h6 font-weight-bold">Recent History</span>
        <v-spacer></v-spacer>
        <v-btn icon="mdi-refresh" variant="text" color="indigo-darken-1" @click="fetchHistory" :loading="loading"></v-btn>
      </v-card-title>
      
      <v-data-table
        :headers="headers"
        :items="history"
        :loading="loading"
        class="bg-transparent px-4 pb-4"
        hover
      >
        <template v-slot:item.createdAt="{ item }">
          {{ formatDate(item.createdAt) }}
        </template>
        <template v-slot:item.wpm="{ item }">
          <v-chip color="green-darken-1" size="small" class="font-weight-bold px-3">
            {{ item.wpm }}
          </v-chip>
        </template>
        <template v-slot:item.accuracy="{ item }">
          <span :class="getAccuracyColor(item.accuracy)" class="font-weight-medium">
            {{ item.accuracy }}%
          </span>
        </template>
        <template v-slot:item.timeSeconds="{ item }">
          {{ item.timeSeconds }}s
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

definePageMeta({
  layout: 'typing'
});

const router = useRouter();
const user = ref(null);
const history = ref([]);
const loading = ref(true);
const isAuthChecked = ref(false);

const headers = [
  { title: 'Date', key: 'createdAt', width: '20%' },
  { title: 'Lesson', key: 'lessonTitle', width: '40%' },
  { title: 'WPM', key: 'wpm', width: '15%' },
  { title: 'Accuracy', key: 'accuracy', width: '15%' },
  { title: 'Time', key: 'timeSeconds', width: '10%' }
];

const userInitials = computed(() => {
  if (!user.value?.name) return 'U';
  return user.value.name.substring(0, 2).toUpperCase();
});

const totalTests = computed(() => history.value.length);
const avgWpm = computed(() => {
  if (history.value.length === 0) return 0;
  const sum = history.value.reduce((acc, curr) => acc + curr.wpm, 0);
  return Math.round(sum / history.value.length);
});
const avgAccuracy = computed(() => {
  if (history.value.length === 0) return 0;
  const sum = history.value.reduce((acc, curr) => acc + curr.accuracy, 0);
  return (sum / history.value.length).toFixed(1);
});
const bestWpm = computed(() => {
  if (history.value.length === 0) return 0;
  return Math.max(...history.value.map(h => h.wpm));
});

const formatDate = (dateString) => {
  const d = new Date(dateString);
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const getAccuracyColor = (acc) => {
  if (acc >= 95) return 'text-green-darken-2';
  if (acc >= 90) return 'text-amber-darken-3';
  return 'text-red-darken-2';
};

const fetchHistory = async () => {
  loading.value = true;
  const token = localStorage.getItem('typing_token');
  
  if (!token) {
    router.push('/typing/login');
    return;
  }

  try {
    const res = await fetch('http://localhost:3001/api/typing-history', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (res.ok) {
      history.value = await res.json();
    } else if (res.status === 401) {
      localStorage.removeItem('typing_token');
      localStorage.removeItem('typing_user');
      router.push('/typing/login');
    }
  } catch (err) {
    console.error('Failed to fetch history:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const userData = localStorage.getItem('typing_user');
  const token = localStorage.getItem('typing_token');
  if (userData && token) {
    user.value = JSON.parse(userData);
    fetchHistory();
    isAuthChecked.value = true;
  } else {
    router.push('/typing/login');
  }
});
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #4338ca, #7e22ce);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-card {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.6) !important;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(99, 102, 241, 0.1) !important;
}

.glass-table-card {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.6) !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04) !important;
}

/* Make Vuetify table transparent to let glassmorphism show through */
:deep(.v-table) {
  background: transparent !important;
}
:deep(.v-table th) {
  font-weight: 700 !important;
  color: #475569 !important;
  background: transparent !important;
}
:deep(.v-table td) {
  border-bottom-color: rgba(226, 232, 240, 0.5) !important;
}
</style>
