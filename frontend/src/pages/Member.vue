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
import { computed, ref } from "vue";
import  Usermodal  from '@/components/reusable/modals/usermodal.vue'
import  Useredit  from '@/components/reusable/modals/editusermodal.vue'

// Sample users data
const allUsers = ref([
  {
    email: "kean@gmail.com",
    name: "Kean Lucas",
    project: " project",
    role: "Member",
    status: "Active",
  },
  {
    email: "kean@gmail.com",
    name: "Kean Lucas",
    project: " project",
    role: "Member",
    status: "Active",
  },
  {
    email: "kean@gmail.com",
    name: "Kean Lucas",
    project: " project",
    role: "Member",
    status: "Deactivated",
  },
  {
    email: "kean@gmail.com",
    name: "Kean Lucas",
    project: " project",
    role: "Member",
    status: "Active",
  },
  {
    email: "admin@example.com",
    name: "Admin User",
    project: "Admin Project",
    role: "Manager",
    status: "Active",
  },
  {
    email: "cheska.lucas@example.com",
    name: "Cheska Lucas",
    project: "Marketing",
    role: "Member",
    status: "Active",
  },
  {
    email: "john.doe@example.com",
    name: "John Doe",
    project: "Development",
    role: "Manager",
    status: "Active",
  },
]);

const getStatusVariant = (status: string) => {
  switch (status.toLowerCase()) {
    case 'manager':
      return 'manager';
    case 'member':
      return 'member';
    case 'active':
      return 'active';
    case 'deactivated':
      return 'destructive';
    default:
      return 'default';
  }
};

// Pagination settings
const currentPage = ref(1);
const itemsPerPage = 5;

// Paginated users
const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return allUsers.value.slice(start, start + itemsPerPage);
});

// Total number of pages
const totalPages = computed(() =>
  Math.ceil(allUsers.value.length / itemsPerPage)
);

</script>

<template>
  <Tabs default-value="all">
    <div class="flex items-center">
      <CardHeader>
                <CardTitle>Member Management </CardTitle>
                <CardDescription>
                  List of manager and member.
                </CardDescription>
              </CardHeader>
      <div class="ml-auto flex items-center gap-2">
        
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" size="sm" class="h-7 gap-1">
              <ListFilter class="h-3.5 w-3.5" />
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Filter
              </span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Filter by</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Manager</DropdownMenuItem>
            <DropdownMenuItem>Member</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <Usermodal />
      </div>
    </div>
    
    <TabsContent value="all">
      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead class="hidden md:table-cell">Role</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Project</TableHead>
                <TableHead class="hidden md:table-cell">Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="paginatedUsers.length">
                <TableRow v-for="(user, index) in paginatedUsers" :key="index">
                  <TableCell>{{ user.name }}</TableCell>
                  <TableCell>
                    <Badge :variant="getStatusVariant( user.role )">
                      {{ user.role }}
                    </Badge>
                  </TableCell>
                  <TableCell>{{ user.email }}</TableCell>
                  <TableCell>{{ user.project }}</TableCell>
                  <TableCell>
                    <Badge :variant="getStatusVariant( user.status )">
                      {{ user.status }}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger as-child>
                        <Button
                          aria-haspopup="true"
                          size="icon"
                          variant="ghost"
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
        <CardFooter class="flex justify-between items-center">
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
        </CardFooter>
      </Card>
    </TabsContent>
  </Tabs>
</template>
