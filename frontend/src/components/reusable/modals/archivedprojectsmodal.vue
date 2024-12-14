<template>
  <div>
    <!-- Dropdown Menu Item -->
    <div 
    class="w-full text-left font-medium flex items-center justify-start space-x-3 cursor-pointer"
    @click="viewArchivedProjects"
  >
    <!-- Full-Length Button with Icon -->
    <Button variant="outline" class="w-full flex items-center px-4 py-2">
      <!-- Icon -->
      <Archive class="h-5 w-5 mr-2" />
      <!-- Button Text -->
      <span>Archived Projects</span>
    </Button>
  </div>

    <!-- Dialog -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <!-- Updated DialogContent size -->
      <DialogContent class="max-w-[600px]">
        <DialogHeader>
                    <DialogTitle class="text-2xl font-bold">Archived Projects</DialogTitle>
          <DialogDescription class=" text-lg">
Click on an archived project and press Unarchive.</DialogDescription>
        </DialogHeader>
         <Select v-model="selectedProject">
            <SelectTrigger class="w-flex">
              <SelectValue placeholder="Select an archived project" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem
                        v-for="(project, index) in archivedProjects"
                    :key="index"

                      :value="project.project_id"
>
                  {{ project.project_name }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
<!--        <p>Selected Project: {{ selectedProject }}</p>-->
        <DialogFooter>
          <Button type="button" @click="unarchiveProject" class="w-full sm:w-auto">
  <PlusCircle class="mr-2 h-4 w-4" />
  Unarchive
</Button>

        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup>
import { ref,computed } from 'vue';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { PlusCircle , Archive} from 'lucide-vue-next';
import { getAPI } from '@/axios';
import { useAuthStore } from '@/store/auth';
import {DropdownMenuItem} from "@/components/ui/dropdown-menu";
const archivedProjects = ref([]);

const projectName = ref('');
const projectDescription = ref('');
// Access the authentication store
const authStore = useAuthStore();
// Use a computed property to get the user ID from the store
const userId = computed(() => authStore.user?.id);
const managerId = computed(() => authStore.user?.manager_id);

const unarchiveProject = async () => {
  try {
    if (!userId.value) {
      console.error('User ID is not available.');
      return;
    }

    const response = await getAPI.post(`/api/projects/unarchive/${selectedProject.value}/`, {
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
const selectedProject = ref(''); // This will hold the selected value

// Function to open dialog
const viewArchivedProjects = async () => {
    try {
    if (userId.value) {

      const response = await getAPI.get(`/projects/archives/${managerId.value}`);
      console.log('Project Archives:', response.data);
      archivedProjects.value = response.data;
        isDialogOpen.value = true;

      return;
    }

  } catch (error) {
    console.error('Error getting archived project:', error);
  }


};

// Function to close dialog (can be used if Dialog doesn't automatically close)
const closeDialog = () => {
  isDialogOpen.value = false;
};
</script>
