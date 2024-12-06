<template>
  <div class="login flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <h1 class="text-3xl font-bold mb-6 text-gray-700">Login</h1>
    <form @submit.prevent="login" class="bg-white p-8 shadow-md rounded-lg w-96">
      <div class="mb-4">
        <label for="email" class="block text-gray-600 font-medium mb-2">Email:</label>
        <input
          v-model="email"
          id="email"
          type="text"
          required
          @input="resetError"
          class="w-full px-4 py-2 border rounded-md text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <div class="mb-4">
        <label for="password" class="block text-gray-600 font-medium mb-2">Password:</label>
        <input
          v-model="password"
          id="password"
          type="password"
          required
          @input="resetError"
          class="w-full px-4 py-2 border rounded-md text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <button
        type="submit"
        class="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition"
      >
        Login
      </button>
    </form>
    <p v-if="error" class="error text-red-500 mt-4">{{ error }}</p>
  </div>
</template>


<script>
import { useAuthStore } from '../store/auth'

export default {
  setup() {
    const authStore = useAuthStore()
    return {
      authStore
    }
  },
  data() {
    return {
      email: "",
      password: "",
      error: ""
    }
  },
  methods: {
    async login(){
      await this.authStore.login(this.email, this.password, this.$router)
      if (!this.authStore.isAuthenticated){
        this.error = 'Login failed. Please check your credentials.'
      }
    },
    resetError(){
      this.error = ""
    }
  }
}
</script>
