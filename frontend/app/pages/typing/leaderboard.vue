<template>
  <v-container fluid class="leaderboard-container pa-4 pa-md-8">
    <v-row class="ma-0 justify-center">
      <v-col cols="12" lg="10" xl="8">
        
        <!-- Header -->
        <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between mb-8 gap-4">
          <div>
            <div class="d-flex align-center gap-2 mb-1">
              <v-icon color="amber-accent-3" size="36">mdi-trophy-award</v-icon>
              <h1 class="text-h4 font-weight-black text-white">Typing Leaderboard</h1>
            </div>
            <p class="text-subtitle-1 text-grey-lighten-1">
              ອັນດັບຄົນພິມໄວທີ່ສຸດ - Top Competitors Ranked by Speed (WPM)
            </p>
          </div>

          <div class="d-flex align-center gap-3">
            <v-btn
              color="amber-accent-4"
              variant="flat"
              prepend-icon="mdi-keyboard-outline"
              to="/typing/typing-test"
              height="48"
              class="font-weight-bold"
            >
              Start Challenge
            </v-btn>
            
            <v-btn
              icon="mdi-refresh"
              variant="tonal"
              color="blue-lighten-2"
              @click="fetchLeaderboard"
              :loading="loading"
              title="Refresh Scores"
            ></v-btn>
          </div>
        </div>

        <!-- Filter bar -->
        <v-card class="bg-blue-grey-darken-4 text-white pa-4 rounded-xl mb-8 elevation-4 border-slate">
          <v-row align="center" dense>
            <v-col cols="12" sm="6" md="4">
              <v-select
                v-model="selectedLessonFilter"
                :items="lessonOptions"
                label="Filter by Lesson"
                variant="outlined"
                density="compact"
                hide-details
                color="amber-accent-3"
                base-color="grey-lighten-1"
                @update:modelValue="fetchLeaderboard"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" md="8" class="d-flex justify-end">
              <span class="text-caption text-grey-lighten-1 d-flex align-center">
                <v-icon size="16" class="mr-1 text-green-accent-3">mdi-check-circle</v-icon>
                Rankings calculated by Official Standard WPM (5 chars/word)
              </span>
            </v-col>
          </v-row>
        </v-card>

        <!-- Loading state -->
        <v-row v-if="loading">
          <v-col class="text-center my-12">
            <v-progress-circular indeterminate color="amber-accent-3" size="64"></v-progress-circular>
            <p class="text-grey-lighten-1 mt-4">Loading championship leaderboard...</p>
          </v-col>
        </v-row>

        <div v-else>
          <!-- Top 3 Podium -->
          <v-row class="mb-8 justify-center align-end" v-if="topThree.length > 0">
            <!-- 2nd Place (Silver) -->
            <v-col cols="12" sm="4" class="order-2 order-sm-1" v-if="topThree[1]">
              <v-card class="podium-card silver pa-5 text-center elevation-6 rounded-xl">
                <div class="podium-badge silver-badge mb-2">🥈 2nd Place</div>
                <v-avatar color="grey-darken-3" size="64" class="mb-3 border-silver">
                  <v-icon size="36" color="grey-lighten-2">mdi-account</v-icon>
                </v-avatar>
                <div class="text-h6 font-weight-bold text-white text-truncate">{{ topThree[1].username }}</div>
                <div class="text-h4 font-weight-black text-silver my-2">{{ topThree[1].wpm }} <span class="text-body-2">WPM</span></div>
                <div class="text-caption text-grey-lighten-1">{{ topThree[1].cpm }} CPM • {{ topThree[1].accuracy }}% Acc</div>
                <div class="text-caption text-grey text-truncate mt-1">{{ topThree[1].lessonTitle }}</div>
              </v-card>
            </v-col>

            <!-- 1st Place (Gold) -->
            <v-col cols="12" sm="4" class="order-1 order-sm-2">
              <v-card class="podium-card gold pa-6 text-center elevation-10 rounded-xl">
                <div class="podium-crown">👑</div>
                <div class="podium-badge gold-badge mb-2">🥇 Champion</div>
                <v-avatar color="amber-darken-4" size="80" class="mb-3 border-gold">
                  <v-icon size="48" color="amber-accent-2">mdi-trophy</v-icon>
                </v-avatar>
                <div class="text-h5 font-weight-black text-white text-truncate">{{ topThree[0].username }}</div>
                <div class="text-h3 font-weight-black text-amber-accent-3 my-2">{{ topThree[0].wpm }} <span class="text-h6 font-weight-medium">WPM</span></div>
                <div class="text-body-2 text-grey-lighten-1 font-weight-medium">{{ topThree[0].cpm }} CPM • {{ topThree[0].accuracy }}% Accuracy</div>
                <div class="text-caption text-amber-lighten-3 text-truncate mt-1 font-italic">{{ topThree[0].lessonTitle }}</div>
              </v-card>
            </v-col>

            <!-- 3rd Place (Bronze) -->
            <v-col cols="12" sm="4" class="order-3 order-sm-3" v-if="topThree[2]">
              <v-card class="podium-card bronze pa-5 text-center elevation-6 rounded-xl">
                <div class="podium-badge bronze-badge mb-2">🥉 3rd Place</div>
                <v-avatar color="brown-darken-3" size="64" class="mb-3 border-bronze">
                  <v-icon size="36" color="amber-lighten-3">mdi-account</v-icon>
                </v-avatar>
                <div class="text-h6 font-weight-bold text-white text-truncate">{{ topThree[2].username }}</div>
                <div class="text-h4 font-weight-black text-bronze my-2">{{ topThree[2].wpm }} <span class="text-body-2">WPM</span></div>
                <div class="text-caption text-grey-lighten-1">{{ topThree[2].cpm }} CPM • {{ topThree[2].accuracy }}% Acc</div>
                <div class="text-caption text-grey text-truncate mt-1">{{ topThree[2].lessonTitle }}</div>
              </v-card>
            </v-col>
          </v-row>

          <!-- Full Table -->
          <v-card class="bg-blue-grey-darken-4 rounded-xl elevation-6 border-slate overflow-hidden">
            <v-card-title class="pa-5 font-weight-bold text-h6 text-white d-flex align-center justify-space-between border-b border-white-10">
              <span>Full Rankings ({{ leaderboard.length }})</span>
              <span class="text-caption text-grey-lighten-1">Sorted by Speed (WPM)</span>
            </v-card-title>

            <v-table class="bg-transparent text-white" hover>
              <thead>
                <tr>
                  <th class="text-left text-grey-lighten-1 font-weight-bold">Rank</th>
                  <th class="text-left text-grey-lighten-1 font-weight-bold">Competitor</th>
                  <th class="text-left text-grey-lighten-1 font-weight-bold">WPM (Speed)</th>
                  <th class="text-left text-grey-lighten-1 font-weight-bold">CPM</th>
                  <th class="text-left text-grey-lighten-1 font-weight-bold">Accuracy</th>
                  <th class="text-left text-grey-lighten-1 font-weight-bold">Lesson</th>
                  <th class="text-right text-grey-lighten-1 font-weight-bold">Date</th>
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
                      <v-avatar size="32" color="blue-grey-darken-3" class="mr-3">
                        <v-icon size="18" color="blue-lighten-3">mdi-account</v-icon>
                      </v-avatar>
                      <span class="font-weight-bold text-white">{{ item.username }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="text-h6 font-weight-black text-amber-accent-3">{{ item.wpm }}</span>
                    <span class="text-caption text-grey-lighten-1 ml-1">WPM</span>
                  </td>
                  <td>
                    <span class="text-body-1 font-weight-medium text-cyan-accent-2">{{ item.cpm }}</span>
                    <span class="text-caption text-grey-lighten-1 ml-1">CPM</span>
                  </td>
                  <td>
                    <v-chip
                      size="small"
                      :color="item.accuracy >= 95 ? 'green-accent-3' : item.accuracy >= 85 ? 'amber-accent-3' : 'orange-accent-3'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      {{ item.accuracy }}%
                    </v-chip>
                  </td>
                  <td class="text-grey-lighten-1 text-truncate" style="max-width: 180px;">
                    {{ item.lessonTitle }}
                  </td>
                  <td class="text-right text-caption text-grey">
                    {{ formatDate(item.date) }}
                  </td>
                </tr>

                <tr v-if="leaderboard.length === 0">
                  <td colspan="7" class="text-center py-10 text-grey-lighten-1">
                    <v-icon size="48" class="mb-2 text-grey-darken-1">mdi-timer-off-outline</v-icon>
                    <div>No typing records found yet. Be the first to complete a challenge!</div>
                    <v-btn
                      color="amber-accent-4"
                      class="mt-4 font-weight-bold"
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
      ? `http://localhost:3001/api/typing-leaderboard?lessonTitle=${encodeURIComponent(selectedLessonFilter.value)}`
      : 'http://localhost:3001/api/typing-leaderboard';
    
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
    const res = await fetch('http://localhost:3001/api/typing-lessons');
    const data = await res.json();
    lessons.value = Array.isArray(data) ? data : [];
  } catch (err) {
    console.error('Error fetching lessons', err);
  }
};

