<template>
  <header class="fixed top-0 left-0 right-0 z-40 w-full border-b bg-background">
    <div class="flex h-16 items-center justify-between px-4 md:px-6">
      <!-- Logo Section -->
      <div class="flex items-center space-x-2">
        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary">
          <span class="text-lg font-bold text-primary-foreground">PM</span>
        </div>
        <span class="hidden text-xl font-semibold sm:inline-block">Projman</span>
      </div>

      <!-- Right Section for Larger Screens -->
      <div class="hidden md:flex md:flex-1 md:items-center md:justify-end md:space-x-4">
        <!-- Search Bar -->
        <form class="hidden md:block">
          <div class="relative">
            <Search class="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search..."
              class="w-[220px] pl-10 md:w-[300px]"
            />
          </div>
        </form>

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
                <AvatarImage
                  src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/340px-Default_pfp.svg.png"
                  alt="@user"
                />
                <AvatarFallback>CN</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="navigateTo('/profile')">Profile</DropdownMenuItem>
            <DropdownMenuItem @click="logout">Log out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { Bell, Search } from 'lucide-vue-next';
import NotificationsModal from '@/components/ui/layout/notif.vue'; // Ensure the path is correct

// Router and Store
const router = useRouter();
const authStore = useAuthStore();

// State Management
const isNotificationOpen = ref(false);

// Methods
const toggleNotifications = () => {
  isNotificationOpen.value = !isNotificationOpen.value;
};

const navigateTo = (path) => {
  router.push(path);
};

const logout = async () => {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
</script>

<style>
/* Custom Scrollbar */
div[max-h]::-webkit-scrollbar {
  width: 6px;
}

div[max-h]::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 9999px;
}

div[max-h]::-webkit-scrollbar-track {
  background-color: transparent;
}

div[max-h] {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

nav {
  background-color: #1a1a1a;
}
</style>
