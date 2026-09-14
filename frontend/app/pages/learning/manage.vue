<template>
  <div class="pa-6">
    <v-card class="bg-grey-darken-4 rounded-xl border-thin border-white-10" elevation="10">
      <v-card-title class="d-flex justify-space-between align-center pa-6 pb-2">
        <div class="text-h4 font-weight-bold text-white">Manage Learning Videos</div>
        <v-btn color="blue-accent-2" prepend-icon="mdi-plus" @click="openAddDialog">
          Add New Video
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="videos"
          :loading="loading"
          theme="dark"
          class="bg-transparent"
        >
          <template v-slot:item.flag="{ item }">
            <span class="text-h6">{{ item.flag }}</span>
          </template>
          <template v-slot:item.videoUrl="{ item }">
            <v-chip size="small" :color="item.videoUrl ? 'green' : 'grey'">
              {{ item.videoUrl ? 'Yes' : 'No' }}
            </v-chip>
          </template>
          <template v-slot:item.flipbookUrl="{ item }">
            <v-chip size="small" :color="item.flipbookUrl ? 'blue' : 'grey'">
              {{ item.flipbookUrl ? 'Yes' : 'No' }}
            </v-chip>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-icon size="small" class="me-2 text-blue-lighten-2" @click="openEditDialog(item)">
              mdi-pencil
            </v-icon>
            <v-icon size="small" class="text-red-lighten-2" @click="deleteItem(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card class="bg-grey-darken-4 text-white">
        <v-card-title>
          <span class="text-h5">{{ isEditing ? 'Edit Video' : 'Add New Video' }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.category"
                  :items="['hmong', 'hmong-video', 'lao', 'english', 'vocab']"
                  label="Category"
                  variant="outlined"
                  bg-color="rgba(255,255,255,0.05)"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedItem.flag"
                  label="Flag/Icon Emoji (e.g. 📖, ▶️, 🇱🇦)"
                  variant="outlined"
                  bg-color="rgba(255,255,255,0.05)"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.title"
                  label="Title"
                  variant="outlined"
                  bg-color="rgba(255,255,255,0.05)"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.description"
                  label="Description"
                  rows="3"
                  variant="outlined"
                  bg-color="rgba(255,255,255,0.05)"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.videoUrl"
                  label="Video URL (e.g. YouTube Embed Link)"
                  variant="outlined"
                  bg-color="rgba(255,255,255,0.05)"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.flipbookUrl"
                  label="Flipbook URL (e.g. FlipHTML5 Link)"
                  variant="outlined"
                  bg-color="rgba(255,255,255,0.05)"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-lighten-1" variant="text" @click="closeDialog">
            Cancel
          </v-btn>
          <v-btn color="blue-accent-2" variant="elevated" @click="saveItem">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

definePageMeta({
  layout: 'learning'
});

const config = useRuntimeConfig();
const API_BASE = config.public.apiBase || 'http://localhost:3001';

const loading = ref(false);
const dialog = ref(false);
const isEditing = ref(false);
const videos = ref([]);

const headers = [
  { title: 'Flag', key: 'flag', sortable: false },
  { title: 'Category', key: 'category' },
  { title: 'Title', key: 'title' },
  { title: 'Description', key: 'description' },
  { title: 'Has Video', key: 'videoUrl' },
  { title: 'Has Book', key: 'flipbookUrl' },
  { title: 'Actions', key: 'actions', sortable: false },
];

const defaultItem = {
  id: null,
  category: 'hmong',
  title: '',
  flag: '▶️',
  description: '',
  videoUrl: '',
  flipbookUrl: ''
};

const editedItem = ref({ ...defaultItem });

const fetchVideos = async () => {
  loading.value = true;
  try {
    const res = await fetch(`${API_BASE}/api/learning-videos`);
    if (res.ok) {
      videos.value = await res.json();
    }
  } catch (error) {
    console.error('Failed to fetch videos', error);
  } finally {
    loading.value = false;
  }
};

const openAddDialog = () => {
  isEditing.value = false;
  editedItem.value = { ...defaultItem };
  dialog.value = true;
};

const openEditDialog = (item) => {
  isEditing.value = true;
  editedItem.value = { ...item };
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
};

const saveItem = async () => {
  try {
    const method = isEditing.value ? 'PUT' : 'POST';
    const url = isEditing.value 
      ? `${API_BASE}/api/learning-videos/${editedItem.value.id}` 
      : `${API_BASE}/api/learning-videos`;

    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editedItem.value)
    });

    if (res.ok) {
      closeDialog();
      fetchVideos();
    } else {
      alert('Failed to save video post');
    }
  } catch (error) {
    console.error(error);
  }
};

const deleteItem = async (item) => {
  if (confirm(`Are you sure you want to delete "${item.title}"?`)) {
    try {
      const res = await fetch(`${API_BASE}/api/learning-videos/${item.id}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        fetchVideos();
      }
    } catch (error) {
      console.error(error);
    }
  }
};

onMounted(() => {
  fetchVideos();
});
</script>

<style scoped>
.border-white-10 {
  border-color: rgba(255, 255, 255, 0.1) !important;
}
</style>
