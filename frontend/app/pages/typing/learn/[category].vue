<template>
  <v-container fluid class="pa-4 pa-md-8 text-slate-800">
    <v-row class="ma-0 justify-center">
      <v-col cols="12" lg="10" xl="8">
        
        <!-- Header & Category Badge -->
        <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between mb-6 gap-4">
          <div>
            <div class="d-flex align-center gap-2 mb-1">
              <v-chip color="teal-darken-2" variant="tonal" size="small" class="font-weight-bold">
                LESSON MODULE
              </v-chip>
              <h1 class="text-h4 font-weight-black text-indigo-darken-4">{{ currentLesson.title }}</h1>
            </div>
            <p class="text-subtitle-1 text-grey-darken-1">{{ currentLesson.description }}</p>
          </div>

          <div class="d-flex flex-wrap align-center gap-2">
            <v-btn
              v-for="(cat, key) in categories"
              :key="key"
              :to="`/typing/learn/${key}`"
              :color="currentKey === key ? 'indigo-darken-2' : 'grey-darken-1'"
              :variant="currentKey === key ? 'flat' : 'tonal'"
              size="small"
              class="font-weight-bold rounded-pill"
              :class="{'text-white': currentKey === key}"
            >
              {{ cat.shortTitle }}
            </v-btn>
          </div>
        </div>

        <!-- Touch Typing Tips Banner -->
        <v-card class="learning-tip-card pa-4 mb-6 rounded-2xl elevation-2 bg-white">
          <div class="d-flex align-center gap-3">
            <v-icon color="amber-darken-2" size="32">mdi-lightbulb-on-outline</v-icon>
            <div>
              <div class="font-weight-bold text-amber-darken-3">Touch Typing Pro Tip</div>
              <div class="text-body-2 text-slate-600">{{ currentLesson.tip }}</div>
            </div>
          </div>
        </v-card>

        <!-- Stats Row -->
        <v-row class="mb-6">
          <v-col cols="6" sm="4">
            <div class="stat-badge">
              <div class="text-caption text-slate-500 text-uppercase font-weight-bold">Progress</div>
              <div class="text-h4 font-weight-black text-indigo-darken-3">{{ progressPercentage }}%</div>
            </div>
          </v-col>
          <v-col cols="6" sm="4">
            <div class="stat-badge">
              <div class="text-caption text-slate-500 text-uppercase font-weight-bold">Accuracy</div>
              <div class="text-h4 font-weight-black text-green-darken-2">{{ Math.round(accuracy) }}%</div>
            </div>
          </v-col>
          <v-col cols="12" sm="4">
            <div class="stat-badge">
              <div class="text-caption text-slate-500 text-uppercase font-weight-bold">Speed (WPM)</div>
              <div class="text-h4 font-weight-black text-amber-darken-3">{{ wpm }} <span class="text-body-2">WPM</span></div>
            </div>
          </v-col>
        </v-row>

        <!-- Interactive Typing Box (Light Glassmorphism) -->
        <div 
          class="typing-learn-box pa-6 pa-md-8 rounded-2xl elevation-3 mb-6 bg-white"
          :class="{ 'error-flash': showErrorFlash }"
          @click="focusInput"
        >
          <div class="d-flex justify-space-between align-center mb-3">
            <div class="text-subtitle-2 text-slate-500 font-weight-bold">Drill Exercise:</div>
            <div class="text-caption text-indigo-darken-3 font-weight-black">
              {{ userInput.length }} / {{ targetTextArray.length }} Characters
            </div>
          </div>

          <v-progress-linear 
            :model-value="progressPercentage" 
            color="indigo-accent-3" 
            height="6" 
            class="mb-6 rounded-pill"
            bg-color="#e2e8f0"
          ></v-progress-linear>

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

          <div v-if="!isTyping && !isFinished" class="text-center mt-6 text-body-2 text-indigo-darken-2 font-weight-medium">
            Click here and start typing this drill...
          </div>

          <div v-if="isFinished" class="text-center mt-6">
            <div class="text-h5 font-weight-bold text-green-darken-2 mb-2">🎉 Drill Completed!</div>
            <v-btn color="indigo-darken-2" class="text-white font-weight-bold rounded-pill" prepend-icon="mdi-refresh" @click="resetDrill">
              Repeat Drill
            </v-btn>
          </div>
        </div>

        <!-- Virtual Keyboard & Finger Guide -->
        <VirtualKeyboard 
          :target-char="targetChar" 
          :error-map="errorMap"
          :show-heatmap="isFinished"
        />

        <!-- Hidden input for keyboard capture -->
        <input 
          ref="hiddenInput"
          :value="userInput"
          @input="handleInputNative"
          class="hidden-input"
          type="text"
          :disabled="isFinished"
          autocomplete="off"
        />

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
definePageMeta({
  layout: 'typing'
});

