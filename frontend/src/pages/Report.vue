<script setup lang="ts">
import {computed, defineComponent, ref, watchEffect, onMounted} from "vue";
import { Button } from '@/components/ui/button'
import {
  DropdownMenu, DropdownMenuContent,
  DropdownMenuItem, DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import {Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle} from '@/components/ui/card'
import {
  ArrowDown,
  ArrowRight, ArrowUp, ArrowUpDown,
  ArrowUpRight,
  CalendarClock, Circle,
  CircleAlert,
  CircleCheckBig, CircleX, LayoutList,
  List,
  ListFilter, MoreHorizontal,
  PlusCircle, Users
} from "lucide-vue-next";
import {getAPI} from "@/axios.ts";
import {useAuthStore} from "@/store/auth.ts";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {Badge} from "@/components/ui/badge";
import AddTask from "@/components/reusable/modals/taskmodal.vue";
import {Tabs, TabsContent} from "@/components/ui/tabs";
import EditTask from "@/components/reusable/modals/edittaskmodal.vue";

const userId = computed(() => authStore.user?.id);
import { useProjectStore } from '@/store/project';
import {useTaskStore} from "@/store/taskStore.ts";
import {useAllTasksStore} from "@/store/allTasksStore.ts";
const projectStore = useProjectStore();
  const selectedStatus = ref<string | null>(null);
const projectId = computed(() => projectStore.project_id);
const taskStore = useTaskStore();
const allTasksStore = useAllTasksStore();
// Automatically fetch tasks when projectId changes
const now = new Date(); // Create a new Date object for the current date and time
const logs = ref<any[]>([]);
const currentDate = ref(""); // Format as MM/DD/YYYY (locale-specific)
const currentTime = ref(""); // Fo

import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import ProjectModal from "@/components/reusable/modals/editprojectmodal.vue";

const fetchLogs = async () => {
  try {
    const response = await getAPI.get(`/api/logs/${projectId.value}/`);
    logs.value = response.data;
    console.log('LOGS: ',response.data);
  } catch (error) {
    console.error('Failed to fetch logs:', error);
  }
};
const updateDateTime = () => {
  const now = new Date();
  currentDate.value = now.toLocaleDateString(); // Format as MM/DD/YYYY
  currentTime.value = now.toLocaleTimeString(); // Format as HH:MM:SS AM/PM
};

onMounted(() => {
  updateDateTime(); // Set initial date and time
  setInterval(updateDateTime, 1000); // Update every second
});

const applyStatusFilter = (status: string) => {
  selectedStatus.value = status;
  const id = projectId.value;
  if (id) {
    allTasksStore.fetchTasks(id, status); // Fetch tasks with the selected status filter
  }
};



watchEffect(() => {

  const id = projectId.value;
  if (id) {
    allTasksStore.fetchTasks(id, selectedStatus.value); // Fetch tasks from the store
  }
});

const createReport = async () => {
   console.log('Trying report');
  try {
    if (userId.value) {
      const response = await getAPI.post(`/reports/create_report/`, {
    user: userId.value,
    // If you have more fields to update, include them here.
    // Example: project_name: projectName.value,
});
      console.log('Report Created:', response.data);
      return;
    }

  } catch (error) {
    console.error('Error creating report:', error);
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
    fetchLogs();
  }
});

const isAssignee = (task: any) => {
  return task.assignee === authStore.user?.name || userRole.value === 'Manager';
};

console.log('USER ROLE:',userRole.value);
// Pagination state
const selectedUser = ref<string>('');

// Pagination state
const currentPage = ref(1);
const logsPerPage = 10;

// Computed property to filter logs based on selected user
const filteredLogs = computed(() => {
  if (selectedUser.value === '' && managerId.value === userId.value) {
        console.log('returning ALL filter');

    return logs.value; // No filter, show all logs
  }
  if(managerId.value === userId.value){
     console.log('mngr iD: ',managerId.value);
      console.log('user iD: ',userId.value);
        console.log('returning SELECTED USER filter');

      return logs.value.filter(log => log.log_user_created === selectedUser.value);

  } else{
        console.log('returning RESTRICTED filter');
     console.log('mngr iD: ',managerId.value);
      console.log('user iD: ',userId.value);
     return logs.value.filter(log => log.log_user_created === userId.value);
  }
});

// Computed properties
const totalPages = computed(() => Math.ceil(filteredLogs.value.length / logsPerPage));

const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * logsPerPage;
  const end = start + logsPerPage;
  return filteredLogs.value.slice(start, end);
});

// Methods to handle page navigation
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};
const applyUserFilter = (userId: string) => {
  selectedUser.value = userId; // Set the selected user for filtering
};

