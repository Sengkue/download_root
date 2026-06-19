<template>
  <div class="ai-chat-widget">
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
      <v-card v-if="isOpen" class="chat-card elevation-10 rounded-xl d-flex flex-column" width="350" height="500">
        <!-- Header -->
        <v-toolbar color="primary" density="compact" class="flex-grow-0 px-2 rounded-t-xl">
          <v-icon icon="mdi-robot-outline" class="mr-2"></v-icon>
          <v-toolbar-title class="text-subtitle-1 font-weight-bold">AI Assistant</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" variant="text" size="small" @click="isOpen = false"></v-btn>
        </v-toolbar>

        <!-- Messages Area -->
        <v-card-text class="messages-area flex-grow-1 overflow-y-auto pa-4 d-flex flex-column" ref="messagesContainer">
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
            >
              {{ msg.content }}
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
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue';

const isOpen = ref(false);
const input = ref('');
const messages = ref([]);
const isLoading = ref(false);
const messagesContainer = ref(null);
const chatInputRef = ref(null);

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

const sendMessage = async () => {
  if (!input.value.trim() || isLoading.value) return;

  const userText = input.value.trim();
  messages.value.push({ role: 'user', content: userText });
  input.value = '';
  scrollToBottom();

  isLoading.value = true;

  try {
    const response = await fetch('http://localhost:3001/api/chat', {
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
  bottom: 24px;
  right: 24px;
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
