<template>
    <div>
      <!-- Button to Trigger Modal -->
      <div class="flex justify-center m-5">
        <Button size="sm" class="h-7 gap-1" @click="openDialog">
          <PlusCircle class="h-3.5 w-3.5" />
          <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
            Add Task
          </span>
        </Button>
      </div>
      <!-- Dialog for Task Creation -->
      <Dialog v-model:open="isDialogOpen" @close="closeDialog">
        <DialogContent class="max-w-2xl">
          <DialogHeader>
            <DialogTitle class="text-2xl font-bold">Add Task</DialogTitle>
            <DialogDescription class=" text-lg">
            Fill out the form below to add new task. Provide the necessary details and click "Add new task."
          </DialogDescription>
          </DialogHeader>
  
          <form @submit.prevent="handleSubmit">
            <div class="grid gap-4 py-4 sm:grid-cols-1 md:grid-cols-2">
              <!-- Feature input should stay in one column -->
              <div class="grid gap-2 md:col-span-2">
                <Label for="name">Features</Label>
                <Input
                  id="name"
                  v-model="formData.name"
                  placeholder="Type features"
                  required
                />
              </div>
  
              <!-- Sprint input -->
              <div class="grid gap-2">
                <Label for="price">Sprint</Label>
                <Input
                  id="price"
                  type="number"
                  v-model="formData.price"
                  placeholder="Sprint"
                  required
                />
              </div>
  
              <!-- Status Select -->
              <div class="grid gap-2">
                <Label for="status">Status</Label>
                <Select v-model="formData.status">
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Not started">Not started</SelectItem>
                    <SelectItem value="In Progress">In Progress</SelectItem>
                    <SelectItem value="Completed">Completed</SelectItem>
                    <SelectItem value="Cancelled">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
              </div>
  
              <!-- Assignee Select -->
              <div class="grid gap-2">
                <Label for="assignee">Assignee</Label>
                <Select v-model="formData.assignee">
                  <SelectTrigger>
                    <SelectValue placeholder="Select assignee" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="John Doe">John Doe</SelectItem>
                    <SelectItem value="Jane Smith">Jane Smith</SelectItem>
                    <SelectItem value="Alice Johnson">Alice Johnson</SelectItem>
                    <SelectItem value="Bob Brown">Bob Brown</SelectItem>
                  </SelectContent>
                </Select>
              </div>
  
              <!-- Priority Select -->
              <div class="grid gap-2">
                <Label for="priority">Priority</Label>
                <Select v-model="formData.priority">
                  <SelectTrigger>
                    <SelectValue placeholder="Select priority" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Low">Low</SelectItem>
                    <SelectItem value="Medium">Medium</SelectItem>
                    <SelectItem value="High">High</SelectItem>
                    <SelectItem value="Very High">Very High</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
  
            <DialogFooter>
              <Button type="submit" class="mt-6 w-full sm:w-auto">
                <PlusCircle class="mr-2 h-4 w-4" />
                Add new task
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
  import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
  import { PlusCircle, X } from 'lucide-vue-next';
  
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
  