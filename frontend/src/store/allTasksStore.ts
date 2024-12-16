import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { getAPI } from '@/axios';

export const useAllTasksStore = defineStore('allTasksStore', () => {
  const allTasks = ref<any[]>([]); // To store all tasks for a project


  // Fetch tasks based on project ID and status
  const fetchTasks = async (projectId: number, status: string | null, userId:number | null) => {
    try {
      let url = `/tasks/${projectId}/`;
       // Add query parameters conditionally
    const params: string[] = [];
    if (status) {
      params.push(`status=${status}`);
    }
    if (userId) {
      params.push(`userId=${userId}`);
    }

    // Append query parameters to the URL
    if (params.length > 0) {
      url += `?${params.join('&')}`;
    }
      const response = await getAPI.get(url);
      allTasks.value = response.data; // Update the tasks list in the store

      console.log('Fetched tasks:', response.data);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    }
  };

  // Add a new task to the list
  const addTask = (task: any) => {
    allTasks.value.push(task); // Add new task to the store
  };
  const updateTask = (updatedTask: any) => {
    const index = allTasks.value.findIndex(task => task.task_id === updatedTask.task_id);
    if (index !== -1) {
      // Task already exists, update it
      allTasks.value[index] = updatedTask;
    } else {
      // Task does not exist, add it
      allTasks.value.push(updatedTask);
    }
  };


  return {
    allTasks,
    fetchTasks,
    addTask,
    updateTask
  };
});
