<template>
  <v-container fluid class="typing-master-container pa-0 fill-height align-start">
    <v-row class="ma-0 w-100 justify-center pt-8">
      <v-col cols="12" md="10" lg="8">
        
        <!-- Header & Lesson Selection -->
        <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between mb-6 gap-4">
          <div>
            <h1 class="text-h4 font-weight-bold text-white mb-1">Touch Typing Simulator</h1>
            <p class="text-subtitle-1 text-grey-lighten-1">Feel the difference and improve your English typing skills.</p>
          </div>
          <div class="d-flex flex-wrap align-center gap-3">
            <!-- Competitor Name Chip -->
            <v-chip
              color="amber-accent-3"
              variant="tonal"
              size="large"
              prepend-icon="mdi-account"
              class="font-weight-bold cursor-pointer"
              @click="nameDialog = true"
              title="Click to change your competitor name"
            >
              {{ competitorName || 'Set Competitor Name' }}
              <v-icon end size="16" class="ml-1">mdi-pencil</v-icon>
            </v-chip>

            <!-- Leaderboard Button -->
            <v-btn
              color="amber-accent-4"
              variant="tonal"
              prepend-icon="mdi-trophy"
              to="/typing/leaderboard"
              height="44"
              class="font-weight-bold"
            >Leaderboard</v-btn>

            <v-select
              v-model="selectedLesson"
              :items="lessons"
              item-title="title"
              return-object
              label="Select Lesson"
              variant="solo"
              bg-color="#334155"
              base-color="#f8fafc"
              color="blue-lighten-2"
              hide-details
              style="min-width: 220px;"
              density="comfortable"
              @update:modelValue="resetTest"
            ></v-select>
          </div>
        </div>

        <!-- Competitor Name Dialog -->
        <v-dialog v-model="nameDialog" max-width="450">
          <v-card class="bg-blue-grey-darken-4 text-white pa-2 rounded-xl">
            <v-card-title class="text-h5 font-weight-bold pa-4 border-b border-white-10 d-flex align-center">
              <v-icon color="amber-accent-3" class="mr-2">mdi-account-edit</v-icon>
              Competitor Registration
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p class="text-body-2 text-grey-lighten-1 mb-4">
                Enter your name or nickname to register your scores on the public Leaderboard (ແຂງຂັນກັນ).
              </p>
              <v-text-field
                v-model="tempCompetitorName"
                label="Your Name / Nickname"
                placeholder="e.g. JohnSpeed"
                variant="outlined"
                color="amber-accent-3"
                base-color="grey-lighten-1"
                autofocus
                @keydown.enter="saveCompetitorName"
              ></v-text-field>
            </v-card-text>
            <v-card-actions class="pa-4 pt-0">
              <v-spacer></v-spacer>
              <v-btn color="grey-lighten-1" variant="text" @click="nameDialog = false">Cancel</v-btn>
              <v-btn 
                color="amber-accent-4" 
                variant="flat" 
                @click="saveCompetitorName"
                :disabled="!tempCompetitorName.trim()"
              >Save Name</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Completion Modal -->
        <v-dialog v-model="isFinished" max-width="500" persistent>
          <v-card class="bg-blue-grey-darken-4 text-white pa-4 rounded-xl text-center">
            <div class="text-h2 my-2">🎉</div>
            <v-card-title class="text-h4 font-weight-black text-amber-accent-3 justify-center">
              Challenge Completed!
            </v-card-title>
            <div class="text-subtitle-1 text-grey-lighten-1 mb-6">
              Great job, <strong class="text-white">{{ competitorName }}</strong>!
            </div>

            <v-row class="mb-6 justify-center" dense>
              <v-col cols="4">
                <div class="stat-badge pa-3">
                  <div class="text-caption text-grey-lighten-1">Speed</div>
                  <div class="text-h5 font-weight-black text-amber-accent-3">{{ wpm }} <span class="text-caption">WPM</span></div>
                </div>
              </v-col>
              <v-col cols="4">
                <div class="stat-badge pa-3">
                  <div class="text-caption text-grey-lighten-1">Accuracy</div>
                  <div class="text-h5 font-weight-black text-green-accent-3">{{ Math.round(accuracy) }}%</div>
                </div>
              </v-col>
              <v-col cols="4">
                <div class="stat-badge pa-3">
                  <div class="text-caption text-grey-lighten-1">Time</div>
                  <div class="text-h5 font-weight-black text-orange-lighten-1">{{ formattedTime }}</div>
                </div>
              </v-col>
            </v-row>

            <v-card-actions class="d-flex flex-column gap-3 pa-0">
              <v-btn
                v-if="!hasSubmitted"
                color="amber-accent-4"
                variant="flat"
                block
                size="large"
                prepend-icon="mdi-trophy-award"
                @click="submitResult"
                :loading="submitting"
                class="font-weight-bold"
              >
                Submit Score to Leaderboard
              </v-btn>

              <v-btn
                v-else
                color="green-accent-3"
                variant="tonal"
                block
                size="large"
                prepend-icon="mdi-check-circle"
                disabled
              >
                Score Saved to Leaderboard!
              </v-btn>

              <div class="d-flex w-100 gap-2 mt-2">
                <v-btn
                  color="blue-lighten-2"
                  variant="outlined"
                  class="flex-grow-1"
                  prepend-icon="mdi-trophy"
                  to="/typing/leaderboard"
                >
                  Leaderboard
                </v-btn>
                <v-btn
                  color="red-lighten-1"
                  variant="tonal"
                  class="flex-grow-1"
                  prepend-icon="mdi-refresh"
                  @click="resetTest"
                >
                  Practice Again
                </v-btn>
              </div>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-row v-if="loading">
          <v-col class="text-center my-10">
            <v-progress-circular indeterminate color="blue-lighten-2" size="64"></v-progress-circular>
          </v-col>
        </v-row>

        <div v-else>
          <!-- Stats Row -->
          <v-row class="mb-6">
            <v-col cols="6" sm="3">
              <div class="stat-badge">
                <div class="text-caption text-grey-lighten-1 text-uppercase font-weight-bold">Speed (WPM)</div>
                <div class="text-h4 font-weight-black text-blue-lighten-2">{{ wpm }} <span class="text-body-2">WPM</span></div>
              </div>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="stat-badge">
                <div class="text-caption text-grey-lighten-1 text-uppercase font-weight-bold">Speed (CPM)</div>
                <div class="text-h4 font-weight-black text-cyan-accent-2">{{ Math.round(cpm) }} <span class="text-body-2">CPM</span></div>
              </div>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="stat-badge">
                <div class="text-caption text-grey-lighten-1 text-uppercase font-weight-bold">Accuracy</div>
                <div class="text-h4 font-weight-black text-green-accent-3">{{ Math.round(accuracy) }}%</div>
              </div>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="stat-badge">
                <div class="text-caption text-grey-lighten-1 text-uppercase font-weight-bold">Time</div>
                <div class="text-h4 font-weight-black text-orange-lighten-1">{{ formattedTime }}</div>
              </div>
            </v-col>
          </v-row>

          <!-- Typing Box -->
          <div class="typing-master-box pa-8 rounded-lg elevation-6 mb-8" 
               :class="{ 'error-flash': showErrorFlash }"
               @click="focusInput">
            
            <div class="d-flex justify-space-between align-center mb-3">
              <div class="text-subtitle-1 text-grey-lighten-1">Text Progress:</div>
              <div class="text-subtitle-1 text-white font-weight-bold">{{ progressPercentage }}%</div>
            </div>
            <v-progress-linear 
              :model-value="progressPercentage" 
              color="blue-lighten-2" 
              height="8" 
              class="mb-8 rounded-pill"
              bg-color="#1e293b"
            ></v-progress-linear>

            <div class="typing-text-display font-monospace text-h5">
              <span 
                v-for="(char, index) in targetTextArray" 
                :key="index" 
                :class="getCharClass(index)"
              >{{ char }}</span>
            </div>

            <div v-if="!isTyping && !isFinished && targetTextArray.length > 0" class="text-center mt-6 text-body-1 text-blue-grey-lighten-1 font-weight-medium">
              Click here and start typing to begin...
            </div>
          </div>

          <div class="d-flex justify-center mb-6" v-if="isFinished || isTyping || targetTextArray.length > 0">
            <v-btn
              color="red-lighten-1"
              variant="tonal"
              prepend-icon="mdi-refresh"
              @click="resetTest"
              class="mr-4"
            >Restart Lesson</v-btn>

            <v-btn
              v-if="isFinished"
              color="blue-lighten-1"
              prepend-icon="mdi-cloud-upload"
              @click="submitResult"
              :loading="submitting"
              :disabled="hasSubmitted"
            >
              {{ hasSubmitted ? 'Saved to Sheets' : 'Save to Google Sheets' }}
            </v-btn>
          </div>

          <!-- Graphical Keyboard -->
          <VirtualKeyboard 
            :target-char="targetChar" 
            :error-map="errorMap"
            :show-heatmap="isFinished"
          />

          <!-- Hidden Input for IME support -->
          <input 
            ref="hiddenInput"
            :value="userInput"
            @input="handleInputNative"
            class="hidden-input"
            type="text"
            :disabled="isFinished"
            autocomplete="off"
          />
        </div>
      </v-col>
    </v-row>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" color="success" timeout="3000">
      Result saved successfully to your Google Sheet!
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';

