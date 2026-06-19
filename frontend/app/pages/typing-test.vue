<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" md="8" lg="8">
        <v-card class="elevation-12 rounded-xl" theme="dark">
          <v-card-item class="bg-primary text-center py-6">
            <v-card-title class="text-h4 font-weight-bold">
              <v-icon icon="mdi-music-note" size="large" class="mr-2"></v-icon>
              Lyric Typing Test
            </v-card-title>
            <v-card-subtitle class="text-h6 mt-2 opacity-80">
              Type the song to test your speed!
            </v-card-subtitle>
          </v-card-item>

          <v-card-text class="pa-6">
            <!-- Results Section -->
            <v-slide-y-transition>
              <div v-if="isFinished" class="text-center mb-6">
                <v-row>
                  <v-col cols="6">
                    <v-card color="surface-variant" variant="flat" class="pa-4 rounded-lg">
                      <div class="text-overline mb-1">Speed</div>
                      <div class="text-h3 font-weight-black text-primary">{{ wpm }} <span class="text-h6">WPM</span></div>
                    </v-card>
                  </v-col>
                  <v-col cols="6">
                    <v-card color="surface-variant" variant="flat" class="pa-4 rounded-lg">
                      <div class="text-overline mb-1">Accuracy</div>
                      <div class="text-h3 font-weight-black text-success">{{ accuracy }}<span class="text-h6">%</span></div>
                    </v-card>
                  </v-col>
                </v-row>
                <v-btn color="primary" size="large" class="mt-6" @click="resetTest" prepend-icon="mdi-refresh" rounded="pill">
                  Try Again
                </v-btn>
              </div>
            </v-slide-y-transition>

            <!-- Song Selection -->
            <v-expand-transition>
              <div class="mb-6" v-if="!isStarted && !isFinished">
                <v-select
                  v-model="selectedSong"
                  :items="songLibrary"
                  item-title="title"
                  item-value="id"
                  label="Select a Song to Type"
                  variant="outlined"
                  color="primary"
                  hide-details
                  @update:model-value="changeSong"
                  prepend-inner-icon="mdi-playlist-music"
                >
                  <template v-slot:selection="{ item }">
                    <div class="d-flex flex-column">
                      <span class="font-weight-bold">{{ item.raw.title }}</span>
                      <span class="text-caption text-medium-emphasis">{{ item.raw.artist }}</span>
                    </div>
                  </template>
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="item.raw.title" :subtitle="item.raw.artist"></v-list-item>
                  </template>
                </v-select>
              </div>
            </v-expand-transition>

            <div class="mb-4 d-flex align-center justify-space-between" v-if="isStarted || isFinished">
               <div>
                 <div class="text-h6">Now Playing: <strong>{{ currentSongDetails?.title }}</strong></div>
                 <div class="text-subtitle-2 text-medium-emphasis">{{ currentSongDetails?.artist }}</div>
               </div>
            </div>

            <!-- Typing Area -->
            <div class="typing-container rounded-lg pa-6 mb-6" :class="{ 'is-focused': isFocused, 'blur': isFinished }">
              <div class="words-display text-h5" @click="focusInput">
                <span 
                  v-for="(word, index) in words" 
                  :key="index"
                  class="word"
                  :class="{
                    'current-word': index === currentWordIndex,
                    'correct': word.status === 'correct',
                    'incorrect': word.status === 'incorrect',
                    'text-medium-emphasis': word.status === 'untyped' && index !== currentWordIndex
                  }"
                >
                  <span 
                    v-for="(char, charIndex) in word.originalText.split('')" 
                    :key="charIndex"
                    class="char"
                    :class="getCharClass(index, charIndex)"
                  >{{ char }}</span><span class="space">&nbsp;</span>
                </span>
              </div>
            </div>

            <!-- Hidden Input -->
            <input 
              ref="typeInput"
              v-model="currentInput"
              @keydown="handleKeydown"
              @focus="isFocused = true"
              @blur="isFocused = false"
              class="hidden-input"
              type="text"
              autocomplete="off"
              :disabled="isFinished"
              autofocus
            />
            
            <div class="text-center text-medium-emphasis text-caption mt-2" v-if="!isStarted && !isFinished">
              Start typing to begin the test...
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const songLibrary = [
  {
    id: 1,
    title: "Never Gonna Give You Up",
    artist: "Rick Astley",
    lyrics: "Never gonna give you up never gonna let you down never gonna run around and desert you"
  },
  {
    id: 2,
    title: "Bohemian Rhapsody",
    artist: "Queen",
    lyrics: "Is this the real life is this just fantasy caught in a landslide no escape from reality"
  },
  {
    id: 3,
    title: "Shape of You",
    artist: "Ed Sheeran",
    lyrics: "The club isn't the best place to find a lover so the bar is where I go me and my friends at the table doing shots"
  },
  {
    id: 4,
    title: "Billie Jean",
    artist: "Michael Jackson",
    lyrics: "Billie Jean is not my lover she's just a girl who claims that I am the one but the kid is not my son"
  }
]

const selectedSong = ref(songLibrary[0].id)
const currentSongDetails = computed(() => songLibrary.find(s => s.id === selectedSong.value))

const lyricsText = computed(() => currentSongDetails.value?.lyrics || '')
const words = ref([])
const currentWordIndex = ref(0)
const currentInput = ref('')
const isFocused = ref(false)
const isStarted = ref(false)
const isFinished = ref(false)
const startTime = ref(null)
const endTime = ref(null)
const typeInput = ref(null)

