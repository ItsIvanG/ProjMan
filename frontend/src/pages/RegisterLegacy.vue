<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-50">
      <Card class="w-full max-w-sm">
        <CardHeader>
          <CardTitle class="text-2xl text-center">
            Register
          </CardTitle>
          <CardDescription class="text-center">
            Create an account by entering your email and password below.
          </CardDescription>
        </CardHeader>
        <CardContent class="grid gap-4">
          <!-- Display error message -->
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
          <p v-if="success" class="text-green-500 text-sm">{{ success }}</p>
  
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input
              v-model="email"
              id="email"
              type="email"
              placeholder="m@example.com"
              required
              class="text-gray-700"
            />
          </div>
  
          <div class="grid gap-2">
            <Label for="password">Password</Label>
            <Input
              v-model="password"
              id="password"
              type="password"
              required
              placeholder="••••••••"
              class="text-gray-700"
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button class="w-full" @click.prevent="register">
            Register
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
  import { getCSRFToken } from "@/store/auth";
  
  export default {
    data() {
      return {
        email: "",
        password: "",
        error: "",
        success: "",
      };
    },
    methods: {
      async register() {
        try {
          const response = await fetch("http://localhost:8000/api/register", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            }),
            credentials: "include",
          });
          const data = await response.json();
          if (response.ok) {
            this.success = "Registration successful! Redirecting to login...";
            setTimeout(() => {
              this.$router.push("/login");
            }, 1000);
          } else {
            this.error = data.error || "Registration failed.";
          }
        } catch (err) {
          this.error = "An error occurred during registration: " + err;
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