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
                <v-select label="Category" v-model="category" :items="categoryItems"></v-select>
                <v-tooltip :text="infoCategory">
                    <template v-slot:activator="{ props }">
                        <v-icon color="info" v-bind="props" density="compact" class="mt-5 ml-2">mdi-information</v-icon>
                    </template>
                </v-tooltip>
            </v-col>

            <!--Category Button-->
            <v-col cols="2" class="mt-2 text-start">
                <v-btn v-if="display.mdAndDown.value" color="info" @click="openCategoryDialog" icon="mdi-bookshelf"></v-btn>
                <v-btn v-else class="" color="info" @click="openCategoryDialog">Edit Categories</v-btn>
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
            <v-data-table :items="data" :headers="headers">

                <!--Keyword-->
                <template v-slot:item.keyword="{ item }">
                    <v-row class="align-center">
                        <div class="ml-4 mr-1 " v-if="conflicts.includes(item.id)">
                            <v-tooltip text="Conflict with another assignment">
                                <template v-slot:activator="{ props }">
                                    <v-btn color="red" v-bind="props" density="compact" icon="mdi-alert-circle"></v-btn>
                                </template>
                            </v-tooltip>
                        </div> 
                        <div class="ml-4">
                            {{ item.keyword }} 
                        </div>
                    </v-row>
                </template>

                <!--Category-->
                <template v-slot:item.category="{ item }">
                    <v-chip :color="item.color" link @click="openCategoryEdit(item)">{{ item.categoryName }}</v-chip>
                </template>

                <!--Recipient-->
                <template v-slot:item.checkRecipient="{ item }">
                    <v-row class="justify-center">
                        <v-icon v-if="item.checkRecipient">mdi-check</v-icon>
                        <v-icon v-else>mdi-close</v-icon>  
                    </v-row>
               </template>

                <!--Description-->
                <template v-slot:item.checkDescription="{ item }">
                   <v-row class="justify-center">
                        <v-icon v-if="item.checkDescription">mdi-check</v-icon>
                        <v-icon v-else>mdi-close</v-icon>  
                    </v-row>
               </template>

                <!--Action-->
                <template v-slot:item.action="{ item }">
                    <v-row class="justify-center">
                        <EditAssignment :keyword="item.keyword" :category="item.categoryName" :id="item.id" :recipient="item.checkRecipient" :description="item.checkDescription"/>
                        <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="deleteItem(item)">
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
                <h2 class="mt-8">Transactions without a category</h2>
            </v-col>
        </v-row>
        <v-row>
            <v-data-table :items="dataUnmatched" :headers="headersUnmatched">
                <!--Date-->
                <template v-slot:item.date="{ item }">
                    {{ new Date(item.date).toLocaleDateString() }}
                </template>

                <!--Amount-->
                <template v-slot:item.amount="{ item }">
                    <v-row class="justify-end mr-12">
                        {{ item.amount.toFixed(2) }}
                    </v-row>
                </template>
            </v-data-table>
        </v-row>
    </div>
    <v-divider class="mt-8"></v-divider>    
    <DialogCategoryManagement/>
    <EditCategory></EditCategory>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useDisplay } from 'vuetify'
import { API } from '../composables/API.js'
import { useAlertStore } from '../stores/AlertStore'
import { useUpdateStore } from '../stores/UpdateStore'
import { useDialogStore } from '../stores/DialogStore'
import DialogCategoryManagement from '../components/DialogCategoryManagement.vue'
import EditAssignment from '../components/EditAssignment.vue'
import EditCategory from '@/components/EditCategory.vue'
import { watch } from 'vue'

// Operational
const keyword = ref('')
const checkMode = ref('recipient_or_description')
const category = ref('')
const categoryItems = ref([])
const display = useDisplay()


// Data
const data = ref([])
const dataUnmatched = ref([])
const alertStore = useAlertStore()
const updateStore = useUpdateStore()
const dialogStore = useDialogStore()
var conflicts = []
const checkItems = [{ 'value': 'recipient_or_description', 'title': 'Keyword must be in recipient or description' },
                    { 'value': 'recipient_only', 'title': 'Keyword must be in recipient only' },
                    { 'value': 'description_only', 'title': 'Keyword must be in description only' },
                    { 'value': 'recipient_and_description', 'title': 'Keyword must be in recipient and description' }]

// Table Variables
const headers = [
    { title: 'Keyword', value: 'keyword', sortable: true},
    { title: 'Category', value: 'category', sortable: true},
    { title: 'Check-Mode', value: 'checkMode', sortable: true, align: 'center' },
    { title: 'Action', value: 'action', sortable: false, align: 'center'},
]

const headersUnmatched = [
    { title: 'Date', value: 'date', sortable: true },
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true, align: 'center'},

]

// Tooltips
const infoKeyword = 'These characters will be search for in the transactions. The keyword is case-insensitive.'
const infoCheckMode = 'The check mode determines where the keyword will be searched for in the transaction.'
const infoCategory = 'The category that will be assigned to the transaction if the keyword is found.'

// Methods
const loadTable = async () => {
    const rawData = await API('assignments', 'GET')
    data.value = rawData.map(item => ({ ...item, action: null }))
}

const loadCategoryItems = async () => {
    const rawData = await API('categories', 'GET')
    categoryItems.value = rawData.map(item => item.name)
}

const loadDataUnmatched = async () => {
    const rawData = await API('transactions_without_category', 'GET')
    dataUnmatched.value = rawData.map(item => ({ ...item, action: null }))
}

const loadConflicts = async () => {
    conflicts = await API('assignments_conflicts', 'GET')
}

const createAssignment = async () => {
    if (keyword.value === '' || category.value === '' || checkMode.value === '') {
        alertStore.showAlert('Input Failure', 'Please check your input fields', 'error', 4000)
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
        loadConflicts()
        loadTable()
        loadDataUnmatched()
    }
}

const deleteItem = async (item) => {
    await API('assignments', 'DELETE', item)
    loadConflicts()
    loadTable()
}

const openCategoryEdit = (item) => {
    dialogStore.categoryEditId = item.category
    dialogStore.categoryEdit = !dialogStore.categoryEdit
}

const openCategoryDialog = () => {
    dialogStore.category = !dialogStore.category
}


// Lifecycle
const load = () => {
    loadTable()
    loadDataUnmatched()
    loadCategoryItems()
    loadConflicts()
}

onMounted(async () => {
    load()
})

watch(() => updateStore.dialogTrigger, () => {
    load()
})

watch(() => updateStore.refresh, () => {
    load()
})
</script>