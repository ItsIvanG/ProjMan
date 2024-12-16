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
          <DialogDescription class="text-lg">
            Fill out the form below to add a new task. Provide the necessary details and click "Add new task."
          </DialogDescription>
        </DialogHeader>

        <form @submit.prevent="handleSubmit">
          <div class="grid gap-4 py-4 sm:grid-cols-1 md:grid-cols-2">
            <!-- features input -->
            <div class="grid gap-3 ">
              <Label for="features">Features</Label>
              <Input
                id="features"
                v-model="formData.features"
                placeholder="Type features"
                required
              />
            </div>

            <!-- Sprint input -->
            <div class="grid gap-2">
              <Label for="sprint">Sprint</Label>
              <Input
                id="sprint"
                type="number"
                v-model="formData.sprint"
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

            <!-- Deadline Date Picker -->
            <div class="grid gap-2">
              <Label for="deadline">Start date</Label>
              <Input
                id="deadline"
                type="date"
                v-model="formData.start_date"
                required
              />
            </div>

             <div class="grid gap-2">
              <Label for="deadline">Deadline</Label>
              <Input
                id="deadline"
                type="date"
                v-model="formData.deadline"
                required
              />
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
import { ref, reactive, computed } from 'vue';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PlusCircle } from 'lucide-vue-next';
import { getAPI } from '@/axios';
import { useProjectStore } from '@/store/project';
import { useAllTasksStore } from '@/store/allTasksStore'; // Import the new allTasksStore
import { useToast } from '@/components/ui/toast/use-toast'

const { toast } = useToast()

const projectStore = useProjectStore();
const allTasksStore = useAllTasksStore(); // Use allTasksStore
const projectId = computed(() => projectStore.project_id);

// Form data for the task
const formData = reactive({
  features: '',
  sprint: '',
  status: '',
  priority: '',
  deadline: '',
  start_date:'',
});

// Dialog state
const isDialogOpen = ref(false);

// Open and Close Dialog
const openDialog = () => {
  isDialogOpen.value = true;
};

const closeDialog = () => {
  isDialogOpen.value = false;
};

// Handle form submission to create a new task
const handleSubmit = async () => {
    // Convert the start_date and deadline to Date objects for comparison
  const startDate = new Date(formData.start_date);
  const deadlineDate = new Date(formData.deadline);

  // Check if the deadline is after the start date
  if (deadlineDate <= startDate) {
    toast({
      title: 'Invalid Dates',
      description: 'The deadline must be after the start date.',
      variant: 'destructive',
    });
    return;  // Prevent form submission if validation fails
  }
  try {
    // Sending the task data to the backend API
    const response = await getAPI.post('/tasks/create/', {
      features: formData.features,
      sprint: formData.sprint,
      status: formData.status,
      assignee: null,
      project: projectId.value,
      priority: formData.priority,
      deadline: formData.deadline,
      start_date: formData.start_date,
    });

    toast({
      title: 'Task Created',
      description: 'Your task has been created successfully.',
    });

    // Ensure any previously lingering toasts are cleared after 3 seconds
    setTimeout(() => {
      // This can trigger any toast cleanup if needed
    }, 3000);

    // Use the store's addTask method to add the new task to the task list
    allTasksStore.addTask(response.data);

    // Close the dialog and reset the form data
    closeDialog();
    formData.features = '';
    formData.sprint = '';
    formData.status = '';
    formData.priority = '';
    formData.deadline = '';
  } catch (error) {
    console.error('Error creating task:', error);
  }
};
</script>


