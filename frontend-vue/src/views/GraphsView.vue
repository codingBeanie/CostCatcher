<template>
    <!--Titles-->
    <Title title="Graphs" subtitle="Discover your data in a graphs."></Title>

    <Divider title="Bar Graph"></Divider>
    <!--Selectors-->
    <v-row class="mt-2">
        <!--fromDate-->
        <v-col>
            <v-text-field clearable label="From Date" 
                        type="date"
                        v-model="dateFromBar" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="loadBarGraph"
                        >
            </v-text-field>
        </v-col>

        <!--toDate-->
        <v-col>
            <v-text-field clearable label="To Date" 
                        type="date"
                        v-model="dateToBar" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="loadBarGraph"
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
                v-model="selectedCategoriesBar"
                multiple
                @update:model-value="loadBarGraph"
                ></v-select>
        </v-col>
    </v-row>

    <v-row v-if="waitingBar">
        <v-progress-linear
            color="accent"
            indeterminate
        ></v-progress-linear>
    </v-row>

    <!--Bar Graph-->
    <v-row class="mt-2 bg-primaryLight">
        <canvas ref="barGraphPlaceholder"></canvas>
    </v-row>


    <Divider title="Pie Chart" spacing="16"></Divider>
    <!-- Selectors Pie-->
    <v-row class="mt-2">
        <!--fromDate-->
        <v-col>
            <v-text-field clearable label="From Date" 
                        type="date"
                        v-model="dateFromPie" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="loadPieGraph"
                        >
            </v-text-field>
        </v-col>

        <!--toDate-->
        <v-col>
            <v-text-field clearable label="To Date" 
                        type="date"
                        v-model="dateToPie" 
                        placeholder="e.g. 01.01.23"
                        @update:model-value="loadPieGraph"
                        >
            </v-text-field>
        </v-col>

        <!--Filter Mode-->
        <v-col cols="3">
            <v-radio-group inline v-model="filterMode" @update:model-value="loadPieGraph" class="mt-2">
                <v-radio label="Income" value="income"></v-radio>
                <v-radio label="Expense" value="expense"></v-radio>
            </v-radio-group>
        </v-col>
    </v-row>

    <v-row v-if="waitingPie">
        <v-progress-linear
            color="accent"
            indeterminate
        ></v-progress-linear>
    </v-row>

    <!--Bar Graph-->
    <v-row class="bg-primaryLight">
        <canvas ref="pieGraphPlaceholder"></canvas>
    </v-row>
    

</template>

<script setup>
import { ref, onMounted, shallowRef } from 'vue'
import { API } from '../composables/API.js'
import { watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useAlertStore } from '../stores/AlertStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { barGraphOptions, pieGraphOptions} from '../composables/graphSettings.js'
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
const waitingBar = ref(false)
const waitingPie = ref(false)

// Data Objects
const categories = ref([])
const barData = ref([])
const pieData = ref([])

// Graph Objects
const barGraph = shallowRef(null)
const barGraphPlaceholder = ref(null)
const pieGraph = shallowRef(null)
const pieGraphPlaceholder = ref(null)

// Input Objects
const dateFromBar = ref(``)
const dateToBar = ref(``)
const selectedCategoriesBar = ref(['Net'])
const dateFromPie = ref(``)
const dateToPie = ref(``)
const filterMode = ref('income')

// Display Objects
const currency = ref('€')
const locale = ref('de-DE')


////////////////////////////////////////////////////////////////
// Data Methods
////////////////////////////////////////////////////////////////
const loadDateRange = async () => {
    if (dateFromBar.value == '' && dateToBar.value == '') {
        // Load the default date range
        const data = await API('datespan', 'GET')
        if(data == undefined || data == 0) {
            alertStore.showAlert('No data available.', 'error')
            return
        }
        dateFromBar.value = data.defaultFirst
        dateToBar.value = data.defaultLast

        const lastYear = data.defaultLast.split('-')[0]
        const lastMonth = data.defaultLast.split('-')[1]
        dateFromPie.value = `${lastYear}-${lastMonth}-01`
        dateToPie.value = data.defaultLast
    }
}

// Bar Graph //////////////////////////////////////////////////////////
const loadBarData = async () => {
    barData.value = await API(`statistics/?datefrom=${dateFromBar.value}&dateto=${dateToBar.value}`, 'GET')
    categories.value = barData.value.map(item => item.Category.name)
    barData.value = barData.value.filter(item => selectedCategoriesBar.value.includes(item.Category.name))
}


const loadBarGraph = async () => {
    waitingBar.value = true
    await loadBarData()
    let data = barData.value.map(item => item.Data)
    let categories = barData.value.map(item => item.Category)

    if (data.length == 0) {
        return
    }

    let labels = Object.keys(data[0])
    let datasets = []
    for (let i = 0; i < data.length; i++) { 
        datasets.push({
            label: categories[i].name,
            data: Object.values(data[i]).map(Math.abs),
            backgroundColor: categories[i].color,
        })
    }
    if (!barGraph.value) {
        initBarGraph()
    }
    barGraph.value.data.labels = labels
    barGraph.value.data.datasets = datasets
    barGraph.value.options = barGraphOptions
    barGraph.value.update()
    waitingBar.value = false
}

const initBarGraph = () => {
    barGraph.value = new Chart(
        barGraphPlaceholder.value,
        {
            type: 'bar',
            data: {
                labels: [''],
                datasets: []
            },
        }
    )
}

// Pie Graph //////////////////////////////////////////////////////////
const loadPieData = async () => {
    pieData.value = await API(`statistics/?datefrom=${dateFromPie.value}&dateto=${dateToPie.value}&totals=False&filtermode=${filterMode.value}&showTotals=false`, 'GET')
}

const loadPieGraph = async () => {
    waitingPie.value = true
    await loadPieData()

    if (!pieGraph.value) {
        initPieGraph()
    }

    let data = pieData.value.map(item => item.Data)
    let categories = pieData.value.map(item => item.Category)
    pieGraph.value.data.labels = categories.map(item => item.name)
    for (let i = 0; i < data.length; i++) {
        let sum = 0
        for (let key in data[i]) {
            sum += data[i][key]
        }
        data[i] = sum
    }
    pieGraph.value.data.datasets = [{
        data: data,
        backgroundColor: categories.map(item => item.color)
    }]
    pieGraph.value.options = pieGraphOptions
    pieGraph.value.update()

    waitingPie.value = false
}

const initPieGraph = () => {
    pieGraph.value = new Chart(
        pieGraphPlaceholder.value,
        {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: []
            },
        }
    )
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = async () => {
    await loadDateRange()
    loadBarGraph()
    loadPieGraph()
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