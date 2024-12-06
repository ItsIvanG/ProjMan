<template>
  <div class="flex items-center justify-center min-h-screen">
    <Card class="w-full max-w-sm">
      <CardHeader>
        <CardTitle class="text-2xl">
          Login
        </CardTitle>
        <CardDescription>
          Enter your email below to login to your account.
        </CardDescription>
      </CardHeader>
      <CardContent class="grid gap-4">
        <!-- Display error message -->
        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>
        <div class="grid gap-2">
          <Label for="email">Email</Label>
          <Input
            id="email"
            type="email"
            v-model="email"
            placeholder="m@example.com"
            required
            @input="resetError"
          />
        </div>
        <div class="grid gap-2">
          <Label for="password">Password</Label>
          <Input
            id="password"
            type="password"
            v-model="password"
            required
            @input="resetError"
          />
        </div>
      </CardContent>
      <CardFooter>
        <Button class="w-full" @click="login">
         Log in
        </Button>
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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuthStore } from '../store/auth'

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
      error: "",
    };
  },
  methods: {
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
