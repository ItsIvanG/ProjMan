<template>
    <div>
      <!-- Button to Trigger Modal -->
      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem @click="openDialog">Edit</DropdownMenuItem>
                        <DropdownMenuItem>Deactivated</DropdownMenuItem>
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
            <div class="grid gap-4 py-4 sm:grid-cols-1 md:grid-cols-2">
              <!-- Feature input should stay in one column -->
              <div class="grid gap-2 md:col-span-2">
                <Label for="name">Email</Label>
                <Input
                  id="name"
                  v-model="formData.name"
                  placeholder="Type email"
                  required
                />
              </div>
  
              <!-- Sprint input -->
              <div class="grid gap-2">
                <Label for="Name">Name</Label>
                <Input
                  id="Name"
                  v-model="formData.name"
                  placeholder="Sprint"
                  required
                />
              </div>
  
              <!-- Assignee Select -->
              <div class="grid gap-2">
                <Label for="assignee">Project</Label>
                <Select v-model="formData.assignee">
                  <SelectTrigger>
                    <SelectValue placeholder="Select Project" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Project 1">Project 1</SelectItem>
                    <SelectItem value="Project 1">Project 1h</SelectItem>
                    <SelectItem value="Project 1">Project 1n</SelectItem>
                    <SelectItem value="Project 1">Project 1n</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
  
            <DialogFooter>
              <Button type="submit" class="mt-6 w-full sm:w-auto">
                <PlusCircle class="mr-2 h-4 w-4" />
               Save changes
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive } from 'vue';
  import { Button } from '@/components/ui/button';
  import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
  import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
  import { PlusCircle } from 'lucide-vue-next';
  
  // Dialog state
  const isDialogOpen = ref(false);
  
  // Form data
  const formData = reactive({
    name: '',
    price: '',
    status: '',
    assignee: '',
    priority: ''
  });
  
  // Open and Close Dialog
  const openDialog = () => {
    isDialogOpen.value = true;
  };
  
  const closeDialog = () => {
    isDialogOpen.value = false;
  };
  
  // Handle form submission
  const handleSubmit = () => {
    // Add your form submission logic here
    console.log('Form submitted:', formData);
    closeDialog();
  };
  </script>
  