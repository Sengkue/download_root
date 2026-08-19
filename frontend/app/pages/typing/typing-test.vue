<template>
  <v-container fluid class="typing-master-container pa-2 pa-md-4 fill-height align-start">
    <v-row class="ma-0 w-100 justify-center pt-1 pt-md-2">
      <v-col cols="12" md="10" lg="9" xl="8">
        
        <!-- Minimalist Top Controls -->
        <div class="d-flex flex-wrap align-center justify-end mb-3 gap-2">
            <!-- Competitor Name Chip -->
            <v-chip
              color="indigo-darken-3"
              variant="flat"
              size="large"
              prepend-icon="mdi-account"
              class="font-weight-bold cursor-pointer text-white elevation-2"
              @click="nameDialog = true"
              title="Click to change your competitor name"
            >
              {{ competitorName || 'Set Competitor Name' }}
              <v-icon end size="16" class="ml-1">mdi-pencil</v-icon>
            </v-chip>

            <!-- Leaderboard Button -->
            <v-btn
              color="amber-darken-1"
              variant="flat"
              prepend-icon="mdi-trophy"
              to="/typing/leaderboard"
              height="44"
              class="font-weight-bold text-white elevation-2"
            >Leaderboard</v-btn>

            <!-- Sound Toggle -->
            <v-btn
              :icon="soundEnabled ? 'mdi-volume-high' : 'mdi-volume-off'"
              variant="tonal"
              :color="soundEnabled ? 'indigo-darken-3' : 'grey'"
              @click="toggleSound"
              :title="soundEnabled ? 'Sound ON — Click to mute' : 'Sound OFF — Click to enable'"
              height="44"
              width="44"
              class="bg-white elevation-1"
            ></v-btn>

            <!-- Fullscreen Toggle -->
            <v-btn
              :icon="isFullscreen ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'"
              variant="tonal"
              color="indigo-darken-3"
              @click="toggleFullScreen"
              title="Toggle Fullscreen"
              height="44"
              width="44"
              class="bg-white elevation-1"
            ></v-btn>

            <v-select
              v-model="selectedLesson"
              :items="lessons"
              item-title="title"
              return-object
              label="Select Lesson"
              variant="solo"
              bg-color="white"
              base-color="#475569"
              color="indigo-darken-3"
              hide-details
              style="min-width: 220px;"
              density="comfortable"
              class="elevation-1 rounded-lg"
              @update:modelValue="resetTest"
            ></v-select>
        </div>

        <!-- Competitor Name Dialog -->
        <v-dialog v-model="nameDialog" max-width="450">
          <v-card class="bg-white text-slate-800 pa-2 rounded-2xl elevation-10">
            <v-card-title class="text-h5 font-weight-bold pa-4 border-b d-flex align-center text-indigo-darken-3">
              <v-icon color="indigo-accent-3" class="mr-2">mdi-account-edit</v-icon>
              Competitor Registration
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p class="text-body-2 text-grey-darken-1 mb-4">
                Enter your name or nickname to register your scores on the public Leaderboard (ແຂງຂັນກັນ).
              </p>
              <v-text-field
                v-model="tempCompetitorName"
                label="Your Name / Nickname"
                placeholder="e.g. JohnSpeed"
                variant="outlined"
                color="indigo-darken-2"
                base-color="grey-darken-1"
                autofocus
                @keydown.enter="saveCompetitorName"
              ></v-text-field>
            </v-card-text>
            <v-card-actions class="pa-4 pt-0">
              <v-spacer></v-spacer>
              <v-btn color="grey-darken-1" variant="text" @click="nameDialog = false">Cancel</v-btn>
              <v-btn 
                color="indigo-darken-2" 
                variant="flat" 
                @click="saveCompetitorName"
                :disabled="!tempCompetitorName.trim()"
                class="text-white font-weight-bold"
              >Save Name</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Completion Modal -->
        <v-dialog v-model="isFinished" max-width="500" persistent>
          <v-card class="bg-white text-slate-800 pa-6 rounded-2xl text-center elevation-12">
            <div class="text-h2 my-2">🎉</div>
            <v-card-title class="text-h4 font-weight-black text-indigo-darken-3 justify-center">
              Challenge Completed!
            </v-card-title>
            <div class="text-subtitle-1 text-grey-darken-1 mb-6">
              Great job, <strong class="text-indigo-darken-4">{{ competitorName }}</strong>!
            </div>

            <v-row class="mb-6 justify-center" dense>
              <v-col cols="4">
                <div class="stat-badge-modal pa-3 rounded-xl">
                  <div class="text-caption text-grey-darken-1 font-weight-bold">Speed</div>
                  <div class="text-h5 font-weight-black text-indigo-darken-3">{{ wpm }} <span class="text-caption">WPM</span></div>
                </div>
              </v-col>
              <v-col cols="4">
                <div class="stat-badge-modal pa-3 rounded-xl">
                  <div class="text-caption text-grey-darken-1 font-weight-bold">Accuracy</div>
                  <div class="text-h5 font-weight-black text-green-darken-2">{{ Math.round(accuracy) }}%</div>
                </div>
              </v-col>
              <v-col cols="4">
                <div class="stat-badge-modal pa-3 rounded-xl">
                  <div class="text-caption text-grey-darken-1 font-weight-bold">Time</div>
                  <div class="text-h5 font-weight-black text-amber-darken-3">{{ formattedTime }}</div>
                </div>
              </v-col>
            </v-row>

            <v-card-actions class="d-flex flex-column gap-3 pa-0">
              <v-btn
                v-if="!hasSubmitted"
                color="indigo-darken-2"
                variant="flat"
                block
                size="large"
                prepend-icon="mdi-trophy-award"
                @click="submitResult"
                :loading="submitting"
                class="font-weight-bold text-white"
              >
                Submit Score to Leaderboard
              </v-btn>

              <v-btn
                v-else
                color="green-darken-2"
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
                  color="indigo-darken-2"
                  variant="outlined"
                  class="flex-grow-1 font-weight-bold"
                  prepend-icon="mdi-trophy"
                  to="/typing/leaderboard"
                >
                  Leaderboard
                </v-btn>
                <v-btn
                  color="red-darken-1"
                  variant="tonal"
                  class="flex-grow-1 font-weight-bold"
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
            <v-progress-circular indeterminate color="indigo-accent-3" size="64"></v-progress-circular>
          </v-col>
        </v-row>

        <div v-else>
          <!-- Typing Box (Light Glassmorphism) -->
          <div class="typing-master-box pa-5 pa-md-6 rounded-2xl elevation-3 mb-3" 
               :class="{ 'error-flash': showErrorFlash }"
               @click="focusInput">
            
            <!-- Live Status Indicator Bar (Time, Speed, Accuracy, Progress) -->
            <div class="d-flex flex-wrap align-center justify-space-between mb-3 gap-2">
              <div class="d-flex align-center gap-2">
                <!-- Live Timer Pill -->
                <div class="live-pill timer-pill">
                  <v-icon size="16" color="amber-darken-3" class="mr-1">mdi-timer-outline</v-icon>
                  <span class="font-weight-bold">{{ formattedTime }}</span>
                </div>

                <!-- Live Speed Pill -->
                <div class="live-pill speed-pill">
                  <v-icon size="16" color="indigo-darken-2" class="mr-1">mdi-lightning-bolt</v-icon>
                  <span class="font-weight-bold">{{ wpm }} WPM</span>
                </div>

                <!-- Live Accuracy Pill -->
                <div class="live-pill accuracy-pill">
                  <v-icon size="16" color="green-darken-2" class="mr-1">mdi-target</v-icon>
                  <span class="font-weight-bold">{{ Math.round(accuracy) }}%</span>
                </div>
              </div>

              <!-- Progress Percentage -->
              <div class="text-subtitle-2 text-indigo-darken-3 font-weight-black">
                {{ progressPercentage }}%
              </div>
            </div>

            <!-- Progress Bar -->
            <v-progress-linear 
              :model-value="progressPercentage" 
              color="indigo-accent-3" 
              height="6" 
              class="mb-5 rounded-pill"
              bg-color="#e2e8f0"
            ></v-progress-linear>

            <!-- Text Display (Word-Level Wrapping) -->
            <div class="typing-text-display font-monospace text-h5">
              <span 
                v-for="(word, wIdx) in targetWords" 
                :key="wIdx" 
                class="word-wrap"
              >
                <span 
                  v-for="item in word" 
                  :key="item.globalIndex" 
                  :class="getCharClass(item.globalIndex)"
                >{{ item.char }}</span>
              </span>
            </div>

            <div v-if="!isTyping && !isFinished && targetTextArray.length > 0" class="text-center mt-4 text-body-2 text-indigo-darken-2 font-weight-medium">
              Click here and start typing to begin...
            </div>
          </div>

          <div class="d-flex justify-center mb-3" v-if="isFinished || isTyping || targetTextArray.length > 0">
            <v-btn
              color="red-lighten-1"
              variant="tonal"
              prepend-icon="mdi-refresh"
              @click="resetTest"
              class="font-weight-bold"
            >Restart Lesson</v-btn>
          </div>

          <!-- Graphical Keyboard (Always 100% Clear & Sharp) -->
          <div>
            <VirtualKeyboard 
              :target-char="targetChar" 
              :error-map="errorMap"
              :show-heatmap="isFinished"
              :show-hands="false"
            />
          </div>

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
definePageMeta({
  layout: 'typing'
});

