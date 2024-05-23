<template>
    <v-row class="ml-4 mr-4 d-flex">
        <v-col cols="4" class="justify-center">
            <v-row class="d-flex justify-center">
                <p class="text-overline">Period Mode</p>
            </v-row>
            <v-row class="d-flex justify-center">
                <v-btn-toggle mandatory v-model="filterType" :onUpdate:modelValue="updateFilter">
                    <v-btn value="0">Monthly</v-btn>
                    <v-btn value="1">Quarterly</v-btn>
                    <v-btn value="2">Yearly</v-btn>
                </v-btn-toggle>
            </v-row>
       </v-col>
       <v-col></v-col>
        <v-col class="mt-2" cols="2">
            <v-select label="From" :items="years" v-model="fromYear" @change="updateFilter"></v-select>
        </v-col>
        <v-col class="mt-2" cols="2">
            <v-select label="To" :items="years" v-model="toYear" @change="updateFilter"></v-select>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref } from 'vue'
import { useFilterStore } from '../stores/FilterStore.js'
import { onMounted } from 'vue';
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const filterStore = useFilterStore()
const filterType = ref(0)

const fromYear = ref(2024)
const toYear = ref(2024)
const years = ref([2024,2023])

const props = defineProps({
    object: String
})

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const updateFilter = () => {
    // Filter Mode
    if (filterType.value == 0) {
        filterStore[props.object].type = 'monthly'
    } else if (filterType.value == 1) {
        filterStore[props.object].type = 'quarterly'
    } else if (filterType.value == 2) {
        filterStore[props.object].type = 'yearly'
    } else {
        filterStore[props.object].type = null
    }

    // From/To Year
    filterStore[props.object].fromYear = fromYear.value
    filterStore[props.object].toYear = toYear.value
}

// Lifecycle Hooks
onMounted(() => {

    if (filterStore[props.object].type == 'monthly') {
        filterType.value = 0
    } else if (filterStore[props.object].type == 'quarterly') {
        filterType.value = 1
    } else if (filterStore[props.object].type == 'yearly') {
        filterType.value = 2
    }
})
</script>