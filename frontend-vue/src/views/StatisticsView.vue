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

    COL: {{ selectCell.column }}
    ROW: {{ selectCell.row }}

    <!--File-Table-->
    <v-row>
        <v-container>
            <v-table v-if="dataStats" class="fill-width">
                <thead>
                    <tr>
                        <th v-for="column in columns" :key="column" class="text-right bg-secondary">{{ column }}</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="row in dataStats" :key="row.id">
                        <td v-for="column in columns" :key="column" class="text-right pa-0">
                            <!--First Column-->
                            <div v-if="column=='Category'" class="pa-2">
                                <!--Income-->
                                <div v-if="row[column]==='Income'">
                                    <v-icon color="success" size="x-large">mdi-cash-plus</v-icon>
                                </div>

                                <!--Expenses-->
                                <div v-else-if="row[column]==='Expenses'">
                                    <v-icon color="error" size="x-large">mdi-cash-minus</v-icon>
                                </div>

                                <!--Net-->
                                <div v-else-if="row[column]==='Net'">
                                    <v-icon color="info" size="x-large">mdi-cash-multiple</v-icon>
                                </div>

                                <!--Categories-->
                                <div v-else>
                                    <v-chip v-if="row[column].id != 0" :color="row[column].color" link @click="mainStore.openCategoryEdit(row[column].id)">{{ row[column].name }}</v-chip>
                                    <v-chip v-if="row[column].id == 0" :color="row[column].color" class="cursor-not-allowed">{{ row[column].name }}</v-chip>
                                </div>
                            </div>
                            
                            <!--Month Columns-->
                            <div v-else-if="column!='Sum' && column!='Average' && column!='Median'" class="cursor-pointer">

                                <!--Income--> 
                                <div v-if="row['Category'] === 'Income'" @mouseover="updateSelection(row['Category'].id, column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-info': selectCell.row === row['Category'].id && selectCell.column === column}">
                                 {{ parseFloat(row[column]).toFixed(rounding) }} {{ currency }}
                                 {{ row }}
                                </div>

                                <!--Expenses-->
                                <div v-else-if="row['Category'] === 'Expenses'" @mouseover="updateSelection(row['Category'].id, column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-info': selectCell.row === row['Category'].id && selectCell.column === column}">
                                    {{ parseFloat(row[column]).toFixed(rounding) }} {{ currency }}
                                </div>

                                <!--Net-->
                                <div v-else-if="row['Category'] === 'Net'" @mouseover="updateSelection(row['Category'].id, column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-info': selectCell.row === row['Category'].id && selectCell.column === column}">
                                    <div v-if="row[column] < 0" color="error">{{ parseFloat(row[column]).toFixed(rounding) }} {{ currency }}</div>
                                    <div v-if="row[column] >= 0" color="success">{{ parseFloat(row[column]).toFixed(rounding) }} {{ currency }}</div>
                                </div>

                                <!--Categories-->
                                <div v-else @mouseover="updateSelection(row['Category'].id, column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-info': selectCell.row === row['Category'].id && selectCell.column === column}">
                                  {{ parseFloat(row[column]).toFixed(rounding) }} {{ currency }}
                                </div>
                            </div>

                            <!--Statistics Column-->
                            <div v-else class="justify-end cursor-not-allowed align-center bg-primaryLight d-flex fill-height fill-width grow">
                                {{ parseFloat(row[column]).toFixed(rounding) }} {{ currency }}
                            </div>
                        </td>
                    </tr>
                </tbody>
            </v-table>
        </v-container>    
    </v-row>

    <v-divider class="mt-8 mb-8"></v-divider>
    
    <v-row>
        <h2>Detail View</h2>
    </v-row>
    <v-row>
        <p class="mb-4 text-h7">Click on a sum in the table above to see how the value is composed </p>
    </v-row>
    <!--Detail Table-->
    <v-row>
        <v-data-table :items="dataDetails" :headers="headersDetail">
        </v-data-table>
    </v-row>
    
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useMainStore } from '../stores/MainStore.js'
import { API } from '../composables/API.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const mainStore = useMainStore()
const hover = ref(false)

// Data
const dataStats = ref([])
const dataDetails = ref([])
let columns = []

// Inputs
const dateFrom = ref(`${new Date().getFullYear()}-01-01`)
const dateTo = ref(`${new Date().getFullYear()}-12-31`)

// Selection
const selectCell = ref({'column': '', 'row': ''})

// Settings
const currency = ref('€')
const rounding = ref(2)  

// Tables
const headersDetail = [
    { title: 'Date', value: 'date', sortable: true},
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true, align: 'end'}
]

////////////////////////////////////////////////////////////////
// Load Functions
////////////////////////////////////////////////////////////////
const loadTable = async () => {
    dataStats.value = await API(`statistics/?datefrom=${dateFrom.value}&dateto=${dateTo.value}`, 'GET')
    if (dataStats.value != undefined && dataStats.value.length > 0) {
        columns = Object.keys(dataStats.value[0])
    }
    console.log(dataStats.value)
}

const loadDetail = async (category, period) => { 
    const periodDate = new Date(`${period}-01`)
    const periodDateTo = new Date(periodDate.getFullYear(), periodDate.getMonth() + 1, 0)
    const periodTo = periodDateTo.getFullYear() + '-' + (periodDateTo.getMonth() + 1) + '-' + periodDateTo.getDate()
    const categoryQuery = await API(`categories/?name=${category}`, 'GET')
    dataDetails.value = await API(`transactions/?categories=${categoryQuery.id}&datefrom=${period}-01&dateto=${periodTo}`, 'GET')
}

const loadSettings = async () => {
    const settings = await API('settings', 'GET')
    currency.value = settings.currency
    rounding.value = settings.rounding
}

const updateSelection = (category, period) => {
    selectCell.value.column = period
    selectCell.value.row = category
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

watch(() => mainStore.app.refresh, () => {
    load()
})

</script>

<style scoped>
    .hover {
        background-color: #f0f0f0;
    }
</style>