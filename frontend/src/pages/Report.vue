<script setup lang="ts">
import {computed, defineComponent} from "vue";
import { Button } from '@/components/ui/button'
import {
  DropdownMenu, DropdownMenuContent,
  DropdownMenuItem, DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import {CardDescription, CardFooter, CardHeader, CardTitle} from '@/components/ui/card'
import {PlusCircle} from "lucide-vue-next";
import {getAPI} from "@/axios.ts";
import {useAuthStore} from "@/store/auth.ts";

const authStore = useAuthStore();

const userId = computed(() => authStore.user?.manager_id);

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
          <Button variant="default" size="sm" class="h-7 gap-1" @click="createReport">
              <PlusCircle>
              </PlusCircle>
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Add
              </span>
            </Button>
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" size="sm" class="h-7 gap-1">

              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Add
              </span>
            </Button>

          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Filter by</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Not Started</DropdownMenuItem>
            <DropdownMenuItem>In Progress</DropdownMenuItem>
            <DropdownMenuItem>Completed</DropdownMenuItem>
            <DropdownMenuItem>Cancelled</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>


      </div>

    </div>
</template>