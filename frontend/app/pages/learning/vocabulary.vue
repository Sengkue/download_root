<template>
  <div class="pa-6">
    <div class="max-w-7xl mx-auto space-y-12 pb-12">
      
      <!-- Hero Section -->
      <v-card class="bg-primary text-on-primary rounded-xl pa-8 pa-md-12 position-relative overflow-hidden" elevation="10">
        <!-- Background Blur Orbs -->
        <div class="position-absolute bg-secondary-container" style="width: 300px; height: 300px; border-radius: 50%; filter: blur(80px); right: -60px; top: -60px; opacity: 0.2; pointer-events: none;"></div>
        <div class="position-absolute bg-tertiary-fixed" style="width: 250px; height: 250px; border-radius: 50%; filter: blur(60px); right: 33%; bottom: -60px; opacity: 0.15; pointer-events: none;"></div>
        
        <div class="position-relative z-10 d-flex flex-column flex-lg-row align-start align-lg-center justify-space-between gap-6">
          <div style="max-width: 650px;">
            <div class="d-inline-flex align-center gap-2 px-3 py-1 rounded-pill bg-white text-primary-fixed text-caption font-weight-bold text-uppercase mb-4" style="background-color: rgba(255,255,255,0.15) !important;">
              <span class="bg-tertiary-fixed rounded-pill" style="width: 8px; height: 8px;"></span>
              Pob Lus A-Z • ວັດຈະນານຸກົມ 3 ພາສາ • Trilingual Dictionary
            </div>
            <h1 class="text-h3 font-weight-black text-on-primary mb-4" style="letter-spacing: -0.02em;">Vocabulary Hub & A-Z Explorer</h1>
            <p class="text-h6 font-weight-regular text-primary-fixed mb-0">
              Comprehensive trilingual concordance linking <strong class="text-on-primary font-weight-bold">Hmong RPA</strong>, <strong class="text-on-primary font-weight-bold">ພາສາລາວ (Lao Script)</strong>, and <strong class="text-on-primary font-weight-bold">English</strong> with pronunciation audio, tonal analysis, and context phrases.
            </p>
          </div>
          <div class="d-flex flex-wrap gap-4 w-100 w-lg-auto">
            <v-btn color="secondary-container" class="text-on-secondary-container font-weight-bold flex-1-1" size="x-large" rounded="xl" prepend-icon="mdi-help-circle" elevation="0" style="box-shadow: 0 4px 0 #8f0045 !important;">
              Practice Quiz
            </v-btn>
            <v-btn color="rgba(255,255,255,0.2)" variant="flat" class="text-on-primary font-weight-bold flex-1-1" size="x-large" rounded="xl" prepend-icon="mdi-download" elevation="0">
              Export PDF
            </v-btn>
          </div>
        </div>

        <div class="position-relative z-10 mt-8 pt-4 d-flex flex-wrap align-center justify-space-between gap-4 rounded-lg px-4 py-3" style="background-color: rgba(26,54,93,0.6); backdrop-filter: blur(10px);">
          <div class="d-flex align-center gap-4">
            <div class="d-flex align-center gap-2">
              <v-icon color="tertiary-fixed" size="small">mdi-check-decagram</v-icon>
              <span class="text-caption text-on-primary">Dialect Mode:</span>
              <v-chip size="small" color="rgba(0,61,56,0.8)" class="text-tertiary-fixed font-weight-bold">White Hmong (Dawb) / Green (Leeg)</v-chip>
            </div>
            <span class="text-on-primary-container opacity-40 d-none d-md-inline">|</span>
            <div class="d-none d-md-flex align-center gap-2">
              <v-icon color="secondary-fixed" size="small">mdi-book-open-variant</v-icon>
              <span class="text-caption text-primary-fixed">842 Active Trilingual Headwords</span>
            </div>
          </div>
          <div class="d-flex align-center gap-2 w-100" style="max-width: 200px;">
            <v-progress-linear model-value="25" color="tertiary-fixed" bg-color="rgba(255,255,255,0.2)" rounded height="8"></v-progress-linear>
            <span class="text-caption text-primary-fixed font-weight-bold whitespace-nowrap">Index A-Z</span>
          </div>
        </div>
      </v-card>

      <!-- Search & Filters Container -->
      <div class="bg-surface-container-low pa-4 rounded-xl shadow-sm d-flex flex-column gap-4">
        
        <!-- Search Row -->
        <div class="d-flex flex-column flex-lg-row align-center justify-space-between gap-4">
          <v-text-field
            variant="solo"
            density="compact"
            placeholder="Search dictionary across RPA (dej, ntoo...), Lao (ນົກ, ນ້ຳ...), or English (bird, tree...)..."
            prepend-inner-icon="mdi-magnify"
            hide-details
            bg-color="surface-container-lowest"
            class="search-input w-100 flex-1-1"
          ></v-text-field>
          <div class="d-flex align-center gap-2 overflow-x-auto w-100 w-lg-auto pb-2 pb-lg-0">
            <span class="text-caption font-weight-bold text-on-surface-variant mr-2">Tone:</span>
            <v-btn size="small" color="primary" class="font-weight-bold rounded" elevation="0">All</v-btn>
            <v-btn size="small" color="surface-container-lowest" variant="flat" class="font-weight-bold rounded text-on-surface text-none" elevation="0" v-for="tone in ['-b (˥)', '-m (˩)', '-j (˥˧)', '-v (˨˦)', '-s (˩˧)', '-g (˧˩)', '-d']" :key="tone">{{ tone }}</v-btn>
          </div>
        </div>

        <v-divider class="bg-surface-container-highest"></v-divider>

        <!-- A-Z Row -->
        <div class="d-flex align-center gap-1 overflow-x-auto pb-2 -mx-4 px-4 mx-sm-0 px-sm-0">
          <span class="text-caption font-weight-bold text-on-surface-variant text-uppercase tracking-widest pr-2 flex-shrink-0">A-Z:</span>
          <v-btn size="small" color="primary" variant="flat" class="font-weight-bold rounded-lg min-w-0 px-2" height="32" elevation="0">All</v-btn>
          <v-btn v-for="letter in 'ABCDEFGHIJKLM'.split('')" :key="letter" size="small" color="surface-container-lowest" variant="flat" class="font-weight-bold rounded-lg min-w-0 px-2 text-on-surface" height="32" elevation="0">{{ letter }}</v-btn>
          <v-btn size="small" color="secondary" variant="flat" class="font-weight-bold rounded-lg min-w-0 px-2 text-on-secondary shadow-sm" height="32" elevation="0">N</v-btn>
          <v-btn v-for="letter in 'OPQRSTUVWXYZ'.split('')" :key="letter" size="small" color="surface-container-lowest" variant="flat" class="font-weight-bold rounded-lg min-w-0 px-2 text-on-surface" height="32" elevation="0">{{ letter }}</v-btn>
        </div>

        <!-- Categories Row -->
        <div class="d-flex flex-wrap align-center justify-space-between gap-2 pt-1">
          <div class="d-flex align-center gap-2 flex-wrap">
            <span class="text-caption font-weight-bold text-on-surface-variant">Categories:</span>
            <v-chip color="primary" class="font-weight-bold shadow-sm">All Categories</v-chip>
            <v-chip color="surface-container-lowest" class="text-on-surface font-weight-bold shadow-sm" v-for="cat in ['🐾 Animals (Tsiaj)', '🌿 Nature (Xwm Txheem)', '🍲 Food (Khoom Noj)', '🏡 Home & Everyday']" :key="cat">{{ cat }}</v-chip>
          </div>
          <div class="d-flex align-center gap-2">
            <span class="text-caption font-weight-bold text-on-surface-variant">View:</span>
            <v-btn size="small" color="surface-container-lowest" variant="flat" class="font-weight-bold text-primary shadow-sm px-2 text-none" elevation="0" prepend-icon="mdi-view-grid">Cards</v-btn>
            <v-btn size="small" color="surface-container" variant="flat" class="font-weight-bold text-on-surface-variant px-2 text-none" elevation="0" prepend-icon="mdi-format-list-bulleted">Table A-Z</v-btn>
          </div>
        </div>
      </div>

      <!-- Featured Word Section -->
      <div class="space-y-4">
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center gap-2">
            <v-icon color="secondary">mdi-star-circle</v-icon>
            <h2 class="text-h5 font-weight-black text-on-surface" style="letter-spacing: -0.01em;">Featured Trilingual Headword</h2>
            <v-chip size="x-small" color="secondary-fixed" text-color="on-secondary-fixed" class="font-weight-bold text-uppercase ml-2 rounded">Letter N • Word of the Day</v-chip>
          </div>
          <span class="text-caption font-weight-medium text-on-surface-variant d-none d-sm-inline">Tap speaker buttons to hear native audio</span>
        </div>

        <v-card class="bg-surface-container-lowest rounded-xl shadow-md overflow-hidden" elevation="0" border>
          <v-row no-gutters>
            <!-- Left Image -->
            <v-col cols="12" lg="5" class="bg-surface-container-low pa-6 pa-sm-8 d-flex flex-column align-center justify-center min-h-[280px]">
              <v-card class="rounded-xl bg-surface-container-lowest pa-3 d-flex align-center justify-center shadow-sm" width="256" height="256" elevation="0" border>
                <v-img src="https://lh3.googleusercontent.com/aida/AEtjO1VqYlD_TC0QocW2m2Uk4QRlWaM3ZeQPEpxdLLRWjVY7LtnzGtXxMxqu-jPk18RRHsbpsB-6iAwHmkdL-aCvCmjeHflcBEyWYCTfHPadLr3i8sclia8zA4SgqKMF9qohUdAkml7HH0x9l57WozzX8_xk86hsj9xFIonxOm6Dt2cxHBWFkpSUJ2OxnenJiWXMqC89WafzxXGkoYSt2vlWMZM_b8_GwpRpWkG5rcO_3pOyi6dWyae7V7kfTpZe" class="rounded-lg w-100 h-100"></v-img>
              </v-card>
              <div class="mt-6 d-flex align-center gap-2">
                <span class="bg-secondary rounded-full" style="width: 10px; height: 10px;"></span>
                <span class="text-caption text-on-surface-variant text-uppercase font-weight-bold tracking-widest">Topic: Tsiaj (Animals) • ສັດ</span>
              </div>
            </v-col>

            <!-- Right Content -->
            <v-col cols="12" lg="7" class="pa-6 pa-sm-8 d-flex flex-column justify-space-between gap-6">
              <div class="d-flex flex-column gap-4 w-100">
                <!-- Hmong -->
                <div class="pa-4 rounded-xl bg-surface-container-low d-flex align-center justify-space-between gap-4 row-hover">
                  <div>
                    <div class="d-flex align-center gap-2 mb-1">
                      <v-chip size="x-small" color="primary" class="font-weight-bold rounded">Hmong (RPA)</v-chip>
                      <span class="text-caption text-on-surface-variant">White: <strong class="text-on-surface font-weight-bold">Dawb</strong> | Green: <strong class="text-on-surface font-weight-bold">nquab</strong></span>
                    </div>
                    <div class="d-flex align-baseline gap-3">
                      <span class="text-h4 font-weight-black text-primary">noog</span>
                      <span class="text-caption text-on-surface-variant text-mono">[nɔ̃ŋ˦]</span>
                      <v-chip size="x-small" color="tertiary-fixed" text-color="on-tertiary-fixed" class="font-weight-bold rounded">Tone -g (High Falling)</v-chip>
                    </div>
                  </div>
                  <v-btn icon color="primary" elevation="0" class="shadow-btn-primary"><v-icon>mdi-volume-high</v-icon></v-btn>
                </div>

                <!-- Lao -->
                <div class="pa-4 rounded-xl bg-surface-container-low d-flex align-center justify-space-between gap-4 row-hover">
                  <div>
                    <div class="d-flex align-center gap-2 mb-1">
                      <v-chip size="x-small" color="tertiary-container" text-color="on-tertiary-fixed" class="font-weight-bold rounded">ພາສາລາວ (Lao)</v-chip>
                      <span class="text-caption text-on-surface-variant">Tone: ສຽງຕີ (High tone)</span>
                    </div>
                    <div class="d-flex align-baseline gap-3">
                      <span class="text-h4 font-weight-black text-tertiary">ນົກ</span>
                      <span class="text-caption text-on-surface-variant text-mono">nók</span>
                      <v-chip size="x-small" color="surface-container-highest" text-color="on-surface-variant" class="font-weight-bold rounded">IPA: /nók/</v-chip>
                    </div>
                  </div>
                  <v-btn icon color="tertiary-container" text-color="on-tertiary-container" elevation="0" class="shadow-btn-tertiary"><v-icon>mdi-volume-high</v-icon></v-btn>
                </div>

                <!-- English -->
                <div class="pa-4 rounded-xl bg-surface-container-low d-flex align-center justify-space-between gap-4 row-hover">
                  <div>
                    <div class="d-flex align-center gap-2 mb-1">
                      <v-chip size="x-small" color="secondary-container" text-color="on-secondary-container" class="font-weight-bold rounded">English</v-chip>
                      <span class="text-caption text-on-surface-variant">Noun • Singular</span>
                    </div>
                    <div class="d-flex align-baseline gap-3">
                      <span class="text-h4 font-weight-black text-secondary">bird</span>
                      <span class="text-caption text-on-surface-variant text-mono">/bɜːrd/</span>
                    </div>
                  </div>
                  <v-btn icon color="secondary-container" text-color="on-secondary-container" elevation="0" class="shadow-btn-secondary"><v-icon>mdi-volume-high</v-icon></v-btn>
                </div>
              </div>

              <!-- Context Sentences -->
              <div class="mt-4 pa-4 rounded-lg bg-surface-container w-100">
                <div class="d-flex align-center justify-space-between mb-2">
                  <span class="text-caption font-weight-bold text-uppercase tracking-widest text-on-surface-variant d-flex align-center gap-1">
                    <v-icon size="small">mdi-chat</v-icon> Context Sentences
                  </span>
                  <a href="#" class="text-caption text-primary font-weight-bold text-decoration-none">Play All</a>
                </div>
                <v-row dense>
                  <v-col cols="12" md="4">
                    <div class="pa-2 rounded bg-surface-container-lowest h-100">
                      <div class="text-caption font-weight-bold text-primary">Hmong</div>
                      <p class="text-body-2 font-italic text-on-surface mt-1 mb-0">"Tus noog hu nkauj thaum sawv ntxov."</p>
                    </div>
                  </v-col>
                  <v-col cols="12" md="4">
                    <div class="pa-2 rounded bg-surface-container-lowest h-100">
                      <div class="text-caption font-weight-bold text-tertiary">Lao</div>
                      <p class="text-body-2 font-italic text-on-surface mt-1 mb-0">"ນົກຮ້ອງໃນຕອນເຊົ້າ."</p>
                    </div>
                  </v-col>
                  <v-col cols="12" md="4">
                    <div class="pa-2 rounded bg-surface-container-lowest h-100">
                      <div class="text-caption font-weight-bold text-secondary">English</div>
                      <p class="text-body-2 font-italic text-on-surface mt-1 mb-0">"The bird sings in the morning."</p>
                    </div>
                  </v-col>
                </v-row>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </div>

      <!-- Dynamic Sections -->
      <DictionarySection letter="B" title="Cov Lus Tsab Ntawv B" count="2" :items="bItems" />
      <DictionarySection letter="D" title="Cov Lus Tsab Ntawv D" count="2" :items="dItems" />
      <DictionarySection letter="F & H" title="Flower, House & Horse" count="Core everyday vocabulary entries" :items="fhItems" />
      <DictionarySection letter="P & W" title="Fish & Water" count="Nature & aquatic essentials" :items="pwItems" />

      <!-- Feature Blocks -->
      <v-row class="pt-6">
        <v-col cols="12" md="4">
          <v-card class="bg-surface-container-lowest pa-6 rounded-xl shadow-sm h-100 d-flex flex-column justify-space-between" elevation="0" border>
            <div class="space-y-2 mb-4">
              <div class="bg-primary-fixed text-primary font-weight-bold d-flex align-center justify-center rounded-lg text-body-2 mb-3" style="width: 40px; height: 40px;">RPA</div>
              <h4 class="text-h6 font-weight-bold text-primary">Lus Hmoob (Hmong)</h4>
              <p class="text-body-2 text-on-surface-variant">Master 8 tone marks (-b, -m, -d, -j, -v, -s, -g, blank), 14 vowels, and single/double/triple/quadruple consonant onsets.</p>
            </div>
            <a href="#" class="text-body-2 text-primary font-weight-bold text-decoration-none hover-underline d-flex align-center gap-1">
              Explore RPA Tone Guide <v-icon size="small">mdi-arrow-right</v-icon>
            </a>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="bg-surface-container-lowest pa-6 rounded-xl shadow-sm h-100 d-flex flex-column justify-space-between" elevation="0" border>
            <div class="space-y-2 mb-4">
              <div class="bg-tertiary-fixed text-tertiary font-weight-bold d-flex align-center justify-center rounded-lg text-body-2 mb-3" style="width: 40px; height: 40px;">ສຽງ</div>
              <h4 class="text-h6 font-weight-bold text-tertiary">ພາສາລາວ (Lao Script)</h4>
              <p class="text-body-2 text-on-surface-variant">Explore 27 consonants, vowel diacritics, tone markers (ໄມ້ເອກ, ໄມ້ໂທ), and direct phonetic transliteration guides.</p>
            </div>
            <a href="#" class="text-body-2 text-tertiary font-weight-bold text-decoration-none hover-underline d-flex align-center gap-1">
              Explore Lao Syllabary <v-icon size="small">mdi-arrow-right</v-icon>
            </a>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="bg-surface-container-lowest pa-6 rounded-xl shadow-sm h-100 d-flex flex-column justify-space-between" elevation="0" border>
            <div class="space-y-2 mb-4">
              <div class="bg-secondary-fixed text-secondary font-weight-bold d-flex align-center justify-center rounded-lg text-body-2 mb-3" style="width: 40px; height: 40px;">ESL</div>
              <h4 class="text-h6 font-weight-bold text-secondary">English (Lus Askiv)</h4>
              <p class="text-body-2 text-on-surface-variant">Bilingual grammar tips, common idioms, conversational dialogues, and pronunciation drills crafted specifically for heritage speakers.</p>
            </div>
            <a href="#" class="text-body-2 text-secondary font-weight-bold text-decoration-none hover-underline d-flex align-center gap-1">
              Explore English Drills <v-icon size="small">mdi-arrow-right</v-icon>
            </a>
          </v-card>
        </v-col>
      </v-row>

    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'learning'
});

