<script setup lang="ts">
import { useProjectStore } from '@/store/project';
import { computed, ref, watchEffect } from "vue";
import Draggable from "vuedraggable";
import { getAPI } from "@/axios.js";
import { useAuthStore } from "@/store/auth.ts";
import { toast } from "@/components/ui/toast";
import {CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {
  DropdownMenu, DropdownMenuContent,
  DropdownMenuItem, DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import AddTask from "@/components/reusable/modals/taskmodal.vue";
import {Button} from "@/components/ui/button";
import {ListFilter} from "lucide-vue-next";
import {Badge} from "@/components/ui/badge";

const initialTasks = ref([
  {
    task_id: 1,
    task_code: "TASK-001",
    features: "Feature A",
    status: "Not started",
    assignee: null,
    sprint: 1,
    priority: "High",
    deadline: "2024-12-20",
    start_date: "2024-12-10",
    project: 1,
  },
  {
    task_id: 2,
    task_code: "TASK-002",
    features: "Feature B",
    status: "In Progress",
    assignee: null,
    sprint: 1,
    priority: "Medium",
    deadline: "2024-12-22",
    start_date: "2024-12-11",
    project: 1,
  },
  {
    task_id: 3,
    task_code: "TASK-003",
    features: "Feature C",
    status: "Completed",
    assignee: null,
    sprint: 1,
    priority: "Low",
    deadline: "2024-12-25",
    start_date: "2024-12-12",
    project: 1,
  },
]);

const error = ref<string | null>(null); // Error message

// Reactive Kanban columns
const taskColumns = ref({
  "Not started": [],
  "In Progress": [],
  "Completed": [],
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
// Handle cloning of tasks during drag
const cloneTask = (task) => ({ ...task });
const onDragEnd = async (event) => {
  console.log('onDragEnd');

  // Access the task directly from the event
  const task = event.item ? event.item.__draggable_context.element : null;

  // Check if task exists
  if (!task) {
    console.error('Task not found in event');
    return;
  }

  // Access the new column name (status) from the event.to element
  const newColumnElement = event.to.closest('[data-column]'); // Get the closest element with the data-column
  const newColumn = newColumnElement ? newColumnElement.dataset.column : null;

  // Check if new column is found
  if (!newColumn) {
    console.error('Column not found');
    return;
  }

  // Update the task status based on the new column
  const updatedTaskData = {
    ...task,
    status: newColumn, // Update the status to match the new column
  };
  console.log('Updating task with data: ', updatedTaskData);

  try {
    // API call to update the task status
    const response = await getAPI.put(`/tasks/edit/${task.task_id}/`, updatedTaskData);
    console.log('Task updated:', response.data);

    // Toast notification for success
    toast({
      title: 'Task status updated',
      description: 'Your progress has been updated successfully.',
    });

    // Log the update
    await getAPI.post("/api/add-log/", {
      log_user_created: userId.value,
      log_content: `Set ${task.task_code} status to ${newColumn}`,
      log_user_concern: null,
      log_project: projectStore?.project_id,
    });

    // Send notification
    await getAPI.post("/api/notifications/", {
      notification_user_created: userId.value,
      notification_content: `Set ${task.task_code} status to ${newColumn}.`,
      notification_user_concern: projectStore?.project_manager,
      notification_project: projectStore?.project_id,
    });
  } catch (error) {
    console.error('Error updating task:', error);
    toast({
      title: 'Error',
      description: 'There was an error updating the task.',
    });
  }
};


const projectStore = useProjectStore();
console.log('Project Name:', projectStore.project_name);
console.log('Project ID:', projectStore.project_id);
console.log('Project Description:', projectStore.project_description);

const fetchTasks = async (projectId: number, assigneeId: number) => {
  try {
    const response = await getAPI.get('/api/tasks/filter/', {
      params: {
        project_id: projectId,
        assignee_id: assigneeId,
        status: "completed",
      },
    });

    console.log("Filtered tasks success: ", response.data);
    initialTasks.value = response.data; // Update tasks with API response
    console.log("initial tasks: ", initialTasks.value);

    taskColumns.value = {
      "Not started": initialTasks.value.filter((task) => task.status === "Not started"),
      "In Progress": initialTasks.value.filter((task) => task.status === "In Progress"),
      "Completed": initialTasks.value.filter((task) => task.status === "Completed"),
    };
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to fetch tasks.';
  }
};

const authStore = useAuthStore();
const projectId = computed(() => projectStore.project_id);
const userId = computed(() => authStore.user?.id);

watchEffect(() => {
  const id = projectId.value;
  if (id) {
    fetchTasks(id, authStore.user?.id);
  }
});


</script>

<template>
  <div class="flex items-center">
        <CardHeader>
          <CardTitle>{{ projectStore.project_name }} Kanban Board</CardTitle>
          <CardDescription>
            Drag and drop tasks to set its status.
          </CardDescription>
        </CardHeader>

      </div>
  <div class="flex gap-4 p-4 unselectable">
    <div
      v-for="(tasks, column) in taskColumns"
      :key="column"
      class="w-1/3 border rounded-lg p-4"
      :data-column="column"
    >
      <h2 class="font-semibold text-lg mb-4 text-center ">
<Badge :variant="getStatusVariant(column)" class="flex items-center justify-center text-md px-2 py-1 ">
  {{ column }}
</Badge>      </h2>
      <Draggable
        v-model="taskColumns[column]"
        group="tasks"
        :clone="cloneTask"
        :item-key="'task_id'"
        @end="onDragEnd"
      >
        <template #item="{ element }">
          <div class="bg-secondary shadow rounded-lg p-3 mb-3">
            <h3 class="font-medium">{{ element.features }}</h3>
            <h3 class="font-medium text-sm">{{ element.task_code }}</h3>
            <Badge :variant="getSprintVariant('Sprint ' + element.sprint)">
            <p class="text-xs">Sprint: {{ element.sprint }}</p>
                </Badge><br>
                <Badge :variant="getPriorityVariant(element.priority)">
            <p class="text-xs">Priority: {{ element.priority }}</p>
                </Badge>
            <p class="text-xs">Deadline: {{ element.deadline }}</p>
          </div>
        </template>
      </Draggable>
    </div>
  </div>
</template>

<style scoped>
.unselectable {
    -moz-user-select: -moz-none;
    -khtml-user-select: none;
    -webkit-user-select: none;
    -o-user-select: none;
    user-select: none;
}
</style>