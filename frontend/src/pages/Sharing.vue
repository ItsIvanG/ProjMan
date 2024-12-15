<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Folder, PlusCircle, ArrowDownCircle, File } from 'lucide-vue-next';
import { getAPI } from '@/axios';
import { useProjectStore } from '@/store/project';
import { useAuthStore } from '@/store/auth'; 
import  Addfile  from '@/components/reusable/modals/filemodal.vue'

const projectStore = useProjectStore();
const projectId = computed(() => projectStore.project_id);


const files = ref<any[]>([]);
const isLoading = ref(true);  // Flag to manage loading state
const hasError = ref(false);  // Flag to manage error state

// Define fetchFiles function first to avoid reference errors
const fetchFiles = async (projectId: number) => {
  isLoading.value = true;  // Set loading to true while fetching
  hasError.value = false;  // Reset error state
  try {
    const response = await getAPI(`/files/project/${projectId}/`);
    files.value = response.data.map((file: any) => {
      const fileName = decodeURIComponent(file.filename.split('/').pop()!);
      const fileUrl = `/media/${file.filename}`;
      return { ...file, filename: fileName, fileUrl };
    });
  } catch (error) {
    console.error('Error fetching files:', error);
    hasError.value = true;  // Set error state if something goes wrong
  } finally {
    isLoading.value = false;  // Set loading to false once fetch is done
  }
};

// Watch for projectId changes and fetch files accordingly
watchEffect(() => {
  const id = projectId.value;
  if (id) {
    fetchFiles(id);
  }
});

// Download file function
const downloadFile = (file: any) => {
  const link = document.createElement('a');
  link.href = file.fileUrl;
  link.download = file.filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<template>
  <div class="flex flex-1 flex-col gap-6 p-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">File Sharing</h1>
      <template v-if="files.length > 0">
        <Button
          size="sm"
          class="h-7 gap-1"
        >
          <PlusCircle class="h-3.5 w-3.5" />
          <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">Add File</span>
        </Button>
      </template>
    </div>

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="flex items-center justify-center">
      <span>Loading...</span>
    </div>

    <!-- Error State -->
    <div v-if="hasError" class="flex items-center justify-center text-red-500">
      <span>Error loading files. Please try again later.</span>
    </div>

    <div v-if="!isLoading && !hasError" class="flex flex-1 flex-col gap-4">
      <template v-if="files.length === 0">
        <div class="flex flex-1 items-center justify-center rounded-lg border border-dashed border-gray-300 p-6 shadow-sm">
          <div class="flex flex-col items-center gap-6 text-center p-20">
            <Folder class="w-24 h-24 text-gray-400" />
            <h3 class="text-xl font-bold">You have no files</h3>
            <p class="text-sm text-gray-500">Start sharing by adding your first files.</p>
            <div class="flex justify-center mt-5">
              <Button
                size="sm"
                class="h-7 gap-1"
              >
                <PlusCircle class="h-3.5 w-3.5" />
                <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">Add File</span>
              </Button>

            </div>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card v-for="(file, index) in files" :key="index" class="p-4 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader class="flex items-center gap-4">
              <File class="w-16 h-16 text-gray-500" />
              <CardTitle class="text-lg font-semibold">{{ file.filename }}</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription class="text-sm text-gray-500">
  <span class="font-bold">Uploaded by:</span> {{ file.user_name }}<br />
  <span class="font-bold">Role:</span> {{ file.user_role }} <br />
  <span class="font-bold">Shared with:</span> 
  {{ file.share_name || 'Anyone' }}
</CardDescription>

              <Button
                size="sm"
                class="mt-4 w-full"
                @click="downloadFile(file)"
              >
                <ArrowDownCircle class="h-4 w-4 mr-2" />
                Download
              </Button>
            </CardContent>
          </Card>
        </div>
      </template>
    </div>
  </div>
</template>
