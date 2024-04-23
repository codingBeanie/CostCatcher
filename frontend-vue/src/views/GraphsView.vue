<template>
    <!--Titles-->
    <Title title="Graphs" subtitle="Discover your data in a graphs."></Title>
    <Divider title="Monthly Statistics"></Divider>

    <!--Bar Graph-->


</template>

<script setup>
import { ref, onMounted } from 'vue'
import { API } from '../composables/API.js'
import { watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useAlertStore } from '../stores/AlertStore.js'
import { useUserStore } from '../stores/UserStore.js'
import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const alertStore = useAlertStore()

// Data Objects

// Input Objects

// Display Objects
const currency = ref('€')
const locale = ref('de-DE')


////////////////////////////////////////////////////////////////
// Data Methods
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = async () => {
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