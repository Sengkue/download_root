<template>
  <div :class="['page-container', { 'full-screen-page': isFullScreenChat }]">
    <div :class="['chat-container', { 'full-screen-chat': isFullScreenChat }]">
      <div class="chat-header">
        <div class="d-flex align-center" style="gap: 15px;">
          <div class="avatar">🤖</div>
          <div class="header-info">
            <h1>AI Assistant</h1>
            <p><span class="status-dot"></span> ພ້ອມໃຫ້ບໍລິການແລ້ວ</p>
          </div>
        </div>
        <div style="flex-grow: 1"></div>
        <v-btn
          :icon="isFullScreenChat ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'"
          variant="text"
          color="white"
          @click="isFullScreenChat = !isFullScreenChat"
        ></v-btn>
      </div>

      <div class="chat-messages" ref="messagesContainer" @click="handleMessageClick">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role === 'user' ? 'user' : 'bot']"
          v-html="msg.content"
        ></div>

        <div class="typing-indicator" v-if="isTyping">
          <span></span><span></span><span></span>
        </div>
      </div>

      <div class="chat-input-container">
        <input
          type="text"
          v-model="inputMessage"
          @keypress.enter="sendMessage"
          class="chat-input"
          placeholder="ພິມຂໍ້ຄວາມຂອງທ່ານບ່ອນນີ້..."
          autocomplete="off"
          autofocus
        />
        <button
          class="send-btn"
          @click="sendMessage"
          :disabled="!inputMessage.trim() || isTyping"
        >
          <svg viewBox="0 0 24 24">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Image Viewer Dialog -->
    <v-dialog v-model="isImageDialogOpen" fullscreen transition="dialog-bottom-transition" z-index="10000">
      <v-card class="bg-black d-flex flex-column">
        <v-toolbar color="rgba(0,0,0,0.5)" theme="dark" density="compact" class="flex-grow-0" style="position: absolute; top: 0; width: 100%; z-index: 1;">
          <v-spacer></v-spacer>
          <v-btn icon="mdi-download" @click="downloadSelectedImage"></v-btn>
          <v-btn icon="mdi-close" @click="isImageDialogOpen = false"></v-btn>
        </v-toolbar>
        <v-img :src="selectedImage" class="flex-grow-1" style="height: 100vh;" contain></v-img>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";

const config = useRuntimeConfig();
const OPENROUTER_API_KEY = config.public.openRouterApiKey;

const messages = ref([
  {
    role: "bot",
    content:
      "ສະບາຍດີ! ຂ້ອຍແມ່ນ AI Assistant. ມີຫຍັງໃຫ້ຂ້ອຍຊ່ວຍມື້ນີ້ບໍ່? (ພິມເປັນພາສາລາວໄດ້ເລີຍ)",
  },
]);
const chatHistory = [];
const inputMessage = ref("");
const isTyping = ref(false);
const messagesContainer = ref(null);

