<script setup lang="ts">
import { useAuthStore } from '../store/auth'
import {CardDescription, CardHeader, CardTitle, Card, CardContent, CardFooter} from "@/components/ui/card";
import {Separator} from "@/components/ui/separator/";
import {Input} from "@/components/ui/input/";
import {useProjectStore} from "@/store/project.ts";
import {computed, onMounted, ref, watch, watchEffect} from "vue";
import {getAPI} from "@/axios.ts";
import {Button} from "@/components/ui/button/";
import {File, Archive, Check, Users, Circle, LayoutList, ArrowUpDown, CalendarClock, List} from "lucide-vue-next";
import ProjectModal from '@/components/reusable/modals/editprojectmodal.vue';
import Archiveprojectmodal from "@/components/reusable/modals/archiveprojectmodal.vue";
import router from "@/router";
import  popupproject  from '@/components/reusable/modals/popupproject.vue'
import {Table, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,} from "@/components/ui/select";

const projectStore = useProjectStore();

// Watch the `project_id` for changes


const authStore = useAuthStore()

const userRole = computed(() => authStore.user?.role);
const userId = computed(() => authStore.user?.id);

const user = ref(null);
//

// watch(
//   () => projectStore.project_id,
//   (newValue, oldValue) => {
//     console.log(`Project ID changed from ${oldValue} to ${newValue}`);
//     if (!newValue) {
//       console.log('Project ID was cleared.');
//     }
//   }
// );

if(!authStore.isAuthenticated){
  console.log("not logged in! going to login");
  router.push("/login");
}
const projectId = computed(() => projectStore.project_id);



const loading = ref(false); // Loading state
const error = ref<string | null>(null); // Error messag

const filteredTasks = ref([]);

const fetchTasks = async (projectId: number, assigneeId: number) => {
  loading.value = true;
  error.value = null; // Reset error

  try {
    const response = await getAPI.get('/api/tasks/filter/', {
      params: {
        project_id: projectId,
        assignee_id: assigneeId,
      },
    });

    console.log("Filtered tasks success: ",response.data);
    filteredTasks.value = response.data; // Update tasks with API response
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to fetch tasks.';
  } finally {
    loading.value = false;
  }
};

// Group tasks by sprint
const groupedTasks = ref({});

import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { format, differenceInDays, parseISO, eachDayOfInterval ,differenceInMonths, differenceInYears, } from "date-fns";
import {toast} from "@/components/ui/toast";
// Add state for grouping selection
const groupingLate = ref("day"); // Default is "day"
const startDateLate = ref("2024-12-01");
const endDateLate = ref("2024-12-15");
// State
const days = ref([]);
const tasks = ref([
]);

const grouping = ref();
const startDate = ref();
const endDate = ref();


const groupTasksBySprint = () => {
  groupedTasks.value = tasks.value.reduce((acc, task) => {
    if (!acc[task.sprint]) acc[task.sprint] = [];
    acc[task.sprint].push(task);
    return acc;
  }, {});
};

// Update generateDays to handle different groupings
const generateDays = () => {

  grouping.value = groupingLate.value;
  endDate.value = endDateLate.value;
  startDate.value = startDateLate.value;
  const parsedStart = parseISO(startDate.value);
  const parsedEnd = parseISO(endDate.value);
  if ( endDate.value <= startDate.value) {
     toast({
       title: 'Invalid Dates',
       description: 'Gantt chart start date must be before end date.',
       variant: 'destructive',
     });
     return;
   }
  // Clear the previous days array
  days.value = [];

  if (grouping.value === "day") {
    // Group by day
    days.value = eachDayOfInterval({ start: parsedStart, end: parsedEnd }).map((date) =>
      format(date, "MMM d")
    );
  } else if (grouping.value === "month") {
    // Group by month
    let currentMonth = parsedStart.getMonth();
    while (parsedStart <= parsedEnd) {
      days.value.push(format(parsedStart, "MMM yyyy"));
      parsedStart.setMonth(parsedStart.getMonth() + 1);
    }
  } else if (grouping.value === "year") {
    // Group by year
    let currentYear = parsedStart.getFullYear();
    while (parsedStart <= parsedEnd) {
      days.value.push(format(parsedStart, "yyyy"));
      parsedStart.setFullYear(parsedStart.getFullYear() + 1);
    }
  }
};

