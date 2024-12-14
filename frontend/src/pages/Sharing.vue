<script setup lang="ts">
import { ref } from 'vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Folder, PlusCircle } from 'lucide-vue-next';

// State to manage files
const files = ref([]); // Start with an empty array
const addFile = () => {
  // Example file addition (you can replace this logic to handle actual file uploads)
  files.value.push({ name: `File ${files.value.length + 1}` });
};
</script>

<template>
  <div class="flex flex-1 flex-col gap-6 p-6">
    <!-- Header Section -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">File Sharing</h1>
      <template v-if="files.length > 0">
        <!-- Add File Button for non-empty state -->
        <Button
          size="sm"
          class="h-7 gap-1"
          @click="addFile"
        >
          <PlusCircle class="h-3.5 w-3.5" />
          <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
            Add File
          </span>
        </Button>
      </template>
    </div>

    <!-- Content Section -->
    <div class="flex flex-1 flex-col gap-4">
      <!-- Check if files exist -->
      <template v-if="files.length === 0">
        <!-- Empty State -->
        <div class="flex flex-1 items-center justify-center rounded-lg border border-dashed border-gray-300 p-6 shadow-sm">
          <div class="flex flex-col items-center gap-6 text-center p-20">
            <Folder class="w-24 h-24 text-gray-400" /> <!-- Enlarged Folder Icon -->
            <h3 class="text-xl font-bold">You have no files</h3>
            <p class="text-sm text-gray-500">Start sharing by adding your first files.</p>
            <div class="flex justify-center mt-5">
              <Button
                size="sm"
                class="h-7 gap-1"
                @click="addFile"
              >
                <PlusCircle class="h-3.5 w-3.5" />
                <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                  Add File
                </span>
              </Button>
            </div>
          </div>
        </div>
      </template>

      <template v-else>
        <!-- Files List -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card v-for="(file, index) in files" :key="index" class="p-4">
            <CardHeader>
              <Folder class="w-16 h-16 text-gray-500" />
              <CardTitle>{{ file.name }}</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>File description.</CardDescription>
            </CardContent>
          </Card>
        </div>
      </template>
    </div>
  </div>
</template>
