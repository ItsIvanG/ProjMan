<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    
    <form @submit.prevent="register" class="bg-white p-8 shadow-lg rounded-lg w-96">
      <h2 class="text-2xl font-bold text-gray-800 mb-6 flex flex-col items-center justify-center ">Register</h2>
      <div class="mb-4">
        <label for="email" class="block text-gray-700 font-medium mb-2">Email:</label>
        <input
          v-model="email"
          id="email"
          type="email"
          required
          class="w-full px-4 py-2 border rounded-md text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <div class="mb-4">
        <label for="password" class="block text-gray-700 font-medium mb-2">Password:</label>
        <input
          v-model="password"
          id="password"
          type="password"
          required
          class="w-full px-4 py-2 border rounded-md text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <Button
        type="submit"
        class="w-full"
      >
        Register
      </Button>
    </form>
    <p v-if="error" class="text-red-500 mt-4">{{ error }}</p>
    <p v-if="success" class="text-green-500 mt-4">{{ success }}</p>
  </div>
</template>


<script>
import { getCSRFToken } from '../store/auth'
import { Button } from '@/components/ui/button'

export default {
  data() {
    return {
      email: '',
      password: '',
      error: '',
      success: ''
    }
  },
  methods: {
    async register() {
      try {
        const response = await fetch('http://localhost:8000/api/register', {
          method: 'POST',
           headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          }),
          credentials: 'include'
        })
        const data = await response.json()
        if (response.ok) {
          this.success = 'Registration successful! Please log in.'
          setTimeout(() => {
            this.$router.push('/login')
          }, 1000)
        } else {
          this.error = data.error || 'Registration failed'
        }
      } catch (err) {
        this.error = 'An error occurred during registration: ' + err
      }
    }
  },
  components:  {
    Button
  }
}
</script>