const loading = ref(true);
const lessons = ref([]);
const selectedLesson = ref(null);

const userInput = ref('');
const hiddenInput = ref(null);

const isTyping = ref(false);
const isFinished = ref(false);
const hasSubmitted = ref(false);
const startTime = ref(null);
const timeElapsedMs = ref(0);
const timeElapsed = computed(() => Math.floor(timeElapsedMs.value / 1000));
let timerInterval = null;

const errorMap = ref({});
const showErrorFlash = ref(false);

const submitting = ref(false);
const snackbar = ref(false);

const targetTextArray = computed(() => {
  if (!selectedLesson.value || !selectedLesson.value.content) return [];
  return selectedLesson.value.content.split('');
});

const targetChar = computed(() => {
  if (userInput.value.length < targetTextArray.value.length) {
    return targetTextArray.value[userInput.value.length];
  }
  return '';
});

// International Standard: 1 standard word = 5 keystrokes/characters
const cpm = computed(() => {
  if (timeElapsedMs.value === 0 || userInput.value.length === 0) return 0;
  const minutes = timeElapsedMs.value / 60000;
  return Math.round(userInput.value.length / minutes);
});

const wpm = computed(() => {
  if (timeElapsedMs.value === 0 || userInput.value.length === 0) return 0;
  const minutes = timeElapsedMs.value / 60000;
  const wordsTyped = userInput.value.length / 5;
  return Math.round(wordsTyped / minutes);
});

