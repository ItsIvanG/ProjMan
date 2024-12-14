import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTaskStore = defineStore('task', () => {
  const task = ref<Record<string, any> | null>(null); // Store the entire task object

  const setTask = (taskData: Record<string, any>) => {
    task.value = taskData;
    console.log('Task data set to:', taskData); // Optional: log for debugging
  };

  return {
    task,
    setTask,
  };
});
