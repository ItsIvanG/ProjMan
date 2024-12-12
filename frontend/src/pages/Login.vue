<template>
  <div class="flex items-center justify-right min-h-screen">
    <Card class="max-w-[500px] w-full h-[650px] border border-white p-6 rounded-lg shadow-md overflow-auto ml-[850px]">
      <CardHeader class="text-center mt-10">
        <CardTitle class="text-2xl mt">Welcome Back!</CardTitle>
        <CardDescription>
          Kindly enter your account details.
        </CardDescription>
      </CardHeader>
         <CardContent class="grid gap-4">
      <!-- Email/Username Field -->
      <div class="relative mb-2">
  <Label for="identifier">Email/Username</Label>
  <Input
            id="identifier"
            v-model="identifier"
            placeholder="Email/Username"
            required
          />
          <span v-if="showErrors.identifier" class="text-red-500 text-sm">
            Please enter a valid email or username (at least 3 characters).
          </span>
        </div>

      <!-- Password Field -->
      <div class="grid gap-2 relative">
        <Label for="password">Password</Label>
        <Input
          id="password"
          :type="showPassword ? 'text' : 'password'"
          v-model="password"
          placeholder="••••••••"
          required
          class="w-full border border-white rounded p-2 bg-black text-white"
        />
        <span v-if="showErrors.password" class="text-red-500 text-sm">
          Password should be at least 8 characters.
        </span>
        <span
          class="absolute right-3 top-10 cursor-pointer"
          @click="togglePassword"
        >
          <AkEyeClosed v-if="!showPassword" class="text-gray-400" />
          <AkEyeOpen v-if="showPassword" class="text-gray-400" />
        </span>
      </div>

      <!-- Remember Me and Forgot Password -->
      <div class="flex items-center justify-between text-sm">
        <div class="flex items-center">
          <input
            id="remember"
            type="checkbox"
            v-model="rememberMe"
            class="h-4 w-4 text-blue-400 border-gray-300 rounded focus:ring-blue-300"
          />
          <label for="remember" class="ml-2 text-gray-300">Remember Me</label>
        </div>
        <router-link to="/forgotpass" class="text-blue-200 hover:underline">Forgot Password?</router-link>
      </div>
    </CardContent>
      <CardFooter class="flex flex-col gap-4">
        <!-- Login Button -->
        <Button class="w-full hover:bg-blue-300" @click="login">
          Log in
        </Button>

                  <!-- Separator with "Sign in with" -->
          <div class="justify-center relative flex items-center mx-2 ">
            <span class="text-white text-sm px-2 py-1">or</span>
          </div>

          <!-- Google Sign-In Button -->
          <Button
            class="w-full bg-white hover:bg-blue-300 flex items-center justify-center mt-2"
            @click="googleSignIn"
          >
            <span class="mr-2"><DeGoogleOriginal /></span>
            <span class="text-black">Continue with Google</span>
          </Button>


        <p class="text-center text-sm text-gray-500">
          Don't have an account?
          <button
            class="text-blue-200 hover:underline focus:outline-none"
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
import { DeGoogleOriginal } from "@kalimahapps/vue-icons";
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
      identifier: "", // Field for email/username
      password: "",
      showPassword: false,
      error: "",
      showErrors: {
        identifier: false, // Error tracking for email/username
        password: false,
      },
    };
  },
  watch: {
    identifier(value) {
      this.showErrors.identifier = !this.validateIdentifier(value);
    },
    password(value) {
      this.showErrors.password = value.length < 8;
    },
  },
  methods: {
    validateIdentifier(identifier) {
      // Accepts either a valid email or a valid username
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const usernamePattern = /^[a-zA-Z0-9_]{3,}$/; // At least 3 alphanumeric characters or underscores
      return emailPattern.test(identifier) || usernamePattern.test(identifier);
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      // Validate fields before submission
      this.showErrors.identifier = !this.validateIdentifier(this.identifier);
      this.showErrors.password = this.password.length < 8;

      if (this.showErrors.identifier || this.showErrors.password) {
        this.error = "Please fix the highlighted fields.";
        return;
      }

      try {
        await this.authStore.login(this.identifier, this.password, this.$router);
        if (!this.authStore.isAuthenticated) {
          this.error = "Login failed. Please check your credentials.";
        }
      } catch (err) {
        console.error(err);
        this.error = "An error occurred. Please try again.";
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
    DeGoogleOriginal,
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
