<template>
  <div class="flex h-screen">
    <ScrollArea class="h-full">
      
      <div class="space-y-4 py-4">
        <div class="px-3">
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
                  Project Management
                </div>
                <ChevronDown 
                  class="h-4 w-4 shrink-0 transition-transform duration-200 ease-in-out group-data-[state=open]:rotate-180" 
                />
              </CollapsibleTrigger>
              <CollapsibleContent class="space-y-1 px-2 py-2">
                <Button
                  variant="ghost"
                  :class="{ 'bg-accent text-accent-foreground': isActive('/task') }"
                  class="w-full justify-start pl-8 text-sm"
                  @click="navigateTo('/task')"
                >
                  All Tasks
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
              Member Management
            </Button>
          </div>
        </div>

        <!-- Resources Section -->
        <div class="px-3">
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
              :class="{ 'bg-accent text-accent-foreground': isActive('/help') }"
              class="w-full justify-start"
              @click="navigateTo('/help')"
            >
              <HelpCircle class="mr-2 h-4 w-4" />
              Placeholder
            </Button>
          </div>
        </div>
      </div>
    </ScrollArea>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { ChevronDown, File, FileText, HelpCircle, LayoutDashboard, Users } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

// Function for navigation
const navigateTo = (path) => {
  router.push(path)
}

// Check if a route is active
const isActive = (path) => route.path === path
</script>
