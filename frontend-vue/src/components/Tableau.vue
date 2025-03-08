<template>
    <v-row class="mt-4">
    <!--FILTER-->
        <Filter object="tableau" :message="message" :periodMode="true" :yearsSelect="true" :categoriesSelection="true" :statistics="true"></Filter>
    </v-row>
    
    <!--MAINFRAME-->
    <v-container class="d-flex-row overflow-x-auto bg-white mt-4">

        <!--HEADERS-->
        <v-row no-gutters class="d-flex flex-nowrap">
            <v-col class="chip mr-1">
                <p class="text-button"></p>
            </v-col>
            <!--PERIODS-->
            <v-col v-for="(header, index) in headers" :key="index" :class="index % 2 === 0 ? 'column bg-primaryLight' : 'column'">
                <p class="text-button border-b full-width pl-12">{{ header.title }}</p>
            </v-col>
            
            <!--STATISTICS-->
            <v-col v-if="filterStore.tableau.statistics" class="column bg-accent ml-1 mr-1">
                <p class="text-button border-b full-width text-center">SUM</p>
            </v-col>
            <v-col v-if="filterStore.tableau.statistics" class="column bg-accent mr-1">
                <p class="text-button border-b full-width text-center">AVERAGE</p>
            </v-col>
            <v-col v-if="filterStore.tableau.statistics" class="column bg-accent">
                <p class="text-button border-b full-width text-center">MEDIAN</p>
            </v-col>
        </v-row>


