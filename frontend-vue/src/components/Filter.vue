<template>
    <v-row class="ml-4 mr-4 d-flex">

        <!--Period Mode-->
        <v-col v-if="periodMode" class="justify-center">
            <v-row class="d-flex justify-center">
                <p class="text-overline">Period Mode</p>
            </v-row>
            <v-row class="d-flex justify-center">
                <v-col class="text-center">
                    <v-btn-toggle mandatory v-model="filterPeriodMode" :onUpdate:modelValue="updateFilter">
                        <v-btn value="0">Monthly</v-btn>
                        <v-btn value="1">Quarterly</v-btn>
                        <v-btn value="2">Yearly</v-btn>
                    </v-btn-toggle>
                </v-col>
            </v-row>
       </v-col>

        <!--IncomeExpense Mode-->
        <v-col v-if="incomeExpense" class="justify-center">
            <v-row class="d-flex justify-center">
                <p class="text-overline">FILTER-TYPES</p>
            </v-row>
            <v-row class="d-flex justify-center">
                <v-col class="text-center">
                    <v-btn-toggle mandatory v-model="filterIncomeExpense" :onUpdate:modelValue="updateFilter">
                        <v-btn value="0">BOTH</v-btn>
                        <v-btn value="1">INCOME</v-btn>
                        <v-btn value="2">EXPENSE</v-btn>
                    </v-btn-toggle>
                </v-col>
            </v-row>
       </v-col>

       <!--From/To Year-->
        <v-col v-if="yearsSelect">
            <v-row class="d-flex justify-center">
                <p class="text-overline">Year Selection</p>
            </v-row>
            <v-row  class="d-flex justify-center align-center">
                <v-col>
                    <v-select label="From" :items="years" v-model="fromValue" :onUpdate:modelValue="updateFilter"></v-select>
                </v-col>
                <v-col>
                    <v-select label="To" :items="years" v-model="toValue" :onUpdate:modelValue="updateFilter"></v-select>
                </v-col>
            </v-row>
        </v-col>

    </v-row>
</template>

<script setup>
import { ref } from 'vue'
import { useFilterStore } from '../stores/FilterStore.js'
import { useComponentStore } from '../stores/ComponentStore'
import { useAlertStore } from '../stores/AlertStore'
import { onMounted } from 'vue'
import { API } from '../composables/API.js' 
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// Setup
const filterStore = useFilterStore()
const componentStore = useComponentStore()
const alertStore = useAlertStore()
const filterPeriodMode = ref(0)
const filterIncomeExpense = ref(0)
const message = ref('')

const fromValue = ref(null)
const toValue = ref(null)
const years = ref([])


// Props
const props = defineProps({
    object: String,
    periodMode: {
        type: Boolean,
        default: true
    },
    yearsSelect: {
        type: Boolean,
        default: true
    },
    incomeExpense: {
        type: Boolean,
        default: false
    }
})

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const updateFilter = () => {
    // Period Mode
    if (props.periodMode) { 
        if (filterPeriodMode.value == 0) {
            filterStore[props.object].type = 'monthly'
        } else if (filterPeriodMode.value == 1) {
            filterStore[props.object].type = 'quarterly'
        } else if (filterPeriodMode.value == 2) {
            filterStore[props.object].type = 'yearly'
        } else {
            filterStore[props.object].type = null
        }
    }

    // Year Selection
    if (props.yearsSelect) {
        filterStore[props.object].from = fromValue.value
        filterStore[props.object].to = toValue.value

        if (fromValue.value > toValue.value) {
        alertStore.showAlert('Selection Error', 'From-year must be smaller than to-year', 'error', 5000)
        }
    }

    // Income/Expense Mode
    if (props.incomeExpense) {
        if (filterIncomeExpense.value == 0) {
            filterStore[props.object].filter = 'both'
        } else if (filterIncomeExpense.value == 1) {
            filterStore[props.object].filter = 'income'
        } else if (filterIncomeExpense.value == 2) {
            filterStore[props.object].filter = 'expense'
        }
    }

    componentStore.refreshApp()
}

const loadFilter = async () => {
    // Period Mode
    if (props.periodMode){
        if (filterStore[props.object].type == 'monthly') {
            filterPeriodMode.value = 0
        } else if (filterStore[props.object].type == 'quarterly') {
            filterPeriodMode.value = 1
        } else if (filterStore[props.object].type == 'yearly') {
            filterPeriodMode.value = 2
        }
    }

    // Year Selection
    if (props.yearsSelect) {
        let currentYear = await API('period/default', 'GET')
        fromValue.value = filterStore[props.object].from == null ? currentYear.value : filterStore[props.object].from
        toValue.value = filterStore[props.object].to == null ? currentYear.value : filterStore[props.object].to
        years.value = await API('period/list', 'GET')
    }

    // Income/Expense Mode
    if (props.incomeExpense) {
        if (filterStore[props.object].filter == 'both') {
            filterIncomeExpense.value = 0
        } else if (filterStore[props.object].filter == 'income') {
            filterIncomeExpense.value = 1
        } else if (filterStore[props.object].filter == 'expense') {
            filterIncomeExpense.value = 2
        }
    }
}

// Lifecycle Hooks
onMounted(async () => {
    loadFilter()
    
})
</script>