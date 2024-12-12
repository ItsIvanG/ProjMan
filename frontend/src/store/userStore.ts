// src/store/task.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserInfoStore = defineStore('user', () => {
  const user = ref<Record<string, any> | null>(null); 

  const setTask = (userData: Record<string, any>) => {
    user.value = userData;
    console.log('User data set to:', userData); 
  };

  return {
    user,
    setTask,
  };
});