import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';

const loading = ref(true);
const isFullscreen = ref(false);
const isFullscreenMode = useState('isFullscreenMode', () => false);
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

// ── Sound Engine (HTML5 Audio with generated WAV) ──
const soundEnabled = ref(true);
let clickSoundUrl = null;
let errorSoundUrl = null;
let chimeSoundUrl = null;
const clickPool = [];
const POOL_SIZE = 8;

// Helper: write string into DataView
const wavWriteStr = (view, offset, str) => {
  for (let i = 0; i < str.length; i++) {
    view.setUint8(offset + i, str.charCodeAt(i));
  }
};

// Generate a WAV blob URL from Int16 sample data
const createWavUrl = (samples, sampleRate = 44100) => {
  const numSamples = samples.length;
  const buffer = new ArrayBuffer(44 + numSamples * 2);
  const view = new DataView(buffer);
  wavWriteStr(view, 0, 'RIFF');
  view.setUint32(4, 36 + numSamples * 2, true);
  wavWriteStr(view, 8, 'WAVE');
  wavWriteStr(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  wavWriteStr(view, 36, 'data');
  view.setUint32(40, numSamples * 2, true);
  for (let i = 0; i < numSamples; i++) {
    view.setInt16(44 + i * 2, samples[i], true);
  }
  const blob = new Blob([buffer], { type: 'audio/wav' });
  return URL.createObjectURL(blob);
};

const generateClickSound = () => {
  const rate = 44100;
  const len = Math.floor(rate * 0.06);
  const samples = new Int16Array(len);
  for (let i = 0; i < len; i++) {
    const t = i / rate;
    const envelope = Math.exp(-t * 60);
    const click = Math.sin(2 * Math.PI * 800 * t) * 0.6;
    const noise = (Math.random() * 2 - 1) * 0.4;
    samples[i] = Math.floor((click + noise) * envelope * 20000);
  }
  return createWavUrl(samples, rate);
};

const generateErrorSound = () => {
  const rate = 44100;
  const len = Math.floor(rate * 0.15);
  const samples = new Int16Array(len);
  for (let i = 0; i < len; i++) {
    const t = i / rate;
    const envelope = Math.exp(-t * 20);
    const freq = 200 - t * 400;
    const wave = Math.sin(2 * Math.PI * freq * t) > 0 ? 1 : -1;
    samples[i] = Math.floor(wave * envelope * 12000);
  }
  return createWavUrl(samples, rate);
};

const generateChimeSound = () => {
  const rate = 44100;
  const len = Math.floor(rate * 0.8);
  const samples = new Int16Array(len);
  const freqs = [523.25, 659.25, 783.99];
  for (let i = 0; i < len; i++) {
    const t = i / rate;
    let val = 0;
    freqs.forEach((f, idx) => {
      const onset = idx * 0.15;
      if (t >= onset) {
        const localT = t - onset;
        const env = Math.exp(-localT * 4) * Math.min(localT * 40, 1);
        val += Math.sin(2 * Math.PI * f * localT) * env;
      }
    });
    samples[i] = Math.floor(val * 10000);
  }
  return createWavUrl(samples, rate);
};

const initSounds = () => {
  if (typeof window === 'undefined') return;
  clickSoundUrl = generateClickSound();
  errorSoundUrl = generateErrorSound();
  chimeSoundUrl = generateChimeSound();
  // Pre-fill click pool for rapid typing
  for (let i = 0; i < POOL_SIZE; i++) {
    const audio = new Audio(clickSoundUrl);
    audio.volume = 0.5;
    clickPool.push(audio);
  }
};

let clickPoolIndex = 0;
const playKeyClick = () => {
  if (!soundEnabled.value || clickPool.length === 0) return;
  const audio = clickPool[clickPoolIndex % POOL_SIZE];
  audio.currentTime = 0;
  audio.play().catch(() => {});
  clickPoolIndex++;
};

const playErrorSound = () => {
  if (!soundEnabled.value || !errorSoundUrl) return;
  const audio = new Audio(errorSoundUrl);
  audio.volume = 0.5;
  audio.play().catch(() => {});
};

const playCompletionChime = () => {
  if (!soundEnabled.value || !chimeSoundUrl) return;
  const audio = new Audio(chimeSoundUrl);
  audio.volume = 0.6;
  audio.play().catch(() => {});
};

const toggleSound = () => {
  soundEnabled.value = !soundEnabled.value;
  if (typeof window !== 'undefined') {
    localStorage.setItem('typing_sound_enabled', soundEnabled.value ? '1' : '0');
  }
  if (soundEnabled.value) playKeyClick();
};

const targetTextArray = computed(() => {
  if (!selectedLesson.value || !selectedLesson.value.content) return [];
  return selectedLesson.value.content.split('');
});

const targetWords = computed(() => {
  if (!selectedLesson.value || !selectedLesson.value.content) return [];
  const text = selectedLesson.value.content;
  const words = [];
  let currentWord = [];
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    currentWord.push({ char, globalIndex: i });
    if (char === ' ' || char === '\n') {
      words.push(currentWord);
      currentWord = [];
    }
  }
  if (currentWord.length > 0) {
    words.push(currentWord);
  }
  return words;
});

