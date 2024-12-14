<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import Sidebar from "@/components/ui/layout/sidebar.vue";
import Navbar from "@/components/ui/layout/navbar.vue";
import Toaster from '@/components/ui/toast/Toaster.vue'

const route = useRoute();
</script>

<template>
  <!-- Only show sidebar and navbar if not on login or register pages -->
  <div v-if="!['/login', '/register','/forgotpass'].includes(route.path)">
    <!-- Sidebar -->
    <aside 
      :class="[
        'fixed inset-y-0 left-0 z-50 w-64 bg-background pt-16',
        'lg:translate-x-0',
        'shadow-sm border-r'
      ]"
    >
      <Sidebar />
    </aside>

    <!-- Navbar -->
    <nav class="fixed left-0 right-0 top-0 z-50 border-b bg-background shadow-sm">
      <Navbar />
    </nav>
  </div>
  <Toaster />
  <!-- Main content will only be displayed if not on login or register pages -->
  <main v-if="!['/login', '/register', '/forgotpass'].includes(route.path)" class="p-4 md:ml-64 h-auto pt-20">
    <router-view />
  </main>

  <!-- Main content will be empty if on login or register pages -->
  <main v-else >
    <router-view />
  </main>
</template>
