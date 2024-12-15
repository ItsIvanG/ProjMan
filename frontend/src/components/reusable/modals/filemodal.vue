<template>
    <div>
      <!-- Dialog -->
      <Dialog v-model:open="isDialogOpen" @close="closeDialog">
  <DialogContent>
    <DialogHeader>
      <DialogTitle class="text-2xl font-bold">Add New File</DialogTitle>
      <DialogDescription class="text-lg">
        Upload a file and select who to share it with. Fill out the form below and click "Save File."
      </DialogDescription>
    </DialogHeader>
    <div class="grid gap-6 py-6">
      <!-- File Upload Field -->
      <div class=" items-center gap-6">
        <Label for="file" class="text-right text-lg font-medium">
          Add File
        </Label>
        <Input
          id="file"
          type="file"
          @change="handleFileChange"
          class="col-span-3 p-3 border rounded-lg"
          required
        />
      </div>

      <!-- Share With Select (Styled dropdown) -->
      <div class="grid grid-cols-4 items-center gap-6">
        <Label for="shareWith" class="text-right text-lg font-medium">
          Share With
        </Label>
        <Select
          id="shareWith"
          v-model="shareWith"
          class="col-span-3 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <SelectTrigger>
            <SelectValue :placeholder="shareWithLabel" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="everyone">Everyone</SelectItem>
            <SelectItem value="team">Team</SelectItem>
            <SelectItem value="specific">Specific Users</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
    <DialogFooter>
      <Button type="button" @click="saveFile" class="w-full sm:w-auto">
        <PlusCircle class="mr-2 h-4 w-4" />
        Save File
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>


    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
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
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
  import { getAPI } from '@/axios';
  import { useToast } from '@/components/ui/toast/use-toast';
  import { useAuthStore } from '@/store/auth';
  
  const { toast } = useToast();
  
  const isDialogOpen = ref(false);
  const file = ref(null);
  const shareWith = ref('everyone');
  
  // Computed property for the selected value's label
  const shareWithLabel = computed(() => {
    switch (shareWith.value) {
      case 'everyone':
        return 'Everyone';
      case 'team':
        return 'Team';
      case 'specific':
        return 'Specific Users';
      default:
        return 'Select an option';
    }
  });
  
  const saveFile = async () => {
    try {
      // Validation to check if the file is selected
      if (!file.value) {
        toast({
          title: 'Error',
          description: 'Please select a file to upload.',
          variant: 'destructive',
        });
        return;
      }
  
      const formData = new FormData();
      formData.append('file', file.value);
      formData.append('shareWith', shareWith.value);
  
      const response = await getAPI.post('/api/files/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
  
      // Close the dialog and reset values
      closeDialog();
  
      toast({
        title: 'File Uploaded',
        description: 'Your file has been uploaded successfully.',
      });
  
      // Reset form fields
      file.value = null;
      shareWith.value = 'everyone';
  
    } catch (error) {
      console.error('Error uploading file:', error);
      toast({
        title: 'Error',
        description: 'An error occurred while uploading the file.',
        variant: 'destructive',
      });
    }
  };
  
  const closeDialog = () => {
    isDialogOpen.value = false;
  };
  
  const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target?.files?.length) {
      file.value = target.files[0];
    }
  };
  
  // Automatically open the dialog on component mount (or trigger it by other means)
  onMounted(() => {
    isDialogOpen.value = true;
  });
  </script>
  