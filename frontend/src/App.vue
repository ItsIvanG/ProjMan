<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Sidebar from "@/components/ui/layout/sidebar.vue";
import Navbar from "@/components/ui/layout/navbar.vue";


const route = useRoute();

</script>

<template>
  <!-- Only show Sidebar and Navbar if the route is not login or register -->
  <router-view />
  <div v-if="!['/login', '/register'].includes(route.path)">
    <Sidebar />


  </div>
  
 
</template>
