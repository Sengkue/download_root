<template>
  <div class="login-wrapper">
    <!-- Back to Main Button -->
    <div class="back-btn-container pa-4">
      <v-btn
        prepend-icon="mdi-arrow-left"
        variant="text"
        color="indigo-darken-3"
        size="large"
        class="font-weight-bold"
        to="/"
      >
        Back to Main Layout
      </v-btn>
    </div>

    <v-container class="fill-height d-flex align-center justify-center">
      <v-card
        class="glass-card pa-8 rounded-xl"
        width="100%"
        max-width="450"
        elevation="0"
      >
        <div class="text-center mb-8">
          <div class="brand-icon mx-auto mb-4">
            <v-icon color="white" size="36">mdi-keyboard</v-icon>
          </div>
          <h1 class="text-h4 font-weight-black gradient-text mb-2">
            Typing Master Pro
          </h1>
          <p class="text-subtitle-1 text-medium-emphasis">
            {{
              isLogin
                ? "Welcome back! Ready to type?"
                : "Create an account to track your progress"
            }}
          </p>
        </div>

        <v-form @submit.prevent="handleSubmit" ref="form">
          <v-slide-y-transition>
            <div
              v-if="error"
              class="error-banner mb-6 px-4 py-3 rounded-lg d-flex align-center"
            >
              <v-icon color="red-darken-2" class="mr-2"
                >mdi-alert-circle</v-icon
              >
              <span class="text-red-darken-2 font-weight-medium">{{
                error
              }}</span>
            </div>
          </v-slide-y-transition>

          <v-text-field
            v-if="!isLogin"
            v-model="name"
            label="Full Name"
            variant="outlined"
            prepend-inner-icon="mdi-account"
            class="mb-2"
            color="indigo-accent-2"
            bg-color="rgba(255, 255, 255, 0.5)"
            :rules="[(v) => !!v || 'Name is required']"
          ></v-text-field>

          <v-text-field
            v-model="username"
            label="Username"
            variant="outlined"
            prepend-inner-icon="mdi-at"
            class="mb-2"
            color="indigo-accent-2"
            bg-color="rgba(255, 255, 255, 0.5)"
            :rules="[(v) => !!v || 'Username is required']"
          ></v-text-field>

          <v-text-field
            v-model="password"
            label="Password"
            variant="outlined"
            prepend-inner-icon="mdi-lock"
            :type="showPassword ? 'text' : 'password'"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            class="mb-6"
            color="indigo-accent-2"
            bg-color="rgba(255, 255, 255, 0.5)"
            :rules="[
              (v) => !!v || 'Password is required',
              (v) => v.length >= 6 || 'Min 6 characters',
            ]"
          ></v-text-field>

          <v-btn
            type="submit"
            color="indigo-accent-3"
            size="x-large"
            block
            class="font-weight-bold text-white rounded-lg mb-4"
            :loading="loading"
            elevation="2"
          >
            {{ isLogin ? "Sign In" : "Create Account" }}
          </v-btn>

          <div class="text-center">
            <v-btn
              variant="text"
              color="indigo-darken-1"
              class="font-weight-medium text-none"
              @click="toggleMode"
            >
              {{
                isLogin
                  ? "Don't have an account? Sign up"
                  : "Already have an account? Sign in"
              }}
            </v-btn>
          </div>
        </v-form>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useRuntimeConfig } from "#app";

definePageMeta({
  layout: false, // Custom full-page layout
});

const config = useRuntimeConfig();
const router = useRouter();
const form = ref(null);

const isLogin = ref(true);
const loading = ref(false);
const error = ref("");

const name = ref("");
const username = ref("");
const password = ref("");
const showPassword = ref(false);

const toggleMode = () => {
  isLogin.value = !isLogin.value;
  error.value = "";
  form.value?.resetValidation();
};

const handleSubmit = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;

  loading.value = true;
  error.value = "";

  const apiBaseUrl = useApiBaseUrl();
  const endpoint = isLogin.value ? "/api/auth/login" : "/api/auth/register";
  const payload = isLogin.value
    ? { username: username.value, password: password.value }
    : { username: username.value, password: password.value, name: name.value };

  try {
    const res = await fetch(`${apiBaseUrl}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Authentication failed");
    }

    // Save auth data
    localStorage.setItem("typing_token", data.token);
    localStorage.setItem("typing_user", JSON.stringify(data.user));

    // Redirect to profile page instead of typing test
    router.push("/typing/profile");
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  position: relative;
  background:
    radial-gradient(at 0% 0%, #e0e7ff 0px, transparent 50%),
    radial-gradient(at 100% 0%, #fae8ff 0px, transparent 50%),
    radial-gradient(at 100% 100%, #e0f2fe 0px, transparent 50%),
    radial-gradient(at 0% 100%, #ede9fe 0px, transparent 50%), #f8fafc;
}

.back-btn-container {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
}

.glass-card {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5) !important;
  box-shadow: 0 10px 40px -10px rgba(99, 102, 241, 0.15) !important;
}

.brand-icon {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

.gradient-text {
  background: linear-gradient(135deg, #4338ca, #7e22ce);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.error-banner {
  background: rgba(254, 226, 226, 0.8);
  border: 1px solid rgba(248, 113, 113, 0.5);
}
</style>
