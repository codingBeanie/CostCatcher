<template>
<v-footer app class="bg-primary text-center">
  <v-row>
    <v-col v-for="link in links">
      <v-btn :icon="link.icon" :to="link.to" color="secondary"></v-btn>
    </v-col>
  </v-row>
</v-footer>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { getUserdata } from '../composables/LocalStorage'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const componentStore = useComponentStore()
const userStore = useUserStore()
const username = ref(null)

// Link List
const links = [
  { 'icon': 'mdi-upload', 'to': 'import' },
  { 'icon': 'mdi-tag-multiple', 'to': 'assignments' },
  { 'icon': 'mdi-text-box-search', 'to': 'review' },
  { 'icon': 'mdi-sigma', 'to': 'statistics' },
  { 'icon': 'mdi-chart-bar', 'to': 'graphs' }
]
////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
onMounted(() => {

})
</script>