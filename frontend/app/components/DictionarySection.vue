<template>
  <div class="space-y-6 pt-4">
    <div class="d-flex align-center justify-space-between">
      <div class="d-flex align-center gap-3">
        <div class="bg-primary text-on-primary font-weight-bold d-flex align-center justify-center rounded-lg text-h6" style="width: 32px; height: 32px;">
          {{ letter }}
        </div>
        <div>
          <h3 class="text-h6 font-weight-bold text-on-surface mb-0 lh-1">Section {{ letter }} • {{ title }}</h3>
          <p class="text-caption text-on-surface-variant mb-0">{{ count }} entries in this section</p>
        </div>
      </div>
      <a href="#" class="text-caption text-primary font-weight-bold text-decoration-none hover-underline d-none d-sm-inline">
        View all {{ letter }} terms →
      </a>
    </div>

    <v-row>
      <v-col cols="12" md="6" v-for="item in items" :key="item.id">
        <v-card class="bg-surface-container-lowest rounded-xl pa-4 shadow-sm h-100 d-flex flex-column gap-3 card-hover" elevation="0" border>
          <div class="d-flex align-start justify-space-between">
            <div class="d-flex align-center gap-3">
              <div :class="`bg-${item.color}-fixed text-${item.color} d-flex align-center justify-center rounded-xl shadow-sm`" style="width: 48px; height: 48px;">
                <v-icon size="24">{{ item.icon }}</v-icon>
              </div>
              <div>
                <div class="text-caption text-uppercase font-weight-bold text-on-surface-variant tracking-widest lh-1 mb-1">Dictionary Entry</div>
                <h4 class="text-body-1 font-weight-bold text-on-surface lh-1">{{ item.title }}</h4>
              </div>
            </div>
            <v-chip size="x-small" color="surface-container" text-color="on-surface-variant" class="font-weight-bold">{{ item.tag }}</v-chip>
          </div>

          <div class="bg-surface-container-low pa-3 rounded-lg flex-1-1">
            <v-row dense>
              <v-col cols="4" class="d-flex flex-column gap-1">
                <div class="text-caption font-weight-bold text-primary">Hmong RPA</div>
                <div class="text-body-1 font-weight-bold text-primary lh-1">{{ item.hmong.word }}</div>
                <div><v-chip size="x-small" :color="item.hmong.toneColor" :text-color="item.hmong.textToneColor" class="rounded px-1">{{ item.hmong.tone }}</v-chip></div>
              </v-col>
              <v-col cols="4" class="d-flex flex-column gap-1">
                <div class="text-caption font-weight-bold text-tertiary">ພາສາລາວ</div>
                <div class="text-body-1 font-weight-bold text-tertiary lh-1">{{ item.lao.word }}</div>
                <div class="text-caption text-on-surface-variant text-mono">{{ item.lao.sub }}</div>
              </v-col>
              <v-col cols="4" class="d-flex flex-column gap-1">
                <div class="text-caption font-weight-bold text-secondary">English</div>
                <div class="text-body-1 font-weight-bold text-secondary lh-1">{{ item.eng.word }}</div>
                <div class="text-caption text-on-surface-variant text-mono">{{ item.eng.sub }}</div>
              </v-col>
            </v-row>
          </div>

          <div class="d-flex align-center justify-space-between pt-1">
            <p class="text-caption text-on-surface-variant font-italic mb-0">{{ item.context }}</p>
            <v-btn icon size="small" variant="flat" color="surface-container" class="hover-primary-btn text-primary"><v-icon size="small">mdi-volume-high</v-icon></v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
defineProps({
  letter: String,
  title: String,
  count: String,
  items: Array
});
</script>

<style scoped>
.space-y-6 > * + * {
  margin-top: 1.5rem;
}
.gap-3 {
  gap: 0.75rem;
}
.lh-1 {
  line-height: 1.1;
}
.tracking-widest {
  letter-spacing: 0.1em;
}
.text-mono {
  font-family: monospace;
}
.hover-underline:hover {
  text-decoration: underline !important;
}
.card-hover {
  transition: all 0.2s ease;
}
.card-hover:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
  transform: translateY(-2px);
}
.hover-primary-btn {
  transition: all 0.2s ease;
}
.hover-primary-btn:hover {
  background-color: var(--v-theme-primary) !important;
  color: var(--v-theme-on-primary) !important;
}
</style>
