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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
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
  import { PlusCircle , List , ArrowUpDown, Users,  CaseSensitive , Circle,CircleCheckBig, CircleX, CircleAlert, ArrowDown , ArrowUp , ArrowRight , ArrowUpRight,LayoutList, CalendarClock     } from 'lucide-vue-next';
  import { useToast } from '@/components/ui/toast/use-toast'

const { toast } = useToast()


import { getAPI } from '@/axios';
import { useProjectStore } from '@/store/project';
import { useTaskStore } from '@/store/taskStore';
import { useAuthStore } from '@/store/auth'
import { useAllTasksStore } from '@/store/allTasksStore';

const taskStore = useTaskStore();
const allTasksStore = useAllTasksStore();

const groupedTasks = computed(() => {
  const grouped: Record<string, any[]> = {};
  
  allTasksStore.allTasks.forEach((task) => {
    const sprint = `Sprint ${task.sprint}`;
    if (!grouped[sprint]) {
      grouped[sprint] = [];
    }
    grouped[sprint].push(task);
  });
  
  return grouped;
});

  const selectedStatus = ref<string | null>(null);
const projectStore = useProjectStore();
const projectId = computed(() => projectStore.project_id);

// Automatically fetch tasks when projectId changes
watchEffect(() => {
  const id = projectId.value;
  if (id) {
    allTasksStore.fetchTasks(id, selectedStatus.value); // Fetch tasks from the store
  }
});

const applyStatusFilter = (status: string) => {
  selectedStatus.value = status;
  const id = projectId.value;
  if (id) {
    allTasksStore.fetchTasks(id, status); // Fetch tasks with the selected status filter
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
      return 'high';
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
const userRole = computed(() => authStore.user?.role);
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
  const selectedTask = taskStore.task;
  if (!selectedTask) {
    console.error('No task selected');
    return;
  }

  if (!formData.assignee_id) {
    console.log('No assignee selected, closing the modal');
    closeDialog();
    return;
  }

  try {
    const response = await getAPI.put(`/tasks/assign/${selectedTask.task_id}/`, formData);
    console.log('Task updated:', response.data);

    toast({
  title: 'Member Assigned',
  description: 'The member has been assigned to the task successfully.',
});

// Ensure any previously lingering toasts are cleared after 3 seconds
setTimeout(() => {
  // This can trigger any toast cleanup if needed
}, 3000);

    // Update the task in the store
    taskStore.task = response.data;
    allTasksStore.updateTask(response.data); // Update the task list with the new data

    closeDialog();
  } catch (error) {
    console.error('Error updating task:', error);
  }
};





</script>


<template>
    <Tabs default-value="all">
      <div class="flex items-center">
        <CardHeader>
          <CardTitle>{{ projectStore.project_name }}</CardTitle>
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
              <DropdownMenuItem @click="applyStatusFilter('Not started')">Not Started</DropdownMenuItem>
              <DropdownMenuItem @click="applyStatusFilter('In Progress')">In Progress</DropdownMenuItem>
              <DropdownMenuItem @click="applyStatusFilter('Completed')">Completed</DropdownMenuItem>
              <DropdownMenuItem @click="applyStatusFilter('Cancelled')">Cancelled</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <AddTask v-if="userRole !== 'Member'" />
        </div>
      </div>
      <TabsContent value="all" >
  <div v-if="Object.keys(groupedTasks).length" class="flex flex-wrap gap-6 grid grid-cols-3">
    <!-- Render each sprint as a section -->
    <div
      v-for="(tasks, sprint) in groupedTasks"
      :key="sprint"
      class="flex-1 min-w-[300px]  bg-background shadow-lg rounded-lg overflow-hidden"
    >
      <!-- Sprint Card -->
      <Card class="h-full col-span-1">
        <!-- Sprint Header -->
        <CardHeader class="py-4 px-6">
  <Badge 
    :variant="getSprintVariant(sprint)" 
    class="flex items-center justify-center text-md px-2 py-1 font-medium"
  >
    {{ sprint }}
  </Badge>
</CardHeader>


        <!-- Card Content -->
        <CardContent class="p-4">
          <Table class="w-full border-collapse">
            <TableHeader class="border-b">
              <TableRow>
                <TableHead>
    Tasks

</TableHead>
                <TableHead>
                  <div class="flex items-center">
    <LayoutList class="mr-2 h-4 w-4" />
                  Features </div></TableHead>
                <TableHead>  <div class="flex items-center">
    <Circle class="mr-2 h-4 w-4" />Status</div></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <!-- Tasks for the current sprint -->
              <TableRow
                v-for="task in tasks"
                :key="task.id"
                class="hover:bg-muted transition-colors"
              >
              <TableCell>{{task.task_code}}</TableCell>
                <TableCell class="py-2 px-4 text-sm text-foreground">
                  {{ task.features }}
                </TableCell>
                <TableCell>
  <Badge :variant="getStatusVariant(task.status)">
    <template v-if="task.status.toLowerCase() === 'not started'">
      <CircleAlert class="mr-2 h-4 w-4" /> {{ task.status }}
    </template>
    <template v-if="task.status.toLowerCase() === 'in progress'">
      <Circle class="mr-2 h-4 w-4" /> {{ task.status }}
    </template>
    <template v-if="task.status.toLowerCase() === 'completed'">
      <CircleCheckBig class="mr-2 h-4 w-4" /> {{ task.status }}
    </template>
    <template v-if="task.status.toLowerCase() === 'cancelled'">
      <CircleX class="mr-2 h-4 w-4" /> {{ task.status }}
    </template>
  </Badge>
</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  </div>

  <!-- No Tasks Fallback -->
  <template v-else>
    <Card class="text-center shadow-lg rounded-lg p-6 bg-muted">
      <CardContent>
        <p class="text-sm text-muted-foreground">
          <template v-if="userRole === 'Member'">
            No tasks available. Contact the project manager to add tasks.
          </template>
          <template v-else>
            No tasks available. Add a new task to get started.
          </template>
        </p>
      </CardContent>
    </Card>
  </template>
</TabsContent>


    </Tabs>
  
  </template>
  
