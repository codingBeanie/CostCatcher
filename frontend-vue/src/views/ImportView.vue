<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Import</h1>
        <p class="mb-4 text-h7">Upload a csv-file with your transaction data here.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--File-Input-->
    <v-row>
        <v-col cols="10"><v-file-input label="Select a csv-file" accept=".csv" @change="loadFile" v-model="inputFile"></v-file-input></v-col>
        <v-col cols="2" class="mt-2"><ImportDialog/></v-col>
    </v-row>

    <!--Preview-Table-->
    <div v-if="previewData.length > 0">
        <v-divider class="mb-8"></v-divider>
        <v-row>
            <h3 class="ml-3">Preview Table</h3>
        </v-row>
        <v-row>
            <v-col>
                <p class="text-h7">Check if your data is recognised correctly. Adjust the schema settings if needed.</p>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn color="accent" @click="uploadData" prependIcon="mdi-upload">Upload</v-btn>
            </v-col> 
        </v-row>
        <v-row>
            <v-data-table :items="previewData" density="compact"/>
        </v-row>
    </div>


 
</template>

<script setup>
import { ref } from 'vue'
import moment from 'moment'
import { getData } from '../composables/API.js'
import { postData } from '../composables/API.js'
import ImportDialog from '../components/ImportDialog.vue'
import { watch } from 'vue'
import { useUpdateStore } from '../stores/UpdateStore.js'
import { useAlertStore } from '../stores/AlertStore.js'
import { useRouter } from 'vue-router'

const rawData = ref([])
const previewData = ref([])
const updateStore = useUpdateStore()
const updateAlert = useAlertStore()
const fileLoaded = ref(false)
const inputFile = ref()
const router = useRouter()

// load the file from input
const loadFile = async (e) => { 
    const file = e.target.files[0]
    const schema = await getData('schema')
    const reader = new FileReader()
    reader.onload = (e) => { 
        const content = e.target.result.replace(/"/g, '')
        const lines = content.split('\n')
        lines.forEach(line => { 
            const values = line.split(schema[0].delimiter)
            rawData.value.push(values)
        })
    }
    reader.readAsText(file, 'ISO-8859-1')
    fileLoaded.value = true
    convertData(rawData.value)
}

// converting data based on import scheme
const convertData = async (data) => {
    // get the import scheme
    const schema = await getData('schema')
    const maxRows = data.length
    const fileName = inputFile.value[0].name
    const fileDate = new Date().toISOString()

    try { 
        data.forEach((entry, index) => {
            if (index >= schema[0].rowFirst && index < maxRows - schema[0].rowLast) {
                const rawDate = entry[schema[0].colDate - 1]
                const parsedDate = moment(rawDate, 'DD.MM.YYYY')
                const date = parsedDate.format('YYYY-MM-DD')
                const recipient = entry[schema[0].colRecipient - 1]
                const description = entry[schema[0].colDescription - 1]
                const amount = entry[schema[0].colAmount - 1].replace(schema[0].thousandsSeparator, '').replace(schema[0].decimalSeparator, '.')
                previewData.value.push({ date, recipient, description, amount, fileName, fileDate })
            }
        })
    } catch (error) {
        updateAlert.showAlert('Error', 'The import scheme is not valid. Please check the import scheme in the settings.', 'error', 5000)
    }
}

// uploading data
const uploadData = async () => {
    try {
        await postData(previewData.value, 'transactions')
        router.push('/files')
    }
    catch (error) {
        console.log(error)
    }
}

watch(() => updateStore.schemaClosed, () => {
    if (fileLoaded.value) {
        previewData.value = []
        convertData(rawData.value)
    }
    })
</script>