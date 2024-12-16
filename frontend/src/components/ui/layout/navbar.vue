<template>
  <header class="fixed top-0 left-0 right-0 z-40 w-full border-b bg-background">
    <div class="flex h-16 items-center justify-between px-4 md:px-6">
      <!-- Logo Section -->
     <projmanlogo class="ml-10"/>

      <!-- Right Section for Larger Screens -->
      <div class="hidden md:flex md:flex-1 md:items-center md:justify-end md:space-x-4">
<!--        &lt;!&ndash; Search Bar &ndash;&gt;-->
<!--        <form class="hidden md:block">-->
<!--          <div class="relative">-->
<!--            <Search class="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />-->
<!--            <Input-->
<!--              type="search"-->
<!--              placeholder="Search..."-->
<!--              class="w-[220px] pl-10 md:w-[300px]"-->
<!--            />-->
<!--          </div>-->
<!--        </form>-->
<!--        Dark/Light mode Toggle-->
      <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline">
              <Icon icon="radix-icons:sun" class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Icon icon="radix-icons:moon" class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
              <span class="sr-only">Toggle theme</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem @click="mode = 'light'">
              Light
            </DropdownMenuItem>
            <DropdownMenuItem @click="mode = 'dark'">
              Dark
            </DropdownMenuItem>
            <DropdownMenuItem @click="mode = 'auto'">
              System
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <!-- Notifications Dropdown -->
<!--        <DropdownMenu>-->
<!--          <DropdownMenuTrigger asChild>-->
<!--            <Button variant="ghost" size="icon">-->

         <!-- Bell Icon and Notifications -->
          <div class="relative">
            <Button variant="ghost" size="icon" @click="toggleNotifications">
              <Bell class="h-5 w-5" />
              <span class="sr-only">Notifications</span>
            </Button>

            <!-- Notifications Modal -->
            <div
              v-if="isNotificationOpen"
              class="absolute right-0 mt-2 w-[320px] max-h-[400px] overflow-hidden rounded-lg"
            >
              <NotificationsModal :isVisible="isNotificationOpen" @closePanel="toggleNotifications" />
            </div>
          </div>

        <!-- User Account Dropdown -->
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" class="relative h-8 w-8 rounded-full">
              <Avatar class="h-8 w-8">
                <AvatarImage :src="profilePictureUrl" alt="@shadcn" />
                <AvatarFallback><User/></AvatarFallback>
              </Avatar>
              
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>{{ userName}}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="navigateTo('/profile')">Profile</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="showLogoutDialog">Log out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  </header>

    <Dialog v-model:open="isLoginDialog" @close="closeDialog">
      <!-- Updated DialogContent size -->
      <DialogContent class="max-w-[600px]">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold">Log out?</DialogTitle>
          <DialogDescription class=" text-lg">
           Are you sure you want to log out? You will be redirected to the login page.
          </DialogDescription>
        </DialogHeader>

        <DialogFooter>
          <Button type="button" @click="closeDialog" class="w-full sm:w-auto" variant="outline">
            Cancel
          </Button>
          <Button type="button" @click="logout" class="w-full sm:w-auto" variant="destructive">
            <LogOut class="mr-2 h-4 w-4" />
            Log out
          </Button>

        </DialogFooter>
      </DialogContent>
    </Dialog>
</template>

<script setup lang="ts">
import {ref, onMounted, computed} from 'vue';
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator
} from '@/components/ui/dropdown-menu'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import {Bell, Search, Trash, User, LogOut} from 'lucide-vue-next'
import { Icon } from '@iconify/vue'
import { useColorMode } from '@vueuse/core'


;
import NotificationsModal from '@/components/ui/layout/notif.vue';
import Projmanlogo from "@/components/reusable/projmanlogo.vue";
import {getAPI} from "@/axios.ts";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog"; // Ensure the path is correct

// Router and Store
const router = useRouter();
const authStore = useAuthStore();
// Pass { disableTransition: false } to enable transitions
const mode = useColorMode()


const user = ref(null);

const logout = async () => {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

const userName = computed(() => authStore.user?.username);

// State Management
const isNotificationOpen = ref(false);

// Methods
const toggleNotifications = () => {
  isNotificationOpen.value = !isNotificationOpen.value;
};

const navigateTo = (path) => {
  router.push(path);
};

const userId = computed(() => authStore.user?.id);

interface User {
  name?: string;
  email?: string;
  username?: string;
  role?: string;
  profile_picture?: string | null;
  password?: string;
}


// Reactive state
const userfields = ref<User>({
  name: "",
  email: "",
  profile_picture: "",
});


const getUserFieldsById = async (userId: number): Promise<User> => {
  try {
    console.log("trying to fetch profile by ID: ",userId);
    const response = await getAPI.get(`/api/userprofile/${userId}/`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching user:", error);
    throw error;
  }
};

const profilePictureUrl = computed(() =>
  userfields.value.profile_picture ? `http://localhost:8000/${userfields.value.profile_picture}` : null
);

const isLoginDialog = ref(false);

// Function to open dialog
const showLogoutDialog = () => {
  isLoginDialog.value = true;

};

const closeDialog = () => {
  isLoginDialog.value = false;
};

onMounted(async () => {
  await authStore.fetchUser();
  user.value = authStore.user;
  userfields.value = await getUserFieldsById(userId.value);
  console.log("navbar picture URL: ",profilePictureUrl.value);
});

</script>

