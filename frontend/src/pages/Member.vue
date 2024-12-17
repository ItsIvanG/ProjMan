<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter, CardHeader, CardDescription, CardTitle } from '@/components/ui/card'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Tabs,
  TabsContent,
} from '@/components/ui/tabs'
import {
  Pagination,
} from '@/components/ui/pagination'
import {
  ListFilter,
  MoreHorizontal,
} from 'lucide-vue-next'
import { computed, ref, watchEffect } from "vue";
import  Usermodal  from '@/components/reusable/modals/usermodal.vue'
import  Useredit  from '@/components/reusable/modals/editusermodal.vue'
import { getAPI } from '@/axios';
import { useAuthStore } from '@/store/auth'
import { useUserInfoStore } from '@/store/userStore';
import { useUserListStore } from '@/store/userListStore';

const userStore = useUserInfoStore();


const userRole = computed(() => authStore.user?.role);

const authStore = useAuthStore();
const managerId  = computed(() => authStore.user?.manager_id);
const userListStore = useUserListStore();

const filterStatus = ref<string>('All'); // Track selected filter status

// Fetch users from the API
const fetchUsers = async (managerId: number, status: string) => {
  try {
    let url = `/manager/${managerId}/`;
    if (status !== 'All') {
      url += `?is_active=${status === 'Active' ? 1 : 0}`;
    }
    const response = await getAPI.get(url);
    userListStore.setUsers(response.data); // Update the store with fetched users
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

// Watch for changes in filterStatus and fetch users accordingly
watchEffect(() => {
  if (managerId.value) {
    fetchUsers(managerId.value, filterStatus.value);
  }
});

const getStatusVariant = (status: string) => {
  switch (status.toLowerCase()) {
    case 'manager':
      return 'manager';
    case 'member':
      return 'member';
    case 'active':
      return 'active';
    case 'archived':
      return 'archived';
    default:
      return 'default';
  }
};



</script>

<template>
  <Tabs default-value="all">
    <div class="flex items-center">
      <CardHeader>
        <CardTitle v-if="userRole !== 'Member'">Member Management</CardTitle>
<CardTitle v-if="userRole === 'Member'">Project Member</CardTitle>

                <CardDescription>
                  List of manager and member.
                </CardDescription>
              </CardHeader>
      <div class="ml-auto flex items-center gap-2">
        
<!--        <DropdownMenu>-->
<!--          <DropdownMenuTrigger as-child>-->
<!--            <Button variant="outline" size="sm" class="h-7 gap-1">-->
<!--              <ListFilter class="h-3.5 w-3.5" />-->
<!--              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">-->
<!--                Filter-->
<!--              </span>-->
<!--            </Button>-->
<!--          </DropdownMenuTrigger>-->
<!--          <DropdownMenuContent align="end">-->
<!--            <DropdownMenuLabel>Filter by</DropdownMenuLabel>-->
<!--            <DropdownMenuSeparator />-->
<!--            <DropdownMenuItem @click="filterStatus = 'All'">All</DropdownMenuItem> -->
<!--            <DropdownMenuItem @click="filterStatus = 'Active'">Active</DropdownMenuItem>-->
<!--            <DropdownMenuItem @click="filterStatus = 'Archived'">Archived</DropdownMenuItem>-->
<!--          </DropdownMenuContent>-->
<!--        </DropdownMenu>-->
        <Usermodal v-if="userRole !== 'Member'"/>
      </div>
    </div>
    
    <TabsContent value="all">
      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Username</TableHead>
                <TableHead class="hidden md:table-cell">Role</TableHead>
                <TableHead>Email</TableHead>
<!--                <TableHead class="hidden md:table-cell">Status</TableHead>-->
                <TableHead v-if="userRole !== 'Member'">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="userListStore.users.length">
                <TableRow v-for="(user, index) in userListStore.users" :key="index">
                  <TableCell>{{ user.name }}</TableCell>
                  <TableCell>{{ user.username }}</TableCell>
                  <TableCell>
                    <Badge :variant="getStatusVariant( user.role )">
                      {{ user.role }}
                    </Badge>
                  </TableCell>
                  <TableCell>{{ user.email }}</TableCell>
<!--                  <TableCell>-->
<!--  <Badge :variant="getStatusVariant(user.is_active ? 'Active' : 'Archived')">-->
<!--    {{ user.is_active ? 'Active' : 'Archived' }}-->
<!--  </Badge>-->
<!--</TableCell>-->


                  <TableCell v-if="userRole !== 'Member'">
                    <DropdownMenu>
                      <DropdownMenuTrigger as-child>
                        <Button
                          aria-haspopup="true"
                          size="icon"
                          variant="ghost"
                          @click="userStore.setTask(user)"
                        >
                          <MoreHorizontal class="h-4 w-4" />
                          <span class="sr-only">Toggle menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <Useredit />
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              </template>
              <template v-else>
                <TableRow>
                  <TableCell colspan="5" class="text-center">
                    <p class="text-sm text-muted-foreground">
                      No users available. Add a new user to get started.
                    </p>
                  </TableCell>
                </TableRow>
              </template>
            </TableBody>
          </Table>
        </CardContent>
        <!-- <CardFooter class="flex justify-between items-center">
          <div class="text-xs text-muted-foreground">
            Showing <strong>{{ (currentPage - 1) * itemsPerPage + 1 }}</strong> to
            <strong>{{ Math.min(currentPage * itemsPerPage, allUsers.length) }}</strong>
            of <strong>{{ allUsers.length }}</strong> users
          </div>
          <Pagination
            :current-page="currentPage"
            :total-pages="totalPages"
            @page-change="currentPage = $event"
          />
        </CardFooter> -->
      </Card>
    </TabsContent>
  </Tabs>
</template>
