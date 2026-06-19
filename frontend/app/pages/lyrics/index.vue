<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

const searchQuery = ref('');
const isSearching = ref(false);
const results = ref<any[]>([]);
const errorMessage = ref('');

const isViewingSong = ref(false);
const isLoadingSong = ref(false);
const currentSong = ref<any>(null);

const formattedLyrics = computed(() => {
  if (!currentSong.value || !currentSong.value.lyrics) return '';
  
  let text = currentSong.value.lyrics;
  
  // The backend scraper is returning hidden directional characters and exactly two newlines
  // between EVERY single line, permanently losing the original stanza breaks.
  // We must strip it and intelligently reconstruct the stanzas.
  text = text.replace(/[\u202C\u202D]/g, '');
  
  // Collapse all spacing down to single newlines
  text = text.replace(/\n\s*\n/g, '\n');
  text = text.replace(/\n+/g, '\n');
  
  // Reconstruct stanzas: Add a blank line before any verse header like "(Rap I:Jin)" or "[Chorus]"
  text = text.replace(/\n([ \t]*[\(\[].*?[\)\]])/g, '\n\n$1');
  
  return text.trim();
});

// Home data
const featuredLyrics = ref<any[]>([]);
const latestLyrics = ref<any[]>([]);
const isLoadingHome = ref(true);

const alphabet = '# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' ');

const fetchHomeData = async () => {
  try {
    const res = await fetch('http://localhost:3001/api/lyrics/home');
    const data = await res.json();
    if (res.ok) {
      featuredLyrics.value = data.featured || [];
      latestLyrics.value = data.latest || [];
    }
  } catch (e) {
    console.error("Failed to load home data", e);
  } finally {
    isLoadingHome.value = false;
  }
};

onMounted(() => {
  fetchHomeData();
});

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return;
  
  if (searchQuery.value.includes('hmonglyrics.net/lyrics/')) {
     await viewSong({ url: searchQuery.value, title: 'Direct Link' });
     return;
  }

  isSearching.value = true;
  errorMessage.value = '';
  results.value = [];
  isViewingSong.value = false;

  try {
    const res = await fetch(`http://localhost:3001/api/lyrics/search?q=${encodeURIComponent(searchQuery.value)}`);
    const data = await res.json();
    
    if (!res.ok) throw new Error(data.error || 'Failed to search lyrics.');
    
    results.value = data.results || [];
    if (results.value.length === 0) {
       errorMessage.value = "No lyrics found for your search.";
    }
  } catch (err: any) {
    errorMessage.value = err.message || "An error occurred while searching.";
  } finally {
    isSearching.value = false;
  }
};

const viewSong = async (song: any) => {
  isLoadingSong.value = true;
  errorMessage.value = '';
  isViewingSong.value = true;
  currentSong.value = null; // Clear old

  try {
    const res = await fetch(`http://localhost:3001/api/lyrics/song`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: song.url })
    });
    
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to fetch song lyrics.');
    
    currentSong.value = data;
  } catch (err: any) {
    errorMessage.value = err.message || "An error occurred while fetching the song.";
    isViewingSong.value = false;
  } finally {
    isLoadingSong.value = false;
  }
};

const backToSearch = () => {
  isViewingSong.value = false;
  currentSong.value = null;
};

const backToHome = () => {
  searchQuery.value = '';
  results.value = [];
  errorMessage.value = '';
  isViewingSong.value = false;
  currentSong.value = null;
};

const downloadLyricsText = () => {
   if (!currentSong.value || !currentSong.value.lyrics) return;
   
   const textContent = `${currentSong.value.title}\nArtist: ${currentSong.value.artist}\n\n${formattedLyrics.value}`;
   const blob = new Blob([textContent], { type: 'text/plain' });
   const url = URL.createObjectURL(blob);
   
   const a = document.createElement('a');
   a.href = url;
   a.download = `${currentSong.value.title.replace(/[^a-zA-Z0-9]/g, '_')}_Lyrics.txt`;
   document.body.appendChild(a);
   a.click();
   document.body.removeChild(a);
   URL.revokeObjectURL(url);
};

