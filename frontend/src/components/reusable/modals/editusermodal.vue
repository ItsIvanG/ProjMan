<template>
  <div>
    <!-- Button to Trigger Modal -->
    <DropdownMenuContent align="end">
      <DropdownMenuItem @click="openDialog">Edit</DropdownMenuItem>
      <DropdownMenuItem 
        v-if="status" 
        @click="openDeactivateDialog">Archive</DropdownMenuItem>
    </DropdownMenuContent>
    
    <!-- Dialog for Task Creation -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <DialogContent class="max-w-2xl">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Edit user</DialogTitle>
          <DialogDescription class=" text-lg">
            Fill out the form below to edit user. Provide the necessary details and click "Save changes."
          </DialogDescription>
        </DialogHeader>

        <form @submit.prevent="handleSubmit">
          <div class="grid gap-6 py-6 sm:grid-cols-1 md:grid-cols-2">
            <!-- Name input -->
            <div class="grid gap-2">
              <Label for="name" class="font-semibold text-sm">Name</Label>
              <Input
                id="name"
                v-model="formData.name"
                placeholder="Enter full name"
                class="border-gray-300 focus:ring-2 focus:ring-blue-500 py-2 px-3 rounded-md"
                required
              />
              <p class="text-red-500 text-xs mt-1 min-h-[1.25rem]">
                {{ errors.name || ' ' }}
              </p>
            </div>

            <!-- Email input -->
            <div class="grid gap-2">
              <Label for="email" class="font-semibold text-sm">Email</Label>
              <Input
                id="email"
                v-model="formData.email"
                placeholder="Enter a valid email address"
                class="border-gray-300 focus:ring-2 focus:ring-blue-500 py-2 px-3 rounded-md"
                required
              />
              <p class="text-red-500 text-xs mt-1 min-h-[1.25rem]">
                {{ errors.email || ' ' }}
              </p>
            </div>

            <!-- Username input -->
            <div class="grid gap-2">
              <Label for="username" class="font-semibold text-sm">Username</Label>
              <Input
                id="username"
                v-model="formData.username"
                placeholder="Create a unique username"
                class="border-gray-300 focus:ring-2 focus:ring-blue-500 py-2 px-3 rounded-md"
                required
              />
              <p class="text-red-500 text-xs mt-1 min-h-[1.25rem]">
                {{ errors.username || ' ' }}
              </p>
            </div>
          </div>

          <DialogFooter>
            <Button type="submit" class="mt-4 w-full sm:w-auto bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500">
              <PlusCircle class="mr-2 h-4 w-4" />
              Save changes
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>

    <!-- AlertDialog for Deactivation -->
    <AlertDialog v-model:open="isDeactivateDialogOpen">
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone. This will permanently archive this account.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <Button variant="outline" @click="closeDeactivateDialog">Cancel</Button>
      <Button variant="destructive" @click="handleDeactivation">Yes, Archive</Button>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { Button } from '@/components/ui/button';
import { DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel } from '@/components/ui/dropdown-menu';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertDialog, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { PlusCircle } from 'lucide-vue-next';
import { useUserInfoStore } from '@/store/userStore';
import { getAPI } from '@/axios';
import { useToast } from '@/components/ui/toast/use-toast'

const { toast } = useToast()

const userStore = useUserInfoStore();
const userID = computed(() => userStore.user?.id);
const status = computed(() => userStore.user?.is_active);


console.log("kean:",userStore.user); // Debugging line to check if user data is available


// Dialog states
const isDialogOpen = ref(false);
const isDeactivateDialogOpen = ref(false);

// Open and Close Dialog for Editing
const openDialog = () => {
  if (!userID.value) {
    console.error('No task ID selected.');
    return;
  }

  const user = userStore.user;
  if (user) {
    formData.name = user.name || '';
    formData.email = user.email || '';
    formData.username = user.username || '';
  }

  isDialogOpen.value = true;
};

const closeDialog = () => {
  formData.name = '';
  formData.email = '';
  formData.username = '';
  clearErrors();
  isDialogOpen.value = false;
};

// Deactivation Dialog logic
const openDeactivateDialog = () => {
  isDeactivateDialogOpen.value = true;
};

const closeDeactivateDialog = () => {
  isDeactivateDialogOpen.value = false;
};

// Deactivate user
const handleDeactivation = async () => {
  if (!userID.value) {
    console.error('No user ID found.');
    return;
  }

  try {
    clearErrors();
    const response = await getAPI.put(`/user/${userID.value}/deactivate/`, { is_active: false });
    console.log('User deactivated successfully:', response.data);

    toast({
  title: 'User Archived',
  description: 'The user has been archived successfully.',
});

// Ensure any previously lingering toasts are cleared after 3 seconds
setTimeout(() => {
  // This can trigger any toast cleanup if needed
}, 3000);


    // Update the user data in the store
    if (userStore.user && userID.value === userStore.user.id) {
      Object.assign(userStore.user, response.data); // Merge updated data into the store
    }

    closeDeactivateDialog();  // Close the dialog after successful deactivation
  } catch (error) {
    console.error('Error deactivating user:', error);
  }
};

// Form state and errors
const formData = reactive({
  name: '',
  email: '',
  username: '',
});

const errors = reactive({
  name: '',
  email: '',
  username: '',
});

// Clear form errors
const clearErrors = () => {
  errors.name = '';
  errors.email = '';
  errors.username = '';
};

// Handle form submission for editing user
const handleSubmit = async () => {
  if (!userID.value) {
    console.error('No user ID found.');
    return;
  }

  try {
    clearErrors();
    const response = await getAPI.put(`/manager/edit/${userID.value}/`, formData);
    console.log('Form submitted successfully:', response.data);
    toast({
  title: 'User Edited',
  description: 'The user details have been updated successfully.',
});

// Ensure any previously lingering toasts are cleared after 3 seconds
setTimeout(() => {
  // This can trigger any toast cleanup if needed
}, 3000);
    // Update the user data in the store
    if (userStore.user && userID.value === userStore.user.id) {
      Object.assign(userStore.user, response.data); // Merge updated data into the store
    }

    closeDialog();  // Close the dialog after successful submission
  } catch (error) {
    if (error.response && error.response.data) {
      const apiErrors = error.response.data;
      errors.name = apiErrors.name ? apiErrors.name[0] : '';
      errors.email = apiErrors.email ? apiErrors.email[0] : '';
      errors.username = apiErrors.username ? apiErrors.username[0] : '';
    } else {
      console.error('Unexpected error:', error);
    }
  }
};
</script>
