<script setup>
import { useProjectStore } from '@/store/useProjectStore';

// Access the project store
const projectStore = useProjectStore();

// You can directly access selectedProject from the store
const selectedProject = projectStore.selectedProject;
</script>


<template>
    <h2 class="text-2xl font-bold text-white-800 mb-6 flex flex-col items-center justify-center ">global selected</h2>


</template>


