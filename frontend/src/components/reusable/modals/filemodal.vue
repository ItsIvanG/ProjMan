<template>
  <div>
    <!-- Button to Trigger Modal -->
    <div class="flex justify-center m-5">
      <Button size="sm" class="h-7 gap-1" @click="openDialog">
        <PlusCircle class="h-3.5 w-3.5" />
        <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
          Add File
        </span>
      </Button>
    </div>

    <!-- Dialog for File Upload -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <DialogContent class="max-w-lg">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Add File</DialogTitle>
          <DialogDescription class="text-lg">
            Fill out the form below to add a new file. Provide the necessary details and click "Add File."
          </DialogDescription>
        </DialogHeader>

        <form @submit.prevent="handleSubmit">
          <div class="grid gap-4 py-4 sm:grid-cols-1 md:grid-cols-2">
            <!-- File Input and Share Option placed side by side -->
            <div class="flex gap-4 md:col-span-2">
              <!-- File Input -->
              <div class="flex-1">
                <Label for="filename">Upload File</Label>
                <Input
                  id="filename"
                  type="file"
                  class="w-full file:text-muted-foreground"
                  required
                  @change="onFileChange"
                />
              </div>

              <!-- Share Option Select -->
              <div class="flex-2" v-if="userRole !== 'Member'">
                <Label for="share_option">Share Option</Label>
                <Select v-model="formData.shareOption" class="w-full">
                  <SelectTrigger>
                    <SelectValue placeholder="Select sharing option" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="anyone">Anyone</SelectItem>
                    <SelectItem value="share_with">Share with</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <!-- Share with Select (Visible if "Share With" is selected) -->
            <div v-if="formData.shareOption === 'share_with'&& userRole !== 'Member'" class="grid gap-3 md:col-span-2" >
              <Label for="share_id">Share With</Label>
              <Select v-model="formData.share_id" class="w-full">
                <SelectTrigger>
                  <SelectValue placeholder="Select user to share with" />
                </SelectTrigger>
                <SelectContent>
                  <!-- Render dynamic user options -->
                  <SelectItem
                    v-for="user in users"
                    :key="user.id"
                    :value="user.id"
                  >
                    {{ user.name }}
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <DialogFooter>
            <Button type="submit" class="mt-6 w-full sm:w-auto">
              <PlusCircle class="mr-2 h-4 w-4" />
              Add File
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PlusCircle } from 'lucide-vue-next';
import { getAPI } from '@/axios'; 
import { useProjectStore } from '@/store/project';
import { useAuthStore } from '@/store/auth';
import { useFileListStore } from '@/store/fileListStore';  // Pinia store
import { useToast } from '@/components/ui/toast/use-toast'

const { toast } = useToast()

const projectStore = useProjectStore();
const projectId = computed(() => projectStore.project_id);

const authStore = useAuthStore();
const userID = computed(() => authStore.user?.id);
const managerId = computed(() => authStore.user?.manager_id);
const userRole = computed(() => authStore.user?.role);

const formData = reactive({
  filename: null,
  share_id: '',
  project: projectId.value,
  user: userID.value,
  shareOption: 'anyone', // Default to 'Anyone'
});

const users = ref<any[]>([]);

// Fetch users for the given manager ID
const fetchUsers = async () => {
  try {
    const response = await getAPI.get(`/manager/${managerId.value}/`);
    users.value = response.data; // Assuming the response contains an array of users
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

const isDialogOpen = ref(false);

const fileListStore = useFileListStore(); // Pinia store

const onFileChange = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  formData.filename = file || null;
};

// Open and Close Dialog
const openDialog = async () => {
  isDialogOpen.value = true;
  await fetchUsers(); // Fetch users when the dialog is opened
};

const closeDialog = () => {
  isDialogOpen.value = false;
  resetForm(); // Reset form when dialog is closed
};

const resetForm = () => {
  // Clear form data
  formData.filename = null;
  formData.share_id = '';
  formData.shareOption = 'anyone';

  // Reset the file input manually
  const fileInput = document.getElementById('filename') as HTMLInputElement;
  if (fileInput) fileInput.value = ''; // Clear file input value
};

const handleSubmit = async () => {
  const form = new FormData();
  
  if (formData.filename) {
    form.append('filename', formData.filename);
  } else {
    console.error('No file selected');
    return;
  }

  // Append other fields
  form.append('share_id', formData.share_id);
  form.append('project', String(formData.project));
  form.append('user', String(formData.user));

  try {
    const response = await getAPI.post('/files/create/', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // Extract and process the filename from the response
    const processedFile = {
      ...response.data,
      filename: decodeURIComponent(response.data.filename.split('/').pop()!),
    };

    // Update Pinia store with the newly uploaded file
    fileListStore.addFile(processedFile);  // Add the newly uploaded file to the Pinia store
    toast({
  title: 'File Uploaded',
  description: 'The file have been uploaded successfully.',
});

// Ensure any previously lingering toasts are cleared after 3 seconds
setTimeout(() => {
  // This can trigger any toast cleanup if needed
}, 3000);
    // Handle success
    closeDialog();
    console.log('File uploaded successfully:', response.data);
  } catch (error) {
    console.error('Error uploading file:', error);
  }
};
</script>