const accuracy = computed(() => {
  if (userInput.value.length === 0) return 100;
  // Official standard accuracy: (Correct Keystrokes / Total Keystrokes Pressed) * 100
  const totalErrors = Object.values(errorMap.value).reduce((a, b) => a + b, 0);
  const totalKeystrokes = userInput.value.length + totalErrors;
  if (totalKeystrokes === 0) return 100;
  return Math.max(0, Math.round(((totalKeystrokes - totalErrors) / totalKeystrokes) * 100));
});

const formattedTime = computed(() => {
  const totalSeconds = timeElapsed.value;
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
});

const progressPercentage = computed(() => {
  if (targetTextArray.value.length === 0) return 0;
  return Math.min(100, Math.round((userInput.value.length / targetTextArray.value.length) * 100));
});

const competitorName = ref('Player 1');
const nameDialog = ref(false);
const tempCompetitorName = ref('');

onMounted(async () => {
  if (typeof window !== 'undefined') {
    const savedName = localStorage.getItem('typing_competitor_name');
    if (savedName) {
      competitorName.value = savedName;
    }
    tempCompetitorName.value = competitorName.value;
  }
  await fetchLessons();
});

const saveCompetitorName = () => {
  if (tempCompetitorName.value.trim()) {
    competitorName.value = tempCompetitorName.value.trim();
    if (typeof window !== 'undefined') {
      localStorage.setItem('typing_competitor_name', competitorName.value);
    }
    nameDialog.value = false;
  }
};

const fetchLessons = async () => {
  loading.value = true;
  try {
    const res = await fetch('http://localhost:3001/api/typing-lessons');
    const data = await res.json();
    lessons.value = data;
    if (data.length > 0 && !selectedLesson.value) {
      selectedLesson.value = data[0];
      nextTick(() => {
        focusInput();
      });
    }
  } catch (err) {
    console.error('Error fetching lessons', err);
  } finally {
    loading.value = false;
  }
};

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval);
});

