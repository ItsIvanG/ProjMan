// store/userListStore.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserListStore = defineStore('userListStore', () => {
  // State: List of users
  const users = ref<any[]>([]);
  const selectedUser = ref<any>(null);

  // Action: Set the users list
  const setUsers = (newUsers: any[]) => {
    users.value = newUsers;
  };

  // Action: Add a new user to the list
  const addUser = (user: any) => {
    users.value.push(user);
  };

  // Action: Set the selected user
  const setSelectedUser = (user: any) => {
    selectedUser.value = user;
  };

  return {
    users,
    selectedUser,
    setUsers,
    addUser,
    setSelectedUser,
  };
});
