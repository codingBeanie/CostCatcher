<template>
    <div>
        <p class="text-h3 mb-2 text-secondary">{{ title }}</p>
        <p v-if="subtitle" class="mb-2 text-subtitle">{{ subtitle }}</p>
        <v-btn v-if="tutorial" @click="componentStore.openTutorial(tutorial)" prepend-icon="mdi-school" color="info" density="compact" variant="tonal" class="mb-10">show tutorial</v-btn>
    </div>
</template>

<script setup>
import { useComponentStore } from '../stores/ComponentStore.js'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const props = defineProps({
    title: String,
    subtitle: String,
    tutorial: String
})
const componentStore = useComponentStore()

</script>