const printLyrics = () => {
   if (!currentSong.value || typeof window === 'undefined') return;
   
   const printWindow = window.open('', '_blank', 'height=800,width=800');
   if (!printWindow) return;
   
   const title = currentSong.value.title || 'Unknown Title';
   const artist = currentSong.value.artist || 'Unknown Artist';
   const lyrics = formattedLyrics.value || '';
   
   printWindow.document.write(`
      <html>
      <head>
         <title>Print - ${title}</title>
         <style>
            body { 
               font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
               padding: 40px; 
               color: #000; 
               background: #fff; 
               max-width: 800px; 
               margin: 0 auto; 
            }
            h1 { font-size: 28pt; margin-bottom: 8px; }
            h2 { font-size: 16pt; color: #555; margin-top: 0; margin-bottom: 40px; }
            pre { 
               font-family: inherit; 
               font-size: 14pt; 
               line-height: 1.8; 
               white-space: pre-wrap; 
            }
            @media print {
               body { padding: 0; max-width: 100%; }
            }
         </style>
      </head>
      <body>
         <h1>${title}</h1>
         <h2>${artist}</h2>
         <pre>${lyrics}</pre>
      </body>
      </html>
   `);
   
   printWindow.document.close();
   printWindow.focus();
   
   setTimeout(() => {
      printWindow.print();
      printWindow.close();
   }, 250);
};

const defaultArtists = [
  'Huab Vwj',
  'HMisfit',
  'Vaj Tsua',
  'ZAJ DUB',
  'Maiv Lis Thoj',
  'Maiv Thoj',
  'Leng Yang',
  'Maa Vue'
];

const isSubmitDialogOpen = ref(false);
const isSubmitting = ref(false);
const submitForm = ref({
  title: '', artist: '', album: '', videoEmbed: '', lyrics: '', submitterName: '', captcha: ''
});

const submitLyric = async () => {
  if (!submitForm.value.title || !submitForm.value.lyrics) return;
  isSubmitting.value = true;
  await new Promise(resolve => setTimeout(resolve, 1500));
  isSubmitting.value = false;
  isSubmitDialogOpen.value = false;
  submitForm.value = { title: '', artist: '', album: '', videoEmbed: '', lyrics: '', submitterName: '', captcha: '' };
  alert('Thank you! Your lyric has been submitted for review.');
};
</script>

