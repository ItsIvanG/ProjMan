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

const isAssignee = (task: any) => {
  return task.assignee === authStore.user?.name;
};

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
            <DropdownMenuItem @click="applyStatusFilter('Not started')">Not Started</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('In Progress')">In Progress</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Completed')">Completed</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Cancelled')">Cancelled</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <AddTask v-if="userRole !== 'Member'" />
      </div>
    </div>
    <TabsContent value="all">
      <Card>
        <CardContent>
          <Table>
            <TableHeader>
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
                <TableHead class="hidden md:table-cell">  <div class="flex items-center">
    <Users class="mr-2 h-4 w-4" />Assigned</div></TableHead>
                <TableHead class="hidden md:table-cell">  <div class="flex items-center">
    <List class="mr-2 h-4 w-4" />Sprint</div></TableHead>
                <TableHead class="hidden md:table-cell">  <div class="flex items-center">
    <ArrowUpDown class="mr-2 h-4 w-4" />Priority</div></TableHead>
                 <TableHead class="hidden md:table-cell">  <div class="flex items-center">
    <CalendarClock  class="mr-2 h-4 w-4" />Start date</div></TableHead>
                <TableHead class="hidden md:table-cell">  <div class="flex items-center">
    <CalendarClock  class="mr-2 h-4 w-4" />Deadline</div></TableHead>
    <TableHead v-if="allTasksStore.allTasks.some(task => isAssignee(task) || userRole === 'Manager')">
  Actions
</TableHead>

              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="allTasksStore.allTasks.length">
              <TableRow v-for="task in allTasksStore.allTasks.filter(isAssignee)" :key="task.id " >
                  <TableCell>{{task.task_code}}</TableCell>
                  <TableCell>{{ task.features }}</TableCell>
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

                  <TableCell>
  <Badge variant="outline">
    <template v-if="userRole !== 'Member'">
      <a
        href="#"
        @click.prevent="openDialog"
        @click="taskStore.setTask(task)"
      >
        {{ task.assignee || 'Assign Member' }}
      </a>
    </template>
    <template v-else>
      <span>{{ task.assignee || 'Assign Member' }}</span>
    </template>
  </Badge>
</TableCell>


                  <TableCell class="hidden md:table-cell">
  <Badge :variant="getSprintVariant('Sprint ' + task.sprint)">
    Sprint {{ task.sprint }}
  </Badge>
</TableCell>


<TableCell class="hidden md:table-cell">
                    <Badge :variant="getPriorityVariant(task.priority)">
    <template v-if="task.priority.toLowerCase() === 'low'">
      <ArrowDown  class="mr-2 h-4 w-4" /> {{ task.priority }}
    </template>
    <template v-if="task.priority.toLowerCase() === 'medium'">
      <ArrowRight  class="mr-2 h-4 w-4" /> {{ task.priority }}
    </template>
    <template v-if="task.priority.toLowerCase() === 'high'">
      <ArrowUpRight  class="mr-2 h-4 w-4" /> {{ task.priority }}
    </template>
    <template v-if="task.priority.toLowerCase() === 'very high'">
      <ArrowUp  class="mr-2 h-4 w-4" /> {{ task.priority }}
    </template>
  </Badge>
</TableCell>

                   <TableCell class="hidden md:table-cell">
                    {{ task.start_date }}
                  </TableCell>
                  <TableCell class="hidden md:table-cell">
                    {{ task.deadline }}
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger as-child>
                        <Button
                        v-if="(isAssignee(task) || userRole === 'Manager')"
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
      <template v-if="userRole === 'Member'">
        No task available. Contact the project manager to add a new task.
      </template>
      <template v-else>
        No task available. Add a new task to get started.
      </template>
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
      <Select v-model="formData.assignee_id" aria-label="Select Member">
        <SelectTrigger>
          <SelectValue 
            :placeholder="selectedMember?.label || 'Select Member'" 
          />
        </SelectTrigger>
        <SelectContent>
          <SelectItem 
            v-for="(member, index) in members" 
            :key="member.value" 
            :value="member.value"
          >
            {{ member.label }}
          </SelectItem>
        </SelectContent>
      </Select>
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
