<template>
  <v-app class="bg-surface">
    <!-- Sidebar Navigation -->
    <v-navigation-drawer
      v-model="drawer"
      class="bg-surface-container-low border-r border-surface-container-highest"
      elevation="0"
      width="288"
      permanent
    >
      <!-- Brand Logo Area -->
      <div class="d-flex align-center gap-2 px-6 h-20">
        <img
          src="/logo.jpg"
          alt="Brand logo"
          style="
            height: 32px;
            width: 32px;
            object-fit: cover;
            border-radius: 8px;
            margin: 5px;
          "
        />
        <div class="d-flex flex-column text-truncate">
          <span
            class="text-h6 font-weight-bold text-primary"
            style="line-height: 1.2"
            >Kawm ntawv</span
          >
          <span
            class="text-caption text-on-surface-variant text-uppercase font-weight-bold tracking-widest text-truncate"
            >Trilingual Hub</span
          >
        </div>
      </div>

      <div class="px-4 py-2">
        <v-list density="compact" nav class="bg-transparent pa-0">
          <!-- Languages -->
          <v-list-subheader
            class="text-caption font-weight-bold text-uppercase text-on-surface-variant tracking-widest px-2 mb-1"
          >
            Languages
          </v-list-subheader>

          <v-list-group value="hmong">
            <template v-slot:activator="{ props }">
              <v-list-item
                v-bind="props"
                prepend-icon="mdi-translate"
                title="Hmong (Lus Hmoob)"
                rounded="lg"
                class="nav-item mb-1 text-on-surface-variant font-weight-bold"
                active-class="bg-primary text-on-primary shadow-nav"
                color="primary"
              >
                <template v-slot:append>
                  <v-chip
                    size="x-small"
                    color="surface-container-highest"
                    class="text-on-surface-variant font-weight-bold ml-2"
                    >RPA</v-chip
                  >
                </template>
              </v-list-item>
            </template>

            <div class="pl-8 pt-1 pb-2">
              <v-list-item
                to="/learning?category=hmong"
                title="Overview"
                class="nav-subitem rounded text-on-surface-variant"
                density="compact"
                :active="$route.query.category === 'hmong'"
                active-class="bg-surface-container text-on-surface font-weight-bold"
              ></v-list-item>
              <v-list-item
                to="/learning/hmong-study"
                title="Study Begin"
                class="nav-subitem rounded text-on-surface-variant"
                density="compact"
                :active="$route.path === '/learning/hmong-study'"
                active-class="bg-surface-container text-on-surface font-weight-bold"
              ></v-list-item>
              <v-list-item
                to="/learning?open=h1"
                title="Flipbook & Read"
                class="nav-subitem rounded text-on-surface-variant"
                density="compact"
              ></v-list-item>
              <v-list-item
                to="/learning?category=hmong-video"
                title="Video Learning"
                class="nav-subitem rounded text-on-surface-variant"
                density="compact"
                :active="$route.query.category === 'hmong-video'"
                active-class="bg-surface-container text-on-surface font-weight-bold"
              ></v-list-item>
            </div>
          </v-list-group>

          <v-list-item
            to="/learning?category=lao"
            prepend-icon="mdi-earth"
            title="Lao (ພາສາລາວ)"
            rounded="lg"
            class="nav-item mb-1 text-on-surface-variant font-weight-bold"
            :active="$route.query.category === 'lao'"
            active-class="bg-primary text-on-primary shadow-nav"
          >
            <template v-slot:append>
              <span class="text-caption text-on-surface-variant ml-2">ສຽງ</span>
            </template>
          </v-list-item>

          <v-list-item
            to="/learning?category=english"
            prepend-icon="mdi-alphabet-latin"
            title="English (Lus Askiv)"
            rounded="lg"
            class="nav-item mb-1 text-on-surface-variant font-weight-bold"
            :active="$route.query.category === 'english'"
            active-class="bg-primary text-on-primary shadow-nav"
          >
            <template v-slot:append>
              <span class="text-caption text-on-surface-variant ml-2">ESL</span>
            </template>
          </v-list-item>

          <v-divider class="my-4 mx-2 bg-surface-container-highest"></v-divider>

          <!-- Practice & Explore -->
          <v-list-subheader
            class="text-caption font-weight-bold text-uppercase text-on-surface-variant tracking-widest px-2 mb-1"
          >
            Practice & Explore
          </v-list-subheader>

          <v-list-item
            to="/learning/vocabulary"
            prepend-icon="mdi-book-open-page-variant"
            title="Vocabulary Hub (A-Z)"
            rounded="lg"
            class="nav-item mb-1 text-on-surface-variant font-weight-bold"
            active-class="bg-primary text-on-primary shadow-nav"
          ></v-list-item>

          <v-list-item
            to="/learning/flipbook"
            prepend-icon="mdi-book-open-page-variant-outline"
            title="Flipbook"
            rounded="lg"
            class="nav-item mb-1 text-on-surface-variant font-weight-bold"
            active-class="bg-primary text-on-primary shadow-nav"
          ></v-list-item>

          <v-list-item
            to="/learning/audio"
            prepend-icon="mdi-volume-high"
            title="Audio Soundboard"
            rounded="lg"
            class="nav-item mb-1 text-on-surface-variant font-weight-bold"
            active-class="bg-primary text-on-primary shadow-nav"
          ></v-list-item>

          <v-divider class="my-4 mx-2 bg-surface-container-highest"></v-divider>

          <!-- Administration -->
          <v-list-subheader
            class="text-caption font-weight-bold text-uppercase text-on-surface-variant tracking-widest px-2 mb-1"
          >
            Administration
          </v-list-subheader>

          <v-list-item
            to="/learning/manage"
            prepend-icon="mdi-cog"
            title="Admin Control"
            rounded="lg"
            class="nav-item mb-1 text-on-surface-variant font-weight-bold"
            active-class="bg-primary text-on-primary shadow-nav"
          ></v-list-item>

          <v-list-item
            to="/"
            prepend-icon="mdi-arrow-left"
            title="Back to Dashboard"
            rounded="lg"
            class="nav-item mb-1 text-on-surface-variant font-weight-bold mt-4"
          ></v-list-item>
        </v-list>
      </div>
    </v-navigation-drawer>

    <!-- Top App Bar -->
    <v-app-bar
      elevation="0"
      height="80"
      class="bg-surface px-4 border-b border-surface-container-highest"
      style="backdrop-filter: blur(20px)"
    >
      <div class="d-flex align-center w-100 gap-4">
        <!-- Dialect Toggle & Search -->
        <div class="d-flex align-center flex-1 max-w-xl gap-4">
          <!-- <div class="flex-1 position-relative">
            <v-text-field
              variant="solo"
              density="compact"
              placeholder="Search Hmong, Lao, English..."
              prepend-inner-icon="mdi-magnify"
              hide-details
              bg-color="surface-container-lowest"
              class="search-input"
            ></v-text-field>
          </div> -->
        </div>

        <v-spacer></v-spacer>

        <!-- Stats & Profile -->
        <div class="d-flex align-center gap-4">
          <div class="d-flex align-center gap-2 ml-2">
            <div class="text-right d-none d-sm-block">
              <div class="text-body-2 font-weight-bold text-on-surface lh-1">
                Xeeb kwm vaj
              </div>
              <div class="text-caption text-on-surface-variant">
                Level 4 • Scholar
              </div>
            </div>
            <v-avatar
              size="36"
              class="border"
              style="border-color: rgba(26, 54, 93, 0.2) !important"
            >
              <v-img
                src="https://lh3.googleusercontent.com/aida/AEtjO1Wa4L33VLcyPCnUg9y2gWbzJQKfJNgOfhMH9aLiK5ppHMjI3QmrpUv68puG6bL8w6tp2pOwClkzVMBg5qUSIo8ZNp6ZIhQDM8qUhzFeN2dA65vxfURQfZYe03Bvoushqnxr5fWWkt2c4PO8QTtscUfF3fgdQwCFjczp00lis9t3o4F_1zyLgPouIdHGn7DV2NGHtYH55poDJm4woMhTep_0Wob_E3Zczu7DJkTzWKbPmmLovYIgZYHlAfw"
              ></v-img>
            </v-avatar>
          </div>
        </div>
      </div>
    </v-app-bar>

    <!-- Main Content Area -->
    <v-main class="bg-surface">
      <div class="page-content-wrapper">
        <slot />
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from "vue";
const drawer = ref(true);
</script>

<style scoped>
.nav-item {
  transition: all 0.2s ease;
}

.nav-item:hover:not(.v-list-item--active) {
  background: var(--v-theme-surface-container) !important;
  color: var(--v-theme-on-surface) !important;
}

.nav-subitem:hover {
  background: var(--v-theme-surface-container) !important;
  color: var(--v-theme-on-surface) !important;
}

.shadow-nav {
  box-shadow: 0 3px 0px #00132b !important;
}

.tracking-widest {
  letter-spacing: 0.1em;
}

.lh-1 {
  line-height: 1.1;
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
</style>
