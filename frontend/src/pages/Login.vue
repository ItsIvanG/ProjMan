<template>
  <div class="flex items-center justify-center min-h-screen">
    <Card class="w-full max-w-sm">
      <CardHeader class="text-center">
        <CardTitle class="text-2xl">Welcome Back!</CardTitle>
        <CardDescription>
          Kindly enter your account details.
        </CardDescription>
      </CardHeader>
      <CardContent class="grid gap-4">
        <!-- Display error message -->
        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>
        <div class="grid gap-2">
          <Label for="email">Email/Username</Label>
          <Input
            id="email"
            type="email"
            v-model="email"
            placeholder="Email/Username"
            required
            @input="resetError"
          />
        </div>
        <div class="grid gap-2 relative">
          <Label for="password">Password</Label>
          <Input
            id="password"
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            placeholder="••••••••"
            required
            @input="resetError"
            class="w-full border border-white rounded p-2 bg-black text-white"
          />
          <span
            class="absolute right-3 top-10 cursor-pointer"
            @click="togglePassword"
          >
            <AkEyeClosed v-if="!showPassword" class="text-gray-400" />
            <AkEyeOpen v-if="showPassword" class="text-gray-400" />
          </span>
        </div>
      </CardContent>
      <CardFooter class="flex flex-col gap-4">
        <Button class="w-full" @click="login">
          Log in
        </Button>
        <!-- Text Button for Registration -->
        <p class="text-center text-sm text-gray-500">
          Don't have an account?
          <button
            class="text-blue-500 hover:underline focus:outline-none"
            @click="redirectToRegister"
          >
            Register here
          </button>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>

<script>
import { AkEyeClosed, AkEyeOpen } from "@kalimahapps/vue-icons";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuthStore } from "../store/auth";

export default {
  setup() {
    const authStore = useAuthStore();
    return {
      authStore,
    };
  },
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      error: "",
    };
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      try {
        await this.authStore.login(this.email, this.password, this.$router);
        if (!this.authStore.isAuthenticated) {
          this.error = "Login failed. Please check your credentials.";
        }
      } catch (err) {
        this.error = "An unexpected error occurred. Please try again.";
        console.error(err);
      }
    },
    resetError() {
      this.error = "";
    },
    redirectToRegister() {
      this.$router.push("/register"); // Replace with your registration page route
    },
  },
  components: {
    AkEyeClosed,
    AkEyeOpen,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
    Input,
    Label,
  },
};
</script>

<style scoped>
/* Customize input and background colors */
input {
  background-color: #1a1a1a;
  color: white;
  border: 1px solid #fff;
}

input:focus {
  outline: none;
}

span {
  cursor: pointer;
}
</style>
