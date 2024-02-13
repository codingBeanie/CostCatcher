<template>
  <div class="">
    <nav class="flex p-3 shadow-lg bg-primary-300">
      <div class="ml-4 mr-20 font-bold text-secondary-100">
        COSTCATCHER
      </div>
      <RouterLink link="import">Import</RouterLink>      
    </nav>
    <div class="p-4">
      <router-view/>
    </div>
    
  </div>

</template>


<script setup>
import RouterLink from './components/RouterLink.vue'
</script>
