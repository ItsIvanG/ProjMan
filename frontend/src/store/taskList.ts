import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTaskListStore = defineStore('taskList', () => {
  const tasks = ref<any[]>([]); // This will hold the list of tasks

  const setTasks = (newTasks: any[]) => {
    tasks.value = newTasks;
  };

  const addTask = (task: any) => {
    tasks.value.push(task); // Adds a new task to the list
  };

  const updateTask = (updatedTask: any) => {
    const index = tasks.value.findIndex((task) => task.id === updatedTask.id);
    if (index !== -1) {
      tasks.value[index] = updatedTask; // Update task if it exists in the list
    }
  };

  return {
    tasks,
    setTasks,
    addTask,
    updateTask,
  };
});
