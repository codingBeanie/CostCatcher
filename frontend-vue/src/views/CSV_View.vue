<template>
    <!--Titles-->
    <div>
        <h1 class="">CSV Management</h1>
        <p class="mb-4 text-h6 font-weight-light">Upload a new csv-file with your transaction data or delete previous uploaded ones if neccesary.</p>
    </div>
    <v-divider class="mb-2"></v-divider>

    <!--File-Input-->
    <v-row>
        <v-col>
            <p v-if="importError==true" class="text-h7 text-error">The import scheme is not valid. Please check the import scheme in the settings <v-btn size="small" variant="plain" icon="mdi-cog" @click="mainStore.openSettings()" class="mb-1"></v-btn>.</p>
        </v-col>
    </v-row>
    <v-row class="">
        <v-col><v-file-input label="Upload a new csv-file" accept=".csv" @change="readFile" v-model="inputFile"></v-file-input></v-col>
    </v-row>


    <v-divider class="mb-8"></v-divider>

    <!--Preview-Table-->
    <div v-if="fileLoaded && !importError"> 
        <v-row>
            <h2 class="mb-4">Preview</h2>
        </v-row>

        <v-row>
            <v-data-table :items="dataPreview" :headers="headersPreview" density="compact">
                <!--Date-->
                <template v-slot:item.date="{ item }">
                    {{ new Date(item.date).toLocaleDateString() }}
                </template>

                <!--Amount-->
                <template v-slot:item.amount="{ item }">
                    <v-row class="justify-end mr-12">
                        <div v-if="item.amount < 0" class="text-error">{{ parseFloat(item.amount).toFixed(rounding) }} {{ currency }}</div>
                        <div v-if="item.amount >= 0" class="text-success">{{ parseFloat(item.amount).toFixed(rounding) }} {{ currency }}</div>
                    </v-row>
                </template>
            </v-data-table>
        </v-row>

        <v-row class="">
            <v-col cols="10" class="mt-2 text-end">
                <p>Check if your data is recognised correctly. Adjust the csv settings <v-btn size="small" variant="plain" icon="mdi-cog" @click="mainStore.openSettings()" class="mb-1"></v-btn> if needed.</p>     
            </v-col>
            <v-col cols="2" class="mt-2 text-end">
                <v-btn color="accent" @click="uploadData()" prependIcon="mdi-upload">Confirm</v-btn>
            </v-col> 
        </v-row>
    </div>

    <!--Uploaded Files Table-->       
    <div v-else>
        <v-row>
            <h2 class="mt-10 mb-4">Uploaded Files</h2>
        </v-row>
        <v-row>
            <v-data-table :items="dataUploads" :headers="headersFiles">
                <!--Date-->
                <template v-slot:item.fileDate="{ item }">
                    {{ new Date(item.fileDate).toLocaleString() }}
                </template>

                <template v-slot:item.action="{ item }">
                    <v-btn density="compact" icon="mdi-delete" color="" @click="mainStore.openDelete('files', { fileName: `${item.fileName}`, fileDate: `${item.fileDate}` }, `${item.fileName}`)">
                    </v-btn>
                </template>
            </v-data-table>
        </v-row>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import moment from 'moment'
import { API } from '../composables/API.js'
import { watch } from 'vue'
import { useMainStore } from '../stores/MainStore.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const mainStore = useMainStore()
const fileLoaded = ref(false)
const importError = ref(false)

// Data Objects
const dataPreview = ref([])
const dataUploads = ref([])
const schema = ref([])
const settings = ref([])

// Input Objects
const inputFile = ref()
const fileName = ref('')
const fileDate = ref('')

// Display Objects
const currency = ref('€')
const rounding = ref(0)

// Table Details
const headersFiles = [
    { title: 'File Name', value: 'fileName' },
    { title: 'Upload Date', value: 'fileDate' },
    { title: 'Actions', value: 'action', align: 'center'}
]
const headersPreview = [
    { title: 'Date', value: 'date' },
    { title: 'Recipient', value: 'recipient' },
    { title: 'Description', value: 'description' },
    { title: 'Amount', value: 'amount', align: 'center' }
]

////////////////////////////////////////////////////////////////
// Data Methods
////////////////////////////////////////////////////////////////
// Load the table
const loadTableUploads = async () => {
    const data = await API('files', 'GET')
    dataUploads.value = data.map(item => ({ ...item, action: null }))
}

const readFile = () => { 
    const data = []
    const file = inputFile.value[0]
    const reader = new FileReader()
    reader.onload = (input) => { 
        const content = input.target.result.replace(/"/g, '')
        const lines = content.split('\n')
        lines.forEach(line => { 
            const values = line.split(schema.value.delimiter)
            data.push(values)
        })
        fileLoaded.value = true
        parseData(data)
    }
    reader.readAsText(file, 'ISO-8859-1')
}

const parseData = (data) => {
    const fileName = inputFile.value[0].name
    const fileDate = new Date().toISOString()
    currency.value = settings.value.currency
    rounding.value = settings.value.rounding

    dataPreview.value = []

    try { 
        data.forEach((entry, index) => {
            if (index >= schema.value.rowFirst && index < data.length - schema.value.rowLast) {
                const originalDate = entry[schema.value.colDate - 1]
                const parsedDate = moment(originalDate, schema.value.dateFormat)
                const date = parsedDate.format('YYYY-MM-DD')
                const recipient = entry[schema.value.colRecipient - 1]
                const description = entry[schema.value.colDescription - 1]
                const amount = entry[schema.value.colAmount - 1].replace(schema.value.thousandsSeparator, '').replace(schema.value.decimalSeparator, '.')
                dataPreview.value.push({ date, recipient, description, amount, fileName, fileDate })
            }
        })
        importError.value = false

    } catch (error) {
        console.log("Error converting data: ", error)
        importError.value = true
        mainStore.showAlert('Error', `The import scheme is not valid. Please check the import scheme in the settings.`, 'error', 5000)
    }
}

const uploadData = async () => {
    await API('transactions', 'POST', dataPreview.value)
    inputFile.value = null
    fileLoaded.value = false
    importError.value = false
    load()
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = async () => {
    schema.value = await API('schema', 'GET')
    settings.value = await API('settings', 'GET')
    loadTableUploads()

    if(fileLoaded.value) {
        readFile()
    }
}

onMounted(async () => {
    load()
})

watch(() => mainStore.app.refresh, () => {
    load()
})

</script>