<template>
  <div class="lyrics-page-wrapper">
    <!-- Top Header (Always visible unless printing) -->
    <div class="d-print-none original-header pt-4 pb-0">
      <v-container class="py-0">
        <h1 class="text-h4 font-weight-bold text-white mb-1 cursor-pointer" @click="backToHome">HmongLyrics.net</h1>
        <h2 class="text-subtitle-1 text-white mb-4 font-weight-regular">Hmong Music</h2>
        
        <div class="d-flex w-100 flex-column flex-md-row">
          <div class="alphabet-bar flex-grow-1 d-flex align-center px-4 py-2 overflow-x-auto text-white">
            <span v-for="letter in alphabet" :key="letter" class="mx-2 font-weight-bold text-caption cursor-pointer alphabet-letter">
              {{ letter }}
            </span>
          </div>
          <button class="submit-btn-original d-flex align-center px-6 py-3 py-md-0 font-weight-bold text-white" @click="isSubmitDialogOpen = true">
            <v-icon icon="mdi-plus" class="mr-2" size="small"></v-icon> Submit Lyric
          </button>
        </div>
      </v-container>
    </div>

    <!-- MAIN HOME VIEW (when not searching and not viewing song) -->
    <v-fade-transition leave-absolute>
      <div v-if="!isViewingSong && results.length === 0" class="d-print-none">
        
        <!-- Search Hero -->
        <div class="search-hero text-center py-12 py-md-16">
          <v-container>
            <h2 class="text-white text-h4 text-md-h3 font-weight-regular mb-8">Search 1120 Song Lyrics</h2>
            <v-row justify="center">
              <v-col cols="12" md="8" lg="6">
                <v-text-field
                  v-model="searchQuery"
                  variant="solo"
                  placeholder="Search: Enter lyrics name keywords hit enter"
                  bg-color="white"
                  elevation="4"
                  rounded="pill"
                  hide-details
                  @keyup.enter="handleSearch"
                  append-inner-icon="mdi-magnify"
                  @click:append-inner="handleSearch"
                  class="search-bar-original"
                  :loading="isSearching"
                ></v-text-field>
                <v-alert v-if="errorMessage" type="error" variant="tonal" class="mt-4 bg-white text-error">
                  {{ errorMessage }}
                </v-alert>
              </v-col>
            </v-row>
          </v-container>
        </div>

        <v-container class="py-8">
          <v-card v-if="isLoadingHome" class="pa-10 text-center rounded-xl bg-transparent border-0" elevation="0">
             <v-progress-circular indeterminate color="white" size="64" width="6"></v-progress-circular>
          </v-card>
          
          <div v-else class="content-wrapper bg-white">
            <!-- Featured Lyrics Carousel/Grid -->
            <div class="pa-4 pa-md-8">
              <div class="section-title mb-6 d-flex align-center">
                <v-icon icon="mdi-star" color="red-darken-1" class="mr-2"></v-icon>
                <h3 class="text-h6 font-weight-bold text-uppercase">Featured Lyrics</h3>
              </div>
              
              <v-slide-group show-arrows class="featured-slide-group">
                <v-slide-group-item v-for="(song, i) in featuredLyrics" :key="i" v-slot="{ isSelected, toggle }">
                  <v-card
                    class="ma-2 featured-card cursor-pointer"
                    width="200"
                    height="300"
                    elevation="0"
                    @click="viewSong(song)"
                  >
                    <v-img :src="song.image" height="100%" cover class="align-end">
                      <div class="featured-overlay pa-4 w-100">
                        <div class="text-white font-weight-bold text-subtitle-1 lh-1">{{ song.title }}</div>
                        <div class="text-white text-caption">{{ song.artist }}</div>
                      </div>
                    </v-img>
                  </v-card>
                </v-slide-group-item>
              </v-slide-group>
            </div>

            <v-divider></v-divider>

            <!-- Latest Lyrics Grid -->
            <div class="pa-4 pa-md-8 bg-grey-lighten-5">
              <div class="section-title mb-6 d-flex align-center">
                <v-icon icon="mdi-clock-outline" color="red-darken-1" class="mr-2"></v-icon>
                <h3 class="text-h6 font-weight-bold text-uppercase">Latest Lyrics</h3>
              </div>
              
              <v-row>
                <v-col v-for="(song, i) in latestLyrics" :key="i" cols="12" md="4" class="py-2">
                  <div class="latest-item d-flex flex-column pa-3 cursor-pointer" @click="viewSong(song)">
                    <span class="font-weight-bold text-body-1 mb-1 latest-title">{{ song.title }}</span>
                    <span class="text-grey-darken-1 text-body-2">{{ song.artist }}</span>
                  </div>
                </v-col>
              </v-row>
            </div>
          </div>
        </v-container>
      </div>
    </v-fade-transition>

    <!-- SEARCH RESULTS VIEW -->
    <v-fade-transition leave-absolute>
      <div v-if="!isViewingSong && results.length > 0" class="d-print-none search-hero py-12 min-h-screen">
        <v-container>
          <div class="d-flex align-center justify-space-between mb-8">
            <h2 class="text-h4 font-weight-black text-white">Search Results ({{ results.length }})</h2>
            <v-btn variant="tonal" color="white" @click="backToHome">Clear Search</v-btn>
          </div>
          <v-row>
            <v-col v-for="(song, i) in results" :key="i" cols="12" sm="6" md="4" lg="3">
              <v-card class="h-100 rounded-xl result-card d-flex flex-column" elevation="4" @click="viewSong(song)">
                <div class="result-card-bg"></div>
                <v-card-title class="text-h6 font-weight-bold pt-6 px-6 pb-2 text-wrap" style="line-height: 1.3;">
                  {{ song.title }}
                </v-card-title>
                <v-card-subtitle class="px-6 pb-4 d-flex align-center font-weight-medium text-purple-darken-1">
                  <v-icon icon="mdi-account-music" size="small" class="mr-2"></v-icon>
                  {{ song.artist }}
                </v-card-subtitle>
                <v-spacer></v-spacer>
                <v-card-actions class="px-6 pb-6 pt-0">
                  <div class="text-caption text-grey-darken-1 font-weight-medium d-flex align-center view-lyrics-text">
                    View Lyrics <v-icon icon="mdi-arrow-right" size="small" class="ml-1"></v-icon>
                  </div>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </div>
    </v-fade-transition>

    <!-- SINGLE SONG VIEWER -->
    <v-fade-transition leave-absolute>
      <div v-if="isViewingSong" class="print-area search-hero min-h-screen py-8">
        <v-container class="print-container py-0">
          <v-btn
             variant="text"
             color="white"
             prepend-icon="mdi-arrow-left"
             class="mb-6 text-none font-weight-bold d-print-none"
             @click="backToSearch"
             size="large"
          >
             Back
          </v-btn>

          <v-card v-if="isLoadingSong" class="pa-10 text-center rounded-xl glass-panel border-0" elevation="10">
             <v-progress-circular indeterminate color="purple" size="64" width="6" class="mb-4"></v-progress-circular>
             <h3 class="text-h5 font-weight-medium text-grey-darken-2">Extracting beautiful lyrics...</h3>
          </v-card>

          <v-card v-else-if="currentSong" class="rounded-0 overflow-hidden bg-white" elevation="12">
             <!-- Hero Banner -->
             <v-img
                v-if="currentSong.backgroundImage"
                :src="currentSong.backgroundImage"
                height="min(450px, 45vh)"
                cover
                class="align-end position-relative banner-img d-print-none"
             >
                <div class="position-absolute w-100 h-100 banner-gradient"></div>
                
                <div class="position-relative pa-6 pa-md-12 text-white z-1">
                   <div class="d-inline-block px-4 py-1 rounded-pill bg-white text-purple-darken-4 font-weight-bold mb-4 elevation-4 text-caption text-uppercase tracking-wider">
                      {{ currentSong.artist }}
                   </div>
                   <h1 class="text-h4 text-md-h2 font-weight-black mb-2" style="text-shadow: 0px 4px 12px rgba(0,0,0,0.4); line-height: 1.1; letter-spacing: -1px;">
                      {{ currentSong.title }}
                   </h1>
                </div>
             </v-img>
             <div v-else class="banner-gradient pa-6 pa-md-12 text-white text-center d-print-none">
                <div class="d-inline-block px-4 py-1 rounded-pill bg-white text-purple-darken-4 font-weight-bold mb-4 elevation-4 text-caption text-uppercase tracking-wider">
                   {{ currentSong.artist }}
                </div>
                <h1 class="text-h4 text-md-h2 font-weight-black mb-2" style="line-height: 1.2; letter-spacing: -1px;">
                   {{ currentSong.title }}
                </h1>
             </div>
             
             <v-row class="ma-0">
               <!-- Lyrics Column -->
               <v-col cols="12" md="8" class="pa-6 pa-md-12 bg-white print-full-width">
                  <div class="d-flex align-center mb-6 pb-4" style="border-bottom: 1px solid #eaeaea;">
                     <h3 class="text-h6 font-weight-black mb-0 text-uppercase" style="letter-spacing: 0.5px; font-family: 'Oswald', sans-serif;">LYRIC</h3>
                     <v-spacer></v-spacer>
                     <a href="#" @click.prevent="printLyrics" class="text-red-darken-1 text-decoration-none font-weight-medium d-print-none print-btn d-flex align-center">
                        <v-icon icon="mdi-printer-outline" class="mr-1"></v-icon> Print
                     </a>
                  </div>
                  <!-- Print-only Title -->
                  <div class="d-none d-print-block mb-6">
                    <h1 class="text-h3 font-weight-bold">{{ currentSong.title }}</h1>
                    <h2 class="text-h5 text-grey-darken-2">{{ currentSong.artist }}</h2>
                  </div>
                  <v-card-text class="pa-0 text-grey-darken-4 lyric-content-text">
                     <pre>{{ formattedLyrics }}</pre>
                  </v-card-text>
               </v-col>
               
               <!-- Sidebar Column -->
               <v-col cols="12" md="4" class="pa-6 pa-md-10 sidebar-col d-print-none">
                  <v-btn class="font-weight-bold text-none w-100 mb-8 elevation-0 bg-grey-lighten-3 text-grey-darken-3" size="x-large" prepend-icon="mdi-download" @click="downloadLyricsText" height="64">
                     Download .txt
                  </v-btn>
                  
                  <div v-if="currentSong.videoUrl" class="mb-6 video-container">
                     <h3 class="text-subtitle-1 font-weight-black mb-4 text-grey-darken-2 text-uppercase tracking-wider">
                        <v-icon icon="mdi-youtube" color="red" class="mr-2"></v-icon> Music Video
                     </h3>
                     <v-responsive aspect-ratio="16/9" class="rounded overflow-hidden elevation-4 video-wrapper">
                       <iframe :src="currentSong.videoUrl" style="width:100%; height:100%; border:none;" allowfullscreen></iframe>
                     </v-responsive>
                  </div>
               </v-col>
             </v-row>
          </v-card>
        </v-container>
      </div>
    </v-fade-transition>

    <!-- Submit Lyric Dialog -->
    <v-dialog v-model="isSubmitDialogOpen" max-width="900" scrollable>
      <v-card class="rounded-0">
        <v-card-title class="pa-4 pa-sm-6 d-flex align-center flex-wrap" style="background-color: #5d5d5d;">
          <span class="text-h4 text-white" style="font-family: 'Oswald', sans-serif;">Submit Lyrics</span>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" variant="text" color="white" @click="isSubmitDialogOpen = false"></v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4 pa-sm-8 bg-white">
          <v-form @submit.prevent="submitLyric">
            
            <v-row class="mb-2" align="center">
              <v-col cols="12" sm="3" class="py-1">
                <label class="text-body-2 text-grey-darken-2">Lyrics Title</label>
              </v-col>
              <v-col cols="12" sm="9" class="py-1">
                <v-text-field v-model="submitForm.title" variant="outlined" density="compact" hide-details bg-color="white"></v-text-field>
              </v-col>
            </v-row>

            <v-row class="mb-0" align="center">
              <v-col cols="12" sm="3" class="py-1">
                <label class="text-body-2 text-grey-darken-2">Artist Name</label>
              </v-col>
              <v-col cols="12" sm="9" class="py-1">
                <v-combobox v-model="submitForm.artist" :items="defaultArtists" placeholder="Select or write a artist name." variant="outlined" density="compact" hide-details bg-color="white"></v-combobox>
              </v-col>
            </v-row>
            <v-row class="mb-2 mt-0">
              <v-col cols="12" sm="3" class="py-0"></v-col>
              <v-col cols="12" sm="9" class="py-0">
                <a href="#" class="text-caption text-grey-darken-2 text-decoration-none">+ Add More Artists</a>
              </v-col>
            </v-row>

            <v-row class="mb-2" align="center">
              <v-col cols="12" sm="3" class="py-1">
                <label class="text-body-2 text-grey-darken-2">Album Name</label>
              </v-col>
              <v-col cols="12" sm="9" class="py-1">
                <v-combobox v-model="submitForm.album" :items="[]" placeholder="Select or write a album name." variant="outlined" density="compact" hide-details bg-color="white"></v-combobox>
              </v-col>
            </v-row>

            <v-row class="mb-2" align="start">
              <v-col cols="12" sm="3" class="py-2">
                <label class="text-body-2 text-grey-darken-2">Video Embed</label>
              </v-col>
              <v-col cols="12" sm="9" class="py-1">
                <v-textarea v-model="submitForm.videoEmbed" variant="outlined" density="compact" hide-details rows="3" bg-color="white"></v-textarea>
              </v-col>
            </v-row>

            <v-row class="mb-2" align="start">
              <v-col cols="12" sm="3" class="py-2">
                <label class="text-body-2 text-grey-darken-2">Lyrics</label>
              </v-col>
              <v-col cols="12" sm="9" class="py-1">
                <v-textarea v-model="submitForm.lyrics" variant="outlined" density="compact" hide-details rows="6" bg-color="white"></v-textarea>
              </v-col>
            </v-row>

            <v-row class="mb-2" align="center">
              <v-col cols="12" sm="3" class="py-1">
                <label class="text-body-2 text-grey-darken-2">Your Name</label>
              </v-col>
              <v-col cols="12" sm="9" class="py-1">
                <v-text-field v-model="submitForm.submitterName" variant="outlined" density="compact" hide-details bg-color="white"></v-text-field>
              </v-col>
            </v-row>

            <v-row class="mb-6" align="center">
              <v-col cols="12" sm="3" class="py-1">
                <label class="text-body-2 text-grey-darken-2">6 + 8 = ?</label>
              </v-col>
              <v-col cols="12" sm="9" class="py-1">
                <v-text-field v-model="submitForm.captcha" variant="outlined" density="compact" hide-details bg-color="white"></v-text-field>
              </v-col>
            </v-row>

            <v-row>
               <v-col cols="12" sm="3"></v-col>
               <v-col cols="12" sm="9" class="text-center">
                  <v-btn color="#e74c3c" variant="flat" rounded="sm" class="px-6 font-weight-bold text-none text-white" :loading="isSubmitting" @click="submitLyric">Submit Lyric</v-btn>
               </v-col>
            </v-row>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

