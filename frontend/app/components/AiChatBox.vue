<template>
  <div class="ai-chat-widget" :style="isFullScreen ? 'bottom: 0; right: 0;' : 'bottom: 24px; right: 24px;'">
    <!-- Floating Action Button -->
    <v-btn
      v-if="!isOpen"
      icon="mdi-robot"
      color="primary"
      size="x-large"
      class="fab-button elevation-4"
      @click="isOpen = true"
    ></v-btn>

    <!-- Chat Box -->
    <v-expand-transition>
      <v-card v-if="isOpen" :class="['chat-card elevation-10 d-flex flex-column', isFullScreen ? 'rounded-0' : 'rounded-xl']" :width="isFullScreen ? '100vw' : '350'" :height="isFullScreen ? '100vh' : '500'">
        <!-- Header -->
        <v-toolbar color="primary" density="compact" class="flex-grow-0 px-2" :class="isFullScreen ? '' : 'rounded-t-xl'">
          <v-icon icon="mdi-robot-outline" class="mr-2"></v-icon>
          <v-toolbar-title class="text-subtitle-1 font-weight-bold">AI Assistant</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn :icon="isFullScreen ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'" variant="text" size="small" @click="isFullScreen = !isFullScreen"></v-btn>
          <v-btn icon="mdi-close" variant="text" size="small" @click="isOpen = false"></v-btn>
        </v-toolbar>

        <!-- Messages Area -->
        <v-card-text class="messages-area flex-grow-1 overflow-y-auto pa-4 d-flex flex-column" ref="messagesContainer" @click="handleMessageClick">
          <div v-if="messages.length === 0" class="text-center text-caption text-grey mt-4">
            Hello! How can I help you today?
          </div>
          
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="['message-wrapper mb-3 d-flex', msg.role === 'user' ? 'justify-end' : 'justify-start']"
          >
            <div
              :class="[
                'message-bubble pa-3 rounded-xl text-body-2',
                msg.role === 'user' ? 'bg-primary text-white rounded-tr-sm' : 'bg-grey-lighten-3 text-black rounded-tl-sm'
              ]"
              style="max-width: 85%;"
              v-html="parseMessage(msg.content)"
            >
            </div>
          </div>

          <div v-if="isLoading" class="message-wrapper mb-3 d-flex justify-start">
            <div class="message-bubble pa-3 rounded-xl bg-grey-lighten-3 text-black rounded-tl-sm d-flex align-center">
               <v-progress-circular indeterminate size="20" width="2" class="mr-2"></v-progress-circular>
               <span class="text-caption">Typing...</span>
            </div>
          </div>
        </v-card-text>

        <!-- Input Area -->
        <v-divider></v-divider>
        <v-card-actions class="pa-2 px-3 bg-grey-lighten-4 rounded-b-xl flex-grow-0">
          <v-text-field
            ref="chatInputRef"
            v-model="input"
            placeholder="Type a message..."
            variant="solo"
            density="compact"
            hide-details
            rounded
            class="mr-2"
            @keyup.enter="sendMessage"
            :disabled="isLoading"
          ></v-text-field>
          <v-btn
            icon="mdi-send"
            color="primary"
            variant="tonal"
            size="small"
            @click="sendMessage"
            :disabled="!input.trim() || isLoading"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-expand-transition>

    <!-- Image Viewer Dialog -->
    <v-dialog v-model="isImageDialogOpen" fullscreen transition="dialog-bottom-transition" z-index="10000">
      <v-card class="bg-black d-flex flex-column">
        <v-toolbar color="rgba(0,0,0,0.5)" theme="dark" density="compact" class="flex-grow-0" style="position: absolute; top: 0; width: 100%; z-index: 1;">
          <v-spacer></v-spacer>
          <v-btn icon="mdi-download" @click="downloadImage"></v-btn>
          <v-btn icon="mdi-close" @click="isImageDialogOpen = false"></v-btn>
        </v-toolbar>
        <v-img :src="selectedImage" class="flex-grow-1" style="height: 100vh;" contain></v-img>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue';

const isOpen = ref(false);
const isFullScreen = ref(false);
const input = ref('');
const messages = ref([]);
const isLoading = ref(false);
const messagesContainer = ref(null);
const chatInputRef = ref(null);

const isImageDialogOpen = ref(false);
const selectedImage = ref('');

watch(isOpen, async (newVal) => {
  if (newVal) {
    await nextTick();
    if (chatInputRef.value) {
      chatInputRef.value.focus();
    }
  }
});

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.$el.scrollTop = messagesContainer.value.$el.scrollHeight;
  }
};

const parseMessage = (text) => {
  if (!text) return '';
  // Convert markdown image ![alt](url) to HTML <img>
  let html = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width: 100%; border-radius: 8px; margin-top: 8px; cursor: pointer;" class="chat-image" />');
  // Convert markdown bold **text** to <strong>text</strong>
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // Convert newlines to <br/>
  html = html.replace(/\n/g, '<br/>');
  return html;
};

const handleMessageClick = (e) => {
  if (e.target && e.target.tagName === 'IMG' && e.target.classList.contains('chat-image')) {
    selectedImage.value = e.target.src;
    isImageDialogOpen.value = true;
  }
};

const downloadImage = async () => {
  try {
    const response = await fetch(selectedImage.value);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ai-image-${Date.now()}.png`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (err) {
    window.open(selectedImage.value, '_blank');
  }
};

const sendMessage = async () => {
  if (!input.value.trim() || isLoading.value) return;

  const userText = input.value.trim();
  messages.value.push({ role: 'user', content: userText });
  input.value = '';
  scrollToBottom();

  isLoading.value = true;

  try {
    const response = await fetch('http://localhost:3005/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages: messages.value }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Failed to get response from AI');
    }

    const data = await response.json();
    messages.value.push({ role: 'model', content: data.message });
  } catch (error) {
    console.error(error);
    messages.value.push({ role: 'model', content: error.message || 'Oops! Something went wrong communicating with the AI.' });
  } finally {
    isLoading.value = false;
    scrollToBottom();
    await nextTick();
    if (chatInputRef.value) {
      chatInputRef.value.focus();
    }
  }
};
</script>

<style scoped>
.ai-chat-widget {
  position: fixed;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.fab-button {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.fab-button:hover {
  transform: scale(1.1);
}

.chat-card {
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.2) !important;
  border: 1px solid rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(10px);
}

.messages-area {
  background-color: #fafafa;
}

.message-bubble {
  word-break: break-word;
  white-space: pre-wrap;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>