<!--*************************************************************************************************-->

        <!--INCOME TITLE-->
        <v-row no-gutters class="d-flex flex-nowrap">
            <v-col class="chip">
                <p class="text-overline text-success">INCOME</p>
            </v-col>
            <v-col v-for="header in headers" class="column">
                <!--EMPTY-->
            </v-col>

        </v-row>
        <!--INCOME DATA-->
        <v-row no-gutters v-for="income in incomeData" class="d-flex flex-nowrap text-end mb-2">
            <!--CATEGORY TITLE-->
            <v-col class="chip text-end align-self-center mr-1">
                <div v-if="income.Category.name == 'UNDEFINED'">
                    <v-tooltip :text="textUndefined">
                        <template v-slot:activator="{ props }">
                            <v-btn v-bind="props" variant="text" color="accent">not assigned</v-btn>
                        </template>
                    </v-tooltip>
                </div>
                <div v-else>
                    <v-chip variant="tonal" label :color="income.Category.color" class="chip" @click="componentStore.openCategoryEdit(income.Category.id)">{{ income.Category.name}}</v-chip>
                </div>
            </v-col>


            <!--INCOME DATA-->
            <v-col v-for="(value, key) in income.Data" :class="key % 2 === 0 ? 'column align-self-center bg-primaryLight' : 'column align-self-center'">
                <v-tooltip :text="income.Category.name + ' | ' + headers[key].title" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="plain"  class="d-flex justify-end" @click="componentStore.openReview(income.Category.id, headers[key])"> {{ parseFloat(value).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>

            <!--STATISTIC DATA-->
            <v-col v-if="filterStore.tableau.statistics" class="column align-self-center ml-1 mr-1">
                <v-tooltip :text="income.Category.name" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="outlined" color="secondary" class="d-flex justify-end"> {{ parseFloat(income.Statistics.Sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>
            <v-col v-if="filterStore.tableau.statistics" class="column align-self-center ml-1 mr-1">
                <v-tooltip :text="income.Category.name" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="outlined" color="secondary" class="d-flex justify-end"> {{ parseFloat(income.Statistics.Average).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>
            <v-col v-if="filterStore.tableau.statistics" class="column align-self-center ml-1 mr-1">
                <v-tooltip :text="income.Category.name" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="outlined" color="secondary" class="d-flex justify-end"> {{ parseFloat(income.Statistics.Median).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>

        </v-row>
        <!--INCOME SUM-->
        <v-row no-gutters class="text-end d-flex flex-nowrap ">
            <v-col class="chip align-self-center mr-1">
                <v-chip label variant="text" color="success" class="text-button">SUM INCOME</v-chip>
            </v-col>
           <v-col v-for="(sum, column, index) in incomeSums" :class="index % 2 === 0 ? 'column bg-successLight' : 'column bg-successLight2'">
                <v-tooltip :text="column" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="text" @click="" class="d-flex justify-end">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>
        </v-row>
            
    <!--*************************************************************************************************-->

        <!--EXPENSE TITLE-->
        <v-row no-gutters class="mt-10 d-flex flex-nowrap">
            <v-col class="chip">
                <p class="text-overline text-error">EXPENSES</p>
            </v-col>
            <v-col v-for="header in headers" class="column">
                <!--EMPTY-->
            </v-col>
        </v-row>
        <!--EXPENSE DATA-->
        <v-row no-gutters v-for="expense in expenseData" class="d-flex flex-nowrap text-end mb-2">
            <!--CATEGORY TITLE-->
            <v-col class="chip align-self-center mr-1">
                <div v-if="expense.Category.name == 'UNDEFINED'">
                    <v-tooltip :text="textUndefined">
                        <template v-slot:activator="{ props }">
                            <v-btn v-bind="props" variant="text" color="accent">not assigned</v-btn>
                        </template>
                    </v-tooltip>
                </div>
                <div v-else>
                    <v-chip label variant="tonal" :color="expense.Category.color" class="chip" @click="componentStore.openCategoryEdit(expense.Category.id)">{{ expense.Category.name}}</v-chip>
                </div>
            </v-col>
            <!--EXPENSE DATA-->
            <v-col v-for="(value, key) in expense.Data" :class="key % 2 === 0 ? 'column align-self-center bg-primaryLight' : 'column align-self-center'">
                <v-tooltip :text="expense.Category.name + ' | ' + headers[key].title" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="plain"  class="d-flex justify-end" @click="componentStore.openReview(income.Category.id, headers[key])"> {{ parseFloat(value).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>

            <!--STATISTIC DATA-->
            <v-col v-if="filterStore.tableau.statistics" class="column align-self-center ml-1 mr-1">
                <v-tooltip :text="expense.Category.name" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="outlined" color="secondary" class="d-flex justify-end"> {{ parseFloat(expense.Statistics.Sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>
            <v-col v-if="filterStore.tableau.statistics" class="column align-self-center ml-1 mr-1">
                <v-tooltip :text="expense.Category.name" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="outlined" color="secondary" class="d-flex justify-end"> {{ parseFloat(expense.Statistics.Average).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>
            <v-col v-if="filterStore.tableau.statistics" class="column align-self-center ml-1 mr-1">
                <v-tooltip :text="expense.Category.name" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="outlined" color="secondary" class="d-flex justify-end"> {{ parseFloat(expense.Statistics.Median).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>
        </v-row>
        <!--EXPENSE SUM-->
        <v-row no-gutters class="text-end d-flex flex-nowrap">
            <v-col class="chip align-self-center mr-1">
                <v-chip label variant="text" color="error" class="text-button">SUM EXPENSE</v-chip>
            </v-col>
           <v-col v-for="(sum, column, index) in expenseSums" :class="index % 2 === 0 ? 'column bg-errorLight' : 'column bg-errorLight2'">
                <v-tooltip :text="column" location="top" :open-delay=openDelay>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" block variant="text" @click="" class="d-flex justify-end">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </template>
                </v-tooltip>
            </v-col>
        </v-row>
        

<!--*************************************************************************************************-->
        <!--NET SUM-->
        <v-row no-gutters class="text-end d-flex flex-nowrap mt-10">
            <v-col class="chip mr-1">
                <v-btn variant="text">NET</v-btn>
            </v-col>
            <v-col v-for="(entry) in netSums" class="column pr-1 pl-1">
                <!--Positive Values-->
                <div v-if="entry.value >= 0">
                    <v-tooltip :text="entry.key.toString()" location="top" :open-delay=openDelay>
                        <template v-slot:activator="{ props }">
                            <v-btn v-bind="props" block variant="tonal" class="d-flex justify-end" color="success">{{ parseFloat(entry.value).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                        </template>
                    </v-tooltip>
                </div>
                <div v-else>
                    <!--Negative Values-->
                    <v-tooltip :text="entry.key.toString()" location="top" :open-delay=openDelay>
                        <template v-slot:activator="{ props }">
                            <v-btn v-bind="props" block variant="tonal" class="d-flex justify-end" color="error">{{ parseFloat(entry.value).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                        </template>
                    </v-tooltip>
                </div>
            </v-col>
        </v-row>

    </v-container>

    <v-row class="mt-4 d-flex text-center justify-center">
        <Hint v-if="!waiting" text="Click on the values (except the sums) to see how they have been formed."></Hint>
    </v-row>

    <v-progress-linear
        v-if="waiting"
        color="accent"
        indeterminate
    ></v-progress-linear>
</template>

<script setup>
import { watch, ref } from 'vue';
import { API } from '../composables/API.js'
import { useComponentStore } from '../stores/ComponentStore'
import { useFilterStore } from '../stores/FilterStore'
import Filter from './Filter.vue'
import { onMounted } from 'vue'
import Hint from './Hint.vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const filterStore = useFilterStore()
const waiting = ref(false)

// variables
const textUndefined = ref('These transactions are not assigned to any category.')
const message = ref('')

// Settings
const currency = ref('€')
const locale = ref('de-DE')
const openDelay = ref("600")

// DataFrames
const headers = ref([])
const incomeData = ref([])
const expenseData = ref([])
const incomeSums = ref([])
const expenseSums = ref([])
const netSums = ref([])

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const loadSettings = async () => {
    const settingsData = await API('settings', 'GET')
    currency.value = settingsData.currency
    locale.value = settingsData.locale
}

const loadData = async () => { 
    waiting.value = true
    // check if data selection is possible
    if (filterStore.tableau.from > filterStore.tableau.to) {
        waiting.value = false
        return
    }
    // get the API DATA dump
    const incomeDataFrame = await API(`statistics/?periodmode=${filterStore.tableau.type}&fromyear=${filterStore.tableau.from}&toyear=${filterStore.tableau.to}&valuemode=income&categories=${filterStore.tableau.categories}&ignorezeros=${filterStore.tableau.ignoreZero}`, 'GET')
    const expenseDataFrame = await API(`statistics/?periodmode=${filterStore.tableau.type}&fromyear=${filterStore.tableau.from}&toyear=${filterStore.tableau.to}&valuemode=expense&categories=${filterStore.tableau.categories}&ignorezeros=${filterStore.tableau.ignoreZero}`, 'GET')

    // fill the dataframes
    incomeData.value = incomeDataFrame['data']
    incomeSums.value = incomeDataFrame['sumData']
    expenseData.value = expenseDataFrame['data']
    expenseSums.value = expenseDataFrame['sumData']
    console.log(expenseSums.value)

    // calculate the net sums
    netSums.value = []
    for (const period in incomeSums.value) {
        let incomeValue = incomeSums.value[period]
        let expenseValue = expenseSums.value[period]
        let netValue = incomeValue + expenseValue
        netSums.value.push({ key:period, value:netValue})
    }
    // extract the headers
    try {
        headers.value = Object.values(incomeData.value[0].Period)
    } catch (error) {
        try {
            headers.value = Object.values(expenseData.value[0].Period)
        } catch (error2) {
            headers.value = []
        }
    }
    waiting.value = false
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
const load = async () => { 
    loadSettings()
    loadData()
}

onMounted(() => {
    load()
})

watch(() => componentStore.app.refresh, () => {
    loadData()
})
</script>

<style scoped>
.overflow {
    overflow-x: auto;
}

.column {
    min-width: 120px;
    max-width: 120px;
}

.full-width {
    width: 100%;
}

.line-height {
    line-height: 1.2;
}

.chip {
    min-width: 150px;
    max-width: 150px;
}
</style>