// Compute Task Bar Styles
const getTaskBarStyle = (task) => {
  if (!task.start_date || !task.deadline) return {};

  let totalIntervals = days.value.length;

  // Calculate the interval difference based on the selected grouping (Day, Month, Year)
  const taskStart = parseISO(task.start_date);
  const taskEnd = parseISO(task.deadline);

  // Get the date difference in terms of selected grouping (Days, Months, or Years)
  let taskStartIndex, taskEndIndex;

  if (grouping.value === "day") {
    taskStartIndex = differenceInDays(taskStart, parseISO(startDate.value));
    taskEndIndex = differenceInDays(taskEnd, parseISO(startDate.value));
  } else if (grouping.value === "month") {
    taskStartIndex = differenceInMonths(taskStart, parseISO(startDate.value));
    taskEndIndex = differenceInMonths(taskEnd, parseISO(startDate.value));
    totalIntervals = Math.ceil(differenceInMonths(parseISO(endDate.value), parseISO(startDate.value))) + 1;
  } else if (grouping.value === "year") {
    taskStartIndex = differenceInYears(taskStart, parseISO(startDate.value));
    taskEndIndex = differenceInYears(taskEnd, parseISO(startDate.value));
    totalIntervals = Math.ceil(differenceInYears(parseISO(endDate.value), parseISO(startDate.value))) + 1;
  }

  const left = `${(taskStartIndex / totalIntervals) * 100}%`;
  const width = `${((taskEndIndex - taskStartIndex + 1) / totalIntervals) * 100}%`;

  return { left, width };
};


interface TaskData {
  completed_percentage: number;
  non_completed_percentage: number;
  total_tasks: number;
  completed: number;
  ongoing :number;
  not_started: number;
}

const taskData = ref<TaskData>({
  completed_percentage: 0,
  non_completed_percentage: 0,
  total_tasks: 0,
  completed: 0,
  ongoing: 0,
  not_started: 0
});

const members = ref();


const errorMessage = ref<string>("");

const fetchUsersByManager = async (managerId: number) => {
  try {
    console.log("getting member number by manager ID: ",managerId);
    const response = await getAPI.get(`/users/manager/${managerId}/`);
    console.log("Mmber count: ",response.data.length);
    members.value = response.data.length;
  } catch (error) {
    errorMessage.value = "An error occurred while fetching the users.";
    console.error(error);
  }
};
const getTaskCompletionPercentage = async () => {
  try {
    const response = await getAPI.get(`/api/tasks/completion-percentage/`, {
      params: { project_id: projectId.value }
    });
    taskData.value = response.data;  // Update the task data
    console.log("taskdata: ",response.data)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.error || "An error occurred while fetching data.";
  }
};
const fetchTaskChart = async (projectId: number) => {
  try {
    console.log("getting task list for chart via projID: ",projectId);
    const response = await getAPI.get(`/tasks/${projectId}/`,
    {
      params: {
        excludeCancelled: "true", // Convert boolean to string for query
      },
    });

    tasks.value = response.data;
        console.log("Tasks: ",response.data);

        generateDays();
        groupTasksBySprint();
  } catch (error) {
    errorMessage.value = "An error occurred while fetching the users.";
    console.error(error);
  }
};

watchEffect(() => {
  const id = projectId.value;
  if (id) {
    fetchTasks(id,authStore.user?.id)
    getTaskCompletionPercentage()
    fetchTaskChart(projectId.value)
    fetchUsersByManager(projectStore.project_manager);
  }
});



let progress = 0;
const size = 200;
const strokeWidth = 10;

// Computed properties
const radius = computed(() => 50 - strokeWidth / 2); // Radius of the circle
const circumference = computed(() => 2 * Math.PI * radius.value); // Circumference
const offset = computed(
  () => circumference.value - (taskData.value.completed_percentage / 100) * circumference.value
);
const circleStyle = computed(() => ({
  strokeDasharray: `${circumference.value} ${circumference.value}`,
  strokeDashoffset: offset.value,
}));
</script>

<style scoped>

