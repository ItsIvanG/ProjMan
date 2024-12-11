<script setup>
import { useProjectStore } from '@/store/project';

// Access the project store
const projectStore = useProjectStore();

console.log('Project Name:', projectStore.project_name);
console.log('Project ID:', projectStore.project_id);
console.log('Project Description:', projectStore.project_description);
</script>

<template>
  <div class="flex flex-col items-center justify-center">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Global Selected</h2>
    <p class="text-lg ">Project Name: {{ projectStore.project_name }}</p>
    <p class="text-lg ">Project ID: {{ projectStore.project_id }}</p>
    <p class="text-lg ">Project Description: {{ projectStore.project_description }}</p>
  </div>
</template>
