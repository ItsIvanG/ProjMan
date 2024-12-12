<template>
  <div>
    <!-- Button to Trigger Modal -->
    <div class="flex justify-center m-5">
      <Button size="sm" class="h-7 gap-1" @click="openDialog">
        <PlusCircle class="h-3.5 w-3.5" />
        <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
          Add user
        </span>
      </Button>
    </div>
    <!-- Dialog for User Creation -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <DialogContent class="max-w-2xl">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Add new user</DialogTitle>
          <DialogDescription class="text-lg">
            Fill out the form below to add a new user. Provide the necessary details and click "Add new user."
          </DialogDescription>
        </DialogHeader>

        <form @submit.prevent="handleSubmit">
          <div class="grid gap-4 py-4 sm:grid-cols-1 md:grid-cols-2">
            <!-- Name input -->
            <div class="grid gap-2">
              <Label for="Name">Name</Label>
              <Input
                id="Name"
                v-model="formData.name"
                placeholder="Enter full name"
                required
              />
              <p v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</p>
            </div>
            <!-- Email input -->
            <div class="grid gap-2">
              <Label for="email">Email</Label>
              <Input
                id="email"
                v-model="formData.email"
                placeholder="Enter a valid email address"
                required
              />
              <p v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</p>
            </div>

            <!-- Username input -->
            <div class="grid gap-2">
              <Label for="username">Username</Label>
              <Input
                id="username"
                v-model="formData.username"
                placeholder="Create a unique username"
                required
              />
              <p v-if="errors.username" class="text-red-500 text-sm">{{ errors.username }}</p>
            </div>

            <!-- Password input -->
            <div class="grid gap-2">
              <Label for="password">Password</Label>
              <div class="relative">
                <Input
                  :type="passwordVisible ? 'text' : 'password'"
                  id="password"
                  v-model="formData.password"
                  placeholder="*********"
                  required
                  autocomplete="new-password"
                />
                <button
                  type="button"
                  @click="togglePasswordVisibility"
                  class="absolute right-3 top-1/2 transform -translate-y-1/2"
                >
                  <span v-if="passwordVisible">
                    <EyeOff class="h-5 w-5 text-gray-600" />
                  </span>
                  <span v-else>
                    <Eye class="h-5 w-5 text-gray-600" />
                  </span>
                </button>
              </div>
              <p v-if="errors.password" class="text-red-500 text-sm">{{ errors.password }}</p>
            </div>
          </div>

          <DialogFooter>
            <Button type="submit" class="mt-6 w-full sm:w-auto">
              <PlusCircle class="mr-2 h-4 w-4" />
              Add new user
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  </div>
</template>

  
  <script setup lang="ts">
  import { ref, reactive, computed } from 'vue';
  import { getAPI } from '@/axios'; // Ensure correct path to axios instance
  import { Button } from '@/components/ui/button';
  import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import { PlusCircle, Eye, EyeOff } from 'lucide-vue-next';
  import { useAuthStore } from '@/store/auth';
  
  const authStore = useAuthStore();
  const managerId = computed(() => authStore.user?.id);
  
  // Dialog state
  const isDialogOpen = ref(false);
  
  // Toggle password visibility
  const togglePasswordVisibility = () => {
    passwordVisible.value = !passwordVisible.value;
  };
  
  const passwordVisible = ref(false);
  
  // Form data
  const formData = reactive({
    name: '',
    email: '',
    username: '',
    password: '',
    role: 'Member',
    is_active: true,
    manager: managerId.value,
  });
  
  // Form errors
  const errors = reactive({
    name: '',
    email: '',
    username: '',
    password: '',
  });
  
  // Open and Close Dialog
  const openDialog = () => {
    isDialogOpen.value = true;
  };
  
  const closeDialog = () => {
    window.location.reload();
    // Reset form data and errors
    formData.name = '';
    formData.email = '';
    formData.username = '';
    formData.password = '';
    clearErrors();
    isDialogOpen.value = false;
  };
  
  // Clear all errors
  const clearErrors = () => {
    errors.name = '';
    errors.email = '';
    errors.username = '';
    errors.password = '';
  };
  
  // Handle form submission
  const handleSubmit = async () => {
  try {
    clearErrors(); // Clear previous errors
    const response = await getAPI.post('manager/create/', formData);
    console.log('Form submitted successfully:', response.data);
    closeDialog(); // Close the dialog upon successful submission
  } catch (error) {
    if (error.response && error.response.data) {
      console.error('API error response:', error.response.data); // Log the API error response
      const apiErrors = error.response.data; // Use the entire response data
      errors.name = apiErrors.name ? apiErrors.name[0] : '';
      errors.email = apiErrors.email ? apiErrors.email[0] : '';
      errors.username = apiErrors.username ? apiErrors.username[0] : '';
      errors.password = apiErrors.password ? apiErrors.password[0] : '';
    } else {
      console.error('Unexpected error:', error);
    }
  }
};



  ;
  </script>
  
  
  