import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const categories = {
  'basics': {
    title: 'Touch Typing Rules & Finger Basics',
    shortTitle: 'Rules & Basics',
    description: 'Learn to anchor your index fingers on F and J bumps and use all 10 fingers without looking down.',
    tip: 'Place your left fingers on A S D F and right fingers on J K L ;. Always return to this Home Row position after pressing any key.',
    drills: 'fff jjj fff jjj fj fj jf jf asdf jkl; asdf jkl; fa da sa ja ka la fjdksla;'
  },
  'home-row': {
    title: 'Home Row Training (ASDF JKL;)',
    shortTitle: 'Home Row',
    description: 'Master the foundation of touch typing: A, S, D, F, G, H, J, K, L, and ;',
    tip: 'Keep your wrists flat and elbows at 90 degrees. Strike keys gently like a piano.',
    drills: 'aaa sss ddd fff ggg hhh jjj kkk lll dad sad fad lad glad ask flash fall half flask salads'
  },
  'top-row': {
    title: 'Top Row Practice (QWERTY UIOP)',
    shortTitle: 'Top Row',
    description: 'Practice reaching up from the home row to hit the top QWERTY keys.',
    tip: 'Reach your fingers upward without lifting your whole hand off the home row baseline.',
    drills: 'qqq www eee rrr ttt yyy uuu iii ooo ppp quiet water tree year you out put write quote power route'
  },
  'bottom-row': {
    title: 'Bottom Row Practice (ZXCVB NM)',
    shortTitle: 'Bottom Row',
    description: 'Master extending fingers downward to accurately hit Z, X, C, V, B, N, M.',
    tip: 'Curl your fingers downward naturally while keeping your palms elevated.',
    drills: 'zzz xxx ccc vvv bbb nnn mmm zero zoo van can man ban cab box mob calm climb maximum vitamin'
  },
  'numbers-symbols': {
    title: 'Numbers & Symbols Drills',
    shortTitle: 'Numbers & Symbols',
    description: 'Build confidence reaching the top number row (1-0) and shift symbols.',
    tip: 'Use your pinkies for the Shift keys while pressing number keys with the corresponding finger.',
    drills: '123 456 789 0 100 200 #45 $99 user@mail.com (1 + 2 = 3) [test] {code} 100% win! count=10;'
  }
};

const currentKey = computed(() => {
  const cat = route.params.category || 'basics';
  return categories[cat] ? cat : 'basics';
});

const currentLesson = computed(() => {
  return categories[currentKey.value] || categories['basics'];
});

const userInput = ref('');
const hiddenInput = ref(null);
const isTyping = ref(false);
const isFinished = ref(false);
const startTime = ref(null);
const timeElapsedMs = ref(0);
let timerInterval = null;
const errorMap = ref({});
const showErrorFlash = ref(false);

const targetTextArray = computed(() => {
  return currentLesson.value.drills.split('');
});

const targetWords = computed(() => {
  const text = currentLesson.value.drills;
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

const progressPercentage = computed(() => {
  if (targetTextArray.value.length === 0) return 0;
  return Math.min(100, Math.round((userInput.value.length / targetTextArray.value.length) * 100));
});

const accuracy = computed(() => {
  if (userInput.value.length === 0) return 100;
  const totalErrors = Object.values(errorMap.value).reduce((a, b) => a + b, 0);
  const totalKeystrokes = userInput.value.length + totalErrors;
  if (totalKeystrokes === 0) return 100;
  return Math.max(0, Math.round(((totalKeystrokes - totalErrors) / totalKeystrokes) * 100));
});

const wpm = computed(() => {
  if (timeElapsedMs.value === 0 || userInput.value.length === 0) return 0;
  const minutes = timeElapsedMs.value / 60000;
  const wordsTyped = userInput.value.length / 5;
  return Math.round(wordsTyped / minutes);
});

const focusInput = () => {
  if (hiddenInput.value && !isFinished.value) {
    hiddenInput.value.focus();
  }
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
  } else {
    userInput.value = newValidInput;
  }

  if (userInput.value.length >= targetTextArray.value.length) {
    if (timerInterval) clearInterval(timerInterval);
    isTyping.value = false;
    isFinished.value = true;
  }
};

const resetDrill = () => {
  if (timerInterval) clearInterval(timerInterval);
  userInput.value = '';
  isTyping.value = false;
  isFinished.value = false;
  timeElapsedMs.value = 0;
  startTime.value = null;
  errorMap.value = {};
  nextTick(() => {
    focusInput();
  });
};

watch(() => route.params.category, () => {
  resetDrill();
});

onMounted(() => {
  nextTick(() => {
    focusInput();
  });
});

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

.learning-tip-card {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(16px);
  border: 1.5px solid rgba(251, 191, 36, 0.3) !important;
}

.stat-badge {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 16px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.04);
}

.typing-learn-box {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(20px);
  border: 1.5px solid rgba(255, 255, 255, 0.9) !important;
  cursor: text;
  transition: all 0.3s ease;
  box-shadow: 0 20px 45px -15px rgba(99, 102, 241, 0.08), 0 0 1px 1px rgba(255, 255, 255, 0.9) inset;
}

.typing-learn-box:hover {
  border-color: rgba(99, 102, 241, 0.4) !important;
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
  line-height: 1.8;
  letter-spacing: 0.5px;
  font-size: 1.5rem;
}

.char-upcoming {
  color: #94a3b8;
  transition: color 0.1s ease;
}

.char-correct {
  color: #0f172a;
  font-weight: 500;
}

.char-incorrect {
  color: #ef4444;
  border-bottom: 2px solid #ef4444;
  background: rgba(254, 226, 226, 0.8);
  border-radius: 3px;
}

.char-active {
  color: #94a3b8;
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
