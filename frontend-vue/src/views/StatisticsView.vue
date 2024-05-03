<template>
    <!--Titles-->
    <Title title="Statistics" subtitle="Overview of your transactions"></Title>
    <Divider title="BASIC TABLE" spacing="8"></Divider>

    <!--Selectors-->
    <v-row class="mt-2">
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

    <!--Status-->
    <div v-if="statusTransactions && !waiting"><p class="text-h4 text-error" >No transactions were found. Please upload a file first: <v-btn class="mb-1" prepend-icon="mdi-file-multiple" color="info" to="/import">CSV-Management</v-btn></p></div>
    <div v-if="statusCategories && !waiting" class="mt-2 mb-4"><p class="text-h6 text-error" >No categories were created. Add categories and categorize your transactions: <v-btn class="mb-1" prepend-icon="mdi-tag-multiple" color="info" to="/assignments">Categorization</v-btn></p></div>
    
    <!--File-Table-->
    <Tableau :incomeData="incomeData" :expenseData="expenseData" :headers="headers"></Tableau>
    <v-row v-if="waiting">
        <v-progress-linear
            color="accent"
            indeterminate
        ></v-progress-linear>
    </v-row>
    
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { API } from '../composables/API.js'
import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
import Tableau from '../components/Tableau.vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const statusTransactions = ref(true)
const statusCategories = ref(true)
const waiting = ref(true)

// Data
const incomeData = ref([])
const expenseData = ref([])
const headers = ref()

// Inputs
const dateFrom = ref(``)
const dateTo = ref(``)

// Info
const infoUndefined = 'These transactions are not assigned to any category.'

// Selection
const selectCell = ref({ 'column': '', 'row': '' })
const sortColumn = ref('Category')
const sortAsc = ref(false)

// Settings
const currency = ref('€')
const locale = ref('de-DE') 

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const loadDateRange = async () => {
    if (dateFrom.value == '' && dateTo.value == '') {
        // Load the default date range
        const data = await API('datespan', 'GET')
        if (data == undefined || data == 0) {
            statusTransactions.value = true
            return
        }
        statusTransactions.value = false
        dateFrom.value = data.defaultFirst
        dateTo.value = data.defaultLast
    }
}

const loadTable = async () => {
    await loadDateRange()
    if (dateFrom.value != undefined && dateTo.value != undefined)
    {   
        waiting.value = true
        incomeData.value = await API(`statistics/?datefrom=${dateFrom.value}&dateto=${dateTo.value}&filtermode=income&showTotals=false`, 'GET')
        expenseData.value = await API(`statistics/?datefrom=${dateFrom.value}&dateto=${dateTo.value}&filtermode=expense&showTotals=false`, 'GET')
        headers.value = (Object.keys(incomeData.value[0].Data))
        waiting.value = false
    }
    // Check if any data is available
    if (incomeData.value.length == 0 && expenseData.value.length == 0) {
        statusTransactions.value = true
    }
    else {
        statusTransactions.value = false
    }
    // Check if any categories are available
    if (incomeData.value.length <= 1 && expenseData.value.length <= 1) {
        statusCategories.value = true
    }
    else {
        statusCategories.value = false
    }
    

}

const loadSettings = async () => {
    const settings = await API('settings', 'GET')
    currency.value = settings.currency
    locale.value = settings.locale
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = () => {
    loadSettings()
    loadTable()
}

onMounted(async () => {
    load()
})

watch(() => componentStore.app.refresh, () => {
    load()
})

watch(() => userStore.username, () => {
    load()
})

</script>

<style scoped>
    td {
        min-width: 135px;
    }
</style>