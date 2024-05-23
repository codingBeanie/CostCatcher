<template>
    <!--Titles-->
    <Title title="Statistics" subtitle="Overview of your transactions"></Title>
    <Divider title="BASIC TABLE" spacing="8"></Divider>

    <v-row>
        <!--File-Table-->
        <Tableau></Tableau>
    </v-row>

    
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
import Tableau from '../components/Tableau.vue'
import Hint from '../components/Hint.vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()

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

