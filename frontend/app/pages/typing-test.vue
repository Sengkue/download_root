<template>
  <v-container fluid class="typing-master-container pa-0 fill-height align-start">
    <v-row class="ma-0 w-100 justify-center pt-8">
      <v-col cols="12" md="10" lg="8">
        
        <!-- Header & Lesson Selection -->
        <div class="d-flex align-center justify-space-between mb-8">
          <div>
            <h1 class="text-h4 font-weight-bold text-white mb-2">Touch Typing Simulator</h1>
            <p class="text-subtitle-1 text-grey-lighten-1">Feel the difference and improve your Lao typing skills.</p>
          </div>
          <div class="d-flex align-center">
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
              style="min-width: 250px;"
              class="mr-4"
              density="comfortable"
              @update:modelValue="resetTest"
            ></v-select>
            
            <v-btn
              color="blue-lighten-1"
              variant="flat"
              prepend-icon="mdi-plus"
              @click="addLessonDialog = true"
              height="48"
            >Custom</v-btn>
          </div>
        </div>

        <!-- Add Custom Lesson Dialog -->
        <v-dialog v-model="addLessonDialog" max-width="500">
          <v-card class="bg-blue-grey-darken-4 text-white">
            <v-card-title class="text-h5 font-weight-bold pa-4 border-b border-white-10">
              Create Custom Lesson
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <v-text-field
                v-model="newLessonTitle"
                label="Lesson Title"
                placeholder="e.g. My Custom Drill"
                variant="outlined"
                color="blue-lighten-2"
                base-color="blue-grey-lighten-2"
                class="mb-2"
              ></v-text-field>
              
              <v-textarea
                v-model="newLessonContent"
                label="Lesson Content (Lao Text)"
                placeholder="Type the Lao characters to practice..."
                variant="outlined"
                color="blue-lighten-2"
                base-color="blue-grey-lighten-2"
                rows="4"
                auto-grow
                hint="Spaces will be preserved as typing pauses."
                persistent-hint
              ></v-textarea>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn color="grey-lighten-1" variant="text" @click="addLessonDialog = false">Cancel</v-btn>
              <v-btn 
                color="blue-lighten-1" 
                variant="flat" 
                @click="saveCustomLesson"
                :loading="savingLesson"
                :disabled="!newLessonTitle || !newLessonContent"
              >Save & Start</v-btn>
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
            <v-col cols="4">
              <div class="stat-badge">
                <div class="text-caption text-grey-lighten-1 text-uppercase font-weight-bold">Speed</div>
                <div class="text-h4 font-weight-black text-blue-lighten-2">{{ Math.round(cpm) }} <span class="text-body-2">CPM</span></div>
              </div>
            </v-col>
            <v-col cols="4">
              <div class="stat-badge">
                <div class="text-caption text-grey-lighten-1 text-uppercase font-weight-bold">Accuracy</div>
                <div class="text-h4 font-weight-black text-green-accent-3">{{ Math.round(accuracy) }}%</div>
              </div>
            </v-col>
            <v-col cols="4">
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
const timeElapsed = ref(0);
let timerInterval = null;

const submitting = ref(false);
const snackbar = ref(false);

const addLessonDialog = ref(false);
const newLessonTitle = ref('');
const newLessonContent = ref('');
const savingLesson = ref(false);

const errorMap = ref({});
const showErrorFlash = ref(false);

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

const cpm = computed(() => {
  if (timeElapsed.value === 0 || userInput.value.length === 0) return 0;
  const minutes = timeElapsed.value / 60;
  return Math.round(userInput.value.length / minutes);
});

const wpm = computed(() => {
  return Math.round(cpm.value / 5);
});

const accuracy = computed(() => {
  if (userInput.value.length === 0) return 100;
  // In strict mode, they can't type incorrect characters, so standard accuracy is technically always 100%.
  // Instead, we calculate accuracy based on the number of errors made vs total keystrokes.
  const totalErrors = Object.values(errorMap.value).reduce((a, b) => a + b, 0);
  const totalKeystrokes = userInput.value.length + totalErrors;
  if (totalKeystrokes === 0) return 100;
  return Math.max(0, Math.round(((totalKeystrokes - totalErrors) / totalKeystrokes) * 100));
});

const formattedTime = computed(() => {
  const mins = Math.floor(timeElapsed.value / 60);
  const secs = timeElapsed.value % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
});

const progressPercentage = computed(() => {
  if (targetTextArray.value.length === 0) return 0;
  return Math.min(100, Math.round((userInput.value.length / targetTextArray.value.length) * 100));
});

onMounted(async () => {
  await fetchLessons();
});

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

const saveCustomLesson = async () => {
  if (!newLessonTitle.value || !newLessonContent.value) return;
  
  savingLesson.value = true;
  try {
    const res = await fetch('http://localhost:3001/api/typing-lessons', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: newLessonTitle.value,
        content: newLessonContent.value
      })
    });
    
    if (res.ok) {
      const newLesson = await res.json();
      await fetchLessons(); // Refresh list
      
      // Select the new lesson
      const found = lessons.value.find(l => l.id === newLesson.id);
      if (found) {
        selectedLesson.value = found;
        resetTest();
      }
      
      // Close and clear
      addLessonDialog.value = false;
      newLessonTitle.value = '';
      newLessonContent.value = '';
    }
  } catch (err) {
    console.error('Error saving custom lesson', err);
  } finally {
    savingLesson.value = false;
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
      timeElapsed.value = Math.floor((Date.now() - startTime.value) / 1000);
    }, 1000);
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
  isTyping.value = false;
  isFinished.value = true;
};

const resetTest = () => {
  if (timerInterval) clearInterval(timerInterval);
  userInput.value = '';
  isTyping.value = false;
  isFinished.value = false;
  hasSubmitted.value = false;
  timeElapsed.value = 0;
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
        lessonTitle: selectedLesson.value.title,
        cpm: cpm.value,
        wpm: wpm.value,
        accuracy: accuracy.value
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
  font-family: 'Noto Sans Lao', 'Courier New', Courier, monospace;
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
