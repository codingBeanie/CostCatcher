<template>
    <v-row class="mt-4">
    <!--FILTER-->
        <Filter object="tableau" :message="message"></Filter>
    </v-row>
    
    <!--MAINFRAME-->
        <v-container class="d-flex-row overflow bg-white mt-4">

            <!--HEADERS-->
            <v-row no-gutters class="border-b  d-flex flex-nowrap text-end">
                <v-col class="column">
                    <p class="text-button"></p>
                </v-col>
                <v-col v-for="header in headers" class="column pr-6">
                    <p class="text-button">{{ header }}</p>
                </v-col>
            </v-row>


<!--*************************************************************************************************-->

            <!--INCOME TITLE-->
            <v-row no-gutters class="d-flex flex-nowrap">
                <v-col class="colunn">
                    <p class="text-overline text-success">INCOME</p>
                </v-col>
                <v-col v-for="header in headers" class="column">
                    <!--EMPTY-->
                </v-col>
            </v-row>
            <!--INCOME DATA-->
            <v-row no-gutters v-for="income in incomeData" class="d-flex flex-nowrap text-end">
                <!--CATEGORY TITLE-->
                <v-col class="column">
                    <div v-if="income.Category.name == 'UNDEFINED'">
                        <v-tooltip :text="textUndefined">
                            <template v-slot:activator="{ props }">
                                <v-btn v-bind="props" variant="text">{{ income.Category.name }}</v-btn>
                            </template>
                        </v-tooltip>
                    </div>
                    <div v-else>
                        <v-btn variant="text" @click="componentStore.openCategoryEdit(income.Category.id)">{{ income.Category.name}}</v-btn>
                    </div>
                </v-col>
                <!--INCOME DATA-->
                <v-col v-for="(value, key) in income.Data" class="column">
                    <v-btn variant="plain" @click="componentStore.openReview(income.Category.id, key)">{{ parseFloat(value).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                </v-col>
            </v-row>
            <!--INCOME SUM-->
            <v-row no-gutters class="border-t text-end d-flex flex-nowrap ">
                <v-col class="column">
                    <v-btn variant="text">SUM INCOME</v-btn>
                </v-col>
                <v-col v-for="sum in incomeSums" class="column">
                    <v-btn variant="text" @click="">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                </v-col>
            </v-row>
                
        <!--*************************************************************************************************-->

            <!--EXPENSE TITLE-->
            <v-row no-gutters class="mt-10 d-flex flex-nowrap">
                <v-col class="column">
                    <p class="text-overline text-error">EXPENSES</p>
                </v-col>
                <v-col v-for="header in headers" class="column">
                    <!--EMPTY-->
                </v-col>
            </v-row>
            <!--EXPENSE DATA-->
            <v-row no-gutters v-for="expense in expenseData" class="d-flex flex-nowrap text-end">
                <!--CATEGORY TITLE-->
                <v-col class="column">
                    <div v-if="expense.Category.name == 'UNDEFINED'">
                        <v-tooltip :text="textUndefined">
                            <template v-slot:activator="{ props }">
                                <v-btn v-bind="props" variant="text">{{ expense.Category.name }}</v-btn>
                            </template>
                        </v-tooltip>
                    </div>
                    <div v-else>
                        <v-btn variant="text" @click="componentStore.openCategoryEdit(expense.Category.id)">{{ expense.Category.name}}</v-btn>
                    </div>
                </v-col>
                <!--EXPENSE DATA-->
                <v-col v-for="(value, key) in expense.Data" class="column">
                    <v-btn variant="plain" @click="componentStore.openReview(expense.Category.id, key)">{{ parseFloat(value).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                </v-col>
            </v-row>
            <!--EXPENSE SUM-->
            <v-row no-gutters class="border-t text-end d-flex flex-nowrap ">
                <v-col class="column">
                    <v-btn variant="text">SUM EXPENSES</v-btn>
                </v-col>
                <v-col v-for="sum in expenseSums" class="column">
                    <v-btn variant="text" @click="">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                </v-col>
            </v-row>
            

    <!--*************************************************************************************************-->
            <!--NET SUM-->
            <v-row no-gutters class="text-end border-t-lg d-flex flex-nowrap mt-10">
                <v-col class="column">
                    <v-btn variant="text">NET</v-btn>
                </v-col>
                <v-col v-for="sum in netSums" class="column">
                    <div v-if="sum >= 0">
                        <v-btn variant="text" color="success">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </div>
                    <div v-else>
                        <v-btn variant="text" color="error">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
                    </div>
                </v-col>
            </v-row>

        </v-container>


   <v-row v-if="waiting" class="">
        <v-progress-linear
            color="accent"
            indeterminate
        ></v-progress-linear>
    </v-row>

    <v-row class="mt-4 d-flex text-center justify-center">
        <Hint v-if="!waiting" text="Click on the values (except the sums) to see how they have been formed."></Hint>
    </v-row>
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
    const data = await API(`statistics/?periodmode=${filterStore.tableau.type}&fromyear=${filterStore.tableau.from}&toyear=${filterStore.tableau.from}`, 'GET')
    console.log(data)
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

watch([() => filterStore.tableau.from, () => filterStore.tableau.to, () => filterStore.tableau.type], () => {
    loadData()
})
</script>

<style scoped>
.overflow {
    overflow-x: auto;
}

.column {
    min-width: 140px;
    max-width: 300px;
}
</style>