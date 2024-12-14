<script setup> 
import { useAuthStore } from '../store/auth'
import {CardDescription, CardHeader, CardTitle, Card, CardContent, CardFooter} from "@/components/ui/card";
import {Separator} from "@/components/ui/separator/";
import {Progress} from "@/components/ui/progress/";
import {Input} from "@/components/ui/input/";
import {useProjectStore} from "@/store/project.ts";
import {computed, onMounted, ref, watch, watchEffect} from "vue";
import {getAPI} from "@/axios.ts";
import {useColorMode} from "@vueuse/core";
import {useRouter} from "vue-router";
import {Button} from "@/components/ui/button/";
import {File, Archive, Check, Users, Circle, LayoutList, ArrowUpDown, CalendarClock, List} from "lucide-vue-next";
import ProjectModal from '@/components/reusable/modals/editprojectmodal.vue';
import Archiveprojectmodal from "@/components/reusable/modals/archiveprojectmodal.vue";
import router from "@/router";
import  popupproject  from '@/components/reusable/modals/popupproject.vue'
import {Table, TableHead, TableHeader, TableRow} from "@/components/ui/table";


const projectStore = useProjectStore();

// Watch the `project_id` for changes


const authStore = useAuthStore()

const userRole = computed(() => authStore.user?.role);

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
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { format, differenceInDays, parseISO, eachDayOfInterval } from "date-fns";

// State
const startDate = ref("2024-12-01");
const endDate = ref("2024-12-15");

const tasks = ref([
  { name: "Design Wireframes", start: "2024-12-02", end: "2024-12-05" },
  { name: "Develop Backend", start: "2024-12-06", end: "2024-12-12" },
  { name: "Testing", start: "2024-12-10", end: "2024-12-14" },
]);

const days = ref([]);

// Generate Days for Timeline
const generateDays = () => {
  const parsedStart = parseISO(startDate.value);
  const parsedEnd = parseISO(endDate.value);
  days.value = eachDayOfInterval({ start: parsedStart, end: parsedEnd }).map((date) =>
    format(date, "MMM d")
  );
};

// Compute Task Bar Styles
const getTaskBarStyle = (task) => {
  const totalDays = days.value.length;
  const taskStart = differenceInDays(parseISO(task.start), parseISO(startDate.value));
  const taskEnd = differenceInDays(parseISO(task.end), parseISO(startDate.value));

  const left = `${(taskStart / totalDays) * 100}%`;
  const width = `${((taskEnd - taskStart + 1) / totalDays) * 100}%`;

  return { left, width };
};

// Initial Load
generateDays();
</script>


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

 <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-4">
   <Card class="lg:col-span-4 md:col-span-2 col-span-1">
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>
          Project Progress
        </CardTitle>

        33%
      </CardHeader>
      <CardContent>
        <Progress :model-value="33" />

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
          69
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
          69
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
          69
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
          69
        </div>

      </CardContent>
   </Card>
</div>
     <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
 <Card class="md:col-span-2 col-span-1">
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>
          Your ongoing tasks
        </CardTitle>
        <CalendarClock />
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
            </TableHeader>
    </Table>
      </CardContent>
   </Card>
<!--Gantt Chart-->

    <Card class="md:col-span-4 col-span-1">
      <CardHeader>
        <CardTitle>Gantt Chart</CardTitle>
        <CardDescription>Manage your project timelines visually.</CardDescription>
      </CardHeader>
      <CardContent>
        <!-- Date Range Picker -->
        <div class="mb-4 flex items-end gap-4">
          <div>
            <label for="start-date" class="block text-sm font-medium">Start Date</label>
            <Input
              id="start-date"
              type="date"
              v-model="startDate"
              class="border rounded  text-sm w-full"
            />
          </div>
          <div>
            <label for="end-date" class="block text-sm font-medium">End Date</label>
            <Input
              id="end-date"
              type="date"
              v-model="endDate"
              class="border rounded text-sm w-full"
            />
          </div>
          <div class="block text-sm mb-1">
             <Button
            @click="generateDays"
            class="rounded text-sm"
          >
            Update Chart
          </Button>
          </div>

        </div>

        <div class="overflow-x-auto">
          <div class="min-w-[800px]">
            <!-- Chart Header -->
            <div class="flex items-center bg-primary-foreground text-sm font-medium">
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
            <!-- Chart Rows -->
            <div v-for="(task, index) in tasks" :key="index" class="flex items-center text-sm">
              <!-- Task Name -->
              <div class="w-40 px-4 py-2 border-r ">
                {{ task.name }}
              </div>
              <!-- Timeline -->
              <div class="flex-1 relative  h-12">
                <Popover>
                  <PopoverTrigger>
                    <div
                      class="absolute h-8 bg-primary rounded-md cursor-pointer"
                      :style="getTaskBarStyle(task)"
                    ></div>
                  </PopoverTrigger>
                  <PopoverContent>
                    <div class="text-sm">
                      <p><strong>Task:</strong> {{ task.name }}</p>
                      <p><strong>Start:</strong> {{ task.start }}</p>
                      <p><strong>End:</strong> {{ task.end }}</p>
                    </div>
                  </PopoverContent>
                </Popover>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>




    <!-- Guest View -->
    <p v-if="!authStore.isAuthenticated">
      You are not logged in. 
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

