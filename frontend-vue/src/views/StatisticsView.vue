<template>
    <!--Titles-->
    <Title title="Statistics" subtitle="Overview of your transactions"></Title>
    <Divider title="BASIC TABLE" spacing="8"></Divider>

    <!--Status-->
    <v-row>
        <div v-if="statusCategories && !waiting" class="mt-2 mb-4"><p class="text-h6 text-error" >No categories were created. Add categories and categorize your transactions: <v-btn class="mb-1" prepend-icon="mdi-tag-multiple" color="info" to="/assignments">Categorization</v-btn></p></div>
        <div v-if="statusTransactions && !waiting"><p class="text-h4 text-error" >No transactions were found. Please upload a file first: <v-btn class="mb-1" prepend-icon="mdi-file-multiple" color="info" to="/import">CSV-Management</v-btn></p></div>
    </v-row>
    
    <v-row>
        <!--File-Table-->
        <Tableau id="tableau" class="mb-4" :incomeData="incomeData" :expenseData="expenseData" :headers="headers"></Tableau>
    </v-row>
   <v-row v-if="waiting" class="">
        <v-progress-linear
            color="accent"
            indeterminate
        ></v-progress-linear>
    </v-row>
    <v-row>
        <Hint v-if="!waiting" text="Click on the values (except the sums) to see how they have been formed."></Hint>
    </v-row>
    
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { API } from '../composables/API.js'
import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
import Tableau from '../components/Tableau.vue'
import Hint from '../components/Hint.vue'
import Filter from '../components/Filter.vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const statusTransactions = ref(true)
const statusCategories = ref(true)
const waiting = ref(true)

// Data
const incomeData = ref([])
const expenseData = ref([])
const headers = ref()

// Inputs

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = () => {
}

onMounted(async () => {
    load()
})

watch(() => componentStore.app.refresh, () => {
    load()
})

watch(() => userStore.username, () => {
    load()
})

</script>

