<template>
  <div class="pa-4 pa-md-8">
    <div class="max-w-7xl mx-auto space-y-8 pb-12">
      
      <!-- Hero Section -->
      <v-card color="primary" class="rounded-xl pa-8 position-relative overflow-hidden shadow-md" elevation="0">
        <div class="position-absolute" style="background-color: var(--v-theme-secondary-container); width: 250px; height: 250px; border-radius: 50%; filter: blur(60px); right: -40px; top: -40px; opacity: 0.15; pointer-events: none;"></div>
        
        <div class="position-relative z-10 d-flex flex-column gap-4">
          <div class="d-inline-flex align-center gap-2 px-3 py-1 rounded-pill text-caption font-weight-bold text-uppercase align-self-start" style="background-color: rgba(255,255,255,0.1) !important; color: #d6e3ff;">
            <v-icon size="small" color="white">mdi-school</v-icon> Study Begin
          </div>
          <h1 class="text-h3 font-weight-black text-white" style="letter-spacing: -0.02em;">Hmong RPA Guide</h1>
          <p class="text-h6 font-weight-regular mb-0 max-w-2xl" style="color: #d6e3ff;">
            Master the foundational building blocks of the Romanized Popular Alphabet (RPA). Click any letter to inspect Lao comparisons, pronunciation, and vocabulary examples.
          </p>
        </div>
      </v-card>

      <!-- Main Content Grid -->
      <v-row>
        <!-- Left Column: Consonants & Vowels -->
        <v-col cols="12" lg="8" class="d-flex flex-column gap-6">
          
          <!-- Consonants Card -->
          <v-card class="bg-surface-container-lowest rounded-xl shadow-sm pa-6 pa-md-8 border" elevation="0">
            <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-6">
              <div class="d-flex align-center gap-3">
                <v-avatar color="primary-fixed" size="48" class="rounded-lg">
                  <v-icon color="primary">mdi-format-letter-case</v-icon>
                </v-avatar>
                <div>
                  <h2 class="text-h5 font-weight-bold text-on-surface lh-1">Txiv Ntawv (Consonants)</h2>
                  <span class="text-caption text-on-surface-variant font-weight-medium">56 Total Consonants</span>
                </div>
              </div>
              <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" prepend-icon="mdi-cursor-default-click">
                Click any letter to study
              </v-chip>
            </div>

            <div class="space-y-6">
              <div v-for="(group, idx) in consonants" :key="idx" class="bg-surface-container-low rounded-lg pa-4">
                <div class="d-flex align-center justify-space-between mb-3">
                  <h3 class="text-body-2 font-weight-bold text-on-surface text-uppercase tracking-widest">{{ group.title }}</h3>
                  <v-chip size="x-small" color="primary" class="font-weight-bold">{{ group.items.length }}</v-chip>
                </div>
                <div class="d-flex flex-wrap gap-2">
                  <v-chip 
                    v-for="letter in group.items" 
                    :key="letter"
                    class="letter-chip font-weight-bold"
                    variant="flat"
                    @click="openLetter(letter)"
                  >
                    <span class="letter-text">{{ letter }}</span>
                  </v-chip>
                </div>
              </div>
            </div>
          </v-card>

          <!-- Vowels Card -->
          <v-card class="bg-surface-container-lowest rounded-xl shadow-sm pa-6 pa-md-8 border" elevation="0">
            <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-6">
              <div class="d-flex align-center gap-3">
                <v-avatar color="tertiary-fixed" size="48" class="rounded-lg">
                  <v-icon color="tertiary">mdi-alpha-a-circle-outline</v-icon>
                </v-avatar>
                <div>
                  <h2 class="text-h5 font-weight-bold text-on-surface lh-1">Niam Suab (Vowels)</h2>
                  <span class="text-caption text-on-surface-variant font-weight-medium">14 Total Vowels</span>
                </div>
              </div>
              <v-chip size="small" color="tertiary" variant="tonal" class="font-weight-bold" prepend-icon="mdi-cursor-default-click">
                Click vowel to inspect
              </v-chip>
            </div>

            <v-row>
              <v-col cols="12" md="6" v-for="(group, idx) in vowels" :key="idx">
                <div class="bg-surface-container-low rounded-lg pa-4 h-100">
                  <div class="d-flex align-center justify-space-between mb-3">
                    <h3 class="text-body-2 font-weight-bold text-on-surface text-uppercase tracking-widest">{{ group.title }}</h3>
                    <v-chip size="x-small" color="tertiary" class="font-weight-bold">{{ group.items.length }}</v-chip>
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <v-chip 
                      v-for="letter in group.items" 
                      :key="letter"
                      class="letter-chip font-weight-bold"
                      variant="flat"
                      @click="openLetter(letter)"
                    >
                      <span class="letter-text">{{ letter }}</span>
                    </v-chip>
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-card>

        </v-col>

        <!-- Right Column: Tones -->
        <v-col cols="12" lg="4">
          <v-card class="bg-surface-container-lowest rounded-xl shadow-sm pa-6 pa-md-8 border h-100" elevation="0">
            <div class="d-flex align-center gap-3 mb-6">
              <v-avatar color="secondary-fixed" size="48" class="rounded-lg">
                <v-icon color="secondary">mdi-music-clef-treble</v-icon>
              </v-avatar>
              <div>
                <h2 class="text-h5 font-weight-bold text-on-surface lh-1">Cim Suab</h2>
                <span class="text-caption text-on-surface-variant font-weight-medium">8 Tone Markers</span>
              </div>
            </div>

            <p class="text-body-2 text-on-surface-variant mb-6">
              Tones change the meaning of a word. In Hmong RPA, the tone is indicated by the last consonant of the word. Click any tone to explore:
            </p>

            <div class="d-flex flex-column gap-3">
              <div 
                v-for="(tone, idx) in tones" 
                :key="idx" 
                class="bg-surface-container-low rounded-lg pa-3 d-flex align-center gap-4 tone-card cursor-pointer"
                @click="openLetter(tone.id)"
              >
                <div class="tone-avatar bg-surface-container-lowest text-secondary font-weight-black d-flex align-center justify-center rounded shadow-sm text-h6">
                  {{ tone.letter }}
                </div>
                <div class="flex-grow-1">
                  <div class="text-body-2 font-weight-bold text-on-surface lh-1 mb-1">{{ tone.name }}</div>
                  <div class="text-caption text-on-surface-variant lh-1">{{ tone.desc }}</div>
                </div>
                <v-icon size="small" color="on-surface-variant">mdi-chevron-right</v-icon>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Letter Study Dialog Modal -->
      <v-dialog v-model="isDialogOpen" max-width="540" transition="dialog-bottom-transition">
        <v-card v-if="currentDetail" class="rounded-2xl overflow-hidden pa-0 border bg-surface-container-lowest" elevation="10">
          
          <!-- Dialog Top Bar -->
          <div class="px-5 pt-4 pb-2 d-flex align-center justify-space-between">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
              {{ currentDetail.category }}
            </v-chip>
            <v-btn icon="mdi-close" variant="text" size="small" density="comfortable" @click="isDialogOpen = false" />
          </div>

          <!-- Illustrated Letter Visual (e.g. Number 9 for C = ຈ / Cuaj) -->
          <div class="px-5 py-1">
            <div class="position-relative overflow-hidden rounded-xl border shadow-sm" style="background: #0b1a2d;">
              <v-img 
                :src="currentDetail.image || generateLetterSvg(currentDetail)" 
                height="230" 
                class="bg-surface-container-low"
                alt="Hmong vocabulary visual"
                cover
              >
                <template #placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  </div>
                </template>
              </v-img>

              <!-- Floating overlay badge on image -->
              <div 
                class="position-absolute d-flex align-center justify-space-between w-100 px-4 py-2" 
                style="bottom: 0; left: 0; background: linear-gradient(to top, rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.35) 70%, transparent);"
              >
                <div class="d-flex align-center gap-2">
                  <span class="text-white font-weight-black text-subtitle-1">
                    {{ currentDetail.letter.toUpperCase() }} = {{ currentDetail.lao }}
                  </span>
                  <span class="text-caption text-grey-lighten-2">({{ currentDetail.letter }})</span>
                </div>
                <div class="d-inline-flex align-center gap-2 px-3 py-1 rounded-pill text-caption font-weight-bold" style="background: rgba(255,255,255,0.22); color: #ffffff; backdrop-filter: blur(8px);">
                  <v-icon size="x-small" color="white">mdi-lightbulb-outline</v-icon>
                  {{ currentDetail.exampleHmong }} = {{ currentDetail.exampleMeaning }}
                </div>
              </div>
            </div>
          </div>

          <!-- Letter Details Body -->
          <div class="px-6 pt-3 pb-4">
            
            <!-- Large Title & Equation (C = ຈ) -->
            <div class="d-flex align-center justify-space-between mb-2">
              <div class="d-flex align-baseline gap-2">
                <span class="text-h3 font-weight-black text-on-surface">{{ currentDetail.letter.toUpperCase() }}</span>
                <span class="text-h4 font-weight-bold text-secondary">=</span>
                <span class="text-h3 font-weight-black text-primary">{{ currentDetail.lao }}</span>
                <span class="text-body-1 text-on-surface-variant font-weight-bold ml-1">({{ currentDetail.letter }})</span>
              </div>
              <v-chip v-if="currentDetail.ipa" size="small" color="primary-fixed" class="font-weight-bold text-primary">
                IPA {{ currentDetail.ipa }}
              </v-chip>
            </div>

            <!-- Phonetic / Sound Guide -->
            <div class="d-flex align-center gap-2 mb-3 px-3 py-2 rounded-lg bg-surface-container-low border">
              <v-icon size="small" color="primary">mdi-volume-high</v-icon>
              <span class="text-body-2 font-weight-bold text-on-surface">
                ສຽງ: {{ currentDetail.soundLike }}
              </span>
            </div>

            <!-- Description -->
            <p class="text-body-2 text-on-surface-variant mb-4 lh-base font-weight-regular">
              {{ currentDetail.description }}
            </p>

            <!-- Vocabulary Example Card -->
            <div class="bg-surface-container-low rounded-xl pa-3 pa-sm-4 border d-flex align-center justify-space-between">
              <div>
                <div class="text-caption font-weight-bold text-on-surface-variant text-uppercase">ຕົວຢ່າງຄຳສັບ (Example Word)</div>
                <div class="text-h6 font-weight-black text-on-surface">
                  {{ currentDetail.exampleHmong }}
                  <span class="text-secondary font-weight-bold text-body-1 ml-1">({{ currentDetail.exampleLao }})</span>
                </div>
              </div>
              <v-chip size="small" color="tertiary" variant="tonal" class="font-weight-bold">
                {{ currentDetail.exampleMeaning }}
              </v-chip>
            </div>

          </div>

          <!-- Bottom Navigation Bar (Previous / Next) -->
          <v-divider />
          <div class="px-6 py-3 bg-surface-container-low d-flex align-center justify-space-between">
            <v-btn 
              variant="outlined" 
              prepend-icon="mdi-chevron-left" 
              @click="prevLetter" 
              :disabled="currentIndex <= 0" 
              class="text-none font-weight-bold"
              size="small"
            >
              Previous
            </v-btn>

            <div class="text-caption font-weight-bold text-on-surface-variant">
              {{ currentIndex + 1 }} / {{ allLetterKeys.length }}
            </div>

            <v-btn 
              color="primary" 
              append-icon="mdi-chevron-right" 
              @click="nextLetter" 
              :disabled="currentIndex >= allLetterKeys.length - 1" 
              class="text-none font-weight-bold"
              size="small"
            >
              Next
            </v-btn>
          </div>

        </v-card>
      </v-dialog>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { hmongAlphabetData, generateLetterSvg } from '~/data/hmongAlphabet';

