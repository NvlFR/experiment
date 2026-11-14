<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <h1 class="text-3xl font-bold mb-8 text-white">Todo List</h1>

      <div class="mb-6">
        <input v-model="newTask" type="text" placeholder="Masukkan tugas baru..." 
               class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
               @keyup.enter="addTask">
        <button @click="addTask" class="mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Add Task
        </button>
      </div>

      <div v-if="tasks.length === 0" class="text-gray-500">Belum ada tugas.</div>

      <div v-for="task in tasks" :key="task.id" class="flex items-center mb-4">
        <input type="checkbox" :checked="task.completed" @change="toggleTask(task)">
        <span :class="{'line-through text-gray-500': task.completed}">{{ task.text }}</span>
        <button @click="deleteTask(task.id)" class="ml-auto text-red-600 hover:text-red-800">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newTask = ref('');
const tasks = ref([
  { id: 1, text: 'Belajar Vue.js', completed: false },
  { id: 2, text: 'Memahami Tailwind CSS', completed: true },
  { id: 3, text: 'Membuat aplikasi web responsif', completed: false },
]);

const addTask = () => {
  if (newTask.value.trim() === '') return;
  tasks.value.push({
    id: Date.now(),
    text: newTask.value,
    completed: false
  });
  newTask.value = '';
};

const toggleTask = (task) => {
  task.completed = !task.completed;
};

const deleteTask = (id) => {
  tasks.value = tasks.value.filter(task => task.id !== id);
};
</script>