const getRankBadgeClass = (rank) => {
  if (rank === 1) return 'badge-gold';
  if (rank === 2) return 'badge-silver';
  if (rank === 3) return 'badge-bronze';
  return 'badge-normal';
};

const formatDate = (isoString) => {
  if (!isoString) return '-';
  try {
    const d = new Date(isoString);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch {
    return isoString;
  }
};
</script>

<style scoped>
.leaderboard-container {
  background-color: #0f172a;
  min-height: 100vh;
}

.border-slate {
  border: 1px solid #334155;
}

.podium-card {
  position: relative;
  transition: transform 0.2s ease;
}

.podium-card:hover {
  transform: translateY(-4px);
}

.podium-card.gold {
  background: linear-gradient(145deg, #1e293b 0%, #1e1b4b 100%);
  border: 2px solid #f59e0b;
  box-shadow: 0 0 25px rgba(245, 158, 11, 0.25) !important;
}

.podium-card.silver {
  background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid #94a3b8;
}

.podium-card.bronze {
  background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid #b45309;
}

.podium-crown {
  font-size: 28px;
  position: absolute;
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
}

.podium-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: bold;
}

.gold-badge {
  background-color: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}

.silver-badge {
  background-color: rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
}

.bronze-badge {
  background-color: rgba(180, 83, 9, 0.2);
  color: #f59e0b;
}

.border-gold { border: 3px solid #f59e0b; }
.border-silver { border: 3px solid #94a3b8; }
.border-bronze { border: 3px solid #b45309; }

.text-silver { color: #e2e8f0; }
.text-bronze { color: #f59e0b; }

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
.badge-normal { color: #94a3b8; font-size: 0.95rem; }

.leaderboard-row {
  transition: background-color 0.15s ease;
}

.leaderboard-row:hover {
  background-color: rgba(255, 255, 255, 0.04) !important;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
