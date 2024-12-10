<template>
    <div>


  

      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem @click="openDialog">Edit</DropdownMenuItem>
                        <DropdownMenuItem @click="openCancelTaskDialog">Cancel Task</DropdownMenuItem>
                      </DropdownMenuContent>
      <!-- Dialog for Task Creation -->
      <Dialog v-model:open="isDialogOpen" @close="closeDialog">
        <DialogContent class="max-w-2xl">
          <DialogHeader>
            <DialogTitle class="text-2xl font-bold">Edit Task</DialogTitle>
            <DialogDescription class=" text-lg">
            Fill out the form below to edit task. Provide the necessary details and click "Save changes."
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
                Save changes
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      <!-- Alert Dialog for Cancel Task -->
      <AlertDialog v-model:open="isCancelTaskDialogOpen">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently cancel your task.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <Button variant="outline" @click="closeCancelTaskDialog">Cancel</Button>
          <Button variant="destructive" @click="handleCancelTask">Yes, Cancel Task</Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>

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
  import { PlusCircle, X } from 'lucide-vue-next';
  import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
  
  // Dialog state
  const isDialogOpen = ref(false);
  const isCancelTaskDialogOpen = ref(false);

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
  

  const openCancelTaskDialog = () => {
  isCancelTaskDialogOpen.value = true;
};

const closeCancelTaskDialog = () => {
  isCancelTaskDialogOpen.value = false;
};

// Handle Cancel Task Action
const handleCancelTask = () => {
  // Add your logic to handle task cancellation here
  console.log('Task has been cancelled');
  closeCancelTaskDialog();
};


  // Handle form submission
  const handleSubmit = () => {
    // Add your form submission logic here
    console.log('Form submitted:', formData);
    closeDialog();
  };
  </script>
  