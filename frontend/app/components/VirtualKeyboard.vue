<template>
  <div class="virtual-keyboard-container my-4 d-flex flex-column align-center" translate="no">
    
    <!-- Hands Graphic Guide -->
    <svg v-if="showHands" viewBox="0 0 500 260" class="hands-svg mb-4" width="100%" max-width="400">
      <!-- Left Hand -->
      <!-- Palm -->
      <rect x="50" y="150" width="130" height="90" rx="30" fill="rgba(255,255,255,0.05)" stroke="#475569" stroke-width="2"/>
      <!-- Fingers -->
      <rect x="50" y="100" width="25" height="80" rx="12" :fill="activeFinger === 'lp' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <rect x="85" y="70" width="25" height="110" rx="12" :fill="activeFinger === 'lr' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <rect x="120" y="50" width="25" height="130" rx="12" :fill="activeFinger === 'lm' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <rect x="155" y="70" width="25" height="110" rx="12" :fill="activeFinger === 'li' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <!-- Thumb -->
      <rect x="155" y="160" width="25" height="70" rx="12" transform="rotate(-45 155 160)" :fill="activeFinger === 'th' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />

      <!-- Right Hand -->
      <!-- Palm -->
      <rect x="320" y="150" width="130" height="90" rx="30" fill="rgba(255,255,255,0.05)" stroke="#475569" stroke-width="2"/>
      <!-- Fingers -->
      <rect x="320" y="70" width="25" height="110" rx="12" :fill="activeFinger === 'ri' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <rect x="355" y="50" width="25" height="130" rx="12" :fill="activeFinger === 'rm' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <rect x="390" y="70" width="25" height="110" rx="12" :fill="activeFinger === 'rr' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <rect x="425" y="100" width="25" height="80" rx="12" :fill="activeFinger === 'rp' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
      <!-- Thumb -->
      <rect x="320" y="160" width="25" height="70" rx="12" transform="rotate(45 320 160)" :fill="activeFinger === 'th' ? '#3b82f6' : 'rgba(255,255,255,0.05)'" stroke="#475569" stroke-width="2" class="finger-anim" />
    </svg>

    <!-- Keyboard Base -->
    <div class="keyboard-base pa-4 rounded-xl elevation-4">
      
      <!-- Row 1 -->
      <div class="keyboard-row">
        <div v-for="(key, i) in row1" :key="'r1-'+i" :class="getKeyClass(key)" class="key-cap" :style="getHeatmapStyle(key)">
          <div v-if="!key.isSpecial && key.shift !== key.base" class="key-shift">{{ key.shift }}</div>
          <div class="key-base" :class="{'text-subtitle-2': key.isSpecial}">{{ key.base }}</div>
        </div>
      </div>

      <!-- Row 2 -->
      <div class="keyboard-row">
        <div v-for="(key, i) in row2" :key="'r2-'+i" :class="getKeyClass(key)" class="key-cap" :style="getHeatmapStyle(key)">
          <div v-if="!key.isSpecial && key.shift !== key.base" class="key-shift">{{ key.shift }}</div>
          <div class="key-base" :class="{'text-subtitle-2': key.isSpecial}">{{ key.base }}</div>
        </div>
      </div>

      <!-- Row 3 -->
      <div class="keyboard-row">
        <div v-for="(key, i) in row3" :key="'r3-'+i" :class="getKeyClass(key)" class="key-cap" :style="getHeatmapStyle(key)">
          <div v-if="!key.isSpecial && key.shift !== key.base" class="key-shift">{{ key.shift }}</div>
          <div class="key-base" :class="{'text-subtitle-2': key.isSpecial}">{{ key.base }}</div>
        </div>
      </div>

      <!-- Row 4 -->
      <div class="keyboard-row">
        <div v-for="(key, i) in row4" :key="'r4-'+i" :class="getKeyClass(key)" class="key-cap" :style="getHeatmapStyle(key)">
          <div v-if="!key.isSpecial && key.shift !== key.base" class="key-shift">{{ key.shift }}</div>
          <div class="key-base" :class="{'text-subtitle-2': key.isSpecial}">{{ key.base }}</div>
        </div>
      </div>
      
      <!-- Row 5 (Spacebar) -->
      <div class="keyboard-row">
        <div class="key-cap width-medium key-special"><div class="key-base text-subtitle-2">Ctrl</div></div>
        <div class="key-cap width-medium key-special"><div class="key-base text-subtitle-2">Win</div></div>
        <div class="key-cap width-medium key-special"><div class="key-base text-subtitle-2">Alt</div></div>
        <div :class="getKeyClass({base: ' ', finger: 'th'})" class="key-cap width-spacebar">
          <div class="key-base"></div>
        </div>
        <div class="key-cap width-medium key-special"><div class="key-base text-subtitle-2">Alt</div></div>
        <div class="key-cap width-medium key-special"><div class="key-base text-subtitle-2">Win</div></div>
        <div class="key-cap width-medium key-special"><div class="key-base text-subtitle-2">Ctrl</div></div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  targetChar: {
    type: String,
    default: ''
  },
  errorMap: {
    type: Object,
    default: () => ({})
  },
  showHeatmap: {
    type: Boolean,
    default: false
  },
  showHands: {
    type: Boolean,
    default: true
  }
});

