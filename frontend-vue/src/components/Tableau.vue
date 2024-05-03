<template>
    <!--MAINFRAME-->
    <v-container class="d-flex-row overflow">

        <!--HEADERS-->
        <v-row class="border-b  d-flex flex-nowrap text-end">
            <v-col class="column">
                <p class="text-button"></p>
            </v-col>
            <v-col v-for="header in headers" class="column pr-6">
                <p class="text-button">{{ header }}</p>
            </v-col>
        </v-row>


<!--*************************************************************************************************-->

        <!--INCOME TITLE-->
        <v-row class="d-flex flex-nowrap">
            <v-col class="colunn">
                <p class="text-overline text-success">INCOME</p>
            </v-col>
            <v-col v-for="header in headers" class="column">
                <!--EMPTY-->
            </v-col>
        </v-row>
        <!--INCOME DATA-->
        <v-row v-for="income in incomeData" class="d-flex flex-nowrap text-end">
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
        <v-row class="border-t text-end d-flex flex-nowrap ">
            <v-col class="column">
                <v-btn variant="text">SUM INCOME</v-btn>
            </v-col>
            <v-col v-for="sum in incomeSums" class="column">
                <v-btn variant="text" @click="">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
            </v-col>
        </v-row>
        
<!--*************************************************************************************************-->

        <!--EXPENSE TITLE-->
        <v-row class="mt-10 d-flex flex-nowrap">
            <v-col class="column">
                <p class="text-overline text-error">EXPENSES</p>
            </v-col>
            <v-col v-for="header in headers" class="column">
                <!--EMPTY-->
            </v-col>
        </v-row>
        <!--EXPENSE DATA-->
        <v-row v-for="expense in expenseData" class="d-flex flex-nowrap text-end">
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
        <v-row class="border-t text-end d-flex flex-nowrap ">
            <v-col class="column">
                <v-btn variant="text">SUM EXPENSES</v-btn>
            </v-col>
            <v-col v-for="sum in expenseSums" class="column">
                <v-btn variant="text" @click="">{{ parseFloat(sum).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</v-btn>
            </v-col>
        </v-row>
        

<!--*************************************************************************************************-->
        <!--NET SUM-->
        <v-row class="text-end border-t-lg d-flex flex-nowrap mt-10">
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
</template>

<script setup>
import { watchEffect, ref } from 'vue';
import { load } from 'webfontloader';
import { API } from '../composables/API.js'
import { useComponentStore } from '../stores/ComponentStore'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()

// Props
const props = defineProps({
    incomeData: Array,
    expenseData: Array,
    headers: Array
})
// variables
const incomeSums = ref([])
const expenseSums = ref([])
const netSums = ref([])
const textUndefined = ref('These transactions are not assigned to any category.')

// Settings
const currency = ref('€')
const locale = ref('de-DE')

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const loadSettings = async () => {
    const settingsData = await API('settings', 'GET')
    currency.value = settingsData.currency
    locale.value = settingsData.locale
}

const sortData = () => {
    // Sort Expense Data
    for (let object of props.expenseData) {
        let values = Object.values(object.Data)
        let sum = values.reduce((accumulator, currentValue) => accumulator + parseFloat(currentValue), 0)
        object.sum = sum
    }
    props.expenseData.sort((a, b) => a.sum - b.sum)

    // Sort Income Data
    for (let object of props.incomeData) {
        let values = Object.values(object.Data)
        let sum = values.reduce((accumulator, currentValue) => accumulator + parseFloat(currentValue), 0)
        object.sum = sum
    }
    props.incomeData.sort((a, b) => b.sum - a.sum)

 }

const calculateSums = () => {
    incomeSums.value = []
    expenseSums.value = []
    netSums.value = []
    for (let period of props.headers) {
        let incomeSum = 0
        let expenseSum = 0
        let netSum = 0

        for (let income of props.incomeData) {
            incomeSum += income.Data[period]
            netSum += income.Data[period]
        }
        for (let expense of props.expenseData) {
            expenseSum += expense.Data[period]
            netSum += expense.Data[period]
        }
        incomeSums.value.push(incomeSum)
        expenseSums.value.push(expenseSum)
        netSums.value.push(netSum)
    }
 }

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watchEffect(() => {
    if (props.incomeData && props.headers) {
    sortData()
    calculateSums()
    loadSettings()
  }
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