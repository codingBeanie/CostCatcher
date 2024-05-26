<template>
    <v-row no-gutters class="mb-1">
        <v-col v-if="props.size!='small'" class="text-center">
            <p class="text-h5 font-weight-bold text-secondary mt-2">{{ title }}</p>
        </v-col>   

        <v-col v-if="props.size=='small'" class="text-center">
            <p class="text-overline text-secondary mt-2">{{ title }}</p>
        </v-col>   
    </v-row>
    <v-divider color="secondary" thickness="1"></v-divider>
</template>

<script setup>
import { useComponentStore } from '../stores/ComponentStore.js'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const props = defineProps({
    title: String,
    size: {
        type: String,
        default: 'big'
    }
})
const componentStore = useComponentStore()

</script>