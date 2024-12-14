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
            <Input
  id="projectName"
  v-model="projectName"
  placeholder="Enter project name"
  class="col-span-3 text-base p-3"
  required
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
import { PlusCircle } from 'lucide-vue-next';
import { getAPI } from '@/axios';
import { useAuthStore } from '@/store/auth';
import { useProjectListStore } from '@/store/projectListStore';
import { useToast } from '@/components/ui/toast/use-toast'

const { toast } = useToast()

const projectListStore = useProjectListStore();

const projectName = ref('');
const projectDescription = ref('');
// Access the authentication store
const authStore = useAuthStore();

// Use a computed property to get the user ID from the store
const userId = computed(() => authStore.user?.id);
const managerId = computed(() => authStore.user?.manager_id);

const saveProject = async () => {
  try {
    if (!userId.value) {
      console.error('User ID is not available.');
      return;
    }

    const response = await getAPI.post('/api/projects/create', {
      project_name: projectName.value,
      project_description: projectDescription.value,
      user: userId.value,
      manager_id: managerId.value,
    });
    console.log('Project Created:', response.data);

    // Close the dialog
    closeDialog();
    projectListStore.addProject(response.data);

    // Set the newly created project as the selected project
    projectListStore.setSelectedProject(response.data);

    // Clear the input fields
    projectName.value = '';
    projectDescription.value = '';

    // Display toast notification for successful creation
    toast({
      title: 'Project Created',
      description: 'Your project has been created successfully.',
    });

    // Ensure any previously lingering toasts are cleared after 3 seconds
    setTimeout(() => {
      // This can trigger any toast cleanup if needed
    }, 3000);
  } catch (error) {
    console.error('Error creating project:', error);
  }
};






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
