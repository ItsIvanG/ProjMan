<template>
  <div class="flex h-screen">
    <ScrollArea class="h-full">
      <div class="space-y-4 py-4">
        <div class="px-3 mb-8">
          <h2 class="mb-2 px-4 text-sm font-semibold tracking-tight text-muted-foreground">
  <template v-if="userRole !== 'Member'">Project Management</template>
  <template v-if="userRole === 'Member'">Project</template>
</h2>

          <div class="space-y-4">
            <DropdownMenu>
              <!-- Dropdown Trigger -->
              <DropdownMenuTrigger asChild>
                <Button
                  variant="outline"
                  class="w-full flex items-center justify-between px-4 py-2 rounded-lg border border-gray-300 hover:border-gray-400 shadow-sm focus:outline-none focus:ring focus:ring-gray-200 transition"
                >
                  <Folder class="mr-2 h-5 w-5" />
                  <span>{{ selectedProject?.project_name || 'Select Project' }}</span>
                  <ChevronsUpDown class="ml-auto h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>

              <!-- Dropdown Content -->
              <DropdownMenuContent
                class="mt-2 rounded-lg border border-gray-200 bg-white shadow-md"
                style="width: 100%"
              >
                <!-- Dropdown Header -->
                <DropdownMenuLabel class="px-4 py-2 text-sm font-medium text-gray-500">
                  Select Project
                </DropdownMenuLabel>
                <DropdownMenuSeparator class="my-2 border-t border-gray-100" />

                <!-- Dropdown Items -->
                <div class="max-h-60 overflow-auto">

                  <DropdownMenuItem
                    v-for="(project, index) in projects"
                    :key="index"
                    class="px-4 py-2 hover:bg-gray-100 text-gray-700 cursor-pointer transition"
                    @click="selectProject(project)"
                  >
                    {{ project.project_name }}

                    </DropdownMenuItem>

                </div>

                <!-- Create New Project Button -->
                <DropdownMenuSeparator class="my-2 border-t border-gray-100" />
                <ProjectModal class="my-2" v-if="userRole !== 'Member'"/>
                <archivedprojectsmodal v-if="userRole !== 'Member'"/>


              </DropdownMenuContent>
            </DropdownMenu>
          </div>



        </div>

        <div class="px-3 mb-8" v-if="projectStore.project_id">
          <h2 class="mb-2 px-4 text-sm font-semibold tracking-tight text-muted-foreground">
            Overview
          </h2>
          <div class="space-y-1">
            <!-- Dashboard Button -->
            <Button
              variant="ghost"
              :class="{ 'bg-accent text-accent-foreground': isActive('/') }"
              class="w-full justify-start"
              @click="navigateTo('/')"
            >
              <LayoutDashboard class="mr-2 h-4 w-4" />
              Dashboard
            </Button>

            <!-- Project Management Collapsible -->
            <Collapsible>
              <CollapsibleTrigger 
                class="flex w-full items-center justify-between rounded-md px-4 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground"
              >
              <div class="flex items-center">
  <File class="mr-4 h-4 w-4" />
  <template v-if="userRole !== 'Member'">Task Management</template>
  <template v-if="userRole === 'Member'">Task Overview</template>
</div>

                <ChevronDown 
                  class="h-4 w-4 shrink-0 transition-transform duration-200 ease-in-out group-data-[state=open]:rotate-180" 
                />
              </CollapsibleTrigger>
              <CollapsibleContent class="space-y-1 px-5 py-2">
                <Button
                  variant="ghost"
                  :class="{ 'bg-accent text-accent-foreground': isActive('/task') }"
                  class="w-full justify-start pl-8 text-sm"
                  @click="navigateTo('/task')"
                >
                  All Tasks
                </Button>
                <Button
                  v-if="userRole !== 'Manager'"
                  variant="ghost"
                  :class="{ 'bg-accent text-accent-foreground': isActive('/own-task') }"
                  class="w-full justify-start pl-8 text-sm"
                  @click="navigateTo('/own-task')"
                >
                  Your Tasks
                </Button>
                <Button
                  variant="ghost"
                  :class="{ 'bg-accent text-accent-foreground': isActive('/sprint') }"
                  class="w-full justify-start pl-8 text-sm"
                  @click="navigateTo('/sprint')"
                >
                  Sprints
                </Button>
                <Button
                  variant="ghost"
                  :class="{ 'bg-accent text-accent-foreground': isActive('/kanban') }"
                  class="w-full justify-start pl-8 text-sm"
                  @click="navigateTo('/kanban')"
                >
                  Kanban Board
                </Button>
                <Button
                  variant="ghost"
                  :class="{ 'bg-accent text-accent-foreground': isActive('/gantt') }"
                  class="w-full justify-start pl-8 text-sm"
                  @click="navigateTo('/gantt')"
                >
                  Gantt Chart
                </Button>
              </CollapsibleContent>
            </Collapsible>

            <!-- Member Management -->
            <Button
  variant="ghost"
  :class="{ 'bg-accent text-accent-foreground': isActive('/member') }"
  class="w-full justify-start"
  @click="navigateTo('/member')"