const targetChar = computed(() => {
  if (userInput.value.length < targetTextArray.value.length) {
    return targetTextArray.value[userInput.value.length];
  }
  return '';
});

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

const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement;
  isFullscreenMode.value = !!document.fullscreenElement;
};

const toggleFullScreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch((err) => {
      console.error(`Error attempting to enable fullscreen: ${err.message}`);
    });
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }
};

onMounted(async () => {
  if (typeof window !== 'undefined') {
    const savedName = localStorage.getItem('typing_competitor_name');
    if (savedName) {
      competitorName.value = savedName;
    }
    const savedSound = localStorage.getItem('typing_sound_enabled');
    if (savedSound !== null) {
      soundEnabled.value = savedSound === '1';
    }
    tempCompetitorName.value = competitorName.value;
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    // Initialize sound WAV files
    initSounds();
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
  if (typeof window !== 'undefined') {
    document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }
  isFullscreenMode.value = false;
});

const focusInput = () => {
  if (hiddenInput.value && !isFinished.value) {
    hiddenInput.value.focus();
  }
  // Pre-warm audio context on user click gesture (required by browsers)
  getAudioCtx();
};

const getCharClass = (index) => {
  if (index === userInput.value.length && !isFinished.value) {
    return 'char-active';
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
    userInput.value = newValidInput;
    if (hiddenInput.value) {
      hiddenInput.value.value = newValidInput;
    }
    showErrorFlash.value = true;
    setTimeout(() => { showErrorFlash.value = false; }, 150);
    playErrorSound();
  } else {
    userInput.value = newValidInput;
    playKeyClick();
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
  playCompletionChime();
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

.typing-master-container {
  min-height: 100%;
}

.live-pill {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.85rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.timer-pill {
  background: rgba(254, 243, 199, 0.8);
  color: #92400e;
  border: 1px solid #fde68a;
}

.speed-pill {
  background: rgba(224, 231, 255, 0.8);
  color: #3730a3;
  border: 1px solid #c7d2fe;
}

.accuracy-pill {
  background: rgba(209, 250, 229, 0.8);
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.stat-badge-modal {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border: 1px solid #e2e8f0;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.typing-master-box {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1.5px solid rgba(255, 255, 255, 0.9);
  border-radius: 24px;
  cursor: text;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 20px 45px -15px rgba(99, 102, 241, 0.08), 0 0 1px 1px rgba(255, 255, 255, 0.9) inset;
}

.typing-master-box:hover {
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.12);
}

.error-flash {
  background-color: rgba(254, 226, 226, 0.7) !important;
  border-color: rgba(239, 68, 68, 0.5) !important;
}

.typing-text-display {
  user-select: none;
  position: relative;
  display: flex;
  flex-wrap: wrap;
  line-height: 1.8;
}

.word-wrap {
  display: inline-flex;
  white-space: pre;
}

.font-monospace {
  font-family: 'JetBrains Mono', monospace;
  line-height: 1.6;
  letter-spacing: 0.5px;
  font-size: clamp(1.2rem, 1.8vw, 1.45rem);
}

.char-upcoming {
  color: #64748b;
  font-weight: 400;
}

.char-correct {
  color: #0f172a;
  font-weight: 700;
}

.char-incorrect {
  color: #dc2626;
  border-bottom: 2px solid #dc2626;
  background: rgba(254, 202, 202, 0.85);
  border-radius: 3px;
  font-weight: 700;
}

.char-active {
  color: #64748b;
  position: relative;
}

.char-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 10%;
  bottom: 10%;
  width: 2.5px;
  background-color: #6366f1;
  animation: blink 1s infinite;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.8);
  border-radius: 2px;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.hidden-input {
  position: absolute;
  opacity: 0;
  height: 0;
  width: 0;
  pointer-events: none;
}
</style>
