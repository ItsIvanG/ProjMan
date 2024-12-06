<script>
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'
import Sidebar from "../components/ui/layout/sidebar.vue";
import Navbar from "../components/ui/layout/navbar.vue";


export default {
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    return {
      authStore, router
    }
  },
  methods: {
    async logout() {
      try {
        await this.authStore.logout(this.$router)
      } catch (error) {
        console.error(error)
      }
    }
  },
  async mounted() {
    await this.authStore.fetchUser()
  },
  components: {
    Sidebar,
    Navbar
  },
}
</script>

<template>

   <Sidebar />
   <Navbar />
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
    <!-- Add Navbar component here -->
   

    <h1 class="text-4xl font-bold text-gray-800 mb-6">Welcome to the home page</h1>
    <div v-if="authStore.isAuthenticated" class="text-center">
    
      <p class="text-xl text-gray-700 mb-2">
        Hi there <span class="font-semibold text-gray-900">{{ authStore.user?.username }}</span>!
      </p>
      <p class="text-lg text-gray-600 mb-4">You are logged in.</p>
      <button
        @click="logout"
        class="bg-gray-500 text-white py-2 px-4 rounded-md hover:bg-red-600 transition"
      >
        Logout
      </button>
    </div>
    <p v-else class="text-center text-lg text-gray-700">
      You are not logged in. 
      <router-link to="/login" class="text-blue-500 underline hover:text-blue-700">
        Login
      </router-link>
    </p>
  </div>
</template>


