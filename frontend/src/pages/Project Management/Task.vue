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
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
} from '@/components/ui/pagination'
import {
  ListFilter,
  MoreHorizontal,
  PlusCircle,
} from 'lucide-vue-next'
import { computed, ref } from "vue";
import  AddTask  from '@/components/reusable/modals/taskmodal.vue'
import  EditTask  from '@/components/reusable/modals/edittaskmodal.vue'


// Sample tasks data
const allTasks = ref([
  {
    name: "Task-01",
    features: "UI/UX enhancements",
    status: "Not Started",
    priority: "High",
    assign: "Kean Lucas",
    sprint: "Sprint 1",
  },
  {
    name: "Task-02",
    features: "Auth system",
    status: "In progress",
    priority: "Medium",
    assign: "Kean Lucas",
    sprint: "Sprint 1"
  },
  {
    name: "Task-03",
    features: "Monthly summary",
    status: "Completed",
    priority: "Low",
    assign: "Kean Lucas",
    sprint: "Sprint 2"
  },
  {
    name: "Task-04",
    features: "Monthly summary",
    status: "Cancelled",
    priority: "Very High",
    assign: "Kean Lucas",
    sprint: "Sprint 2"
  },
  {
    name: "Task-05",
    features: "Performance optimization",
    status: "In progress",
    priority: "Medium",
    assign: "Kean Lucas",
    sprint: "Sprint 3"
  },
  {
    name: "Task-06",
    features: "Bug fixing",
    status: "Not Started",
    priority: "High",
    assign: "Kean Lucas",
    sprint: "Sprint 3"
  },
]);

// Pagination settings
const currentPage = ref(1);
const itemsPerPage = 5;

// Paginated tasks
const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return allTasks.value.slice(start, start + itemsPerPage);
});

// Total number of pages
const totalPages = computed(() =>
  Math.ceil(allTasks.value.length / itemsPerPage)
);

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
                <CardTitle>Project 1 (Placeholder) </CardTitle>
                <CardDescription>
                  Project descriptioooooooooooon.
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
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="paginatedTasks.length">
                <TableRow v-for="(task, index) in paginatedTasks" :key="index">
                  <TableCell>{{ task.name }}</TableCell>
                  <TableCell>{{ task.features }}</TableCell>
                  <TableCell>
                    <Badge :variant="getStatusVariant(task.status)">
                      {{ task.status }}
                    </Badge>
                  </TableCell>
                  <TableCell class="hidden md:table-cell">
                    {{ task.assign }}
                  </TableCell>
                  <TableCell class="hidden md:table-cell">
  <Badge :variant="getSprintVariant(task.sprint)">
    {{ task.sprint }}
  </Badge>
</TableCell>

                  <TableCell class="hidden md:table-cell">
                    <Badge :variant="getPriorityVariant(task.priority)">
                      {{ task.priority }}
                    </Badge>
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
              </template>
              <template v-else>
                <TableRow>
                  <TableCell colspan="6" class="text-center">
                    <p class="text-sm text-muted-foreground">
                      No tasks available. Add a new task to get started.
                    </p>
                  </TableCell>
                </TableRow>
              </template>
            </TableBody>
          </Table>
        </CardContent>
        <CardFooter class="flex justify-between items-center">
          <div class="text-xs text-muted-foreground">
            Showing <strong>{{ (currentPage - 1) * itemsPerPage + 1 }}</strong> to
            <strong>{{ Math.min(currentPage * itemsPerPage, allTasks.length) }}</strong>
            of <strong>{{ allTasks.length }}</strong> tasks
          </div>
          <Pagination
            :current-page="currentPage"
            :total-pages="totalPages"
            @page-change="currentPage = $event"
          />
        </CardFooter>
      </Card>
    </TabsContent>
  </Tabs>
</template>