* {
  font-family: 'Inter', sans-serif;
}

.lyrics-page-wrapper {
  background-color: #274b6c; /* The exact dark blue from the original site */
  min-height: 100vh;
}
.min-h-screen {
  min-height: 100vh;
}

/* Header & Nav */
.original-header {
  background-color: #274b6c;
}
.alphabet-bar {
  background-color: #242424;
  border-radius: 4px 0 0 4px;
}
.alphabet-letter {
  opacity: 0.8;
}
.alphabet-letter:hover {
  opacity: 1;
  color: #ff5252 !important;
}
.submit-btn-original {
  background-color: #f44336; /* Red submit button */
  border-radius: 0 4px 4px 0;
  transition: background-color 0.2s;
}
.submit-btn-original:hover {
  background-color: #d32f2f;
}

/* Search Hero */
.search-hero {
  background-color: #274b6c;
}
.search-bar-original :deep(.v-field__input) {
  padding-top: 14px;
  padding-bottom: 14px;
}
.search-bar-original :deep(.v-icon) {
  color: #f44336 !important;
  font-weight: bold;
}

/* Content Container */
.content-wrapper {
  border-radius: 4px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  overflow: hidden;
}

/* Typography for titles */
h1, h2, h3, .section-title h3 {
  font-family: 'Oswald', sans-serif;
}
.section-title h3 {
  letter-spacing: 0.5px;
}

