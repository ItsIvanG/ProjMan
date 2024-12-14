<script setup lang="ts">
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent } from '@/components/ui/tabs';
import { ListFilter } from 'lucide-vue-next';
import AddTask from '@/components/reusable/modals/taskmodal.vue';
import { CircleAlert, Circle, CircleCheckBig, CircleX, ArrowUpDown, ArrowUpRight, ArrowRight, ArrowDown } from 'lucide-vue-next';

import { computed, ref, watchEffect } from "vue";
import { useProjectStore } from '@/store/project';
import { useAllTasksStore } from '@/store/allTasksStore';
import { useAuthStore } from '@/store/auth';

const projectStore = useProjectStore();
const allTasksStore = useAllTasksStore();
const authStore = useAuthStore();

const selectedStatus = ref<string | null>(null);
const projectId = computed(() => projectStore.project_id);
const userRole = computed(() => authStore.user?.role);

// Automatically fetch tasks when projectId changes
watchEffect(() => {
  if (projectId.value) {
    allTasksStore.fetchTasks(projectId.value, selectedStatus.value);
  }
});

// Apply a status filter and fetch tasks
const applyStatusFilter = (status: string) => {
  selectedStatus.value = status;
  if (projectId.value) {
    allTasksStore.fetchTasks(projectId.value, status);
  }
};

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

// Helper functions for variants
const getVariant = (type: string, value: string) => {
  const variants: Record<string, Record<string, string>> = {
    status: {
      'not started': 'destructive',
      'in progress': 'inProgress',
      'completed': 'completed',
      'cancelled': 'cancelled',
    },
    sprint: {
      default: 'default',
      ...Array.from({ length: 15 }, (_, i) => ({ [`sprint ${i + 1}`]: `sprint${i + 1}` })).reduce((acc, cur) => ({ ...acc, ...cur }), {}),
    },
    priority: {
      high: 'high',
      medium: 'medium',
      low: 'low',
      'very high': 'veryhigh',
    },
  };

  return variants[type]?.[value.toLowerCase()] || 'default';
};

const uniqueSprints = computed(() => {
  return [...new Set(allTasksStore.allTasks.map(task => task.sprint))];
});

// Group tasks by sprint
const tasksGroupedBySprint = computed(() => {
  return allTasksStore.allTasks.reduce((acc, task) => {
    const sprint = task.sprint || 'default';
    if (!acc[sprint]) {
      acc[sprint] = [];
    }
    acc[sprint].push(task);
    return acc;
  }, {} as Record<string, typeof allTasksStore.allTasks>);
});

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

</script>

<template>
  <Tabs default-value="all">
    <div class="flex items-center">
      <CardHeader>
        <CardTitle>{{ projectStore.project_name }}</CardTitle>
        <CardDescription>{{ projectStore.project_description }}</CardDescription>
      </CardHeader>
      <div class="ml-auto flex items-center gap-2">
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" size="sm" class="h-7 gap-1">
              <ListFilter class="h-3.5 w-3.5" />
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">Filter</span>
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
                <!-- Sprint headers -->
                <TableHead v-for="sprint in uniqueSprints" :key="sprint">
                  <Badge :variant="getVariant('sprint', 'Sprint ' + sprint)">
                    Sprint {{ sprint }}
                  </Badge>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="Object.keys(tasksGroupedBySprint).length">
                <!-- Loop over tasks, and each task gets a row -->
                <TableRow v-for="task in allTasksStore.allTasks" :key="task.id">
                  <!-- Each task's sprint will go in the corresponding sprint column -->
                  <TableCell v-for="sprintIndex in uniqueSprints" :key="sprintIndex">
                    <div v-if="task.sprint === sprintIndex">
                      <!-- Render task details only if task belongs to this sprint -->
                      <div>{{ task.task_code }} : {{ task.features }}</div>
                      <div>
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
                      </div>
                      <div class="pt-2">
                        <Badge :variant="getPriorityVariant(task.priority)">
                          <template v-if="task.priority.toLowerCase() === 'low'">
                            <ArrowDown class="mr-2 h-4 w-4" /> {{ task.priority }}
                          </template>
                          <template v-if="task.priority.toLowerCase() === 'medium'">
                            <ArrowRight class="mr-2 h-4 w-4" /> {{ task.priority }}
                          </template>
                          <template v-if="task.priority.toLowerCase() === 'high'">
                            <ArrowUpRight class="mr-2 h-4 w-4" /> {{ task.priority }}
                          </template>
                          <template v-if="task.priority.toLowerCase() === 'very high'">
                            <ArrowUp class="mr-2 h-4 w-4" /> {{ task.priority }}
                          </template>
                        </Badge>
                      </div>
                    </div>
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
</template>