const bItems = [
  { 
    id: 1, 
    color: 'primary', icon: 'mdi-soccer', tag: 'Everyday',
    title: 'Ball / Pob / ໝາກບານ',
    hmong: { word: 'pob', tone: 'Tone -b', toneColor: 'tertiary-fixed', textToneColor: 'on-tertiary-fixed' },
    lao: { word: 'ໝາກບານ', sub: 'mak ban' },
    eng: { word: 'ball', sub: '/bɔːl/' },
    context: '"Ncaws pob" = Play soccer / ເຕະບານ'
  },
  { 
    id: 2, 
    color: 'secondary', icon: 'mdi-book-open-page-variant', tag: 'Study',
    title: 'Book / Phau Ntawv / ປຶ້ມ',
    hmong: { word: 'phau ntawv', tone: 'Tone -v', toneColor: 'secondary-fixed', textToneColor: 'on-secondary-fixed' },
    lao: { word: 'ປຶ້ມ', sub: 'peum' },
    eng: { word: 'book', sub: '/bʊk/' },
    context: '"Nyeem phau ntawv" = Read the book / ອ່ານປຶ້ມ'
  }
];

const dItems = [
  { 
    id: 1, 
    color: 'primary', icon: 'mdi-white-balance-sunny', tag: 'Sky & Time',
    title: 'Day / Sun / Hnub / ຕາເວັນ',
    hmong: { word: 'hnub', tone: 'Tone -b', toneColor: 'tertiary-fixed', textToneColor: 'on-tertiary-fixed' },
    lao: { word: 'ຕາເວັນ', sub: 'ta ven' },
    eng: { word: 'day / sun', sub: '/sʌn/' },
    context: '"Hnub no zoo heev" = Today is very good'
  },
  { 
    id: 2, 
    color: 'tertiary', icon: 'mdi-paw', tag: 'Animals',
    title: 'Dog / Aub / ໝາ',
    hmong: { word: 'aub', tone: 'Tone -b', toneColor: 'tertiary-fixed', textToneColor: 'on-tertiary-fixed' },
    lao: { word: 'ໝາ', sub: 'maa (rising)' },
    eng: { word: 'dog', sub: '/dɔːɡ/' },
    context: '"Tus aub syp tus miv" = The dog sees the cat'
  }
];