const isFullScreenChat = ref(false);
const isImageDialogOpen = ref(false);
const selectedImage = ref("");
const selectedPrompt = ref("");

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const downloadImage = async (url, filename) => {
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = `AI_Image_${filename.replace(/[^a-z0-9]/gi, "_").toLowerCase()}.jpg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(blobUrl);
  } catch (e) {
    window.open(url, "_blank");
  }
};

const downloadSelectedImage = () => {
  if (selectedImage.value) {
    downloadImage(selectedImage.value, selectedPrompt.value || 'download');
  }
};

const handleMessageClick = (e) => {
  if (e.target && e.target.tagName === 'IMG' && e.target.classList.contains('chat-image')) {
    selectedImage.value = e.target.src;
    selectedPrompt.value = e.target.getAttribute('data-prompt') || 'image';
    isImageDialogOpen.value = true;
  }
};

const sendMessage = async () => {
  const text = inputMessage.value.trim();
  if (!text || isTyping.value) return;

  // 1. Add user message to UI
  messages.value.push({ role: "user", content: text.replace(/\n/g, "<br>") });
  inputMessage.value = "";

  // 2. Add to history
  chatHistory.push({ role: "user", content: text });

  // 3. Show typing indicator
  isTyping.value = true;
  scrollToBottom();

    // Image command check
  const isImageCommand =
    text.toLowerCase().startsWith("/image ") ||
    text.startsWith("ແຕ້ມຮູບ ") ||
    text.startsWith("ຮູບ ");

  if (isImageCommand) {
    const promptText = text.replace(/^\/image |^ແຕ້ມຮູບ |^ຮູບ /i, "").trim();
    const encodedPrompt = encodeURIComponent(promptText);
    const imageUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=800&height=800&nologo=true`;

    // Instantly add the loading UI to the chat
    isTyping.value = false;
    const loaderId = 'loader-' + Date.now();
    const imgHtml = `ນີ້ຄືຮູບພາບທີ່ທ່ານສັ່ງ:<br><br>
          <div style="position: relative; display: inline-block; min-height: 250px; min-width: 250px; background: rgba(0,0,0,0.2); border-radius: 12px; text-align: center;">
              <div id="${loaderId}" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; gap: 12px; pointer-events: none;">
                  <svg viewBox="0 0 50 50" style="width: 40px; height: 40px; animation: spin 1s linear infinite;">
                      <circle cx="25" cy="25" r="20" fill="none" stroke-width="4" stroke="#3b82f6" stroke-dasharray="90 150" stroke-dashoffset="0" style="stroke-linecap: round;"></circle>
                  </svg>
                  <span style="color: #94a3b8; font-size: 13px; font-weight: 500;">ກຳລັງແຕ້ມຮູບ...</span>
              </div>
              <img src="${imageUrl}" class="chat-image" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); cursor: pointer; transition: transform 0.2s, opacity 0.5s; opacity: 0;" alt="${promptText}" data-prompt="${promptText}" title="ຄລິກເພື່ອເບິ່ງຮູບເຕັມ" 
              onload="this.style.opacity='1'; document.getElementById('${loaderId}').style.display='none'; this.parentElement.style.background='transparent'; this.parentElement.parentElement.parentElement.scrollTop = this.parentElement.parentElement.parentElement.scrollHeight;" 
              onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
              <div style="position: absolute; bottom: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 5px 10px; border-radius: 20px; color: white; font-size: 12px; pointer-events: none; display: flex; align-items: center; gap: 5px;">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg> ເບິ່ງຮູບເຕັມ
              </div>
          </div>
          <style>@keyframes spin { 100% { transform: rotate(360deg); } }</style>`;
    
    messages.value.push({ role: "bot", content: imgHtml });
    chatHistory.push({ role: "assistant", content: "[ສົ່ງຮູບພາບແລ້ວ]" });
    scrollToBottom();
    return;
  }

  try {
    // 4. Call API
    const response = await fetch(
      "https://openrouter.ai/api/v1/chat/completions",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${OPENROUTER_API_KEY}`,
          "Content-Type": "application/json",
          "HTTP-Referer": "http://localhost",
          "X-Title": "Qwen Local Web Chat",
        },
        body: JSON.stringify({
          model: "openrouter/free",
          messages: chatHistory,
        }),
      },
    );

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    const data = await response.json();
    const reply = data.choices[0].message.content;

    // 5. Add bot reply to UI & history
    isTyping.value = false;
    messages.value.push({ role: "bot", content: reply.replace(/\n/g, "<br>") });
    chatHistory.push({ role: "assistant", content: reply });
    scrollToBottom();
  } catch (err) {
    isTyping.value = false;
    messages.value.push({
      role: "bot",
      content: `❌ ຂໍອະໄພ, ເກີດຂໍ້ຜິດພາດ: ${err.message}`,
    });
    scrollToBottom();
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Noto+Sans+Lao:wght@300;400;500;600&display=swap");

.page-container {
  --bg-color: #0f172a;
  --chat-bg: #1e293b;
  --primary: #3b82f6;
  --primary-hover: #2563eb;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --user-msg: #3b82f6;
  --bot-msg: #334155;
  --border: #334155;

  font-family: "Inter", "Noto Sans Lao", sans-serif;
  background-color: var(--bg-color);
  color: var(--text-main);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: radial-gradient(circle at top right, #1e1b4b, #0f172a);
  padding: 20px;
}

.chat-container {
  width: 100%;
  max-width: 900px;
  height: 90vh;
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(12px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  transition: all 0.3s ease;
}

.chat-container.full-screen-chat {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  max-width: 100vw;
  height: 100vh;
  border-radius: 0;
  border: none;
  z-index: 9999;
}

.page-container.full-screen-page {
  padding: 0;
}

.chat-header {
  padding: 20px 30px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(30, 41, 59, 0.8);
}

.avatar {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
}

.header-info h1 {
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin: 0;
}

.header-info p {
  font-size: 0.85rem;
  color: var(--primary);
  display: flex;
  align-items: center;
  gap: 5px;
  margin: 0;
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 8px #10b981;
}

.chat-messages {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  scroll-behavior: smooth;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}
.chat-messages::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 3px;
}

.message {
  max-width: 80%;
  padding: 15px 20px;
  border-radius: 20px;
  line-height: 1.6;
  font-size: 0.95rem;
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-bottom-right-radius: 4px;
  box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
}

.message.bot {
  align-self: flex-start;
  background: var(--bot-msg);
  border-bottom-left-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.typing-indicator {
  align-self: flex-start;
  background: var(--bot-msg);
  padding: 15px 20px;
  border-radius: 20px;
  border-bottom-left-radius: 4px;
  display: flex;
  gap: 5px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: var(--text-muted);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}
.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.chat-input-container {
  padding: 20px 30px;
  background: rgba(30, 41, 59, 0.9);
  border-top: 1px solid var(--border);
  display: flex;
  gap: 15px;
}

.chat-input {
  flex: 1;
  background: #0f172a;
  border: 1px solid var(--border);
  padding: 15px 25px;
  border-radius: 30px;
  color: white;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
  transition: all 0.3s ease;
}

.chat-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.send-btn {
  background: var(--primary);
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.send-btn:hover {
  background: var(--primary-hover);
  transform: scale(1.05);
}

.send-btn:disabled {
  background: var(--border);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.send-btn svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  transform: translateX(-2px);
}
</style>
