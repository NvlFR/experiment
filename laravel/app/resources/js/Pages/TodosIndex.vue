<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <h1 class="text-3xl font-bold mb-8 text-white">Todo List</h1>

      <div v-if="todos.length === 0" class="text-gray-500">Belum ada tugas.</div>

      <div v-for="todo in todos" :key="todo.id" class="flex items-center mb-4">
        <!-- Input ID untuk update -->
        <input type="number" v-model="todo.id" @input="updateTodo(todo)" class="mr-2 w-16 px-2 py-1 border rounded bg-gray-700 text-white" />
        
        <!-- Checkbox dan tombol untuk mark/unmark -->
        <div class="flex items-center">
          <input type="checkbox" :checked="todo.is_completed" @change="toggleTodo(todo)" />
          <button @click="toggleTodo(todo)" class="ml-2 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">
            {{ todo.is_completed ? 'Unmark' : 'Mark' }}
          </button>
        </div>
        <span :class="{'line-through text-gray-500': todo.is_completed}">{{ todo.title }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePage } from '@inertiajs/vue3';
const todos = usePage('todos').props.todos as Array<{ id: number; title: string; is_completed: boolean }>();

// Fungsi untuk update todo dengan ID yang diubah
const updateTodo = async (todo) => {
  await $put(`/api/todos/${todo.id}`, {
    headers: { 'Accept': 'application/json' },
    body: JSON.stringify({ title: todo.title, is_completed: todo.is_completed }),
  });
};

// Fungsi untuk toggle mark/unmark
const toggleTodo = async (todo) => {
  await $put(`/api/todos/${todo.id}`, {
    headers: { 'Accept': 'application/json' },
    body: JSON.stringify({ title: todo.title, is_completed: !todo.is_completed }),
  });
};
</script>

<script>
export default {
  name: 'TodosIndex',
};
</script>