const totalKeystrokes = ref(0)
const correctKeystrokes = ref(0)

// Initialize words array
const initTest = () => {
  words.value = lyricsText.value.trim().split(/\s+/).map(text => ({
    originalText: text,
    typedText: '',
    status: 'untyped' // 'untyped', 'correct', 'incorrect'
  }))
  currentWordIndex.value = 0
  currentInput.value = ''
  isStarted.value = false
  isFinished.value = false
  startTime.value = null
  endTime.value = null
  totalKeystrokes.value = 0
  correctKeystrokes.value = 0
  
  if (typeInput.value) {
    typeInput.value.focus()
  }
}

const changeSong = () => {
  initTest()
}

onMounted(() => {
  initTest()
})

const focusInput = () => {
  if (typeInput.value) {
    typeInput.value.focus()
  }
}

const wpm = computed(() => {
  if (!startTime.value) return 0
  const end = endTime.value || new Date()
  const timeInMinutes = (end - startTime.value) / 60000
  // Standard WPM calculation: (total characters / 5) / time in minutes
  const totalChars = words.value.reduce((acc, word) => {
    return acc + (word.status === 'correct' ? word.originalText.length + 1 : 0) // +1 for space
  }, 0)
  
  if (timeInMinutes === 0) return 0
  return Math.round((totalChars / 5) / timeInMinutes)
})

const accuracy = computed(() => {
  if (totalKeystrokes.value === 0) return 100
  return Math.round((correctKeystrokes.value / totalKeystrokes.value) * 100)
})

const getCharClass = (wordIndex, charIndex) => {
  if (wordIndex < currentWordIndex.value) {
    // Past words
    const word = words.value[wordIndex]
    return word.status === 'correct' ? 'text-success' : 'text-error'
  } else if (wordIndex === currentWordIndex.value) {
    // Current word
    const char = words.value[wordIndex].originalText[charIndex]
    const typedChar = currentInput.value[charIndex]
    
    if (typedChar === undefined) {
      return 'text-medium-emphasis'
    } else if (typedChar === char) {
      return 'text-white'
    } else {
      return 'text-error bg-error-lighten-4 rounded'
    }
  }
  // Future words
  return 'text-medium-emphasis'
}

const handleKeydown = (e) => {
  if (isFinished.value) return

  // Start timer on first keypress (if it's a valid character)
  if (!isStarted.value && e.key.length === 1) {
    isStarted.value = true
    startTime.value = new Date()
  }

  const currentWord = words.value[currentWordIndex.value]

  if (e.key === ' ') {
    e.preventDefault() // Prevent scrolling or double spaces
    
    // Only proceed if user has typed something
    if (currentInput.value.trim().length > 0) {
      currentWord.typedText = currentInput.value.trim()
      
      // Update keystrokes (simplified metric based on word correctness)
      totalKeystrokes.value += currentWord.originalText.length + 1
      if (currentWord.typedText === currentWord.originalText) {
        currentWord.status = 'correct'
        correctKeystrokes.value += currentWord.originalText.length + 1
      } else {
        currentWord.status = 'incorrect'
        // Add partial correct strokes based on character match could be implemented here
        let matches = 0
        for(let i=0; i<Math.min(currentWord.typedText.length, currentWord.originalText.length); i++) {
           if(currentWord.typedText[i] === currentWord.originalText[i]) matches++
        }
        correctKeystrokes.value += matches
      }

      currentInput.value = ''
      currentWordIndex.value++

      // Check if test is finished
      if (currentWordIndex.value >= words.value.length) {
        finishTest()
      }
    }
  } else if (e.key === 'Backspace') {
    // Optional: Prevent going back to previous words
    // If input is empty and not first word, don't do anything or go back
  }
}

watch(currentInput, (newVal, oldVal) => {
  if(newVal.length > oldVal.length && !isFinished.value) {
     // User typed a character, let's track keystrokes more granularly if needed
     // For now, accuracy is calculated per word upon spacebar, but we can do it per char here if desired
  }
})

const finishTest = () => {
  isFinished.value = true
  endTime.value = new Date()
  isStarted.value = false
}

const resetTest = () => {
  initTest()
}
</script>

<style scoped>
.typing-container {
  background-color: rgba(var(--v-theme-surface-variant), 0.3);
  border: 2px solid transparent;
  transition: all 0.3s ease;
  position: relative;
  min-height: 150px;
  cursor: text;
}

.typing-container.is-focused {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 15px rgba(var(--v-theme-primary), 0.2);
}

.typing-container.blur {
  filter: blur(2px);
  pointer-events: none;
}

.words-display {
  display: flex;
  flex-wrap: wrap;
  line-height: 1.8;
  font-family: 'Roboto Mono', monospace; /* Monospace is better for typing tests */
}

.word {
  margin-bottom: 8px;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.word.current-word {
  border-bottom: 2px solid rgb(var(--v-theme-primary));
}

.word.incorrect {
  text-decoration: underline wavy rgb(var(--v-theme-error));
  text-underline-offset: 4px;
}

.space {
  display: inline-block;
  width: 0.5em;
}

.hidden-input {
  position: absolute;
  opacity: 0;
  top: 0;
  left: 0;
  height: 1px;
  width: 1px;
  pointer-events: none;
}
</style>
