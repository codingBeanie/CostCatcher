<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Statistics</h1>
        <p class="mb-4 text-h7">View the statistics of your data.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Selectors-->
    <v-row>
        <!--fromDate-->
        <v-col>
            <v-text-field clearable label="From Date" 
                        type="date"
                        v-model="dateFrom" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="loadTable"
                        >
            </v-text-field>
        </v-col>

        <!--toDate-->
        <v-col>
            <v-text-field clearable label="To Date" 
                        type="date"
                        v-model="dateTo" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="loadTable"
                        >
            </v-text-field>
        </v-col>
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
const dateFrom = ref(`${new Date().getFullYear()}-01-01`)
const dateTo = ref(`${new Date().getFullYear()}-12-31`)
const updateStore = useUpdateStore()

// Methods
const loadTable = async () => {
    data.value = await API(`statistics/?datefrom=${dateFrom.value}&dateto=${dateTo.value}`, 'GET')
    console.log(data.value)
}


// Lifecycle
onMounted(async () => {
    loadTable()
})

</script>