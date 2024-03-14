<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Statistics</h1>
        <p class="mb-4 text-h7">View the statistics of your data.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <v-row>
       
    </v-row>


    <!--File-Table-->
    <v-row>

    </v-row>
    
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { API } from '../composables/API.js'
import { useUpdateStore } from '../stores/UpdateStore'

// Variables
const data = ref([])
const updateStore = useUpdateStore()

// Methods
const loadTable = async () => {
    data.value = await API('statistics', 'GET')
    console.log(data.value)
}


// Lifecycle
onMounted(async () => {
    loadTable()
})

</script>