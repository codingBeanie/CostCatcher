<template>
    <BoxContainer>
        <h1>Manage Files</h1>
        <h3>View and delete your uploaded Files</h3>
    </BoxContainer>

    <BoxContainer>
        <h2>Table of uploaded files</h2>
        <h3 class="mb-5">See what files you already uploaded and delete them if wanted</h3>
        <Table v-if="data && data.length" :jsonData="data" />   
    </BoxContainer>
    
</template>

<script setup>
import BoxContainer from '../components/BoxContainer.vue'
import Table from '../components/Table.vue'
import { onMounted, ref } from 'vue';
import { getData } from '../composables/API.js'

const data = ref(null)

onMounted(async () => {
    data.value = await getData('files')
})
</script>