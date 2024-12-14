<template>
  <div>
    <!-- Dropdown Menu Item -->
    <div>
    <!-- Full-Length Button with Icon -->
    <Button @click="editProject" variant="destructive" size="sm" class="h-7 gap-1">
              <Trash />
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Archive Project
              </span>
    </Button>

  </div>

    <!-- Dialog -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <!-- Updated DialogContent size -->
      <DialogContent class="max-w-[600px]">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Archive {{ projectStore.project_name }}</DialogTitle>
          <DialogDescription class=" text-lg">
           Are you sure you want to archive {{projectStore.project_name}}? You can undo this later.
          </DialogDescription>
        </DialogHeader>

        <DialogFooter>
          <Button type="button" @click="archiveProj" class="w-full sm:w-auto" variant="destructive">
            <Trash class="mr-2 h-4 w-4" />
            Archive Project
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
import { Trash,Pencil } from 'lucide-vue-next';
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

const archiveProj = async () => {
  try {
    if (!userId.value) {
      console.error('User ID is not available.');
      return;
    }

    const response = await getAPI.post(`/api/projects/archive/${projectStore.project_id}/`, {
      project_name: projectName.value,
      project_description: projectDescription.value,
      user: userId.value,
      manager_id: managerId.value,
    });
    console.log('Project Archived:', response.data);

    // Close the dialog
    closeDialog();

    // Reload the window
    window.location.reload();
  } catch (error) {
    console.error('Error archiving project:', error);
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