/* Featured Lyrics */
.featured-card {
  transition: transform 0.3s;
}
.featured-card:hover {
  transform: translateY(-5px);
}
.featured-overlay {
  background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 50%, transparent 100%);
}
.lh-1 {
  line-height: 1.2;
}

/* Latest Lyrics */
.latest-item {
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}
.latest-item:hover {
  background-color: #fff;
}
.latest-title {
  color: #2c3e50;
  transition: color 0.2s;
}
.latest-item:hover .latest-title {
  color: #f44336;
}

/* Song Viewer */
.banner-gradient {
  background: linear-gradient(to top, #111111 0%, rgba(17,17,17,0.4) 60%, rgba(17,17,17,0.1) 100%);
}
.lyric-content-text pre {
  font-family: inherit;
  font-size: 1.05rem;
  line-height: 1.3;
  white-space: pre-wrap;
  color: #4a4a4a;
}
.sidebar-col {
  background: #f8f9fa;
  border-left: 1px solid rgba(0,0,0,0.05);
}

/* Print Styles */
@media print {
  body { background: white !important; }
  .d-print-none { display: none !important; }
  .print-area { width: 100% !important; margin: 0 !important; padding: 0 !important; }
  .print-full-width { flex: 0 0 100% !important; max-width: 100% !important; padding: 0 !important; }
  .lyric-content-text pre { font-size: 12pt; line-height: 1.5; }
}
</style>
