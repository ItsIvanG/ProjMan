<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
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
import { computed, ref, watchEffect } from "vue";
import  AddTask  from '@/components/reusable/modals/taskmodal.vue'
import  EditTask  from '@/components/reusable/modals/edittaskmodal.vue'


import { getAPI } from '@/axios';
import { useProjectStore } from '@/store/project';

// Reference for tasks
const allTasks = ref<any[]>([]); // Task data from API

// API URL (replace this with the actual backend URL)
const apiUrl = '/tasks/';

// Fetch tasks based on the project ID
const fetchTasks = async (projectId: number) => {
  try {
    if (!projectId) {
      throw new Error("Invalid project ID.");
    }
    // Send GET request to fetch tasks for the specific project_id
    const response = await getAPI.get(`${apiUrl}${projectId}/`);
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
    fetchTasks(id);
  }
});

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
            <DropdownMenuItem>Not Started</DropdownMenuItem>
            <DropdownMenuItem>In Progress</DropdownMenuItem>
            <DropdownMenuItem>Completed</DropdownMenuItem>
            <DropdownMenuItem>Cancelled</DropdownMenuItem>
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

              <TableRow v-for="task in allTasks" :key="task.task_id">
                  <TableCell>{{task.task_code}}</TableCell>
                  <TableCell>{{ task.features }}</TableCell>
                  <TableCell>
                    <Badge :variant="getStatusVariant(task.status)">
                      {{ task.status }}
                    </Badge>
                  </TableCell>
                  <TableCell class="hidden md:table-cell">
                    {{ task.assignee }}
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
                        >
                          <MoreHorizontal class="h-4 w-4" />
                          <span class="sr-only">Toggle menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <EditTask />
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </TabsContent>
  </Tabs>
</template>
