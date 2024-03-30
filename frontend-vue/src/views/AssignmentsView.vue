<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Categorization</h1>
        <p class="mb-4 text-h7">You can create custom categories that are assigned automatically based on a ruleset to your transactions.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Create Form-->
    <div>
        <v-row class="">
            <!--Keyword-->
            <v-col class="d-flex" cols="3">
                <v-text-field v-model="keyword" label="Keyword"></v-text-field>
                <v-tooltip :text="infoKeyword">
                    <template v-slot:activator="{ props }">
                        <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-information</v-icon>
                    </template>
                </v-tooltip>
            </v-col>
            
            <!--CheckMode-->
            <v-col cols="2" class="d-flex">
                <v-select v-model="checkMode" label="Check-Mode" :items="checkItems" item-title="title" item-value="value"/>
                    <v-tooltip :text="infoCheckMode">
                        <template v-slot:activator="{ props }">
                            <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-information</v-icon>
                        </template>
                </v-tooltip>
            </v-col>

            <!--Category-->
            <v-col cols="3" class="d-flex">
                <v-select label="Category" v-model="category" :items="categories" item-title="name" item-value="id"></v-select>
                <v-tooltip :text="infoCategory">
                    <template v-slot:activator="{ props }">
                        <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-information</v-icon>
                    </template>
                </v-tooltip>
            </v-col>

            <!--Category Button-->
            <v-col cols="2" class="mt-2 text-start">
                <v-btn v-if="display.mdAndDown.value" color="info" @click="mainStore.openCategories()" icon="mdi-bookshelf"></v-btn>
                <v-btn v-else class="" color="info" @click="mainStore.openCategories()">Edit Categories</v-btn>
            </v-col>
            
            <!--Button-->
            <v-col cols="2" class="mt-2 text-center">
                <v-btn v-if="display.mdAndDown.value" class="" color="accent" @click="createAssignment" icon="mdi-plus"></v-btn>
                <v-btn v-else class="" color="accent" @click="createAssignment">Create</v-btn>
            </v-col>
        </v-row>

    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Assignment-Table-->
    <div>
        <v-row>
            <v-col>
                <h2 class="">Created Categorizations</h2>
            </v-col>
        </v-row>
        <v-row>
            <v-data-table :items="data" :headers="headersAssignments">

                <!--Keyword-->
                <template v-slot:item.keyword="{ item }">
                    <v-row class="align-center">
                        <div class="ml-4 mr-1 " v-if="item.conflict">
                            <v-tooltip text="Conflict with another assignment">
                                <template v-slot:activator="{ props }">
                                    <v-btn color="error" v-bind="props" density="compact" icon="mdi-alert-circle" variant="tonal"></v-btn>
                                </template>
                            </v-tooltip>
                        </div> 
                        <div class="ml-4">
                            <v-btn variant="text" @click="mainStore.openAssignmentEdit(item.id)">{{ item.keyword }}</v-btn>
                        </div>
                    </v-row>
                </template>

                <!--Category-->
                <template v-slot:item.category="{ item }">
                    <v-chip :color="item.color" link @click="mainStore.openCategoryEdit(item.category)">{{ item.categoryName }}</v-chip>
                </template>

                <!--Recipient-->
                <template v-slot:item.checkMode="{ item }">
                    <v-row class="justify-start">
                        <v-btn v-if="item.checkMode==='recipient_or_description'" variant="plain" @click="mainStore.openAssignmentEdit(item.id)">Recipient OR Description</v-btn>
                        <v-btn v-if="item.checkMode==='recipient_only'" variant="plain" @click="mainStore.openAssignmentEdit(item.id)">Recipient</v-btn>
                        <v-btn v-if="item.checkMode==='description_only'" variant="plain" @click="mainStore.openAssignmentEdit(item.id)">Description</v-btn>
                        <v-btn v-if="item.checkMode==='recipient_and_description'" variant="plain" @click="mainStore.openAssignmentEdit(item.id)">Recipient AND Description</v-btn>
                    </v-row>
               </template>

                <!--Action-->
                <template v-slot:item.action="{ item }">
                    <v-row class="justify-center">
                        <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="mainStore.openAssignmentEdit(item.id)"></v-btn>  
                        <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="mainStore.openDelete('assignments', item.id, item.keyword)">
                        </v-btn>                   
                    </v-row>

                </template>
            </v-data-table>
        </v-row>
    </div>
    <v-divider class="mt-8"></v-divider>
    
    <!--Not assigned-Table-->
    <div>
        <v-row>
            <v-col>
                <h2 class="mt-4">Transactions without a category</h2>
                <p class=" text-h7">See which transactions do not have a category, so you can create a categorization accordingly.</p>
            </v-col>
        </v-row>
        <v-row>
            <v-data-table :items="dataNoCategory" :headers="headersNoCategory">
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

                <template v-slot:item.action="{ item }">
                    <v-row class="justify-center">
                        <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="mainStore.openTransactionEdit(item.id)"></v-btn>  
                        <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="mainStore.openDelete('transactions', item.id, `${item.recipient} | ${item.description}`)">
                        </v-btn>                   
                    </v-row>

                </template>
                
            </v-data-table>
        </v-row>
    </div>
    <v-divider class="mt-8"></v-divider>    

