<template>
    <!--Titles-->
    <Title title="Graphs" subtitle="Discover your data in a graphs."></Title>

    <Divider title="Bar Graph"></Divider>
    <!--Selectors-->
    <v-row class="mt-2">
        <v-col>
            <Filter object="bargraph" :incomeExpense="true" :yearsSelect="true" :periodMode="true"></Filter>
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

    <v-row>
        <v-col>
            <Hint text="You can click on the category names in the legend to hide them. "></Hint>
        </v-col>
    </v-row>

    <Divider title="Pie Chart" spacing="16"></Divider>
    <!-- Selectors Pie-->
    <v-row class="mt-2">
        <!--fromDate-->
        <v-col>
            <Filter object="piechart" :yearsSelect="false" :periodMode="false" :periodSelect="true" :incomeExpense="true"></Filter>
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
import { useFilterStore } from '../stores/FilterStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { barGraphOptions, pieGraphOptions} from '../composables/graphSettings.js'
import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
import Chart from 'chart.js/auto'
import Filter from '../components/Filter.vue'
import Hint from '../components/Hint.vue'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const filterStore = useFilterStore()
const userStore = useUserStore()
const waitingBar = ref(false)
const waitingPie = ref(false)

// Data Objects
const barData = ref([])
const pieData = ref([])

// Graph Objects
const barGraph = shallowRef(null)
const barGraphPlaceholder = ref(null)
const pieGraph = shallowRef(null)
const pieGraphPlaceholder = ref(null)

// Input Objects

////////////////////////////////////////////////////////////////
// Data Methods
////////////////////////////////////////////////////////////////

// Bar Graph //////////////////////////////////////////////////////////
const loadBarGraph = async () => {
    waitingBar.value = true
    const responseData = await API(`statistics/?periodmode=${filterStore.bargraph.type}&fromyear=${filterStore.bargraph.from}&toyear=${filterStore.bargraph.to}&valuemode=${filterStore.bargraph.filter}`, 'GET')
    if (responseData["data"].length == 0) {
        waitingBar.value = false
        return
    }
    barData.value = responseData["data"]

    let data = barData.value.map(item => item.Data)
    let categories = barData.value.map(item => item.Category)
    let periods = barData.value[0].Period.map(item => item.title)

    if (data.length == 0) {
        return
    }

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
    barGraph.value.data.labels = periods 
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
const loadPieGraph = async () => {
    waitingPie.value = true
    const responseData = await API(`statistics/?periodmode=${filterStore.piechart.type}&fromperiod=${filterStore.piechart.from}&toperiod=${filterStore.piechart.to}&valuemode=${filterStore.piechart.filter}`, 'GET')
    pieData.value = responseData["data"]

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