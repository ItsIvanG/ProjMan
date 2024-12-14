<script setup> 
import { useAuthStore } from '../store/auth'
import {CardDescription, CardHeader, CardTitle, Card, CardContent, CardFooter} from "@/components/ui/card";
import {Separator} from "@/components/ui/separator/";
import {Progress} from "@/components/ui/progress/";

import {useProjectStore} from "@/store/project.ts";
import {computed, onMounted, ref, watch, watchEffect} from "vue";
import {getAPI} from "@/axios.ts";
import {useColorMode} from "@vueuse/core";
import {useRouter} from "vue-router";
import {Button} from "@/components/ui/button/";
import {File, Archive, Check, Users} from "lucide-vue-next";
import ProjectModal from '@/components/reusable/modals/editprojectmodal.vue';
import Archiveprojectmodal from "@/components/reusable/modals/archiveprojectmodal.vue";
import router from "@/router";
import  popupproject  from '@/components/reusable/modals/popupproject.vue'


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

 <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
   <Card class="lg:col-span-4 md:col-span-2 col-span-1">
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="text-sm font-medium">
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


    <!-- Guest View -->
    <p v-if="!authStore.isAuthenticated">
      You are not logged in. 
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

