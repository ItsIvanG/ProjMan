<template>
  <div class="grid lg:grid-cols-2">
    <div class="bg-secondary min-h-full  flex flex-col">
    <sidecolumn_welcome/>
    </div>
<div class="flex items-center  min-h-screen p-[100px]">
    <Card class=" w-full p-6 rounded-lg shadow-md overflow-auto  ">
      <CardHeader class="text-center items-center">
             <projmanlogo/>

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
          class="w-full border rounded p-2"
        />
        <span v-if="showErrors.password" class="text-red-500 text-sm">
          Password should be at least 8 characters.
        </span>
        <span
          class="absolute right-3 top-10 cursor-pointer"
          @click="togglePassword"
        >
          <AkEyeClosed v-if="!showPassword" />
          <AkEyeOpen v-if="showPassword" />
        </span>
      </div>

      <!-- Remember Me and Forgot Password -->
<!--      <div class="flex items-center justify-between text-sm">-->
<!--        <div class="flex items-center">-->
<!--          <input-->
<!--            id="remember"-->
<!--            type="checkbox"-->
<!--            v-model="rememberMe"-->
<!--          />-->
<!--          <label for="remember">Remember Me</label>-->
<!--        </div>-->
<!--        <router-link to="/forgotpass" class=" hover:underline">Forgot Password?</router-link>-->
<!--      </div>-->
    </CardContent>
      <CardFooter class="flex flex-col gap-4">
        <!-- Login Button -->
        <Button class="w-full" @click="login">
          Log in
        </Button>
        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>
<!--                  &lt;!&ndash; Separator with "Sign in with" &ndash;&gt;-->
<!--          <div class="justify-center relative flex items-center mx-2 ">-->
<!--            <span class="text-sm px-2 py-1">or</span>-->
<!--          </div>-->

<!--          &lt;!&ndash; Google Sign-In Button &ndash;&gt;-->
<!--          <Button-->
<!--            class="w-full flex items-center justify-center mt-2"-->
<!--            @click="googleSignIn"-->
<!--          >-->
<!--            <span class="mr-2"><DeGoogleOriginal /></span>-->
<!--            <span>Continue with Google</span>-->
<!--          </Button>-->


        <p>
          <span class="text-center text-sm text-gray-500">
          Don't have an account? </span>
          <button
            class="text-center text-sm hover:underline focus:outline-none"
            @click="redirectToRegister"
          >
             Register here
          </button>
        </p>
      </CardFooter>
    </Card>
  </div>
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
import Projmanlogo from "@/components/reusable/projmanlogo.vue";
import Sidecolumn_welcome from "@/components/reusable/sidecolumn_welcome.vue";


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
      this.showErrors.password = value.length < 1;
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
      this.showErrors.password = this.password.length < 1;

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
    Sidecolumn_welcome,
    Projmanlogo,
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



