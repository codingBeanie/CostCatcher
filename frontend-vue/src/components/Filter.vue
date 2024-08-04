<template>
    <v-row class="ml-4 mr-4 d-flex">

        <!--Import Mode-->
        <v-col v-if="importMode" class="justify-center">
            <v-row class="d-flex justify-center">
                <p class="text-overline">Import Mode</p>
            </v-row>
            <v-row class="d-flex justify-center">
                <v-col class="text-center">
                    <v-btn-toggle mandatory v-model="importModeSelect" :onUpdate:modelValue="updateFilter">
                        <v-btn value="0">CSV</v-btn>
                        <v-btn value="1">MANUAL</v-btn>
                    </v-btn-toggle>
                </v-col>
            </v-row>
       </v-col>

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
                    <v-select density="comfortable" label="From" :items="years" v-model="fromYear" :onUpdate:modelValue="updateFilter"></v-select>
                </v-col>
                <v-col>
                    <v-select density="comfortable" label="To" :items="years" v-model="toYear" :onUpdate:modelValue="updateFilter"></v-select>
                </v-col>
            </v-row>
        </v-col>

        <!--Period Select-->
        <v-col v-if="periodSelect">
            <v-row class="d-flex justify-center">
                <p class="text-overline">Period Selection</p>
            </v-row>
            <v-row  class="d-flex justify-center align-center">
                <v-col>
                    <v-select density="comfortable" label="From" :items="periods" v-model="fromPeriod" :onUpdate:modelValue="updateFilter"></v-select>
                </v-col>
                <v-col>
                    <v-select density="comfortable" label="To" :items="periods" v-model="toPeriod" :onUpdate:modelValue="updateFilter"></v-select>
                </v-col>
            </v-row> 
        </v-col>

        <!--Categories Select-->
        <v-col v-if="categoriesSelection">
            <v-row class="d-flex justify-center">
                <p class="text-overline">Categories</p>
            </v-row>
            <v-row  class="d-flex justify-center align-center">
                <v-col>
                    <v-select density="comfortable" multiple label="Category" :items="categories" item-title="name" item-value="id" v-model="categoriesSelect" :onUpdate:modelValue="updateFilter">
                        <template v-slot:selection="{ item, index }">
                            <v-chip desity="compact" size="small" color="item.color" v-if="index < 3">
                                {{ item.title }}
                            </v-chip>
                            <span class="text-caption" v-if="index == 3">
                                (+ more)
                            </span>
                        </template>
                    </v-select>
                </v-col>
            </v-row>
        </v-col>

        <!--Statistics Select-->
        <v-col v-if="statistics">
            <v-row class="d-flex justify-center">
                <p class="text-overline">Show Statistics</p>
            </v-row>
            <v-row class="d-flex justify-center">
                <v-col class="d-flex justify-center">
                    <v-switch inset v-model="statisticsSelect" :onUpdate:modelValue="updateFilter" color="accent"></v-switch>
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
const categories = ref([])
const categoriesSelect = ref([])
const statisticsSelect = ref(false)

const fromYear = ref(null)
const toYear = ref(null)
const fromPeriod = ref(null)
const toPeriod = ref(null)
const years = ref([])
const periods = ref([])
const importModeSelect = ref(0)

// Props
const props = defineProps({
    object: String,
    periodMode: {
        type: Boolean,
        default: false
    },
    yearsSelect: {
        type: Boolean,
        default: false
    },
    periodSelect: {
        type: Boolean,
        default: false
    },
    incomeExpense: {
        type: Boolean,
        default: false
    },
    importMode: {
        type: Boolean,
        default: false
    },
    categoriesSelection: {
        type: Boolean,
        default: false
    },
    statistics: {
        type: Boolean,
        default: false
    }
})

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const updateFilter = () => {
    // Import Mode
    if (props.importMode) {
        filterStore[props.object].mode = importModeSelect.value == 0 ? 'csv' : 'manual'
    }

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
        filterStore[props.object].from = fromYear.value
        filterStore[props.object].to = toYear.value

        if (fromYear.value > toYear.value) {
        alertStore.showAlert('Selection Error', 'From-year must be smaller than to-year', 'error', 5000)
        }
    }

    // Period Selection
    if (props.periodSelect) {
        filterStore[props.object].from = fromPeriod.value
        filterStore[props.object].to = toPeriod.value

        if (fromPeriod.value > toPeriod.value) {
        alertStore.showAlert('Selection Error', 'From-period must be smaller than to-period', 'error', 5000)
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

    // Categories
    if (props.categoriesSelection) {
        filterStore[props.object].categories = categoriesSelect.value
    }

    // Statistics
    if (props.statistics) {
        filterStore[props.object].statistics = statisticsSelect.value
    }

    componentStore.refreshApp()
}

const loadFilter = async () => {
    // Import Mode
    if (props.importMode) {
        if (filterStore[props.object].mode == 'csv') {
            importModeSelect.value = 0
        } else if (filterStore[props.object].mode == 'manual') {
            importModeSelect.value = 1
        }
    }

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
        let latestPeriod = await API('period/default', 'GET')
        fromYear.value = filterStore[props.object].from == null ? latestPeriod.year : filterStore[props.object].from
        toYear.value = filterStore[props.object].to == null ? latestPeriod.year : filterStore[props.object].to
        years.value = await API('period/list/years', 'GET')
    }

    // Period Selection
    if (props.periodSelect) {
        let latestPeriod = await API('period/default', 'GET')
        latestPeriod = latestPeriod.year + '-' + latestPeriod.month
        fromPeriod.value = filterStore[props.object].from == null ? latestPeriod : filterStore[props.object].from
        toPeriod.value = filterStore[props.object].to == null ? latestPeriod : filterStore[props.object].to
        periods.value = await API('period/list/months', 'GET')
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

    // Categories
    if (props.categoriesSelection) {
        // load options
        categories.value = await API('categories', 'GET')

        // load selected
        if (filterStore[props.object].categories != null) {
            categoriesSelect.value = filterStore[props.object].categories
        }
        else {
            const categoryList = categories.value.map(category => category.id)
            categoriesSelect.value = categoryList
        }
    }

    // Statistics
    if (props.statistics) {
        if (filterStore[props.object].statistics) {
            statisticsSelect.value = filterStore[props.object].statistics
        }
        else {
            statisticsSelect.value = false
        }
    }
}

// Lifecycle Hooks
onMounted(async () => {
    loadFilter()
    
})
</script>