.progress-ring {
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

.progress-ring__background {
  fill: none;
  stroke:  theme(colors.secondary.DEFAULT);
}

.progress-ring__circle {
  fill: none;
  stroke: theme(colors.primary.DEFAULT); /* Progress color */
  transition: stroke-dashoffset 0.5s ease;
}

</style>
<template>
  <popupproject v-if="userRole === 'Manager' && !projectStore.project_id" />

  <div >
     <div class="flex items-center">
      <CardHeader v-if="projectStore?.project_name">
        <CardTitle>{{ projectStore?.project_name }} Dashboard</CardTitle>
        <CardDescription>
          View overall project progress and edit project settings.
        </CardDescription>
      </CardHeader>
        <CardHeader v-else>
          <CardTitle>No Project Available</CardTitle>
        <CardDescription>
          Add a new project to get started.
        </CardDescription>
       

      </CardHeader>
       <div class="ml-auto flex items-center gap-2">

        <ProjectModal v-if="userRole !== 'Member' && (userRole !== 'Manager' || projectStore.project_id)" />
<Archiveprojectmodal v-if="userRole !== 'Member' && (userRole !== 'Manager' || projectStore.project_id)" />


    </div>
     </div>

    <Separator class="mb-5"/>

    <!-- Authenticated User Details -->
<!--    <div  class="max-w-md mx-auto border p-4 rounded">-->
<!--      <h2 class="mb-4 text-lg font-medium">User Information</h2>-->
<!--      <ul class="space-y-2">-->
<!--        &lt;!&ndash; Loop Through All User Data &ndash;&gt;-->
<!--        <li v-for="(value, key) in authStore.user" :key="key" class="flex justify-between">-->
<!--          <span class="capitalize">{{ key }}</span>-->
<!--          <span>{{ value }}</span>-->
<!--        </li>-->
<!--      </ul>-->
<!--    </div>-->
  <div v-if="projectStore.project_name">

 <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-4">
   <Card class="md:col-span-2 md:row-span-2  col-span-1">
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>
          Project Progress
        </CardTitle>
      </CardHeader>
      <CardContent>
<!--        <Progress :model-value=taskData.completed_percentage />-->
      <div class="justify-center flex">
        <div class="w-[200px] h-[200px] relative">
    <svg
      class="progress-ring"
      :width="size"
      :height="size"
      viewBox="0 0 100 100"
    >
      <!-- Background Circle -->
      <circle
        class="progress-ring__background"
        cx="50"
        cy="50"
        r="45"
        :stroke-width="strokeWidth"
      />
      <!-- Progress Circle -->
      <circle
        class="progress-ring__circle"
        cx="50"
        cy="50"
        r="45"
        :stroke-width="strokeWidth"
        :style="circleStyle"
      />
    </svg>
    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-xl font-bold">{{ Math.round(taskData.completed_percentage) }}%</div>
  </div>
      </div>
      </CardContent>
   </Card>
   <Card >
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="text-sm font-medium">
          Members
        </CardTitle>
        <Users />
      </CardHeader>
      <CardContent>
        <div class="text-2xl font-bold">
          {{ members }}
        </div>

      </CardContent>
   </Card>
   <Card >
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="text-sm font-medium">
          Not yet started tasks
        </CardTitle>
        <Archive />
      </CardHeader>
      <CardContent>
        <div class="text-2xl font-bold">
          {{ taskData.not_started }}
        </div>

      </CardContent>
   </Card>
    <Card >
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="text-sm font-medium">
          Ongoing Tasks
        </CardTitle>
        <File />
      </CardHeader>
      <CardContent>
        <div class="text-2xl font-bold">
          {{ taskData.ongoing }}
        </div>

      </CardContent>
   </Card>
    <Card >
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="text-sm font-medium">
          Completed Tasks
        </CardTitle>
        <Check />
      </CardHeader>
      <CardContent>
        <div class="text-2xl font-bold">
         {{ taskData.completed }}
        </div>

      </CardContent>
   </Card>
</div>
     <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
       <!--Gantt Chart-->

    <Card class="md:col-span-4 col-span-1">
       <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Gantt Chart</CardTitle>
          <div class=" flex justify-end">
          <Button size="sm" variant="outline" class="mr-3" @click="router.push('/gantt')">
          Expand
        </Button>
          </div>
      </CardHeader>
      <CardContent>
      <!-- Gantt Chart Options -->
        <div class="mb-4 flex items-end gap-4">
  <div>
    <label for="grouping" class="block text-sm font-medium">Group By</label>
    <Select v-model="groupingLate">
    <SelectTrigger class="w-[180px]">
      <SelectValue placeholder="Select a fruit" />
    </SelectTrigger>
    <SelectContent>
      <SelectGroup>
        <SelectItem value="day">
          Day
        </SelectItem>
        <SelectItem value="month">
          Month
        </SelectItem>
        <SelectItem value="year">
          Year
        </SelectItem>
      </SelectGroup>
    </SelectContent>
  </Select>
  </div>
  <div>
    <label for="start-date" class="block text-sm font-medium">Start Date</label>
    <Input
      id="start-date"
      type="date"
      v-model="startDateLate"
      class="border rounded px-3 py-2 text-sm w-full"
    />
  </div>
  <div>
    <label for="end-date" class="block text-sm font-medium">End Date</label>
    <Input
      id="end-date"
      type="date"
      v-model="endDateLate"
      class="border rounded px-3 py-2 text-sm w-full"
    />
  </div>
  <Button
    @click="generateDays"
    class="px-4 py-2 mb-1 rounded text-sm"
  >
    Update Chart
  </Button>
</div>
        <div class="overflow-x-auto w-full">
  <div class="min-w-max w-full">
<!--Chart Header-->
<div class="flex items-center bg-secondary text-sm font-medium">
  <div class="w-40 px-4 py-2 border-r">Task</div>
  <div class="flex-1 grid" :style="{ gridTemplateColumns: `repeat(${days.length}, 1fr)` }">
    <div
      v-for="(day, index) in days"
      :key="index"
      class="text-center py-2 border-r"
    >
      {{ day }}
    </div>
  </div>
</div>

<!-- Update the Grouped Chart Rows -->
<div v-for="(group, sprint) in groupedTasks" :key="sprint">
  <div class="bg-secondary text-sm font-semibold px-4 py-1">
    Sprint {{ sprint }}
  </div>

  <div v-for="(task, index) in group" :key="index" class="flex items-center text-sm">
    <!-- Task Name -->
    <div class="w-40 px-4 py-1 border-r bg-card z-10">
      {{ task.features }}
    </div>

    <!-- Timeline -->
    <div class="relative flex-1 h-12 z-0">
      <Popover >
        <PopoverTrigger >
          <div v-if="task.status == 'Completed'"
            class="absolute h-5 rounded-md bg-secondary cursor-pointer z-20"
            :style="getTaskBarStyle(task)"
          ></div>
           <div v-else
            class="absolute h-5 rounded-md bg-primary cursor-pointer z-20"
            :style="getTaskBarStyle(task)"
          ></div>
        </PopoverTrigger>
        <PopoverContent>
          <div class="text-sm p-2">
            <p><strong>Task:</strong> {{ task.task_code }}</p>
            <p><strong>Start:</strong> {{ task.start_date }}</p>
            <p><strong>End:</strong> {{ task.deadline }}</p>
            <p><strong>Assignee:</strong> {{ task.assignee }}</p>
            <p><strong>Status:</strong> {{ task.status }}</p>
          </div>
        </PopoverContent>
      </Popover>
    </div>
  </div>
</div>
  </div>
        </div>

      </CardContent>
    </Card>
<!--       Ongoing tasks-->
 <Card class="md:col-span-2 col-span-1">
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>
          Your ongoing tasks
        </CardTitle>
       <div class=" flex justify-end">
          <Button size="sm" variant="outline" class="mr-3" @click="router.push('/task')">
          View All
        </Button>
        <CalendarClock />
       </div>
      </CardHeader>
      <CardContent>
    <Table >
            <TableHeader>
              <TableRow>
                <TableHead>
                Tasks
            </TableHead>
            <TableHead>
                  <div class="flex items-center">

                  Features </div></TableHead>
                <TableHead>
                  <div>
                 Deadline</div></TableHead>
              </TableRow>
              <TableRow v-for="task in filteredTasks">
                <TableCell>{{task.task_code}}</TableCell>
                <TableCell>{{ task.features }}</TableCell>
                <TableCell>{{ task.deadline }}</TableCell>
              </TableRow>
            </TableHeader>
    </Table>
      </CardContent>
   </Card>

  </div>




    <!-- Guest View -->
    <p v-if="!authStore.isAuthenticated">
      You are not logged in. 
      <router-link to="/login">Login</router-link>
    </p>
  </div>

  </div>
</template>