>
  <Users class="mr-2 h-4 w-4" />
  <template v-if="userRole !== 'Member'">Member Management</template>
  <template v-if="userRole === 'Member'">Members List</template>
</Button>

          </div>


        <!-- Resources Section -->
        <div class="mt-8">
          <h2 class="mb-2 px-4 text-sm font-semibold tracking-tight text-muted-foreground">
            Resources
          </h2>
          <div class="space-y-1">
            <Button
              variant="ghost"
              :class="{ 'bg-accent text-accent-foreground': isActive('/report') }"
              class="w-full justify-start"
              @click="navigateTo('/report')"
            >
              <FileText class="mr-2 h-4 w-4" />
              Generate Report
            </Button>
            <Button
              variant="ghost"
              :class="{ 'bg-accent text-accent-foreground': isActive('/sharing') }"
              class="w-full justify-start"
              @click="navigateTo('/sharing')"
            >
              <FolderSync class="mr-2 h-4 w-4" />
              File Sharing
            </Button>
          </div>
        </div>
      </div>
         </div>
    </ScrollArea>
  </div>
<!--  <initialprojectmodal/>-->
</template>

<script setup>
import {ref, computed, watchEffect, defineComponent} from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getAPI } from '@/axios';
import { useAuthStore } from '@/store/auth';
import { useProjectStore } from '@/store/project';
import { Button } from '@/components/ui/button';
import ProjectModal from '@/components/reusable/modals/projectmodal.vue';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
    DropdownMenuPortal,
    DropdownMenuSubTrigger,
    DropdownMenuSub
} from '@/components/ui/dropdown-menu';
import {
  ChevronDown,
  ChevronsUpDown,
  File,
  FileText,
  Folder,
  HelpCircle,
  LayoutDashboard,
  Users,
  FolderSync
} from 'lucide-vue-next';
import { useProjectListStore } from '@/store/projectListStore';

import Archivedprojectsmodal from "@/components/reusable/modals/archivedprojectsmodal.vue";


const router = useRouter();
const route = useRoute();
const projects = computed(() => projectListStore.projects);
const selectedProject = computed(() => projectListStore.selectedProject);
const archivedProjects = ref([]);

const userRole = computed(() => authStore.user?.role);

// Access the authentication store
const authStore = useAuthStore();
const projectStore = useProjectStore();


const projectListStore = useProjectListStore();
projectListStore.clearSelectedProject(null);

// Computed user ID
const userId = computed(() => authStore.user?.manager_id);

const fetchProjects = async () => {
  try {
    if (userId.value) {
      const response = await getAPI.get(`/projects/${userId.value}`);
      projectListStore.setProjects(response.data);

      // console.log("RESPONSE SIDEBAR-----------------");
      // Object.keys(response).forEach((key) => {
      //   console.log(`${key}: ${response[key]}`);
      // });
      // Set the first project as the default selected
      if (projects.value.length > 0) {
        projectListStore.setSelectedProject(response.data[0]);
      } else{
        projectStore.clearProject();
      }
    }
  } catch (error) {
    console.error('Error fetching projects:', error);
  }
};

// Watch the login state (authStore.user) and fetch projects when logged in
watchEffect(() => {
  if (authStore.user) {
    fetchProjects();
  }
});

// Select project and update the global store
const selectProject = (project) => {
  projectListStore.setSelectedProject(project); // Store the full project object
  projectStore.setProject(project); // Update the global project store
  console.log('Selected project:', project);
};

watchEffect(() => {
  if (selectedProject.value) {
    projectStore.setProject(selectedProject.value); // Sync selected project with the global store
    console.log('Updated selected project:', selectedProject.value);
  }
});

// Function for navigation
const navigateTo = (path) => {
  router.push(path);
};

// Check if a route is active
const isActive = (path) => route.path === path;

</script>



