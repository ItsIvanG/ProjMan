<script setup lang="ts">
import {computed, onMounted, ref, watch, watchEffect} from "vue";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select/";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { Button } from "@/components/ui/button/";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card/";
import { Input } from "@/components/ui/input/";
import { useAuthStore } from '@/store/auth'
import { toast } from "@/components/ui/toast/";
const authStore = useAuthStore();
const projectStore = useProjectStore();
const filteredTasks = ref([]);
const projectId = computed(() => projectStore.project_id);

const fetchTasks = async (projectId: number, assigneeId: number) => {
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
import {getAPI} from "@/axios.ts";
import {watchEffect} from "vue";
import {useProjectStore} from "@/store/project.ts";
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
    fetchTasks(id,authStore.user?.id);

    fetchTaskChart(projectId.value);

  }
});
</script>


<template>
  <Card class="md:col-span-4 col-span-1">
       <CardHeader>
        <CardTitle>Gantt Chart</CardTitle>
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
</template>