</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useDisplay } from 'vuetify'
import { API } from '../composables/API.js'
import { useMainStore } from '../stores/MainStore'
import { watch } from 'vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const mainStore = useMainStore()

// Settings
const currency = ref('€')
const rounding = ref(0)

// Input
const keyword = ref('')
const checkMode = ref('recipient_or_description')
const category = ref('')
const categories = ref([])
const checkItems = [{ 'value': 'recipient_or_description', 'title': 'Keyword must be in recipient or description' },
                    { 'value': 'recipient_only', 'title': 'Keyword must be in recipient only' },
                    { 'value': 'description_only', 'title': 'Keyword must be in description only' },
                    { 'value': 'recipient_and_description', 'title': 'Keyword must be in recipient and description' }]

// Tooltips
const infoKeyword = 'These characters will be search for in the transactions. The keyword is case-insensitive.'
const infoCheckMode = 'The check mode determines where the keyword will be searched for in the transaction.'
const infoCategory = 'The category that will be assigned to the transaction if the keyword is found.'

// Data
const data = ref([])
const dataNoCategory = ref([])
var conflicts = []

// Table Variables
const headersAssignments = [
    { title: 'Keyword', value: 'keyword', sortable: true},
    { title: 'Category', value: 'category', sortable: true},
    { title: 'Check-Mode', value: 'checkMode', sortable: true, align: 'start' },
    { title: 'Action', value: 'action', sortable: false, align: 'center'},
]

const headersNoCategory = [
    { title: 'Date', value: 'date', sortable: true },
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true, align: 'center' },
    { title: 'Action', value: 'action', sortable: false, align: 'center'}

]

// Utilities
const display = useDisplay()

////////////////////////////////////////////////////////////////
// Loading Methods
////////////////////////////////////////////////////////////////
const loadSettings = async () => {
    const settingsData = await API('settings', 'GET')
    currency.value = settingsData.currency
    rounding.value = settingsData.rounding
}

const loadCategories = async () => {
    categories.value = await API('categories', 'GET') 
}

const loadAssignments = async () => {
    data.value = await API('assignments', 'GET')
}

const loadNoCategory = async () => {
    dataNoCategory.value = await API("transactions/?categories=[0]", 'GET')
}

////////////////////////////////////////////////////////////////
// CRUD Methods
////////////////////////////////////////////////////////////////
const createAssignment = async () => {
    if (keyword.value === '' || category.value === '' || checkMode.value === '') {
        mainStore.showAlert('Input Failure', 'Please check your input fields', 'error', 4000)
        return
    } else {
        const assignment = {
            keyword: keyword.value,
            checkMode: checkMode.value,
            category: category.value
        }
        await API('assignments', 'POST', assignment)
        keyword.value = ''
        category.value = ''
        mainStore.refreshApp()
    }
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = () => {
    loadSettings()
    loadCategories()
    loadAssignments()
    loadNoCategory()
}

onMounted(async () => {
    load()
})

watch([() => mainStore.app.refresh, () => mainStore.categories.trigger], () => {
    load()
})
</script>