<template>
    <v-row justify="center">
        <v-dialog v-model="active" max-width="600px">
            <!--Dialog Content-->
            <template v-slot:default="{ active }">
                <v-card>
                    <v-tabs
                    v-model="tab"
                    bg-color="primary"
                    >
                        <v-tab value="general">General</v-tab>
                        <v-tab value="CSV">CSV Settings</v-tab>
                        
                    </v-tabs>

                    <v-card-text>
                        <v-window v-model="tab">

                            <!--CSV Settings-->
                            <v-window-item value="CSV">
                                <v-container>
                                    <v-row>
                                        <h4>Row settings</h4>
                                    </v-row>
                                    <v-row>

                                        <!--First Row-->
                                        <v-col class="d-flex">
                                            <v-text-field label="Ignore # first rows" v-model="rowFirst" type="number" :rules="[value => (value >= 0 && value <= 1000) || 'Please enter a number']"></v-text-field>
                                            <v-tooltip :text="infoRowFirst">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>

                                        <!--Last Row-->
                                        <v-col class="d-flex">
                                            <v-text-field label="Ignore # last rows" v-model="rowLast" type="number" :rules="[value => (value >= 0 && value <= 1000) || 'Please enter a number']"></v-text-field>
                                            <v-tooltip :text="infoRowLast">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                    </v-row>

                                    <v-row>
                                        <h4>Column settings</h4>
                                    </v-row>
                        
                                    <v-row>
                                        <!--Date-->
                                         <v-col class="d-flex">
                                            <v-text-field label="Column # Date" v-model="colDate" type="number" :rules="[value => (value >= 1 && value <= 1000) || 'Please enter a number']"></v-text-field>
                                            <v-tooltip :text="infoColDate">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>

                                        <!--Recipient-->
                                         <v-col class="d-flex">
                                            <v-text-field label="Column # Recipient" v-model="colRecipient" type="number" :rules="[value => (value >= 1 && value <= 1000) || 'Please enter a number']"></v-text-field>
                                            <v-tooltip :text="infoColRecipient">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                    </v-row>

                                    <v-row>
                                        <!--Description-->
                                         <v-col class="d-flex">
                                            <v-text-field label="Column # Description" v-model="colDescription" type="number" :rules="[value => (value >= 1 && value <= 1000) || 'Please enter a number']"></v-text-field>
                                            <v-tooltip :text="infoColDescription">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>

                                        <!--Amount-->
                                         <v-col class="d-flex">
                                            <v-text-field label="Column # Amount" v-model="colAmount" type="number" :rules="[value => (value >= 1 && value <= 1000) || 'Please enter a number']"></v-text-field>
                                            <v-tooltip :text="infoColAmount">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                    </v-row>

                                    <v-row>
                                        <h4>Data settings</h4>
                                    </v-row>

                                    <v-row>
                                        <!--Delimiter-->
                                         <v-col class="d-flex">
                                            <v-text-field label="CSV delimeter" v-model="delimiter" :rules="[value => (value === ';' || value === ',') || 'Please enter a valid character']"></v-text-field>
                                            <v-tooltip :text="infoDelimiter">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>

                                        <!--Thousands Separator-->
                                         <v-col class="d-flex">
                                            <v-text-field label="Thousands seperator" v-model="thousandsSeparator" :rules="[value => (value === '.' || value === ',') || 'Please enter a valid character']"></v-text-field>
                                            <v-tooltip :text="infoThousandsSeparator">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                    </v-row>    

                                    <v-row>
                                        <!--Decimal Separator-->
                                         <v-col class="d-flex">
                                            <v-text-field label="Decimal seperator" v-model="decimalSeparator" :rules="[value => (value === '.' || value === ',') || 'Please enter a valid character']"></v-text-field>
                                            <v-tooltip :text="infoDecimalSeparator">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                        
                                        <!--Date Format-->
                                         <v-col class="d-flex">
                                            <v-text-field label="Date format" v-model="dateFormat"></v-text-field>
                                            <v-tooltip :text="infoDateFormat">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                    </v-row>

                                </v-container>
                            </v-window-item>
                            
                            <!--General Settings-->
                            <v-window-item value="general">
                                <v-container>
                                    <v-row>
                                        <h4>General settings</h4>
                                    </v-row>
                                    <v-row>
                                        <v-col class="d-flex">
                                            <v-text-field label="Currency" v-model="currency"></v-text-field>
                                            <v-tooltip :text="infoCurrency">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                        <v-col class="d-flex">
                                            <v-text-field label="Rounding" v-model="rounding" type="number"></v-text-field>
                                            <v-tooltip :text="infoRounding">
                                                <template v-slot:activator="{ props }">
                                                    <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-help-circle</v-icon>
                                                </template>
                                            </v-tooltip>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-window-item>

                        </v-window>
                    </v-card-text>

                    <!--Dialog Actions-->
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text="Cancel" color="sucess" @click="close"></v-btn>
                        <v-btn text="Save" color="sucess" @click="save"></v-btn>
                    </v-card-actions>
                </v-card>
            </template>

        </v-dialog>
    </v-row>

