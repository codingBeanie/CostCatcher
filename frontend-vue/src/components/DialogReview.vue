<template>
    <v-row justify="center">
        <v-dialog v-model="active" transition="dialog-bottom-transition" fullscreen>

            <v-card color="primary">
                <v-toolbar color="secondary">
                    <v-btn icon @click="close">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>Review Transactions</v-toolbar-title>
                </v-toolbar>

                <v-card-text>
                    <v-container>
                        <v-row class="mb-4">
                            <h2 class="mr-4 font-weight-thin">Review Transactions</h2>
                            <v-btn class="text-h5 font-weight-bold" variant="text" :color="selectCategory.color">{{ selectCategory.name }}</v-btn>
                            <h2>({{ period }})</h2>
                        </v-row>
                        <v-row>
                            <v-data-table
                                :items="data"
                                :headers="headers"
                            >
                                <!--Date-->
                                <template v-slot:item.date="{ item }">
                                    {{ new Date(item.date).toLocaleDateString(locale) }}
                                </template>

                                <!--Amount-->
                                <template v-slot:item.amount="{ item }">
                                    <v-row class="justify-end mr-12">
                                        <div v-if="item.amount < 0" class="text-error">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2}) }} {{ currency }}</div>
                                        <div v-if="item.amount >= 0" class="text-success">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2}) }} {{ currency }}</div>
                                    </v-row>
                                </template>

                                <!--Action-->
                                <template v-slot:item.action="{ item }">
                                    <v-row class="justify-center">
                                        <v-tooltip v-if="item.overruled" text="Category is locked. Click to unlock.">
                                            <template v-slot:activator="{ props }">
                                                <v-btn v-bind="props" density="compact" icon="mdi-lock" @click="unlock(item)" ></v-btn>
                                            </template>
                                        </v-tooltip>
                                        <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="componentStore.openTransactionEdit(item.id)"></v-btn>  
                                        <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="componentStore.openDelete('transactions', item.id, `${item.recipient} | ${item.description}`)">
                                        </v-btn>                   
                                    </v-row>
                                </template>
                            </v-data-table>
                        </v-row>
                    </v-container>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text="Close" color="sucess" @click="close"></v-btn>
                </v-card-actions>

            </v-card>
        </v-dialog>
    </v-row>

</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { API } from '../composables/API.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const active = ref(false)

// Settings
const currency = ref('€')
const locale = ref('de-DE')

// Query Parameters
const period = ref('')
const category = ref(0)

// Data
const data = ref([])

// Input
const selectCategory = ref("")

// Table Headers
const headers = [
    { title: 'Date', value: 'date', sortable: true },
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true },
    { title: 'Amount', value: 'amount', sortable: true, align: 'center' },
    { title: 'Action', value: 'action', sortable: false, align: 'center'}

]
////////////////////////////////////////////////////////////////
// Load Data
////////////////////////////////////////////////////////////////
const loadSettings = async () => {
    const settingsData = await API('settings', 'GET')
    currency.value = settingsData.currency
    locale.value = settingsData.locale
}

const loadTable = async () => {
    const originalData = await API(`transactions/?category=${category.value}&period=${period.value}`, 'GET')
    data.value = originalData.map(item => ({ ...item, action: null }))
}

const loadCategory = async () => {
    // Undefined
    if(category.value === 0) {
        selectCategory.value = { name: 'Undefined', color: 'info' }
        return
    }
    // Income
    if(category.value === -1) {
        selectCategory.value = { name: 'Income', color: 'success' }
        return
    }
    // Expense
    if(category.value === -2) {
        selectCategory.value = { name: 'Expense', color: 'error' }
        return
    }
    // Net / All
    if(category.value === -3) {
        selectCategory.value = { name: 'All', color: 'info' }
        return
    }
    // Valid Category
    selectCategory.value = await API(`categories/?id=${category.value}`, 'GET')
}

////////////////////////////////////////////////////////////////
// CRUD Operations
////////////////////////////////////////////////////////////////
const unlock = async (item) => {
    item.overruled = false
    item.amount = item.amount / 100
    await API('transactions', 'PUT', item)
    loadTable()
}

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    componentStore.refreshApp()
    active.value = false
}
////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = () => {
    period.value = componentStore.review.period
    category.value = componentStore.review.category
    loadSettings()
    loadCategory()
    loadTable()
}

watch(() => componentStore.review.trigger, () => {
    load()
    active.value = true
})

watch(() => componentStore.app.refresh, () => {
    load()
})

watch(() => userStore.username, () => {
    load()
})
</script>