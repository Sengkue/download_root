<template>
  <v-container fluid class="pa-4">
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-blue-grey-darken-3 mb-2">Manage Typing Lessons</h1>
        <p class="text-subtitle-1 text-grey-darken-1">Add, edit, or remove typing lessons.</p>
      </div>
      <v-btn
        color="blue-lighten-1"
        variant="flat"
        prepend-icon="mdi-plus"
        @click="openAddDialog"
        height="48"
      >
        Add Lesson
      </v-btn>
    </div>

    <v-card class="elevation-3">
      <v-data-table
        :headers="headers"
        :items="lessons"
        :loading="loading"
        class="bg-white"
      >
        <template v-slot:item.content="{ item }">
          <div class="text-truncate" style="max-width: 300px;">
            {{ item.content }}
          </div>
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon="mdi-pencil"
            variant="text"
            color="blue"
            size="small"
            class="mr-2"
            @click="openEditDialog(item)"
          ></v-btn>
          <v-btn
            icon="mdi-delete"
            variant="text"
            color="red"
            size="small"
            @click="deleteLesson(item)"
            :loading="deletingLessonId === item.id"
          ></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add/Edit Lesson Dialog -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card class="bg-blue-grey-darken-4 text-white">
        <v-card-title class="text-h5 font-weight-bold pa-4 border-b border-white-10">
          {{ isEditing ? 'Edit Lesson' : 'Create Custom Lesson' }}
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <v-text-field
            v-model="lessonTitle"
            label="Lesson Title"
            placeholder="e.g. My Custom Drill"
            variant="outlined"
            color="blue-lighten-2"
            base-color="blue-grey-lighten-2"
            class="mb-2"
          ></v-text-field>
          
          <v-textarea
            v-model="lessonContent"
            label="Lesson Content (English Text)"
            placeholder="Type the English characters to practice..."
            variant="outlined"
            color="blue-lighten-2"
            base-color="blue-grey-lighten-2"
            rows="4"
            auto-grow
            hint="Spaces will be preserved as typing pauses."
            persistent-hint
          ></v-textarea>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey-lighten-1" variant="text" @click="dialog = false">Cancel</v-btn>
          <v-btn 
            color="blue-lighten-1" 
            variant="flat" 
            @click="saveLesson"
            :loading="saving"
            :disabled="!lessonTitle || !lessonContent"
          >Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const loading = ref(true);
const lessons = ref([]);

const headers = [
  { title: 'ID', key: 'id', align: 'start', sortable: true },
  { title: 'Title', key: 'title' },
  { title: 'Content Preview', key: 'content' },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

const dialog = ref(false);
const isEditing = ref(false);
const editingId = ref(null);

const lessonTitle = ref('');
const lessonContent = ref('');
const saving = ref(false);
const deletingLessonId = ref(null);

onMounted(async () => {
  await fetchLessons();
});

const fetchLessons = async () => {
  loading.value = true;
  try {
    const res = await fetch('http://localhost:3001/api/typing-lessons');
    const data = await res.json();
    lessons.value = data;
  } catch (err) {
    console.error('Error fetching lessons', err);
  } finally {
    loading.value = false;
  }
};

const openAddDialog = () => {
  isEditing.value = false;
  editingId.value = null;
  lessonTitle.value = '';
  lessonContent.value = '';
  dialog.value = true;
};

const openEditDialog = (item) => {
  isEditing.value = true;
  editingId.value = item.id;
  lessonTitle.value = item.title;
  lessonContent.value = item.content;
  dialog.value = true;
};

const saveLesson = async () => {
  if (!lessonTitle.value || !lessonContent.value) return;
  saving.value = true;
  
  try {
    const url = isEditing.value 
      ? `http://localhost:3001/api/typing-lessons/${editingId.value}`
      : 'http://localhost:3001/api/typing-lessons';
    
    const method = isEditing.value ? 'PUT' : 'POST';

    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: lessonTitle.value,
        content: lessonContent.value
      })
    });
    
    if (res.ok) {
      await fetchLessons();
      dialog.value = false;
    }
  } catch (err) {
    console.error('Error saving lesson', err);
  } finally {
    saving.value = false;
  }
};

const deleteLesson = async (item) => {
  if (!confirm(`Are you sure you want to delete "${item.title}"?`)) return;
  
  deletingLessonId.value = item.id;
  try {
    const res = await fetch(`http://localhost:3001/api/typing-lessons/${item.id}`, {
      method: 'DELETE'
    });
    if (res.ok) {
      await fetchLessons();
    }
  } catch (err) {
    console.error('Error deleting lesson', err);
  } finally {
    deletingLessonId.value = null;
  }
};
</script>
