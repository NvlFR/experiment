<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-6">Todo List</h1>

    <!-- Add Task Section -->
    <div class="mb-6">
      <input
        v-model="newTask"
        type="text"
        placeholder="Enter a new task..."
        class="w-full px-4 py-3 rounded-lg bg-gray-700 border border-gray-600 text-white focus:outline-none focus:border-blue-500 transition-colors"
      />
      <button
        @click="addTask"
        class="mt-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
      >
        Add Task
      </button>
    </div>

    <!-- Task List -->
    <div class="space-y-3">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="flex items-center justify-between px-4 py-3 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors"
      >
        <label>
          <input
            type="checkbox"
            :checked="task.is_completed"
            @change="toggleTask(task)"
            class="mr-3 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
          />
          {{ task.title }}
        </label>
        <button
          @click="deleteTask(task)"
          class="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
        >
          Delete
        </button>
      </div>
    </div>

    <!-- No Tasks Message -->
    <div v-if="tasks.length === 0" class="text-center text-gray-400 mt-8">
      No tasks yet. Add one above!
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Dummy data for tasks
const tasks = ref([
  { id: 1, title: 'Learn Vue.js', is_completed: false },
  { id: 2, title: 'Study Tailwind CSS', is_completed: true },
  { id: 3, title: 'Build a Todo App', is_completed: false },
]);

// New task input field
const newTask = ref('');

// Function to add a new task
const addTask = () => {
  if (newTask.value.trim()) {
    tasks.value.push({
      id: Date.now(),
      title: newTask.value,
      is_completed: false
    });
    newTask.value = '';
  }
};

// Function to toggle task completion status
const toggleTask = (task) => {
  task.is_completed = !task.is_completed;
};

// Function to delete a task with confirmation
const deleteTask = (task) => {
  if (confirm('Are you sure you want to delete this task?')) {
    // In a real application, you would make an API call here
    fetch(`/api/todos/${task.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        alert(data.message);
        // Remove the task from the local array
        tasks.value = tasks.value.filter(t => t.id !== task.id);
      } else {
        alert('Error deleting task: ' + (data.data || 'Unknown error'));
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while deleting the task');
    });
  }
};
</script>
