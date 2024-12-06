<script setup>
import { useRoute } from 'vue-router'
import Sidebar from "@/components/ui/layout/sidebar.vue";
import Navbar from "@/components/ui/layout/navbar.vue";

const route = useRoute();
</script>

<template>
  <!-- Only show Sidebar and Navbar if the route is not login or register -->
  <div v-if="!['/login', '/register'].includes(route.path)">
    <Sidebar />
    <Navbar />
  </div>
  <router-view />
</template>
