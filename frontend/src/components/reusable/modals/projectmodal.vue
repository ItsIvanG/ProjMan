<template>
  <div>
    <!-- Dropdown Menu Item -->
    <div 
    class="w-full text-left font-medium flex items-center justify-start space-x-3 cursor-pointer"
    @click="createNewProject"
  >
    <!-- Full-Length Button with Icon -->
    <Button variant="outline" class="w-full flex items-center px-4 py-2">
      <!-- Icon -->
      <PlusCircle class="h-5 w-5 mr-2" />
      <!-- Button Text -->
      <span>Create New</span>
    </Button>
  </div>

    <!-- Dialog -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <!-- Updated DialogContent size -->
      <DialogContent class="max-w-[600px]">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Create New Project</DialogTitle>
          <DialogDescription class=" text-lg">
            Fill out the form below to create a new project. Provide the necessary details and click "Save Project."
          </DialogDescription>
        </DialogHeader>
        <div class="grid gap-6 py-6">
          <div class="grid grid-cols-4 items-center gap-6">
            <Label for="projectName" class="text-right text-lg font-medium">
              Project Name
            </Label>
            <Input id="projectName" placeholder="Enter project name" class="col-span-3 text-base p-3" />
          </div>
          <div class="grid grid-cols-4 items-center gap-6">
            <Label for="projectDesc" class="text-right text-lg font-medium">
              Description
            </Label>
            <Input id="projectDesc" placeholder="Enter project description" class="col-span-3 text-base p-3" />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" class="w-full sm:w-auto">
                <PlusCircle class="mr-2 h-4 w-4" />
                Save Project
              </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { PlusCircle } from 'lucide-vue-next';

// State to manage dialog visibility
const isDialogOpen = ref(false);

// Function to open dialog
const createNewProject = () => {
  isDialogOpen.value = true;
};

// Function to close dialog (can be used if Dialog doesn't automatically close)
const closeDialog = () => {
  isDialogOpen.value = false;
};
</script>