const fhItems = [
  { 
    id: 1, 
    color: 'secondary', icon: 'mdi-flower', tag: 'Nature',
    title: 'Flower / Paj / ດອກໄມ້',
    hmong: { word: 'paj', tone: 'Tone -j', toneColor: 'primary-fixed', textToneColor: 'primary' },
    lao: { word: 'ດອກໄມ້', sub: 'Dok Mai' },
    eng: { word: 'flower', sub: '/ˈflaʊər/' },
    context: ''
  },
  { 
    id: 2, 
    color: 'secondary', icon: 'mdi-home', tag: 'Home',
    title: 'House / Tsev / ເຮືອນ',
    hmong: { word: 'tsev', tone: 'Tone -v', toneColor: 'tertiary-fixed', textToneColor: 'tertiary' },
    lao: { word: 'ເຮືອນ', sub: 'Heuan' },
    eng: { word: 'house', sub: '/haʊs/' },
    context: ''
  },
  { 
    id: 3, 
    color: 'tertiary', icon: 'mdi-horse', tag: 'Animals',
    title: 'Horse / Nees / ມ້າ',
    hmong: { word: 'nees', tone: 'Tone -s', toneColor: 'secondary-fixed', textToneColor: 'secondary' },
    lao: { word: 'ມ້າ', sub: 'Maa' },
    eng: { word: 'horse', sub: '/hɔːrs/' },
    context: ''
  }
];

