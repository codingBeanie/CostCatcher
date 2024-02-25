<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Import</h1>
        <p class="mb-4 text-h7">Upload a csv-file with your transaction data here.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--File-Input-->
    <v-row>
        <v-col cols="10"><v-file-input label="Select a csv-file" accept=".csv" @change="loadFile"></v-file-input></v-col>
        <v-col cols="2" class="mt-2"><ImportDialog/></v-col>
    </v-row>

    <!--Preview-Table-->


       
</template>

<script setup>
import {  ref } from 'vue'
import ImportDialog from '../components/ImportDialog.vue'

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