</template>

<script setup>
import { onMounted, defineProps, watch } from 'vue';
import { ref } from 'vue'
import { API } from '../composables/API.js'
import { useDialogStore } from '../stores/DialogStore.js'
import { useUpdateStore } from '../stores/UpdateStore.js'

// Operator variables
const active = ref(false)
const tab = ref('CSV')
const dialogStore = useDialogStore()
const updateStore = useUpdateStore()
const props = defineProps({
    buttonSize: String
})

// Info Texts
const infoRowFirst = 'The number of rows to ignore at the beginning of the file. This is useful if the file contains a header or other information that should be ignored.'
const infoRowLast = 'The number of rows to ignore at the end of the file. This is useful if the file contains a footer or other information that should be ignored.'
const infoColDate = 'The column number of the date in the CSV file.'
const infoColRecipient = 'The column number of the recipient in the CSV file.'
const infoColDescription = 'The column number of the description in the CSV file.'
const infoColAmount = 'The column number of the amount in the CSV file.'
const infoDelimiter = 'The character that separates the columns in the CSV file. Typically this is a comma (US) or a semicolon.'
const infoThousandsSeparator = 'The character that separates the thousands in the amount. Typically this is a dot (US) or a comma.'
const infoDecimalSeparator = 'The character that separates the decimal in the amount. Typically this is a comma (US) or a dot.'
const infoDateFormat = 'The format of the date in the CSV file. This is used to parse the date correctly.'
const infoCurrency = 'The currency you want to use for the amounts. (Just for display)'
const infoRounding = 'The number of decimal places to round the amounts to. (Just for display)'

// Default values
const rowFirst = ref(1)
const rowLast = ref(0)

const colDate = ref(1)
const colRecipient = ref(2)
const colDescription = ref(3)
const colAmount = ref(4)

const delimiter = ref(';')
const thousandsSeparator = ref('.')
const decimalSeparator = ref(',')
const dateFormat = ref('DD.MM.YYYY')

const currency = ref()
const rounding = ref()

// Methods
const close = () => {
    active.value = false
}
const save = (async() => {
    const data = {
        rowFirst: rowFirst.value,
        rowLast: rowLast.value,
        colDate: colDate.value,
        colRecipient: colRecipient.value,
        colDescription: colDescription.value,
        colAmount: colAmount.value,
        delimiter: delimiter.value,
        thousandsSeparator: thousandsSeparator.value,
        decimalSeparator: decimalSeparator.value,
        dateFormat: dateFormat.value,
    }
    const update = await API('schema', 'PUT', data)

    const settings = {
        currency: currency.value,
        rounding: rounding.value
    }
    const updateSettings = await API('settings', 'PUT', settings)
    updateStore.refresh = !updateStore.refresh
    active.value = false
})

// Lifecycle
onMounted(async () => {
    try {
        const schema = await API('schema', 'GET')
        rowFirst.value = schema.rowFirst
        rowLast.value = schema.rowLast
        colDate.value = schema.colDate
        colRecipient.value = schema.colRecipient
        colDescription.value = schema.colDescription
        colAmount.value = schema.colAmount
        delimiter.value = schema.delimiter
        thousandsSeparator.value = schema.thousandsSeparator
        decimalSeparator.value = schema.decimalSeparator
        dateFormat.value = schema.dateFormat

        const settings = await API('settings', 'GET')
        currency.value = settings.currency
        rounding.value = settings.rounding
        
    } catch (error) {
        console.log(error)
    }
     })

watch(() => dialogStore.settings, () => {
    active.value = true
})

</script>
