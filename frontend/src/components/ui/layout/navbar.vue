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

        <!-- Notifications Dropdown -->
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon">
              <Bell class="h-5 w-5" />
              <span class="sr-only">Notifications</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="w-[280px] md:w-[300px]">
            <DropdownMenuLabel>Notifications</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <ScrollArea class="h-[300px]">
              <div class="space-y-3 p-4">
                <div v-for="i in 5" :key="i" class="flex items-start gap-3 rounded-lg p-2 hover:bg-accent">
                  <Avatar>
                    <AvatarImage :src="`https://i.pravatar.cc/40?img=${i}`" />
                    <AvatarFallback>U{{ i }}</AvatarFallback>
                  </Avatar>
                  <div class="space-y-1">
                    <p class="text-sm font-medium">New message from User {{ i }}</p>
                    <p class="text-sm text-muted-foreground">Hey, what's up? All set for the presentation?</p>
                    <p class="text-xs text-muted-foreground">2 hours ago</p>
                  </div>
                </div>
              </div>
            </ScrollArea>
            <DropdownMenuSeparator />
            <DropdownMenuItem class="cursor-pointer justify-center">
              View all notifications
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
<!--        Dark/Light mode Toggle-->
      <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline">
              <Icon icon="radix-icons:moon" class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Icon icon="radix-icons:sun" class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
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
        <!-- User Account Dropdown -->
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" class="relative h-8 w-8 rounded-full">
              <Avatar class="h-8 w-8">
                <AvatarImage src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/340px-Default_pfp.svg.png" alt="@shadcn" />
                <AvatarFallback>CN</AvatarFallback>
              </Avatar>
              
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="navigateTo('/profile')">Profile</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="logout">Log out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
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
import { Bell, LayoutGrid, Menu, Search, ShoppingCart, Users, Inbox, Settings, CreditCard, HelpCircle } from 'lucide-vue-next'
import { Icon } from '@iconify/vue'
import { useColorMode } from '@vueuse/core'

// Pass { disableTransition: false } to enable transitions
const mode = useColorMode()
const router = useRouter()
const authStore = useAuthStore()

const apps = [
  { name: 'Sales', icon: ShoppingCart },
  { name: 'Users', icon: Users },
  { name: 'Inbox', icon: Inbox },
  { name: 'Settings', icon: Settings },
  { name: 'Billing', icon: CreditCard },
  { name: 'Help', icon: HelpCircle },
]

const navigateTo = (path) => {
  router.push(path)
}

const logout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error("Logout failed:", error)
  }
}
</script>