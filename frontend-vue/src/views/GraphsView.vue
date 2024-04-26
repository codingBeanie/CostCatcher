<template>
    <!--Titles-->
    <Title title="Graphs" subtitle="Discover your data in a graphs."></Title>
    <Divider title="General Visualisation"></Divider>

    <!--Selectors-->
    <v-row class="mt-2">
        <!--fromDate-->
        <v-col>
            <v-text-field clearable label="From Date" 
                        type="date"
                        v-model="dateFrom" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="load"
                        >
            </v-text-field>
        </v-col>

        <!--toDate-->
        <v-col>
            <v-text-field clearable label="To Date" 
                        type="date"
                        v-model="dateTo" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="load"
                        >
            </v-text-field>
        </v-col>

        <!--Category-->
        <v-col>
            <v-select
                label="Categories"
                :items=categories
                chips
                clearable
                v-model="selectedCategories"
                multiple
                @update:model-value="delayedLoad"
                ></v-select>
        </v-col>
    </v-row>

    <v-row v-if="waiting">
        <v-progress-linear
            color="accent"
            indeterminate
        ></v-progress-linear>
    </v-row>

    <!--Bar Graph-->
    <canvas ref="barGraphPlaceholder"></canvas>

</template>

<script setup>
import { ref, onMounted, shallowRef } from 'vue'
import { API } from '../composables/API.js'
import { watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useAlertStore } from '../stores/AlertStore.js'
import { useUserStore } from '../stores/UserStore.js'
import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
import Chart from 'chart.js/auto'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const alertStore = useAlertStore()
const waiting = ref(false)

// Data Objects
const categories = ref([])
const statData = ref([])

// Graph Objects
const barGraph = shallowRef(null)
const barGraphPlaceholder = ref(null)

// Input Objects
const dateFrom = ref(``)
const dateTo = ref(``)
const selectedCategories = ref(['Net'])

// Display Objects
const currency = ref('€')
const locale = ref('de-DE')


////////////////////////////////////////////////////////////////
// Data Methods
////////////////////////////////////////////////////////////////
const loadDateRange = async () => {
    if (dateFrom.value == '' && dateTo.value == '') {
        // Load the default date range
        const data = await API('datespan', 'GET')
        dateFrom.value = data.defaultFirst
        dateTo.value = data.defaultLast
    }
}

const loadStatData = async () => {
    statData.value = await API(`statistics/?datefrom=${dateFrom.value}&dateto=${dateTo.value}`, 'GET')
    categories.value = statData.value.map(item => item.Category.name)
}

const filterData = () => {
    statData.value = statData.value.filter(item => selectedCategories.value.includes(item.Category.name))
 }

const loadIncomeExpenseGraph = () => {
    let data = statData.value.map(item => item.Data)
    let categories = statData.value.map(item => item.Category)

    if (data.length == 0) {
        return
    }

    let labels = Object.keys(data[0])
    let datasets = []
    for (let i = 0; i < data.length; i++) { 
        datasets.push({
            label: categories[i].name,
            data: Object.values(data[i]),
            backgroundColor: categories[i].color,
        })
    }
    if (!barGraph.value) {
        initializeGraph()
    }
    barGraph.value.data.labels = labels
    barGraph.value.data.datasets = datasets
    barGraph.value.update()
}

const initializeGraph = () => {
    barGraph.value = new Chart(
        barGraphPlaceholder.value,
        {
            type: 'bar',
            data: {
                labels: [''],
                datasets: []
            },
            options: {
                locale: new Intl.NumberFormat(locale.value)
            }
        }
    )
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = async () => {
    waiting.value = true
    await loadDateRange()
    await loadStatData()
    await filterData()
    loadIncomeExpenseGraph()
    waiting.value = false
}

const delayedLoad = () => {
    setTimeout(() => {
        load()
    }, 500)
}

onMounted(() => {
    load()
})

watch(() => userStore.username, () => {
    load()
})

watch(() => componentStore.app.refresh, () => {
    load()
})


</script>