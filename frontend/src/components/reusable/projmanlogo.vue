<template>
  <div class="flex items-center space-x-2">
    <div class="flex h-8 w-8 items-center justify-center rounded-full">
      <span class="flex items-center text-xl font-semibold">
        <logoSVG
          width="30px"
          height="30px"
          class="fill-foreground "

        />
        <span class="ml-3">ProjMan</span>
      </span>
    </div>
  </div>
</template>
<script setup lang="ts">
import logoSVG from '@/assets/projman.svg';
</script>