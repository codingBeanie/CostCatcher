<template>
    <!--Titles-->
    <Title title="Import Data" subtitle="Upload your csv-files here."></Title>
    <Divider title="Upload File"></Divider>
    <!--File-Input-->
    <v-row>
        <v-col>
            <p v-if="importError==true" class="text-h6 text-error">The import scheme is not valid. Please check the import scheme in the settings <v-btn size="small" variant="plain" icon="mdi-cog" @click="componentStore.openSettings('CSV')" class="mb-1"></v-btn>.</p>
        </v-col>
    </v-row>
    <v-row class="">
        <v-col><v-file-input label="Upload a new csv-file" accept=".csv" @change="readFile" v-model="inputFile"></v-file-input></v-col>
    </v-row>

    <!--Preview-Table-->
    <div v-if="fileLoaded && !importError"> 
        <Divider title="PREVIEW" spacing="16"></Divider> 
        <v-row class="mt-4">
            <v-data-table :items="dataPreview" :headers="headersPreview" density="compact">
                <!--Date-->
                <template v-slot:item.date="{ item }">
                    {{ new Date(item.date).toLocaleDateString(locale) }}
                </template>

                <!--Amount-->
                <template v-slot:item.amount="{ item }">
                    <v-row class="justify-end mr-12">
                        <div v-if="item.amount < 0" class="text-error">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2}) }} {{ currency }}</div>
                        <div v-if="item.amount >= 0" class="text-success">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2}) }}{{ currency }}</div>
                    </v-row>
                </template>
            </v-data-table>
        </v-row>

        <v-row class="">
            <v-col cols="10" class="mt-2 text-end">
                <p>Check if your data is recognised correctly. Adjust the csv settings <v-btn size="small" variant="plain" icon="mdi-cog" @click="componentStore.openSettings('CSV')" class="mb-1"></v-btn> if needed.</p>     
            </v-col>
            <v-col cols="2" class="mt-2 text-end">
                <v-btn color="accent" @click="uploadData()" prependIcon="mdi-upload">
                
                    Confirm
                    <v-progress-circular
                    v-if="waitingUpload"
                    class="ml-2"
                    color="primary"
                    indeterminate
                    ></v-progress-circular>    
                </v-btn>

            </v-col> 
        </v-row>
    </div>

    <!--Uploaded Files Table-->       
    <div v-else>
        <Divider title="uploaded Files" spacing="16"></Divider> 
        <v-row class="mt-4">
            <v-data-table :items="dataUploads" :headers="headersFiles">
                <!--Date-->
                <template v-slot:item.fileDate="{ item }">
                    {{ new Date(item.fileDate).toLocaleString() }}
                </template>

                <template v-slot:item.action="{ item }">
                    <v-btn density="compact" icon="mdi-delete" color="" @click="componentStore.openDelete('files', item.uploadID, `${item.fileName}`)">
                    </v-btn>
                </template>
            </v-data-table>
        </v-row>
        <v-row v-if="waitingFileTable">
            <v-progress-linear
                color="accent"
                indeterminate
            ></v-progress-linear>
        </v-row>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import moment from 'moment'
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
const fileLoaded = ref(false)
const importError = ref(false)
const waitingUpload = ref(false)  
const waitingFileTable = ref(false)

// Data Objects
const dataPreview = ref([])
const dataUploads = ref([])
const settings = ref([])

// Input Objects
const inputFile = ref()

// Display Objects
const currency = ref('€')
const locale = ref('de-DE')

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
    waitingFileTable.value = true
    const data = await API('files', 'GET')
    waitingFileTable.value = false
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
            const values = line.split(settings.value.delimiter)
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
    dataPreview.value = []

    try { 
        data.forEach((entry, index) => {
            if (index >= settings.value.rowFirst && index < data.length - settings.value.rowLast) {
                const originalDate = entry[settings.value.colDate - 1]
                const parsedDate = moment(originalDate, settings.value.dateFormat)
                const date = parsedDate.format('YYYY-MM-DD')
                const recipient = entry[settings.value.colRecipient - 1]
                const description = entry[settings.value.colDescription - 1]
                const amount = Math.floor(entry[settings.value.colAmount - 1].replace(settings.value.thousandsSeparator, '').replace(settings.value.decimalSeparator, '.') * 100)
                dataPreview.value.push({ date, recipient, description, amount, fileName, fileDate })
            }
        })
        importError.value = false

    } catch (error) {
        console.log("Error converting data: ", error)
        importError.value = true
        alertStore.showAlert('Error', `The import scheme is not valid. Please check the import scheme in the settings.`, 'error', 5000)
    }
}

const uploadData = async () => {
    waitingUpload.value = true
    await API('transactions', 'POST', dataPreview.value)
    waitingUpload.value = false
    inputFile.value = null
    fileLoaded.value = false
    importError.value = false
    load()
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = async () => {
    settings.value = await API('settings', 'GET')
    locale.value = settings.value.locale
    currency.value = settings.value.currency
    loadTableUploads()

    if(fileLoaded.value) {
        readFile()
    }
}

onMounted(() => {
    load()
})

watch(() => userStore.username, () => {
    fileLoaded.value = false
    inputFile.value = null
    importError.value = false
    load()
})

watch(() => componentStore.app.refresh, () => {
    load()
})


</script>