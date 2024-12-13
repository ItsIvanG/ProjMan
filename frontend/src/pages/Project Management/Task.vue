<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/components/ui/popover';
import {
  Command,
  CommandInput,
  CommandEmpty,
  CommandList,
  CommandGroup,
  CommandItem,
} from '@/components/ui/command';
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter, CardHeader, CardDescription, CardTitle } from '@/components/ui/card'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Tabs,
  TabsContent,
} from '@/components/ui/tabs'
import {
  Pagination,
} from '@/components/ui/pagination'
import {
  ListFilter,
  MoreHorizontal,
} from 'lucide-vue-next'
import { computed, ref, watchEffect, reactive } from "vue";
import  AddTask  from '@/components/reusable/modals/taskmodal.vue'
import  EditTask  from '@/components/reusable/modals/edittaskmodal.vue'
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
  } from '@/components/ui/dialog';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import { PlusCircle , Check } from 'lucide-vue-next';


import { getAPI } from '@/axios';
import { useProjectStore } from '@/store/project';
import { useTaskStore } from '@/store/taskStore';
import { useAuthStore } from '@/store/auth'


const taskStore = useTaskStore();

// Reference for tasks
const allTasks = ref<any[]>([]); // Task data from API
  const selectedStatus = ref<string | null>(null);


// API URL (replace this with the actual backend URL)
const apiUrl = '/tasks/';

// Fetch tasks based on the project ID
const fetchTasks = async (projectId: number, status: string | null) => {
  try {
    if (!projectId) {
      throw new Error("Invalid project ID.");
    }
    let url = `${apiUrl}${projectId}/`;
    
    // Include the status in the query string if provided
    if (status) {
      url += `?status=${status}`;
    }

    // Send GET request to fetch tasks for the specific project_id and status
    const response = await getAPI.get(url);
    allTasks.value = response.data; // Store tasks in the allTasks ref
    
    // Log the fetched task data to the console
    console.log('Fetched tasks:', response.data);
  } catch (error) {
    console.error("Failed to fetch tasks:", error);
  }
};

// Reactive store for project ID
const projectStore = useProjectStore();
const projectId = computed(() => projectStore.project_id);

// Automatically fetch tasks when projectId changes
watchEffect(() => {
  const id = projectId.value;
  if (id) {
    fetchTasks(id, selectedStatus.value);
  }
});

const applyStatusFilter = (status: string) => {
  selectedStatus.value = status;
  const id = projectId.value;
  if (id) {
    fetchTasks(id, status); // Fetch tasks with the selected status filter
  }
};

// Helper function to get the variant for status
const getStatusVariant = (status: string) => {
  switch (status.toLowerCase()) {
    case 'not started':
      return 'destructive';
    case 'in progress':
      return 'inProgress';
    case 'completed':
      return 'completed';
    case 'cancelled':
      return 'cancelled';
    default:
      return 'default';
  }
};

const getSprintVariant = (sprint: string) => {
  switch (sprint.toLowerCase()) {
    case 'sprint 1':
      return 'sprint1';
    case 'sprint 2':
      return 'sprint2';
    case 'sprint 3':
      return 'sprint3';
    case 'sprint 4':
      return 'sprint4';
    case 'sprint 5':
      return 'sprint5';
    case 'sprint 6':
      return 'sprint6';
    case 'sprint 7':
      return 'sprint7';
    case 'sprint 8':
      return 'sprint8';
    case 'sprint 9':
      return 'sprint9';
    case 'sprint 10':
      return 'sprint10';
    case 'sprint 11':
      return 'sprint11';
    case 'sprint 12':
      return 'sprint12';
    case 'sprint 13':
      return 'sprint13';
    case 'sprint 14':
      return 'sprint14';
    case 'sprint 15':
      return 'sprint15';
    default:
      return 'default';
  }
};

// Helper function to get the variant for priority
const getPriorityVariant = (priority: string) => {
  switch (priority.toLowerCase()) {
    case 'high':
      return 'destructive';
    case 'medium':
      return 'medium';
    case 'low':
      return 'low';
    case 'very high':
      return 'veryhigh';
    default:
      return 'default';
  }
};

const members = ref<any[]>([]); 
// Fetch members based on manager_id
const fetchMembers = async (managerId: number) => {
  try {
    const response = await getAPI.get(`/manager/${managerId}/`);
    members.value = response.data.map((member: any) => ({
      value: member.id,
      label: member.name,
    }));
    console.log('Fetched members:', members.value);
  } catch (error) {
    console.error('Failed to fetch members:', error);
  }
};
const authStore = useAuthStore();
const managerId  = computed(() => authStore.user?.manager_id);
watchEffect(() => {
  const managerIdValue = managerId.value;
  if (managerIdValue) {
    fetchMembers(managerIdValue);
  }
});

// Selected member
const selectedMember = ref(null);

// Select a member
const selectMember = (member: any) => {
  selectedMember.value = member;
  formData.assignee_id = member.value;
};
  // Computed task ID
  const selectedTaskId = computed(() => taskStore.task?.task_id);

const isDialogOpen = ref(false);
  
  // Form data for editing the task
  const formData = reactive({
    assignee_id: '',
  });
  
  // Function to open the dialog
