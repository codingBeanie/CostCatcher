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
        <v-container>
            <v-table v-if="data" class="fill-width">
                <thead>
                    <tr>
                        <th v-for="column in columns" :key="column" class="text-right bg-secondary">{{ column }}</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="row in data" :key="row.id">
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
                                    <v-chip>{{ row[column] }}</v-chip>
                                </div>
                            </div>
                            
                            <!--Month Columns-->
                            <div v-else-if="column!='Sum' && column!='Average' && column!='Median'" class="cursor-pointer pa-2" @click="loadDetail(row['Category'], column)">

                                <!--Income--> 
                                <div v-if="row['Category'] === 'Income'" class="">
                                 <v-chip color="info">{{ row[column].toLocaleString() }}</v-chip>
                                </div>

                                <!--Expenses-->
                                <div v-else-if="row['Category'] === 'Expenses'">
                                    <v-chip color="info">{{ row[column].toLocaleString() }}</v-chip>
                                </div>

                                <!--Net-->
                                <div v-else-if="row['Category'] === 'Net'">
                                    <v-chip v-if="row[column] < 0" color="error">{{ row[column].toLocaleString() }}</v-chip>
                                    <v-chip v-if="row[column] >= 0" color="success">{{ row[column].toLocaleString() }}</v-chip>
                                </div>

                                <!--Categories-->
                                <div v-else>
                                    {{ row[column].toLocaleString() }}
                                </div>
                            </div>

                            <!--Statistics Column-->
                            <div v-else class="justify-end pa-2 align-center bg-primaryLight d-flex fill-height fill-width grow">
                                {{ row[column].toLocaleString() }}
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
        <v-data-table :items="detail" :headers="headers">
        </v-data-table>
    </v-row>
    
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { API } from '../composables/API.js'
import { useUpdateStore } from '../stores/UpdateStore'

// Variables
const data = ref([])
const detail = ref([])
const dateFrom = ref(`${new Date().getFullYear()}-01-01`)
const dateTo = ref(`${new Date().getFullYear()}-12-31`)
let columns = []
const hover = ref(false)
const updateStore = useUpdateStore()

const headers = [
    { title: 'Date', value: 'date', sortable: true},
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true, align: 'end'}
]

// Methods
const loadTable = async () => {
    data.value = await API(`statistics/?datefrom=${dateFrom.value}&dateto=${dateTo.value}`, 'GET')
    if (data.value != undefined && data.value.length > 0) {
        columns = Object.keys(data.value[0])
    }
    
}

const loadDetail = async (category, period) => { 
    const periodDate = new Date(`${period}-01`)
    const periodDateTo = new Date(periodDate.getFullYear(), periodDate.getMonth() + 1, 0)
    const periodTo = periodDateTo.getFullYear() + '-' + (periodDateTo.getMonth() + 1) + '-' + periodDateTo.getDate()
    if (category === 'None') {
        category = ""
    }
    detail.value = await API(`transactions/?categories=${category}&datefrom=${period}-01&dateto=${periodTo}`, 'GET')
}


// Lifecycle
onMounted(async () => {
    loadTable()
})

</script>

<style scoped>
    .hover {
        background-color: #f0f0f0;
    }
</style>