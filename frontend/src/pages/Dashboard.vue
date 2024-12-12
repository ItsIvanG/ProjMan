<script setup>
import { useAuthStore } from '../store/auth'
import {CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Separator} from "@/components/ui/separator/";
import {useProjectStore} from "@/store/project.ts";
import {computed, onMounted, ref, watch, watchEffect} from "vue";
import {getAPI} from "@/axios.ts";
import {useColorMode} from "@vueuse/core";
import {useRouter} from "vue-router";
import {Button} from "@/components/ui/button/";
import {Pencil,Trash} from "lucide-vue-next";

const projectStore = useProjectStore();
const selectedProject = ref(null);

const selectProject = (project) => {
  selectedProject.value = project; // Store the full project object
  // projectStore.setProject(project); // Update the global project store
  console.log('Selected project:', project);
};
// Watch the `project_id` for changes

const mode = useColorMode()
const router = useRouter()
const authStore = useAuthStore()
const projects = ref([]);
const user = ref(null);
//

onMounted(async () => {
  await authStore.fetchUser();
  user.value = authStore.user;
});
watch(
  () => projectStore.project_id,
  (newValue, oldValue) => {
    console.log(`Project ID changed from ${oldValue} to ${newValue}`);
    if (!newValue) {
      console.log('Project ID was cleared.');
    }
  }
);


</script>


<template>
  <div class="p-6">
     <div class="flex items-center">
      <CardHeader>
        <CardTitle>{{ projectStore?.project_name || 'Select Project' }} Dashboard </CardTitle>
        <CardDescription>
          View and generate reports for your project.
        </CardDescription>
      </CardHeader>
       <div class="ml-auto flex items-center gap-2">
    <Button variant="default" size="sm" class="h-7 gap-1">
              <Pencil>
              </Pencil>
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Edit Project
              </span>
    </Button>
     <Button variant="destructive" size="sm" class="h-7 gap-1">
              <Trash>
              </Trash>
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Delete Project
              </span>
    </Button>
    </div>
     </div>

    <Separator/>

    <!-- Authenticated User Details -->
    <div v-if="authStore.isAuthenticated" class="max-w-md mx-auto border p-4 rounded">
      <h2 class="mb-4 text-lg font-medium">User Information</h2>
      <ul class="space-y-2">
        <!-- Loop Through All User Data -->
        <li v-for="(value, key) in authStore.user" :key="key" class="flex justify-between">
          <span class="capitalize">{{ key }}</span>
          <span>{{ value }}</span>
        </li>
      </ul>
    </div>

    <!-- Guest View -->
    <p v-else>
      You are not logged in. 
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