// Standard English QWERTY Keyboard Mapping
const row1 = [
  { base: '`', shift: '~', finger: 'lp' }, { base: '1', shift: '!', finger: 'lp' }, { base: '2', shift: '@', finger: 'lp' }, { base: '3', shift: '#', finger: 'lr' },
  { base: '4', shift: '$', finger: 'lm' }, { base: '5', shift: '%', finger: 'li' }, { base: '6', shift: '^', finger: 'ri' }, { base: '7', shift: '&', finger: 'ri' },
  { base: '8', shift: '*', finger: 'rm' }, { base: '9', shift: '(', finger: 'rr' }, { base: '0', shift: ')', finger: 'rp' }, { base: '-', shift: '_', finger: 'rp' },
  { base: '=', shift: '+', finger: 'rp' }, { base: 'Backspace', isSpecial: true, width: 'wide', finger: 'rp' }
];

const row2 = [
  { base: 'Tab', isSpecial: true, width: 'medium', finger: 'lp' },
  { base: 'q', shift: 'Q', finger: 'lp' }, { base: 'w', shift: 'W', finger: 'lr' }, { base: 'e', shift: 'E', finger: 'lm' }, { base: 'r', shift: 'R', finger: 'li' },
  { base: 't', shift: 'T', finger: 'li' }, { base: 'y', shift: 'Y', finger: 'ri' }, { base: 'u', shift: 'U', finger: 'ri' }, { base: 'i', shift: 'I', finger: 'rm' },
  { base: 'o', shift: 'O', finger: 'rr' }, { base: 'p', shift: 'P', finger: 'rp' }, { base: '[', shift: '{', finger: 'rp' }, { base: ']', shift: '}', finger: 'rp' },
  { base: '\\', shift: '|', width: 'medium', finger: 'rp' }
];

const row3 = [
  { base: 'Caps Lock', isSpecial: true, width: 'wide', finger: 'lp' },
  { base: 'a', shift: 'A', finger: 'lp' }, { base: 's', shift: 'S', finger: 'lr' }, { base: 'd', shift: 'D', finger: 'lm' }, { base: 'f', shift: 'F', finger: 'li' },
  { base: 'g', shift: 'G', finger: 'li' }, { base: 'h', shift: 'H', finger: 'ri' }, { base: 'j', shift: 'J', finger: 'ri' }, { base: 'k', shift: 'K', finger: 'rm' },
  { base: 'l', shift: 'L', finger: 'rr' }, { base: ';', shift: ':', finger: 'rp' }, { base: "'", shift: '\"', finger: 'rp' },
  { base: 'Enter', isSpecial: true, width: 'wide', finger: 'rp' }
];

const row4 = [
  { base: 'Shift', isSpecial: true, width: 'extra-wide', isShift: true, finger: 'lp' },
  { base: 'z', shift: 'Z', finger: 'lp' }, { base: 'x', shift: 'X', finger: 'lr' }, { base: 'c', shift: 'C', finger: 'lm' }, { base: 'v', shift: 'V', finger: 'li' },
  { base: 'b', shift: 'B', finger: 'li' }, { base: 'n', shift: 'N', finger: 'ri' }, { base: 'm', shift: 'M', finger: 'ri' }, { base: ',', shift: '<', finger: 'rm' },
  { base: '.', shift: '>', finger: 'rr' }, { base: '/', shift: '?', finger: 'rp' },
  { base: 'Shift', isSpecial: true, width: 'wide', isShift: true, finger: 'rp' }
];

