<template>
  <div class="p-6">
    <!-- Filter, Print, and Progress Section -->
    <div class="flex justify-between items-center mb-6">
      <!-- Title Before Status Filter and Print -->
      <div class="flex items-center">
        <h3 class="text-xl font-semibold">Task Actions</h3>
      </div>

      <!-- Filter and Print Buttons Section -->
      <div class="flex items-center space-x-4 ml-auto">
        <!-- Status Filter with Dropdown Menu -->
        <DropdownMenu>
          <DropdownMenuTrigger class="px-3 py-1 border rounded w-32 text-left flex justify-center items-center">
            {{ statusFilter || "Select Status" }}
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem @click="setStatusFilter('')">All</DropdownMenuItem>
            <DropdownMenuItem @click="setStatusFilter('Completed')">Completed</DropdownMenuItem>
            <DropdownMenuItem @click="setStatusFilter('In Progress')">In Progress</DropdownMenuItem>
            <DropdownMenuItem @click="setStatusFilter('Not Started')">Not Started</DropdownMenuItem>
            <DropdownMenuItem @click="setStatusFilter('Cancelled')">Cancelled</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <!-- Print Report Button with Imported Style -->
        <button
          @click="printReport"
          class="px-3 py-1 border rounded w-32 text-left text-sm flex justify-center items-center"
        >
          Print Report
        </button>
      </div>
    </div>

    <!-- Progress Title Below the Buttons -->
    <div class="flex justify-between mb-6">
      <h3 class="text-lg font-semibold">Progress</h3>
      <span class="text-xs font-semibold">{{ progressPercentage }}%</span>
    </div>

    <!-- Progress Bar Section -->
    <div class="mb-6">
      <div class="relative pt-1">
        <div class="flex mb-2 items-center justify-between">
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div
              class="h-2.5 rounded-full bg-gray-700"
              :style="{ width: progressPercentage + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Task List Section -->
    <section>
      <h2 class="text-xl font-semibold mb-4">Task List</h2>
      <div
        v-for="(task, index) in filteredTasks"
        :key="index"
        class="p-4 mb-2 border rounded flex justify-between items-center"
      >
        <div>
          <p class="font-bold">{{ task.name }}</p>
          <p class="text-sm text-gray-500">
            Due: {{ task.dueDate }} | Priority: {{ task.priority }}
          </p>
        </div>
        <p :class="taskStatusClass(task.status)">{{ task.status }}</p>
      </div>
      <p v-if="filteredTasks.length === 0" class="text-center text-gray-500">
        No tasks to display.
      </p>
    </section>

    <!-- Performance Metrics Section -->
    <section class="mt-8">
      <h3 class="text-xl font-semibold mb-4">Performance Metrics</h3>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p><strong>Efficiency:</strong> 90%</p>
        </div>
        <div>
          <p><strong>Time to Completion:</strong> 4 hours</p>
        </div>
        <div>
          <p><strong>Quality of Work:</strong> 4.5/5</p>
        </div>
      </div>

      <h4 class="text-lg font-semibold mt-6 mb-2">Milestones and Achievements</h4>
      <ul class="list-disc pl-5">
        <li>Completed 7 out of 10 tasks</li>
        <li>Met 80% of deadlines</li>
      </ul>

      <h4 class="text-lg font-semibold mt-6 mb-2">Actionable Insights</h4>
      <h5 class="font-semibold">Areas for Improvement:</h5>
      <ul class="list-disc pl-5">
        <li>Improve task completion speed</li>
        <li>Reduce time spent on low priority tasks</li>
      </ul>
      <h5 class="font-semibold mt-4">Next Steps:</h5>
      <ul class="list-disc pl-5">
        <li>Focus on completing pending tasks</li>
        <li>Improve task prioritization</li>
      </ul>
    </section>
  </div>
</template>

<script>
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
// Import the style of Print Button from the taskmodal component
import AddTask from "@/components/reusable/modals/taskmodal.vue";

export default {
  components: {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
    AddTask, // Register the component
  },
  data() {
    return {
      statusFilter: "", // Default state showing all tasks
      tasks: [
        { name: "Task 1", status: "Completed", dueDate: "2024-12-01", priority: "High" },
        { name: "Task 2", status: "In Progress", dueDate: "2024-12-05", priority: "Medium" },
        { name: "Task 3", status: "Not Started", dueDate: "2024-12-10", priority: "Low" },
        { name: "Task 4", status: "Cancelled", dueDate: "2024-11-30", priority: "High" },
        { name: "Task 5", status: "In Progress", dueDate: "2024-12-02", priority: "Medium" },
        { name: "Task 6", status: "Not Started", dueDate: "2024-12-15", priority: "Low" },
        { name: "Task 7", status: "Completed", dueDate: "2024-12-01", priority: "High" },
      ],
    };
  },
  computed: {
    // Filters tasks based on the status selected
    filteredTasks() {
      if (this.statusFilter) {
        return this.tasks.filter((task) => task.status === this.statusFilter);
      }
      return this.tasks;
    },
    // Calculate the percentage of completed tasks
    progressPercentage() {
      const completedTasks = this.tasks.filter(task => task.status === 'Completed').length;
      return Math.round((completedTasks / this.tasks.length) * 100);
    },
  },
  methods: {
    setStatusFilter(status) {
      this.statusFilter = status;
    },
    taskStatusClass(status) {
      switch (status) {
        case "Completed":
          return "text-green-500";
        case "In Progress":
          return "text-yellow-500";
        case "Cancelled":
          return "text-red-500";
        default:
          return "text-gray-500";
      }
    },
    printReport() {
      window.print();
    },
  },
};
</script>
