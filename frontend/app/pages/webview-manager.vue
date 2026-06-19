<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

const searchQuery = ref('');

const links = ref<any[]>([]);
const isLoading = ref(false);
const isAdding = ref(false);
const activeLink = ref<any>(null);
const isEditing = ref(false);
const editingId = ref<number | null>(null);
const showAddDialog = ref(false);

const newTitle = ref('');
const newUrl = ref('');
const errorMessage = ref('');

const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F06292', '#BA68C8', '#4DD0E1', '#81C784', '#FFD54F'];
const getRandomColor = (title: string) => {
  if (!title) return colors[0];
  let hash = 0;
  for (let i = 0; i < title.length; i++) {
    hash = title.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
};

const filteredLinks = computed(() => {
  if (!searchQuery.value) return links.value;
  const q = searchQuery.value.toLowerCase();
  return links.value.filter(l => 
    l.title.toLowerCase().includes(q) || 
    l.url.toLowerCase().includes(q)
  );
});

const fetchLinks = async () => {
  isLoading.value = true;
  try {
    const res = await fetch('http://localhost:3001/api/webview-links');
    if (res.ok) {
      links.value = await res.json();
    }
  } catch (error) {
    console.error('Failed to fetch links:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchLinks();
});

const openAddDialog = () => {
  isEditing.value = false;
  editingId.value = null;
  newTitle.value = '';
  newUrl.value = '';
  errorMessage.value = '';
  showAddDialog.value = true;
};

const closeDialog = () => {
  showAddDialog.value = false;
  setTimeout(cancelEdit, 300);
};

const submitForm = async () => {
  if (!newTitle.value || !newUrl.value) {
    errorMessage.value = 'Please enter both title and URL';
    return;
  }
  
  let url = newUrl.value;
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }

  isAdding.value = true;
  errorMessage.value = '';

  if (isEditing.value && editingId.value !== null) {
    try {
      const res = await fetch(`http://localhost:3001/api/webview-links/${editingId.value}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle.value, url })
      });
      
      if (res.ok) {
        const data = await res.json();
        const index = links.value.findIndex(l => l.id === editingId.value);
        if (index !== -1) {
          links.value[index] = data.link;
        }
        closeDialog();
      } else {
        const data = await res.json();
        errorMessage.value = data.error || 'Failed to update link';
      }
    } catch (error) {
      console.error('Update link error:', error);
      errorMessage.value = 'An unexpected error occurred';
    } finally {
      isAdding.value = false;
    }
  } else {
    try {
      const res = await fetch('http://localhost:3001/api/webview-links', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle.value, url })
      });
      
      if (res.ok) {
        const addedLink = await res.json();
        links.value.unshift(addedLink);
        closeDialog();
      } else {
        const data = await res.json();
        errorMessage.value = data.error || 'Failed to add link';
      }
    } catch (error) {
      console.error('Add link error:', error);
      errorMessage.value = 'An unexpected error occurred';
    } finally {
      isAdding.value = false;
    }
  }
};

const editLink = (link: any) => {
  isEditing.value = true;
  editingId.value = link.id;
  newTitle.value = link.title;
  newUrl.value = link.url;
  errorMessage.value = '';
  showAddDialog.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  editingId.value = null;
  newTitle.value = '';
  newUrl.value = '';
  errorMessage.value = '';
};

const deleteLink = async (id: number) => {
  try {
    const res = await fetch(`http://localhost:3001/api/webview-links/${id}`, {
      method: 'DELETE'
    });
    if (res.ok) {
      links.value = links.value.filter(link => link.id !== id);
      if (activeLink.value && activeLink.value.id === id) {
        activeLink.value = null;
      }
    }
  } catch (error) {
    console.error('Delete link error:', error);
  }
};

const openWebview = (link: any) => {
  activeLink.value = link;
};
</script>

<template>
  <v-container class="py-6">
    <!-- Header Section -->
    <v-row class="mb-6 align-center">
      <v-col cols="12" md="8">
        <h1 class="text-h4 font-weight-bold mb-2">Webview Manager</h1>
        <p class="text-subtitle-1 text-grey-darken-1">Manage your webview links.</p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right">
        <v-btn 
          color="primary" 
          prepend-icon="mdi-plus"
          @click="openAddDialog"
        >
          New App
        </v-btn>
      </v-col>
    </v-row>

    <!-- App Table -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar color="surface" flat>
            <v-icon icon="mdi-table-large" color="primary" class="mx-3"></v-icon>
            <v-toolbar-title class="font-weight-medium">Links Database</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="searchQuery"
              prepend-inner-icon="mdi-magnify"
              placeholder="Search apps..."
              variant="outlined"
              hide-details
              density="compact"
              class="mx-4"
              style="max-width: 250px;"
              clearable
            ></v-text-field>
          </v-toolbar>
          <v-divider></v-divider>
          <div class="table-container">
            <v-table hover>
              <thead class="bg-grey-lighten-4">
                <tr>
                  <th class="text-left font-weight-bold" style="width: 50px;">ID</th>
                  <th class="text-left font-weight-bold" style="width: 250px;">Title</th>
                  <th class="text-left font-weight-bold">URL</th>
                  <th class="text-center font-weight-bold" style="width: 160px;">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="isLoading">
                  <td colspan="4" class="text-center py-8">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  </td>
                </tr>
                <tr v-else-if="links.length === 0">
                  <td colspan="4" class="text-center py-8 text-grey-darken-1">
                    <v-icon icon="mdi-information-outline" size="32" class="mb-2 opacity-50"></v-icon>
                    <div>No links found. Add a website to get started.</div>
                  </td>
                </tr>
                <tr v-else-if="filteredLinks.length === 0">
                  <td colspan="4" class="text-center py-8 text-grey-darken-1">
                    <v-icon icon="mdi-magnify-close" size="32" class="mb-2 opacity-50"></v-icon>
                    <div>No results for "{{ searchQuery }}"</div>
                  </td>
                </tr>
                <tr 
                  v-for="link in filteredLinks" 
                  :key="link.id" 
                  class="cursor-pointer"
                  :class="{ 'bg-blue-lighten-5': activeLink && activeLink.id === link.id }"
                  @click="openWebview(link)"
                >
                  <td class="text-grey-darken-1">{{ link.id }}</td>
                  <td>
                    <div class="d-flex align-center py-2">
                      <v-avatar size="24" :color="getRandomColor(link.title)" class="mr-3 text-white" style="font-size: 0.75rem;">
                        {{ link.title.charAt(0).toUpperCase() }}
                      </v-avatar>
                      <span>{{ link.title }}</span>
                    </div>
                  </td>
                  <td class="text-truncate" style="max-width: 400px;">
                    <a :href="link.url" target="_blank" @click.stop class="text-decoration-none text-blue-darken-2">
                      {{ link.url }}
                    </a>
                  </td>
                  <td class="text-center">
                    <v-btn
                      color="success"
                      variant="tonal"
                      size="x-small"
                      icon="mdi-play"
                      class="mr-2"
                      @click.stop="openWebview(link)"
                      title="View Website"
                    ></v-btn>
                    <v-btn
                      color="primary"
                      variant="tonal"
                      size="x-small"
                      icon="mdi-pencil"
                      class="mr-2"
                      @click.stop="editLink(link)"
                      title="Edit"
                    ></v-btn>
                    <v-btn
                      color="error"
                      variant="tonal"
                      size="x-small"
                      icon="mdi-delete"
                      @click.stop="deleteLink(link.id)"
                      title="Delete"
                    ></v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="showAddDialog" max-width="500" persistent>
      <v-card>
        <v-toolbar color="surface" flat>
          <v-toolbar-title>
            {{ isEditing ? 'Edit App' : 'New App' }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" variant="text" size="small" @click="closeDialog"></v-btn>
        </v-toolbar>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-form @submit.prevent="submitForm">
            <v-text-field
              v-model="newTitle"
              label="App Title"
              placeholder="e.g. Wikipedia"
              variant="outlined"
              class="mb-4"
              hide-details="auto"
              prepend-inner-icon="mdi-format-title"
            ></v-text-field>
            
            <v-text-field
              v-model="newUrl"
              label="App URL"
              placeholder="https://en.wikipedia.org"
              variant="outlined"
              class="mb-4"
              hide-details="auto"
              prepend-inner-icon="mdi-link"
            ></v-text-field>
            
            <div v-if="errorMessage" class="text-error mb-4 text-caption">
              <v-icon icon="mdi-alert-circle" size="small" class="mr-1"></v-icon> {{ errorMessage }}
            </div>

            <v-btn 
              color="primary" 
              type="submit" 
              :loading="isAdding" 
              block
              class="mt-2"
            >
              {{ isEditing ? 'Save' : 'Add' }}
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Webview Iframe Fullscreen Dialog -->
    <v-dialog
      :model-value="!!activeLink"
      @update:model-value="(val: boolean) => { if (!val) activeLink = null }"
      fullscreen
      transition="dialog-bottom-transition"
    >
      <v-card v-if="activeLink" class="d-flex flex-column rounded-0 bg-white">
        <v-toolbar color="grey-darken-4" density="compact" class="flex-grow-0" style="height: 48px;">
          <v-btn icon="mdi-close" color="white" @click="activeLink = null" title="Close Webview"></v-btn>
          <v-icon icon="mdi-web" class="mx-3 text-white"></v-icon>
          <v-toolbar-title class="text-white text-subtitle-1 font-weight-bold">
            {{ activeLink.title }} - <span class="text-grey-lighten-1 text-caption">{{ activeLink.url }}</span>
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-open-in-new" color="white" variant="text" size="small" :href="activeLink.url" target="_blank" title="Open in new tab"></v-btn>
        </v-toolbar>
        
        <div class="flex-grow-1 w-100" style="height: calc(100vh - 48px);">
          <iframe 
            :src="activeLink.url" 
            frameborder="0" 
            class="w-100 h-100"
            sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
          ></iframe>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.table-container {
  width: 100%;
}
.cursor-pointer {
  cursor: pointer;
}
</style>