const focusInput = () => {
  if (hiddenInput.value && !isFinished.value) {
    hiddenInput.value.focus();
  }
};

const getCharClass = (index) => {
  if (index === userInput.value.length && !isFinished.value) {
    return 'char-active px-1';
  }
  
  if (index < userInput.value.length) {
    return userInput.value[index] === targetTextArray.value[index] ? 'char-correct' : 'char-incorrect';
  }

  return 'char-upcoming';
};

const handleInputNative = (e) => {
  const newValue = e.target.value;
  
  if (!isTyping.value && newValue.length > 0) {
    isTyping.value = true;
    startTime.value = Date.now();
    timerInterval = setInterval(() => {
      timeElapsedMs.value = Date.now() - startTime.value;
    }, 100);
  }

  // Strict Mode Enforcement
  let correctSoFar = true;
  let newValidInput = '';
  
  for (let i = 0; i < newValue.length; i++) {
    if (newValue[i] === targetTextArray.value[i]) {
      newValidInput += newValue[i];
    } else {
      correctSoFar = false;
      const targetChar = targetTextArray.value[i];
      if (targetChar) {
        errorMap.value[targetChar] = (errorMap.value[targetChar] || 0) + 1;
      }
      break;
    }
  }

  if (!correctSoFar) {
    userInput.value = newValidInput; // Update Vue state
    if (hiddenInput.value) {
      hiddenInput.value.value = newValidInput; // Force DOM sync
    }
    showErrorFlash.value = true;
    setTimeout(() => { showErrorFlash.value = false; }, 150);
  } else {
    userInput.value = newValidInput;
  }

  if (userInput.value.length >= targetTextArray.value.length) {
    finishTest();
  }
};

const finishTest = () => {
  if (timerInterval) clearInterval(timerInterval);
  if (startTime.value) {
    timeElapsedMs.value = Date.now() - startTime.value;
  }
  isTyping.value = false;
  isFinished.value = true;
};

const resetTest = () => {
  if (timerInterval) clearInterval(timerInterval);
  userInput.value = '';
  isTyping.value = false;
  isFinished.value = false;
  hasSubmitted.value = false;
  timeElapsedMs.value = 0;
  startTime.value = null;
  errorMap.value = {};
  showErrorFlash.value = false;
  nextTick(() => {
    focusInput();
  });
};

const submitResult = async () => {
  submitting.value = true;
  try {
    const res = await fetch('http://localhost:3001/api/typing-results', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: competitorName.value || 'Anonymous',
        lessonTitle: selectedLesson.value ? selectedLesson.value.title : 'Custom Practice',
        cpm: cpm.value,
        wpm: wpm.value,
        accuracy: accuracy.value,
        timeSeconds: formattedTime.value
      })
    });
    if (res.ok) {
      snackbar.value = true;
      hasSubmitted.value = true;
    }
  } catch (err) {
    console.error('Error saving result', err);
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.typing-master-container {
  background-color: #0f172a; /* Deep slate blue */
  min-height: 100vh;
}

.stat-badge {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.typing-master-box {
  background-color: #1e293b;
  border: 1px solid #334155;
  cursor: text;
  transition: background-color 0.1s ease;
}

.error-flash {
  background-color: rgba(239, 68, 68, 0.2) !important;
}

.typing-text-display {
  user-select: none;
  word-break: break-all;
}

.font-monospace {
  font-family: 'Courier New', Courier, monospace;
  line-height: 2.2;
  letter-spacing: 1px;
}

.char-correct {
  color: #64748b; /* Dimmed correct text */
}

.char-incorrect {
  color: #ef4444; /* Error text */
  text-decoration: underline;
  text-decoration-thickness: 2px;
}

.char-active {
  background-color: #60a5fa; /* TypingMaster blue cursor */
  color: #0f172a;
  border-radius: 4px;
}

.char-upcoming {
  color: #f1f5f9; /* Bright grey for text yet to be typed */
}

.hidden-input {
  position: absolute;
  opacity: 0;
  height: 0;
  width: 0;
  pointer-events: none;
}
</style>
