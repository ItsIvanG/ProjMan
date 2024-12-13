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
import ProjectModal from '@/components/reusable/modals/editprojectmodal.vue';

const projectStore = useProjectStore();

// Watch the `project_id` for changes


const authStore = useAuthStore()

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
  <div >
     <div class="flex items-center">
      <CardHeader>
        <CardTitle>{{ projectStore?.project_name || 'Select Project' }} Dashboard </CardTitle>
        <CardDescription>
          View overall project progress and edit project settings.
        </CardDescription>
      </CardHeader>
       <div class="ml-auto flex items-center gap-2">

         <ProjectModal />
     <Button variant="destructive" size="sm" class="h-7 gap-1">
              <Trash/>
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Delete Project
              </span>
    </Button>
    </div>
     </div>

    <Separator/>

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

    <!-- Guest View -->
    <p v-if="!authStore.isAuthenticated">
      You are not logged in. 
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

