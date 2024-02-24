<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Import</h1>
        <p class="mb-4 text-h7">Upload a csv-file with your transaction data here.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--File-Input-->
    <div>
        <v-file-input label="Select a csv-file" accept=".csv" @change="loadFile"></v-file-input>
    </div>

    <!--Preview-Table-->
    <div v-if="previewData.length">
        <TableImport :arrayData="previewData"/>
    </div>

<!--     <BoxContainer>
        <h1>Import</h1>
        <h3>Import your CSV-File here</h3>
    </BoxContainer>

    <BoxContainer>
        <h2>Select a csv-file here </h2>
        <input id="inputFile" type="file" accept=".csv" @change="loadFile" class="block w-full p-1 text-lg shadow-md rounded-xl bg-primary-200 text-light-100">
    </BoxContainer>
        
    <BoxContainer v-if="previewData.length">
        <TableImport :arrayData="previewData" />     
    </BoxContainer> -->

            
</template>

<script setup>
import {  ref } from 'vue';
import TableImport from '../components/TableImport.vue'

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
    console.log(previewData.value)
    
}

</script>