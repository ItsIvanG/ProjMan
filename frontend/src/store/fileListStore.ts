import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useFileListStore = defineStore('fileListStore', () => {
  // State: List of files
  const files = ref<any[]>([]);
  const selectedFile = ref<any>(null);
  const isLoading = ref<boolean>(false);
  const hasError = ref<boolean>(false);

  // Action: Set the files list
  const setFiles = (newFiles: any[]) => {
    files.value = newFiles;
  };

  // Action: Add a new file to the list
  const addFile = (file: any) => {
    // Ensure the filename is processed and decoded correctly
    const decodedFilename = decodeURIComponent(file.filename.split('/').pop()!);
    files.value.push({ ...file, filename: decodedFilename });
  };

  // Action: Set the selected file
  const setSelectedFile = (file: any) => {
    selectedFile.value = file;
  };

  // Action: Set loading state
  const setLoading = (loading: boolean) => {
    isLoading.value = loading;
  };

  // Action: Set error state
  const setError = (error: boolean) => {
    hasError.value = error;
  };

  return {
    files,
    selectedFile,
    isLoading,
    hasError,
    setFiles,
    addFile,
    setSelectedFile,
    setLoading,
    setError,
  };
});
