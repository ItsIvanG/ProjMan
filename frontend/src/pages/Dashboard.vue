<script>
import { useAuthStore } from '../store/auth'

export default {
  setup() {
    const authStore = useAuthStore()

    return {
      authStore,
    }
  },
  async mounted() {
    await this.authStore.fetchUser()
  },
}
</script>


<template>
  <div class="p-6">

    <!-- Authenticated User Details -->
    <div v-if="authStore.isAuthenticated" class="max-w-md mx-auto border p-4 rounded">
      <h2 class="mb-4 text-lg font-medium">User Information</h2>
      <ul class="space-y-2">
        <!-- Loop Through All User Data -->
        <li v-for="(value, key) in authStore.user" :key="key" class="flex justify-between">
          <span class="capitalize">{{ key }}</span>
          <span>{{ value }}</span>
        </li>
      </ul>
    </div>

    <!-- Guest View -->
    <p v-else>
      You are not logged in. 
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

