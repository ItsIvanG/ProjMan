<template>
  <div>
    <!-- Dropdown Menu Item -->
    <div>
    <!-- Full-Length Button with Icon -->
    <Button @click="editProject" variant="default" size="sm" class="h-7 gap-1">
              <Pencil/>
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Edit Project
              </span>
    </Button>

  </div>

    <!-- Dialog -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <!-- Updated DialogContent size -->
      <DialogContent class="max-w-[600px]">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Edit Project</DialogTitle>
          <DialogDescription class=" text-lg">
           Edit details and click "Save Project."
          </DialogDescription>
        </DialogHeader>
        <div class="grid gap-6 py-6">
          <div class="grid grid-cols-4 items-center gap-6">
            <Label for="projectName" class="text-right text-lg font-medium">
              Project Name
            </Label>
 <Input
  id="projectName"
  v-model="projectName"
  placeholder="Enter project name"
  class="col-span-3 text-base p-3"
/>
          </div>
          <div class="grid grid-cols-4 items-center gap-6">
            <Label for="projectDesc" class="text-right text-lg font-medium">
              Description
            </Label>
            <Input
  id="projectDesc"
  v-model="projectDescription"
  placeholder="Enter project description"
  class="col-span-3 text-base p-3"
/>
          </div>
        </div>
        <DialogFooter>
          <Button type="button" @click="saveProject" class="w-full sm:w-auto">
  <PlusCircle class="mr-2 h-4 w-4" />
  Save Project
</Button>

        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref,computed } from 'vue';
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
import { PlusCircle,Pencil } from 'lucide-vue-next';
import { getAPI } from '@/axios';
import { useAuthStore } from '@/store/auth';
import {useProjectStore} from "@/store/project.ts";

const projectName = ref('');
const projectDescription = ref('');
// Access the authentication store
const authStore = useAuthStore();

// Use a computed property to get the user ID from the store
const userId = computed(() => authStore.user?.id);
const projectStore = useProjectStore();
const managerId = computed(() => authStore.user?.manager_id);

const saveProject = async () => {
  try {
    if (!userId.value) {
      console.error('User ID is not available.');
      return;
    }

    const response = await getAPI.put(`/api/projects/update/${projectStore.project_id}/`, {
      project_name: projectName.value,
      project_description: projectDescription.value,
      user: userId.value,
      manager_id: managerId.value,
    });
    console.log('Project Created:', response.data);

    // Close the dialog
    closeDialog();

    // Reload the window
    window.location.reload();
  } catch (error) {
    console.error('Error creating project:', error);
  }
};




// State to manage dialog visibility
const isDialogOpen = ref(false);

// Function to open dialog
const editProject = () => {
  isDialogOpen.value = true;
  projectName.value = projectStore.project_name;
  projectDescription.value = projectStore.project_description;

};

// Function to close dialog (can be used if Dialog doesn't automatically close)
const closeDialog = () => {
  isDialogOpen.value = false;
};
</script>
