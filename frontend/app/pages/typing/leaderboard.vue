<template>
  <v-container fluid class="leaderboard-container pa-4 pa-md-8 text-slate-800">
    <v-row class="ma-0 justify-center">
      <v-col cols="12" lg="10" xl="8">
        
        <!-- Header -->
        <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between mb-8 gap-4">
          <div>
            <div class="d-flex align-center gap-2 mb-1">
              <v-icon color="amber-darken-2" size="36">mdi-trophy-award</v-icon>
              <h1 class="text-h4 font-weight-black text-indigo-darken-4">Typing Leaderboard</h1>
            </div>
            <p class="text-subtitle-1 text-slate-500">
              ອັນດັບຄົນພິມໄວທີ່ສຸດ - Top Competitors Ranked by Speed (WPM)
            </p>
          </div>

          <div class="d-flex align-center gap-3">
            <v-btn
              color="indigo-darken-2"
              variant="flat"
              prepend-icon="mdi-keyboard-outline"
              to="/typing/typing-test"
              height="48"
              class="font-weight-bold text-white rounded-pill shadow-btn px-5"
            >
              Start Challenge
            </v-btn>
            
            <v-btn
              icon="mdi-refresh"
              variant="tonal"
              color="indigo-darken-2"
              @click="fetchLeaderboard"
              :loading="loading"
              title="Refresh Scores"
              class="bg-white elevation-1"
            ></v-btn>
          </div>
        </div>

        <!-- Filter bar -->
        <v-card class="bg-white text-slate-800 pa-4 rounded-2xl mb-8 elevation-2">
          <v-row align="center" dense>
            <v-col cols="12" sm="6" md="4">
              <v-select
                v-model="selectedLessonFilter"
                :items="lessonOptions"
                label="Filter by Lesson"
                variant="outlined"
                density="compact"
                hide-details
                color="indigo-darken-2"
                base-color="slate-400"
                class="rounded-lg"
                @update:modelValue="fetchLeaderboard"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" md="8" class="d-flex justify-end">
              <span class="text-caption text-slate-500 d-flex align-center font-weight-medium">
                <v-icon size="16" class="mr-1 text-green-darken-2">mdi-check-circle</v-icon>
                Rankings calculated by Official Standard WPM (5 chars/word)
              </span>
            </v-col>
          </v-row>
        </v-card>

        <!-- Loading state -->
        <v-row v-if="loading">
          <v-col class="text-center my-12">
            <v-progress-circular indeterminate color="indigo-accent-3" size="64"></v-progress-circular>
            <p class="text-slate-500 mt-4">Loading championship leaderboard...</p>
          </v-col>
        </v-row>

        <div v-else>
          <!-- Top 3 Podium -->
          <v-row class="mb-8 justify-center align-end" v-if="topThree.length > 0">
            <!-- 2nd Place (Silver) -->
            <v-col cols="12" sm="4" class="order-2 order-sm-1" v-if="topThree[1]">
              <v-card class="podium-card silver pa-5 text-center elevation-3 rounded-2xl bg-white">
                <div class="podium-badge silver-badge mb-2">🥈 2nd Place</div>
                <v-avatar color="slate-100" size="64" class="mb-3 border-silver bg-grey-lighten-3">
                  <v-icon size="36" color="grey-darken-1">mdi-account</v-icon>
                </v-avatar>
                <div class="text-h6 font-weight-bold text-slate-800 text-truncate">{{ topThree[1].username }}</div>
                <div class="text-h4 font-weight-black text-slate-700 my-2">{{ topThree[1].wpm }} <span class="text-body-2">WPM</span></div>
                <div class="text-caption text-slate-500 font-weight-medium">{{ topThree[1].cpm }} CPM • {{ topThree[1].accuracy }}% Acc</div>
                <div class="text-caption text-slate-400 text-truncate mt-1">{{ topThree[1].lessonTitle }}</div>
              </v-card>
            </v-col>

            <!-- 1st Place (Gold) -->
            <v-col cols="12" sm="4" class="order-1 order-sm-2">
              <v-card class="podium-card gold pa-6 text-center elevation-6 rounded-2xl bg-white">
                <div class="podium-crown">👑</div>
                <div class="podium-badge gold-badge mb-2">🥇 Champion</div>
                <v-avatar color="amber-lighten-4" size="80" class="mb-3 border-gold">
                  <v-icon size="48" color="amber-darken-3">mdi-trophy</v-icon>
                </v-avatar>
                <div class="text-h5 font-weight-black text-indigo-darken-4 text-truncate">{{ topThree[0].username }}</div>
                <div class="text-h3 font-weight-black text-amber-darken-3 my-2">{{ topThree[0].wpm }} <span class="text-h6 font-weight-medium">WPM</span></div>
                <div class="text-body-2 text-slate-600 font-weight-bold">{{ topThree[0].cpm }} CPM • {{ topThree[0].accuracy }}% Accuracy</div>
                <div class="text-caption text-amber-darken-2 text-truncate mt-1 font-italic">{{ topThree[0].lessonTitle }}</div>
              </v-card>
            </v-col>

            <!-- 3rd Place (Bronze) -->
            <v-col cols="12" sm="4" class="order-3 order-sm-3" v-if="topThree[2]">
              <v-card class="podium-card bronze pa-5 text-center elevation-3 rounded-2xl bg-white">
                <div class="podium-badge bronze-badge mb-2">🥉 3rd Place</div>
                <v-avatar color="orange-lighten-4" size="64" class="mb-3 border-bronze">
                  <v-icon size="36" color="brown-darken-2">mdi-account</v-icon>
                </v-avatar>
                <div class="text-h6 font-weight-bold text-slate-800 text-truncate">{{ topThree[2].username }}</div>
                <div class="text-h4 font-weight-black text-amber-darken-4 my-2">{{ topThree[2].wpm }} <span class="text-body-2">WPM</span></div>
                <div class="text-caption text-slate-500 font-weight-medium">{{ topThree[2].cpm }} CPM • {{ topThree[2].accuracy }}% Acc</div>
                <div class="text-caption text-slate-400 text-truncate mt-1">{{ topThree[2].lessonTitle }}</div>
              </v-card>
            </v-col>
          </v-row>

          <!-- Full Table (Light Glassmorphic) -->
          <v-card class="bg-white rounded-2xl elevation-3 overflow-hidden">
            <v-card-title class="pa-5 font-weight-bold text-h6 text-indigo-darken-4 d-flex align-center justify-space-between border-b">
              <span>Full Rankings ({{ leaderboard.length }})</span>
              <span class="text-caption text-slate-500">Sorted by Speed (WPM)</span>
            </v-card-title>

            <v-table class="bg-transparent text-slate-800" hover>
              <thead>
                <tr>
                  <th class="text-left text-slate-600 font-weight-bold">Rank</th>
                  <th class="text-left text-slate-600 font-weight-bold">Competitor</th>
                  <th class="text-left text-slate-600 font-weight-bold">WPM (Speed)</th>
                  <th class="text-left text-slate-600 font-weight-bold">CPM</th>
                  <th class="text-left text-slate-600 font-weight-bold">Accuracy</th>
                  <th class="text-left text-slate-600 font-weight-bold">Lesson</th>
                  <th class="text-right text-slate-600 font-weight-bold">Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in leaderboard" :key="item.id" class="leaderboard-row">
                  <td>
                    <span :class="getRankBadgeClass(item.rank)" class="rank-badge">
                      {{ item.rank <= 3 ? ['🥇', '🥈', '🥉'][item.rank - 1] : '#' + item.rank }}
                    </span>
                  </td>
                  <td>
                    <div class="d-flex align-center">
                      <v-avatar size="32" color="indigo-lighten-5" class="mr-3">
                        <v-icon size="18" color="indigo-darken-2">mdi-account</v-icon>
                      </v-avatar>
                      <span class="font-weight-bold text-slate-900">{{ item.username }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="text-h6 font-weight-black text-indigo-darken-3">{{ item.wpm }}</span>
                    <span class="text-caption text-slate-400 ml-1">WPM</span>
                  </td>
                  <td>
                    <span class="text-body-1 font-weight-bold text-teal-darken-2">{{ item.cpm }}</span>
                    <span class="text-caption text-slate-400 ml-1">CPM</span>
                  </td>
                  <td>
                    <v-chip
                      size="small"
                      :color="item.accuracy >= 95 ? 'green-darken-2' : item.accuracy >= 85 ? 'amber-darken-3' : 'orange-darken-3'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      {{ item.accuracy }}%
                    </v-chip>
                  </td>
                  <td class="text-slate-600 text-truncate" style="max-width: 180px;">
                    {{ item.lessonTitle }}
                  </td>
                  <td class="text-right text-caption text-slate-400">
                    {{ formatDate(item.date) }}
                  </td>
                </tr>

                <tr v-if="leaderboard.length === 0">
                  <td colspan="7" class="text-center py-10 text-slate-500">
                    <v-icon size="48" class="mb-2 text-slate-400">mdi-timer-off-outline</v-icon>
                    <div>No typing records found yet. Be the first to complete a challenge!</div>
                    <v-btn
                      color="indigo-darken-2"
                      class="mt-4 font-weight-bold text-white rounded-pill"
                      to="/typing/typing-test"
                    >Take the Test</v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card>
        </div>

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
definePageMeta({
  layout: 'typing'
});

import { ref, computed, onMounted } from 'vue';

const loading = ref(true);
const leaderboard = ref([]);
const lessons = ref([]);
const selectedLessonFilter = ref('All');

const lessonOptions = computed(() => {
  return ['All', ...lessons.value.map(l => l.title)];
});

const topThree = computed(() => {
  return leaderboard.value.slice(0, 3);
});

onMounted(async () => {
  await Promise.all([
    fetchLeaderboard(),
    fetchLessons()
  ]);
});

const fetchLeaderboard = async () => {
  loading.value = true;
  try {
    const url = selectedLessonFilter.value && selectedLessonFilter.value !== 'All'
      ? `http://localhost:3005/api/typing-leaderboard?lessonTitle=${encodeURIComponent(selectedLessonFilter.value)}`
      : 'http://localhost:3005/api/typing-leaderboard';
    
    const res = await fetch(url);
    const data = await res.json();
    leaderboard.value = Array.isArray(data) ? data : [];
  } catch (err) {
    console.error('Error fetching leaderboard', err);
    leaderboard.value = [];
  } finally {
    loading.value = false;
  }
};

const fetchLessons = async () => {
  try {
    const res = await fetch('http://localhost:3005/api/typing-lessons');
    const data = await res.json();
    lessons.value = Array.isArray(data) ? data : [];
  } catch (err) {
    console.error('Error fetching lessons for filter', err);
  }
};

const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'badge-gold';
  if (rank === 2) return 'badge-silver';
  if (rank === 3) return 'badge-bronze';
  return 'badge-normal';
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return isNaN(date) ? dateStr : date.toLocaleDateString();
};
</script>

<style scoped>
.podium-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
}

.podium-card:hover {
  transform: translateY(-4px);
}

.podium-crown {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 2rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, -6px); }
}

.podium-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: bold;
}

.gold-badge {
  background-color: rgba(245, 158, 11, 0.15);
  color: #b45309;
}

.silver-badge {
  background-color: rgba(148, 163, 184, 0.2);
  color: #475569;
}

.bronze-badge {
  background-color: rgba(217, 119, 6, 0.15);
  color: #92400e;
}

.border-gold { border: 3px solid #f59e0b; }
.border-silver { border: 3px solid #94a3b8; }
.border-bronze { border: 3px solid #d97706; }

.rank-badge {
  font-weight: 900;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  font-size: 1.1rem;
}

.badge-gold { font-size: 1.4rem; }
.badge-silver { font-size: 1.4rem; }
.badge-bronze { font-size: 1.4rem; }
.badge-normal { color: #64748b; font-size: 0.95rem; }

.leaderboard-row {
  transition: background-color 0.15s ease;
}

.leaderboard-row:hover {
  background-color: rgba(99, 102, 241, 0.04) !important;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
