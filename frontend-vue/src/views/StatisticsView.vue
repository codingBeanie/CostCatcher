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

    <!--Status-->
    <div v-if="!statusTransactions"><p class="text-h4 text-error" >No transactions were found. Please upload a file first: <v-btn class="mb-1" prepend-icon="mdi-file-multiple" color="info" to="/import">CSV-Management</v-btn></p></div>
    <div v-if="!statusCategories" class="mt-2 mb-4"><p class="text-h6 text-error" >No categories were created. Add categories and categorize your transactions: <v-btn class="mb-1" prepend-icon="mdi-tag-multiple" color="info" to="/assignments">Categorization</v-btn></p></div>
    <!--File-Table-->
    <v-row>
        <v-container>
            <v-table v-if="dataStats" hover class="fill-width">
                <thead>
                    <tr>
                        <th v-for="column in columns" :key="column" class="text-right cursor-pointer bg-secondary" @mouseover="updateSelection('header', column)">
                            <!--Active Ascending-->
                            <v-btn v-if="sortColumn == column && sortAsc == true" variant="text" color="primary" append-icon="mdi-arrow-up" block @click="sortTable(column)">{{ column }}</v-btn>
                            <!--Active Descending-->
                            <v-btn v-else-if="sortColumn == column && sortAsc == false" variant="text" color="primary" append-icon="mdi-arrow-down" block @click="sortTable(column)">{{ column }}</v-btn>
                            <!--Select-->
                            <v-btn v-else-if="selectCell.column == column && selectCell.row === 'header'" variant="text" color="primary" append-icon="mdi-swap-vertical" block @click="sortTable(column)">{{ column }}</v-btn>
                            <!--Default-->
                            <v-btn v-else variant="text" append-icon="mdi" block>{{ column }}</v-btn>
                        </th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="row in dataStats" :key="row.id" :class="{'bg-expense': row['Category'].name ==='Expenses', 'bg-income':row['Category'].name === 'Income', 'bg-net': row['Category'].name === 'Net'}">
                        <template v-for="column in columns" :key="column" class="text-right pa-0">
                            <!--First Column-->
                            <td v-if="column=='Category'" class="pa-2">
                                <!--Income-->
                                <div v-if="row[column].name==='Income'" class="font-weight-bold text-success">
                                    <v-icon color="success" size="x-large">mdi-cash-plus</v-icon> INCOME
                                </div>

                                <!--Expenses-->
                                <div v-else-if="row[column].name==='Expenses'" class="font-weight-bold text-error">
                                    <v-icon color="error" size="x-large">mdi-cash-minus</v-icon> EXPENSES
                                </div>

                                <!--Net-->
                                <div v-else-if="row[column].name==='Net'" class="font-weight-bold">
                                    <v-icon color="info" size="x-large">mdi-cash-multiple</v-icon> NET
                                </div>

                                <!--Categories-->
                                <div v-else>
                                    <v-chip v-if="row[column].id != 0" :color="row[column].color" link @click="mainStore.openCategoryEdit(row[column].id)">{{ row[column].name }}</v-chip>
                                    <!--undefined-->
                                    <template v-else>
                                        <v-chip color="grey" class="cursor-not-allowed">Undefined</v-chip>
                                            <v-tooltip :text="infoUndefined">
                                            <template v-slot:activator="{ props }">
                                            <v-icon color="info" v-bind="props" density="compact" class="ml-2 ">mdi-information</v-icon>
                                            </template>
                                        </v-tooltip>
                                    </template>
                                 </div>
                            </td>
                            
                            <!--Month Columns-->
                            <td v-else-if="column!='Statistics'" class="cursor-pointer">

                                <!--Income--> 
                                <div v-if="row['Category'].name === 'Income'" @click="mainStore.openReview(selectCell.row, selectCell.column)" @mouseover="updateSelection(row['Category'].id, column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-selected': selectCell.row === row['Category'].id && selectCell.column === column}">
                                    {{ parseFloat(row[column]).toLocaleString(locale) }} {{ currency }}
                                </div>

                                <!--Expenses-->
                                <div v-else-if="row['Category'].name === 'Expenses'" @click="mainStore.openReview(selectCell.row, selectCell.column)" @mouseover="updateSelection(row['Category'].id, column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-selected': selectCell.row === row['Category'].id && selectCell.column === column}">
                                    {{ parseFloat(row[column]).toLocaleString(locale) }} {{ currency }}
                                </div>

                                <!--Net-->
                                <div v-else-if="row['Category'].name === 'Net'" @click="mainStore.openReview(selectCell.row, selectCell.column)" @mouseover="updateSelection(row['Category'].id, column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-selected': selectCell.row === row['Category'].id && selectCell.column === column}">
                                    <div v-if="row[column] < 0" class="text-error text-button"> {{ parseFloat(row[column]).toLocaleString(locale) }} {{ currency }}</div>
                                    <div v-if="row[column] >= 0" class="text-success text-button">{{ parseFloat(row[column]).toLocaleString(locale) }} {{ currency }}</div>
                                </div>

                                <!--Categories-->
                                <div v-else @mouseover="updateSelection(row['Category'].id, column)" @click="mainStore.openReview(selectCell.row, selectCell.column)" class="justify-end pa-2 align-center d-flex fill-height fill-width grow" :class="{'bg-selected': selectCell.row === row['Category'].id && selectCell.column === column}">
                                    {{  parseFloat(row[column]).toLocaleString(locale) }} {{ currency }}
                                </div>
                            </td>

                            <!--Statistics Column-->
                            <td v-else class="justify-end cursor-not-allowed text-h7 text-end align-center fill-height fill-width grow">
                                <div class="text-caption">
                                   {{  parseFloat(row[column].Sum).toFixed(2).toLocaleString(locale) }} {{ currency }} | SUM
                                </div>
                                <div class="text-caption">
                                    {{  parseFloat(row[column].Average).toFixed(2).toLocaleString(locale) }} {{ currency }} | AVG
                                </div>
                                <div class="text-caption">
                                    {{  parseFloat(row[column].Median).toFixed(2).toLocaleString(locale) }} {{ currency }} | MED
                                </div>
                            </td>
                        </template>
                    </tr>
                </tbody>
            </v-table>
        </v-container>    
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
const statusTransactions = ref(false)
const statusCategories = ref(false)

// Data
const dataStats = ref([])
let columns = []

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
const loadTable = async () => {
    const data = await API('datespan', 'GET')
    if (data == undefined) {
        return
    }
    dateFrom.value = data.defaultFirst
    dateTo.value = data.defaultLast

    dataStats.value = await API(`statistics/?datefrom=${dateFrom.value}&dateto=${dateTo.value}&sortcolumn=${sortColumn.value}&sortasc=${sortAsc.value}`, 'GET')
    // Set Columns
    if (dataStats.value != undefined && dataStats.value.length > 0) {
        columns = Object.keys(dataStats.value[0])
        statusTransactions.value = true
    } else {
        statusTransactions.value = false
    }
    if (dataStats.value.map((x) => x.Category.name).length > 4) {
        statusCategories.value = true
    } else {
        statusCategories.value = false
    }
}

const loadSettings = async () => {
    const settings = await API('settings', 'GET')
    currency.value = settings.currency
    locale.value = settings.locale
}

const updateSelection = (category, period) => {
    selectCell.value.column = period
    selectCell.value.row = category
}

const sortTable = (column) => { 
    sortColumn.value = column
    sortAsc.value = !sortAsc.value
    load()
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
    td {
        min-width: 135px;
    }
</style>