const needsShift = computed(() => {
  if (!props.targetChar) return false;
  
  const allKeys = [...row1, ...row2, ...row3, ...row4];
  for (const key of allKeys) {
    if (!key.isSpecial && key.shift === props.targetChar && key.base !== props.targetChar) {
      return true;
    }
  }
  return false;
});

const activeFinger = computed(() => {
  if (!props.targetChar) return null;
  if (props.targetChar === ' ') return 'th';

  const allKeys = [...row1, ...row2, ...row3, ...row4];
  for (const key of allKeys) {
    if (!key.isSpecial && (key.base === props.targetChar || key.shift === props.targetChar)) {
      return key.finger;
    }
  }
  return null;
});

const getHeatmapStyle = (key) => {
  if (!props.showHeatmap) return {};
  
  const errors = (props.errorMap[key.base] || 0) + (props.errorMap[key.shift] || 0);
  
  if (errors > 5) return { backgroundColor: 'rgba(239, 68, 68, 0.8)', borderColor: '#b91c1c' };
  if (errors > 2) return { backgroundColor: 'rgba(239, 68, 68, 0.5)', borderColor: '#ef4444' };
  if (errors > 0) return { backgroundColor: 'rgba(239, 68, 68, 0.2)', borderColor: '#f87171' };
  
  return {};
};

const getKeyClass = (key) => {
  let classes = [];
  
  if (key.width === 'wide') classes.push('width-wide');
  else if (key.width === 'extra-wide') classes.push('width-extra-wide');
  else if (key.width === 'medium') classes.push('width-medium');
  else classes.push('width-regular');

  if (key.isSpecial) classes.push('key-special');

  if (!props.showHeatmap) {
    if (key.base === props.targetChar || (!key.isSpecial && key.shift === props.targetChar)) {
      classes.push('key-highlight-target');
    }

    if (needsShift.value && key.isShift) {
      classes.push('key-highlight-shift');
    }
  }

  return classes.join(' ');
};

</script>

<style scoped>
.virtual-keyboard-container {
  width: 100%;
}

.hands-svg {
  max-width: 300px;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
}

.finger-anim {
  transition: fill 0.2s ease-in-out;
}

.keyboard-base {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.06), 0 0 1px 1px rgba(255, 255, 255, 0.9) inset;
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 12px !important;
  border-radius: 20px;
}

.keyboard-row {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-bottom: 5px;
}

.key-cap {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  color: #334155;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  height: 44px;
  font-family: sans-serif;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
  box-shadow: 0 3px 0 #cbd5e1, 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.key-cap:active {
  transform: translateY(2px);
  box-shadow: 0 1px 0 #cbd5e1, 0 2px 3px -1px rgba(0, 0, 0, 0.05);
}

.key-shift {
  font-size: 0.8em;
  color: #94a3b8;
  position: absolute;
  top: 4px;
  left: 6px;
}

.key-base {
  font-size: 1.05em;
  font-weight: 700;
  color: #1e293b;
}

.key-special {
  background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #64748b;
  border-color: #cbd5e1;
}

.key-highlight-target {
  background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
  color: #ffffff !important;
  border-color: #4338ca !important;
  box-shadow: 0 2px 0 #312e81, 0 0 16px rgba(99, 102, 241, 0.6) !important;
  transform: translateY(2px);
}

.key-highlight-target .key-base,
.key-highlight-target .key-shift {
  color: #ffffff !important;
}

.key-highlight-shift {
  background: linear-gradient(135deg, #f59e0b, #d97706) !important;
  border-color: #b45309 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 0 #78350f, 0 0 16px rgba(245, 158, 11, 0.6) !important;
  transform: translateY(2px);
}

.key-highlight-shift .key-base,
.key-highlight-shift .key-shift {
  color: #ffffff !important;
}

.width-regular { width: 40px; }
.width-medium { width: 60px; }
.width-wide { width: 75px; }
.width-extra-wide { width: 95px; }
.width-spacebar { width: 260px; }

@media (max-width: 768px) {
  .key-cap {
    height: 32px;
  }
  .width-regular { width: 26px; }
  .width-medium { width: 40px; }
  .width-wide { width: 50px; }
  .width-extra-wide { width: 60px; }
  .width-spacebar { width: 160px; }
  .key-base { font-size: 0.8rem; }
  .key-shift { font-size: 0.55rem; }
}
</style>
