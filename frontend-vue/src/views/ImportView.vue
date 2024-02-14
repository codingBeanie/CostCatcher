<template>
    <BoxContainer>
        <h1>Import</h1>
        <h3>Import your CSV-File here</h3>
    </BoxContainer>

    <BoxContainer>
        <h2>Select a csv-file here </h2>
        <input type="file" accept=".csv" @change="loadFile" class="block w-full p-1 text-lg shadow-md rounded-xl bg-primary-200 text-light-100">
    </BoxContainer>
        
    <BoxContainer>
        <h2>Table of uploaded files</h2>
        <h3 class="mb-5">See what files you already uploaded and delete them if wanted</h3>
        <Table v-if="data" :jsonData="data" />   
    </BoxContainer>
    
    <BoxContainer v-if="previewData.length">
        <TableSchema :arrayData="previewData" />     
    </BoxContainer>
            
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getData } from '../composables/API.js'
import Table from '../components/Table.vue'
import TableSchema from '../components/TableSchema.vue'
import BoxContainer from '../components/BoxContainer.vue'

const data = ref(null)
const previewData = ref([])

const loadFile = (e) => { 
    const file = e.target.files[0]
    const reader = new FileReader()
    reader.onload = (e) => { 
        const content = e.target.result.replace(/"/g, '')
        const lines = content.split('\n')
        lines.forEach(line => { 
            const values = line.split(';')
            previewData.value.push(values)
        })
    }
    reader.readAsText(file, 'ISO-8859-1')
    
}

onMounted(async () => {
    data.value = await getData('files')
})

</script>