// Function to open the dialog
const openDialog = () => {
  if (!selectedTaskId.value) {
    console.error('No task ID selected.');
    return;
  }
  
  const task = taskStore.task;
  if (task) {
    // Populate the formData with the current values from the selected task
    formData.assignee_id = task.assignee_id || ''; // Set assignee_id or empty if not available
  }
  
  isDialogOpen.value = true; // Open the dialog
};



  
  // Function to close the dialog
  const closeDialog = () => {
    selectedMember.value = null;
    formData.assignee_id = '';
    isDialogOpen.value = false;
  };
  
  // Function to handle form submission for editing the task
  const handleSubmit = async () => {
  if (!selectedTaskId.value) {
    console.error('No task ID selected.');
    return;
  }

  // Check if the form is empty (e.g., assignee_id is not selected)
  if (!formData.assignee_id) {
    console.log('No assignee selected, closing the modal.');
    closeDialog(); // Close the modal if no assignee is selected
    return;
  }

  try {
    const response = await getAPI.put(
      `/tasks/assign/${selectedTaskId.value}/`,
      formData
    );
    console.log('Task updated:', response.data);

    // Update the task in the local store or state
    if (taskStore.task && selectedTaskId.value === taskStore.task.task_id) {
      Object.assign(taskStore.task, response.data); // Merge updated data into the store
    }

    closeDialog(); // Close the modal after successful update
  } catch (error) {
    console.error('Error updating task:', error);
  }
};





</script>


<template>
  <Tabs default-value="all">
    <div class="flex items-center">
      <CardHeader>
                <CardTitle>{{ projectStore.project_name }} </CardTitle>
                <CardDescription>
                  {{ projectStore.project_description }}
                </CardDescription>
              </CardHeader>
      <div class="ml-auto flex items-center gap-2">
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" size="sm" class="h-7 gap-1">
              <ListFilter class="h-3.5 w-3.5" />
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Filter
              </span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Filter by</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="applyStatusFilter('')">All</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Not Started')">Not Started</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('In Progress')">In Progress</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Completed')">Completed</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Cancelled')">Cancelled</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
<AddTask />
      </div>
    </div>
    <TabsContent value="all">
      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Tasks</TableHead>
                <TableHead>Features</TableHead>
                <TableHead>Status</TableHead>
                <TableHead class="hidden md:table-cell">Assigned</TableHead>
                <TableHead class="hidden md:table-cell">Sprint</TableHead>
                <TableHead class="hidden md:table-cell">Priority</TableHead>
                <TableHead class="hidden md:table-cell">Deadline</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="allTasks.length">
              <TableRow v-for="task in allTasks" :key="task.task_id">
                  <TableCell>{{task.task_code}}</TableCell>
                  <TableCell>{{ task.features }}</TableCell>
                  <TableCell>
                    <Badge :variant="getStatusVariant(task.status)">
                      {{ task.status }}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">
        <a
          href="#"
          @click.prevent="openDialog"
          @click="taskStore.setTask(task)"
        >
        {{ task.assignee || 'Assign Member' }}
        </a>
      </Badge>
</TableCell>

                  <TableCell class="hidden md:table-cell">
  <Badge :variant="getSprintVariant('Sprint ' + task.sprint)">
    Sprint {{ task.sprint }}
  </Badge>
</TableCell>


                  <TableCell class="hidden md:table-cell">
                    <Badge :variant="getPriorityVariant(task.priority)">
                      {{ task.priority }}
                    </Badge>
                  </TableCell>
                  <TableCell class="hidden md:table-cell">
                    {{ task.deadline }}
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger as-child>
                        <Button
                          aria-haspopup="true"
                          size="icon"
                          variant="ghost"
                          @click="taskStore.setTask(task)"
                        >
                          <MoreHorizontal class="h-4 w-4" />
                          <span class="sr-only">Toggle menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <EditTask />
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              </template>
              <template v-else>
  <TableRow>
    <TableCell colspan="8" class="text-center">  
      <p class="text-sm text-muted-foreground">
        No task available. Add a new task to get started.
      </p>
    </TableCell>
  </TableRow>
</template>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </TabsContent>
  </Tabs>
        <!-- Dialog for Task Editing -->
        <Dialog v-model:open="isDialogOpen" @close="closeDialog">
        <DialogContent >
          <DialogHeader>
            <DialogTitle class="text-2xl font-bold">Assign Task</DialogTitle>
            <DialogDescription class="text-md">
              Fill out the form below to assign the task. Provide the necessary details and click "Save changes."
            </DialogDescription>
          </DialogHeader>
  
          <form @submit.prevent="handleSubmit">
  <div class="grid gap-4 py-4 sm:grid-cols-1 md:grid-cols-2">
    <!-- Assign Member input -->
    <div class="grid gap-2 md:col-span-2">
      <Label for="assignee_id">Assign Member</Label>
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            class="w-full justify-between"
            aria-label="Select Member"
          >
            {{ selectedMember?.label || 'Select Member' }}
            <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent class="w-full p-0">
          <Command>
            <CommandInput placeholder="Search member..." />
            <CommandEmpty>No member found.</CommandEmpty>
            <CommandList>
              <CommandGroup>
                <CommandItem
                  v-for="(member, index) in members"
                  :key="member.value"
                  @click="selectMember(member)"
                  class="cursor-pointer"
                >
                  <Check
                    v-if="member.value === selectedMember?.value"
                    class="mr-2 h-4 w-4"
                  />
                  {{ member.label }}
                </CommandItem>
                <div
                  v-if="index < members.length - 1"
                  class="border-t border-gray-200 my-1"
                ></div>
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
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
</template>