definePageMeta({
  layout: 'learning'
});

const consonants = [
  {
    title: '1-Letter Consonants',
    items: ['c', 'd', 'f', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z']
  },
  {
    title: '2-Letter Consonants',
    items: ['ch', 'dh', 'hl', 'hm', 'hn', 'kh', 'ml', 'nc', 'nk', 'np', 'nq', 'nr', 'nt', 'ny', 'ph', 'pl', 'qh', 'rh', 'th', 'ts', 'tx', 'xy']
  },
  {
    title: '3-Letter Consonants',
    items: ['hml', 'hny', 'nch', 'nkh', 'nph', 'npl', 'nqh', 'nrh', 'nth', 'nts', 'ntx', 'plh', 'tsh', 'txh']
  },
  {
    title: '4-Letter Consonants',
    items: ['nplh', 'ntsh', 'ntxh']
  }
];

const vowels = [
  {
    title: '1-Letter Vowels',
    items: ['a', 'e', 'i', 'o', 'u', 'w']
  },
  {
    title: '2-Letter Vowels',
    items: ['aa', 'ai', 'au', 'aw', 'ee', 'ia', 'oo', 'ua']
  }
];

const tones = [
  { id: 'tone_b', letter: 'b', name: 'High tone', desc: 'High pitch, level' },
  { id: 'tone_m', letter: 'm', name: 'Low glottalized', desc: 'Low pitch, ends abruptly' },
  { id: 'tone_d', letter: 'd', name: 'Low rising', desc: 'Starts low, rises slightly' },
  { id: 'tone_j', letter: 'j', name: 'High falling', desc: 'Starts high, falls sharply' },
  { id: 'tone_v', letter: 'v', name: 'Mid rising', desc: 'Starts mid, rises to high' },
  { id: 'tone_s', letter: 's', name: 'Low tone', desc: 'Low pitch, level' },
  { id: 'tone_g', letter: 'g', name: 'Falling breathy', desc: 'Starts mid, falls with breath' },
  { id: 'tone_blank', letter: '∅', name: 'Mid tone (Blank)', desc: 'No consonant at the end' }
];

// Dialog state
const isDialogOpen = ref(false);
const currentLetterKey = ref('c');

// All letters ordered for Next / Previous navigation
const allLetterKeys = computed(() => {
  const keys = [];
  consonants.forEach(c => keys.push(...c.items));
  vowels.forEach(v => keys.push(...v.items));
  tones.forEach(t => keys.push(t.id));
  return keys;
});

const currentIndex = computed(() => {
  return allLetterKeys.value.indexOf(currentLetterKey.value);
});

const currentDetail = computed(() => {
  const detail = hmongAlphabetData[currentLetterKey.value];
  if (detail) return detail;

  // Fallback if key missing
  return {
    letter: currentLetterKey.value,
    lao: currentLetterKey.value,
    category: 'Letter Study',
    ipa: '',
    soundLike: currentLetterKey.value,
    exampleHmong: currentLetterKey.value,
    exampleLao: currentLetterKey.value,
    exampleMeaning: 'Example',
    description: `Details for ${currentLetterKey.value}`
  };
});

function openLetter(letter) {
  currentLetterKey.value = letter;
  isDialogOpen.value = true;
}

function nextLetter() {
  if (currentIndex.value < allLetterKeys.value.length - 1) {
    currentLetterKey.value = allLetterKeys.value[currentIndex.value + 1];
  }
}

function prevLetter() {
  if (currentIndex.value > 0) {
    currentLetterKey.value = allLetterKeys.value[currentIndex.value - 1];
  }
}

// Keyboard arrow navigation
function handleKeydown(e) {
  if (!isDialogOpen.value) return;
  if (e.key === 'ArrowRight') {
    nextLetter();
  } else if (e.key === 'ArrowLeft') {
    prevLetter();
  }
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    window.addEventListener('keydown', handleKeydown);
  }
});

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('keydown', handleKeydown);
  }
});
</script>

