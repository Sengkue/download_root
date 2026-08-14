<template>
  <div class="virtual-keyboard-container my-4 d-flex flex-column align-center" translate="no">
    
    <!-- Hands Graphic Guide -->
    <svg viewBox="0 0 500 260" class="hands-svg mb-4" width="100%" max-width="400">
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
  }
});

// Accurate Standard Lao Keyboard Mapping (Kedmanee)
const row1 = [
  { base: '*', shift: '?', finger: 'lp' }, { base: 'ຢ', shift: '1', finger: 'lp' }, { base: 'ຟ', shift: '2', finger: 'lp' }, { base: 'ໂ', shift: '3', finger: 'lr' },
  { base: 'ຖ', shift: '4', finger: 'lm' }, { base: 'ຸ', shift: '໌', finger: 'li' }, { base: 'ູ', shift: 'ຼ', finger: 'ri' }, { base: 'ຄ', shift: '5', finger: 'ri' },
  { base: 'ຕ', shift: '6', finger: 'rm' }, { base: 'ຈ', shift: '7', finger: 'rr' }, { base: 'ຂ', shift: '8', finger: 'rp' }, { base: 'ຊ', shift: '9', finger: 'rp' },
  { base: 'ໍ', shift: '0', finger: 'rp' }, { base: 'Backspace', isSpecial: true, width: 'wide', finger: 'rp' }
];

const row2 = [
  { base: 'Tab', isSpecial: true, width: 'medium', finger: 'lp' },
  { base: 'ົ', shift: 'ັ', finger: 'lp' }, { base: 'ໄ', shift: 'ໝ', finger: 'lp' }, { base: 'ຳ', shift: 'ໜ', finger: 'lr' }, { base: 'ພ', shift: 'ຣ', finger: 'lm' },
  { base: 'ະ', shift: '໋', finger: 'li' }, { base: 'ິ', shift: 'ຶ', finger: 'ri' }, { base: 'ີ', shift: 'ື', finger: 'ri' }, { base: 'ຮ', shift: 'ໍ', finger: 'rm' },
  { base: 'ນ', shift: 'ຯ', finger: 'rr' }, { base: 'ຍ', shift: 'ໆ', finger: 'rp' }, { base: 'ບ', shift: '-', finger: 'rp' }, { base: 'ລ', shift: '×', finger: 'rp' },
  { base: 'ຫຼ', shift: '÷', width: 'medium', finger: 'rp' }
];

const row3 = [
  { base: 'Caps Lock', isSpecial: true, width: 'wide', finger: 'lp' },
  { base: 'ັ', shift: 'ັ້', finger: 'lp' }, { base: 'ຫ', shift: ';', finger: 'lp' }, { base: 'ກ', shift: '.', finger: 'lr' }, { base: 'ດ', shift: ',', finger: 'lm' },
  { base: 'ເ', shift: ':', finger: 'li' }, { base: '້', shift: '໊', finger: 'ri' }, { base: '່', shift: '໋', finger: 'ri' }, { base: 'າ', shift: '!', finger: 'rm' },
  { base: 'ສ', shift: '?', finger: 'rr' }, { base: 'ວ', shift: '%', finger: 'rp' }, { base: 'ງ', shift: '=', finger: 'rp' },
  { base: 'Enter', isSpecial: true, width: 'wide', finger: 'rp' }
];

const row4 = [
  { base: 'Shift', isSpecial: true, width: 'extra-wide', isShift: true, finger: 'lp' },
  { base: 'ຜ', shift: '"', finger: 'lp' }, { base: 'ປ', shift: '(', finger: 'lp' }, { base: 'ແ', shift: ')', finger: 'lr' }, { base: 'ອ', shift: 'ຊ', finger: 'lm' },
  { base: 'ຶ', shift: 'ຽ', finger: 'li' }, { base: 'ື', shift: '໌', finger: 'ri' }, { base: 'ທ', shift: 'ໝ', finger: 'ri' }, { base: 'ມ', shift: 'ໝ', finger: 'rm' },
  { base: 'ໃ', shift: '$', finger: 'rr' }, { base: 'ຝ', shift: '+', finger: 'rp' },
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
  background: linear-gradient(145deg, #1e293b, #0f172a);
  border: 1px solid #334155;
  box-shadow: 0 15px 35px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.keyboard-row {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 8px;
}

.key-cap {
  background: linear-gradient(to bottom, #334155, #1e293b);
  border: 1px solid #000;
  color: #cbd5e1;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  height: 54px;
  font-family: 'Noto Sans Lao', sans-serif;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.1), 0 3px 0 #000, 0 4px 6px rgba(0,0,0,0.5);
}

.key-cap:active {
  transform: translateY(3px);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.1), 0 0 0 #000, 0 1px 2px rgba(0,0,0,0.5);
}

.key-shift {
  font-size: 0.8em;
  color: #64748b;
  position: absolute;
  top: 6px;
  left: 8px;
}

.key-base {
  font-size: 1.05em;
  font-weight: bold;
}

.key-special {
  background: linear-gradient(to bottom, #1e293b, #0f172a);
  color: #64748b;
}

.key-highlight-target {
  background: linear-gradient(to bottom, #3b82f6, #1d4ed8) !important;
  color: #ffffff !important;
  border-color: #1e3a8a;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.2), 0 1px 0 #000, 0 0 15px rgba(59, 130, 246, 0.6) !important;
  transform: translateY(2px);
}

.key-highlight-shift {
  background: linear-gradient(to bottom, #f59e0b, #b45309) !important;
  border-color: #78350f !important;
  color: #ffffff !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.2), 0 1px 0 #000, 0 0 15px rgba(245, 158, 11, 0.6) !important;
  transform: translateY(2px);
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