const generatePDF = () => {
  const content = document.getElementById("content-to-pdf");

  if (content) {
    // Use html2canvas to capture the content of the div as an image
    html2canvas(content).then((canvas) => {
      const imgData = canvas.toDataURL("image/png");

      // Create a new jsPDF instance
      const doc = new jsPDF();

      // Get the width and height of the PDF page
      const pageWidth = doc.internal.pageSize.width;
      const pageHeight = doc.internal.pageSize.height;

      // Get the natural width and height of the image
      const imgWidth = canvas.width;
      const imgHeight = canvas.height;

      // Calculate the aspect ratio of the image
      const aspectRatio = imgWidth / imgHeight;

      // Calculate the new width and height to fit the page while maintaining aspect ratio
      let newWidth = pageWidth;
      let newHeight = pageWidth / aspectRatio;

      // If the calculated height exceeds the page height, scale down based on height
      if (newHeight > pageHeight) {
        newHeight = pageHeight;
        newWidth = pageHeight * aspectRatio;
      }

      // Add the image to the PDF with the calculated width and height
      doc.addImage(imgData, "PNG", 0, 0, newWidth, newHeight);

      // Save the generated PDF
      doc.save("generated.pdf");
    });
  }
};


</script>

<template>
   <div class="flex items-center">
      <CardHeader>
        <CardTitle>Reports </CardTitle>
        <CardDescription>
          View and generate reports for your project.
        </CardDescription>
      </CardHeader>

      <div class="ml-auto flex items-center gap-2">
<!--        member filter-->


          <Button variant="default" size="sm" class="h-7 gap-1" @click="generatePDF">
              <ArrowDown>
              </ArrowDown>
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Download as PDF
              </span>
            </Button>


      </div>

    </div>
  <div class=" rounded-lg border px-20 py-10 m-5 bg-background" id="content-to-pdf">

       <Tabs default-value="all">
    <div class="flex ">
      <CardHeader>
                <p class="text-3xl font-bold">Report for {{ projectStore.project_name }} </p>
                <CardDescription>
                  Report generated by {{authStore.user?.name}}<br>
                  Time generated: {{currentTime}} || {{ currentDate}}<br>
                </CardDescription>
              </CardHeader>

    </div>
    <TabsContent value="all">
      <DropdownMenu v-if="userRole !== 'Member' && (userRole !== 'Manager' || projectStore.project_id)" >
      <DropdownMenuTrigger as-child>
        <Button variant="outline" size="sm" class="h-7 gap-1">
          <ListFilter class="h-3.5 w-3.5" />
          <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
            Filter Logs by User
          </span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>Filter Logs by User</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <!-- Dropdown items for users -->
        <DropdownMenuItem @click="applyUserFilter('')">All</DropdownMenuItem>
        <DropdownMenuItem
          v-for="member in members"
          :key="member.value"
          @click="applyUserFilter(member.value)"
        >
          {{ member.label }}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
           <Card class="my-5">
        <CardContent>
<!--          Log Table-->
   <div>
    <!-- Table Component -->
      <!-- Dropdown Menu to Filter Logs by User -->


    <!-- Logs Table -->
    <Table>
      <TableHeader>
        <TableHead>Log ID</TableHead>
        <TableHead>Date/Time</TableHead>
        <TableHead>Log Created By</TableHead>
        <TableHead>Content</TableHead>
      </TableHeader>
      <TableBody>
        <TableRow v-for="log in paginatedLogs" :key="log.log_id">
          <TableCell>{{ log.log_id }}</TableCell>
          <TableCell>{{ new Date(log.log_datetime).toLocaleString() }}</TableCell>
          <TableCell>{{ log.log_user_created_name }}</TableCell>
          <TableCell>{{ log.log_content }}</TableCell>
        </TableRow>
      </TableBody>
    </Table>

    <!-- Pagination Controls -->
    <div class="pagination-controls mt-10">
      <Button @click="prevPage" :disabled="currentPage === 1" variant="outline">Previous</Button>
      <span class="m-5">Page {{ currentPage }} of {{ totalPages }}</span>
      <Button @click="nextPage" :disabled="currentPage === totalPages" variant="outline">Next</Button>
    </div>
  </div>
<!--          end of Log Table-->
      </CardContent>
      </Card>
         <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" size="sm" class="h-7 gap-1">
              <ListFilter class="h-3.5 w-3.5" />
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Filter Tasks by Status
              </span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Filter Tasks by</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="applyStatusFilter('')">All</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Not started')">Not Started</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('In Progress')">In Progress</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Completed')">Completed</DropdownMenuItem>
            <DropdownMenuItem @click="applyStatusFilter('Cancelled')">Cancelled</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      <Card class="my-5">
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
    <CalendarClock  class="mr-2 h-4 w-4" />Start date</div></TableHead>
                <TableHead class="hidden md:table-cell">  <div class="flex items-center">
    <CalendarClock  class="mr-2 h-4 w-4" />Deadline</div></TableHead>


              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="allTasksStore.allTasks.length">
              <TableRow v-for="task in allTasksStore.allTasks.filter(isAssignee)" :key="task.id " >
                  <TableCell>{{task.task_code}}</TableCell>
                  <TableCell>{{ task.features }}</TableCell>
                  <TableCell>
                    {{task.status}}
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
  Sprint {{ task.sprint }}
</TableCell>




                   <TableCell class="hidden md:table-cell">
                    {{ task.start_date }}
                  </TableCell>
                  <TableCell class="hidden md:table-cell">
                    {{ task.deadline }}
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

  </div>
</template>