const pwItems = [
  { 
    id: 1, 
    color: 'tertiary', icon: 'mdi-fish', tag: 'Animals',
    title: 'Fish / Ntses / ປາ',
    hmong: { word: 'ntses', tone: 'Tone -s', toneColor: 'secondary-fixed', textToneColor: 'secondary' },
    lao: { word: 'ປາ', sub: 'Paa' },
    eng: { word: 'fish', sub: '/fɪʃ/' },
    context: '"Ntses nyob hauv dej" = Fish lives in the water'
  },
  { 
    id: 2, 
    color: 'tertiary', icon: 'mdi-water', tag: 'Nature',
    title: 'Water / Dej / ນ້ຳ',
    hmong: { word: 'dej', tone: 'Tone -j', toneColor: 'tertiary-fixed', textToneColor: 'tertiary' },
    lao: { word: 'ນ້ຳ', sub: 'Nam' },
    eng: { word: 'water', sub: '/ˈwɔːtər/' },
    context: '"Haus dej txias" = Drink cold water / ດື່ມນ້ຳເຢັນ'
  }
];
</script>

<style scoped>
.space-y-12 > * + * {
  margin-top: 3rem;
}
.space-y-4 > * + * {
  margin-top: 1rem;
}
.gap-6 {
  gap: 1.5rem;
}
.shadow-btn-primary { box-shadow: 0 3px 0 #00132b !important; }
.shadow-btn-tertiary { box-shadow: 0 3px 0 #002522 !important; }
.shadow-btn-secondary { box-shadow: 0 3px 0 #8f0045 !important; }

.row-hover {
  transition: all 0.2s ease;
}
.row-hover:hover {
  background-color: var(--v-theme-surface-container) !important;
}
.search-input:deep(.v-field) {
  border-radius: 8px !important;
  border: 1px solid rgba(196, 198, 207, 0.6) !important;
  box-shadow: none !important;
}
.search-input:deep(.v-field--focused) {
  border-color: var(--v-theme-primary) !important;
  box-shadow: 0 0 0 1px var(--v-theme-primary) !important;
}
.tracking-widest {
  letter-spacing: 0.1em;
}
.text-mono {
  font-family: monospace;
}
</style>
