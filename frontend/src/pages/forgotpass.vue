<template>
  <div class="flex items-center justify-center min-h-screen">
    <Card class="max-w-[500px] w-full h-[700px] border p-6 rounded-lg shadow-md overflow-auto ml-[665px]">
      <CardHeader class="text-center mt-[140px]">
        <CardTitle class="text-2xl">Forgot Password</CardTitle>
        <CardDescription>
          Enter your email address to reset your password.
        </CardDescription>
      </CardHeader>

      <CardContent class="grid gap-4">
        <div>
          <Label for="email">Email Address</Label>
          <Input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="Enter your email"
            :class="{ 'border-red-500': showError }"
          />
          <!-- Error Message -->
          <span v-if="showError" class="text-red-500 text-sm mt-2 block">
            Email is required.
          </span>

          <!-- Success Message -->
          <span v-if="message && !showError" class="text-green-600 text-sm mt-2 block">
            {{ message }}
          </span>
        </div>
      </CardContent>

      <CardFooter class="flex flex-col gap-4">
        <Button class="w-full " @click="handleForgotPassword">
          Reset Password
        </Button>

        <p class="text-center text-sm text-gray-500">
          <router-link to="/login" class=" hover:underline">
            Back to Login
          </router-link>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>

<script>
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {Input} from "@/components/ui/input";
import {Label} from "@/components/ui/label";

export default {
  data() {
    return {
      email: '',
      message: '',
      showError: false, // Error state
    };
  },
  methods: {
    handleForgotPassword() {
      // Validation: Check if email is empty
      if (!this.email.trim()) {
        this.showError = true; // Show error
        this.message = ''; // Clear success message
      } else {
        this.showError = false; // Hide error
        // Simulate API call
        this.message = `Password reset link sent to ${this.email}.`;
        this.email = ''; // Clear email field
      }
    },
  },
  components: {
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