<style scoped>
.max-w-7xl {
  max-width: 1280px;
}
.max-w-2xl {
  max-width: 672px;
}
.space-y-8 > * + * {
  margin-top: 2rem;
}
.space-y-6 > * + * {
  margin-top: 1.5rem;
}
.gap-6 {
  gap: 1.5rem;
}
.lh-1 {
  line-height: 1.2;
}
.lh-base {
  line-height: 1.5;
}
.tracking-widest {
  letter-spacing: 0.1em;
}
.cursor-pointer {
  cursor: pointer !important;
}
.letter-chip {
  background-color: #ffffff !important;
  color: #111827 !important;
  border: 1px solid rgba(0, 0, 0, 0.12) !important;
  font-size: 0.95rem !important;
  min-width: 44px;
  justify-content: center;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s, border-color 0.2s;
  cursor: pointer !important;
}
.letter-chip :deep(.v-chip__content),
.letter-text {
  color: #111827 !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em;
}
.letter-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
  border-color: rgba(0, 32, 69, 0.35) !important;
  background-color: #fdfdfd !important;
}
.tone-avatar {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border: 1px solid rgba(0, 0, 0, 0.08);
}
.tone-card {
  transition: all 0.2s ease;
}
.tone-card:hover {
  background-color: var(--v-theme-surface-container) !important;
  transform: translateX(4px);
}
</style>
