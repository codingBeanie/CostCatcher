<template>
    <!--Titles-->
    <div>
        <h1 class="">CSV Management</h1>
        <p class="mb-4 text-h6 font-weight-light">Upload a new csv-file with your transaction data or delete previous uploaded ones if neccesary.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--File-Input-->
    <v-row>
        <v-col><v-file-input label="Upload a new csv-file" accept=".csv" @change="loadFile" v-model="inputFile"></v-file-input></v-col>
    </v-row>

    <v-divider class="mb-8"></v-divider>

    <!--Preview-Table-->
    <div v-if="fileLoaded"> 
        <v-row>
            <h2 class="mb-4">Preview</h2>
        </v-row>

        <v-row>
            <v-data-table :items="previewData" :headers="headers" density="compact">
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
                <p>Check if your data is recognised correctly. Adjust the csv settings <v-btn size="small" variant="plain" icon="mdi-cog" @click="openSettings" class="mb-1"></v-btn> if needed:</p>     
            </v-col>
            <v-col cols="2" class="mt-2">
                <v-btn color="accent" @click="uploadData" prependIcon="mdi-upload">Confirm</v-btn>
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

                <template v-slot:item.amount="{ item }">
                    <v-row class="justify-end mr-12">
                    {{ parseFloat(item.amount).toFixed(rounding) }} {{ currency }}
                    </v-row>
                </template>

                <template v-slot:item.action="{ item }">
                    <v-btn density="compact" icon="mdi-delete" color="" @click="deleteItem(item)">
                    </v-btn>
                </template>
            </v-data-table>
        </v-row>
    </div>

<DialogDeleteConfirmation :item="itemDelete" :itemName="itemDeleteName" :resource="'files'"></DialogDeleteConfirmation>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import moment from 'moment'
import { API } from '../composables/API.js'
import { watch } from 'vue'
import { useDialogStore } from '../stores/DialogStore.js'
import { useUpdateStore } from '@/stores/UpdateStore.js'
import { useAlertStore } from '../stores/AlertStore.js'
import DialogDeleteConfirmation from '@/components/DialogDeleteConfirmation.vue'

// Data
const rawData = ref([])
const previewData = ref([])
const dataUploads = ref([])

// Operational
const dialogStore = useDialogStore()
const updateAlert = useAlertStore()
const updateStore = useUpdateStore()
const fileLoaded = ref(false)
const inputFile = ref()
const itemDelete = ref()
const itemDeleteName = ref()
const currency = ref('€')
const rounding = ref(0)

// tables
const headersFiles = [
    { title: 'File Name', value: 'fileName' },
    { title: 'Upload Date', value: 'fileDate' },
    { title: 'Actions', value: 'action', align: 'center'}
]
const headers = [
    { title: 'Date', value: 'date' },
    { title: 'Recipient', value: 'recipient' },
    { title: 'Description', value: 'description' },
    { title: 'Amount', value: 'amount', align: 'center' }
]

// Methods
// Load the table
// Methods
const loadTable = async () => {
    const apiData = await API('files', 'GET')
    dataUploads.value = apiData.map(item => ({ ...item, action: null }))
}

const deleteItem = async (item) => {
    itemDelete.value = item
    itemDeleteName.value = item.fileName
    dialogStore.delete = !dialogStore.delete
}


// FILE UPLOAD
// load the file from input
const loadFile = async (e) => { 
    const file = e.target.files[0]
    const schema = await API('schema', 'GET')
    const reader = new FileReader()
    reader.onload = (e) => { 
        const content = e.target.result.replace(/"/g, '')
        const lines = content.split('\n')
        lines.forEach(line => { 
            const values = line.split(schema.delimiter)
            rawData.value.push(values)
        })
    }
    reader.readAsText(file, 'ISO-8859-1')
    convertData(rawData.value)
}

// converting data based on import scheme
const convertData = async (data) => {
    // get the import scheme
    const schema = await API('schema', 'GET')
    const maxRows = data.length
    const fileName = inputFile.value[0].name
    const fileDate = new Date().toISOString()

    const settings = await API('settings', 'GET')
    currency.value = settings.currency
    rounding.value = settings.rounding

    try { 
        data.forEach((entry, index) => {
            if (index >= schema.rowFirst && index < maxRows - schema.rowLast) {
                const rawDate = entry[schema.colDate - 1]
                const parsedDate = moment(rawDate, schema.dateFormat)
                const date = parsedDate.format('YYYY-MM-DD')
                const recipient = entry[schema.colRecipient - 1]
                const description = entry[schema.colDescription - 1]
                const amount = entry[schema.colAmount - 1].replace(schema.thousandsSeparator, '').replace(schema.decimalSeparator, '.')
                previewData.value.push({ date, recipient, description, amount, fileName, fileDate })
            }
        })
       fileLoaded.value = true 
    } catch (error) {
        console.log("Error converting data: ", error)
        updateAlert.showAlert('Error', `The import scheme is not valid. Please check the import scheme in the settings.`, 'error', 5000)
    }
}

// uploading data
const uploadData = async () => {
    try {
        await API('transactions', 'POST', previewData.value)
        loadTable()
        inputFile.value = null
        fileLoaded.value = false
    }
    catch (error) {
        console.log(error)
    }
}

const openSettings = () => {
    dialogStore.settings = !dialogStore.settings
}

// Lifecycle
onMounted(async () => {
    loadTable()
})

watch(() => updateStore.refresh, () => {
    if(fileLoaded.value) {
        previewData.value = []
        convertData(rawData.value)
    }
    else {
        loadTable()
    }
})

</script>