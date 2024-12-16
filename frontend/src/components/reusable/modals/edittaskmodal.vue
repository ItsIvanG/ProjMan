<template>
  <div>
    <!-- Dropdown menu for actions -->
    <DropdownMenuContent align="end">
  
      <DropdownMenuItem v-if="userRole === 'Member'" @click="openDialog">
        Update Status
  </DropdownMenuItem>
  <DropdownMenuItem v-else @click="openDialog">
    Edit
  </DropdownMenuItem>
    </DropdownMenuContent>

    <!-- Dialog for Task Editing -->
    <Dialog v-model:open="isDialogOpen" @close="closeDialog">
      <DialogContent :class="{'max-w-2xl': userRole !== 'Member'}">
        <DialogHeader>
  <DialogTitle class="text-2xl font-bold" v-if="userRole !== 'Member'">
    Edit Task
  </DialogTitle>
  <DialogTitle class="text-2xl font-bold" v-if="userRole === 'Member'">
    Report Progress
  </DialogTitle>

  <DialogDescription class="text-lg" v-if="userRole !== 'Member'">
    Fill out the form below to edit the task. Provide the necessary details and click "Save changes."
  </DialogDescription>
  <DialogDescription class="text-lg" v-if="userRole === 'Member'">
    Provide an update on the task progress. Select the status and click "Save changes."
  </DialogDescription>
</DialogHeader>


        <form @submit.prevent="handleSubmit">
           <div class="grid gap-4 py-4 sm:grid-cols-1 md:grid-cols-2">
            <!-- Feature input should stay in one column -->
            <div class="grid gap-2" v-if="userRole !== 'Member'">
              <Label for="features">Features</Label>
              <Input
                id="features"
                v-model="formData.features"
                placeholder="Type features"
                required
              />
            </div>

            <!-- Sprint input -->
            <div class="grid gap-2" v-if="userRole !== 'Member'">
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
            <div class="grid gap-2 md:col-span-2" v-if="userRole === 'Member'" >
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

            <div class="grid gap-2" v-else>
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
            <div class="grid gap-2" v-if="userRole !== 'Member'">
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
<!-- Start date Date Picker -->
            <div class="grid gap-2" v-if="userRole !== 'Member'">
              <Label for="deadline">Start date</Label>
              <Input
                id="start_date"
                type="date"
                v-model="formData.start_date"
                required
              />
            </div>
            <!-- Deadline Date Picker -->
            <div class="grid gap-2" v-if="userRole !== 'Member'">
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
              Save changes
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
import { DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel } from '@/components/ui/dropdown-menu';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PlusCircle } from 'lucide-vue-next';
import { getAPI } from '@/axios';
import { useTaskStore } from '@/store/taskStore';
import { useToast } from '@/components/ui/toast/use-toast'
import { useAuthStore } from '@/store/auth'
import { useProjectStore } from '@/store/project.ts'
import {RangeCalendar} from "@/components/ui/range-calendar";
const authStore = useAuthStore()

const userRole = computed(() => authStore.user?.role);

const { toast } = useToast()
const projectStore = useProjectStore();
const taskStore = useTaskStore();
const selectedTaskId = computed(() => taskStore.task?.task_id); // Added null safety

const selectedTaskCode = computed(() => taskStore.task?.task_code); // Added null safety





// Dialog state
const isDialogOpen = ref(false);

// Form data for editing the task
const formData = reactive({
  features: '',
  sprint: '',
  status: '',
  priority: '',
  deadline: '',
  start_date:'',
});

// Function to open the dialog
const openDialog = () => {
  if (!selectedTaskId.value) {
    console.error('No task ID selected.');
    return;
  }

  // Populate formData directly from taskStore.task
  const task = taskStore.task;
  if (task) {
    formData.features = task.features || '';
    formData.sprint = task.sprint || '';
    formData.status = task.status || '';
    formData.priority = task.priority || '';
    formData.deadline = task.deadline || '';
        formData.start_date = task.start_date || '';

    formData.task_id = task.task_id || '';
    formData.task_code = task.task_code || '';
    formData.project = task.project || '';
  }

  isDialogOpen.value = true;
};

// Function to close the dialog
const closeDialog = () => {
  isDialogOpen.value = false;
};
  const userId = computed(() => authStore.user?.id);
// Function to handle form submission for editing the task
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
  if (!selectedTaskId.value) {
    console.error('No task ID selected.');
    return;
  }

  try {
    const response = await getAPI.put(`/tasks/edit/${selectedTaskId.value}/`, formData);
    console.log('Task updated:', response.data);

    // Conditionally set the toast message based on the user role
    if (userRole.value === 'Member') {
      toast({
        title: 'Report Progress',
        description: 'Your progress has been reported successfully.',
      });

         const logResponse =  getAPI.post(
      "/api/add-log/",
      {
              log_user_created: userId.value,
              log_content: "Set "+selectedTaskCode.value+" status to "+formData.status,
              log_user_concern: null,
              log_project: projectStore?.project_id
            });

               const logNotif = await getAPI.post(
      "/api/notifications/",
      {
              notification_user_created: userId.value,
              notification_content: "Set " + selectedTaskCode.value+  " status to "+formData.status+".",
              notification_user_concern: projectStore?.project_manager,
              notification_project: projectStore?.project_id
            });
    } else {
      toast({
        title: 'Task Edited',
        description: 'The task has been updated successfully.',
      });
    }

    // Ensure any previously lingering toasts are cleared after 3 seconds
    setTimeout(() => {
      // This can trigger any toast cleanup if needed
    }, 1000);

    // Update the task in the local store or state
    if (taskStore.task && selectedTaskId.value === taskStore.task.task_id) {
      Object.assign(taskStore.task, response.data); // Merge updated data into the store
    }

    closeDialog();
  } catch (error) {
    console.error('Error updating task:', error);
  }
};


</script>
