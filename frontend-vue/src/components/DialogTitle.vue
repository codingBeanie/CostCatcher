<template>
    <v-row>
        <v-col class="text-center">
            <p class="text-h5 font-weight-bold text-secondary mt-2">{{ title }}</p>
        </v-col>    
    </v-row>
</template>

<script setup>
import { useComponentStore } from '../stores/ComponentStore.js'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const props = defineProps({
    title: String,
})
const componentStore = useComponentStore()

</script>