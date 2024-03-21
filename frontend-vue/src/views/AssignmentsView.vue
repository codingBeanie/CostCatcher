<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Categorization</h1>
        <p class="mb-4 text-h7">You can create custom categories that are assigned automatically based on a ruleset to your transactions.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Create Form-->
    <div>
        <v-row>
            <!--Keyword-->
            <v-col cols="3">
                <v-text-field v-model="keyword" label="Keyword"></v-text-field>
            </v-col>

            <!--Category-->
            <v-col cols="3">
                <v-select label="Category" v-model="category" :items="categoryItems"></v-select>
            </v-col>

            <!--CheckMode-->
            <v-col cols="4">
                <v-select v-model="checkMode" label="Check-Mode" :items="checkItems" item-title="title" item-value="value"/>
            </v-col>
            
            <!--Button-->
            <v-col cols="2" class="mt-2 text-center">
                <v-btn class="" color="accent" @click="createAssignment" prependIcon="mdi-plus">Create</v-btn>
            </v-col>
        </v-row>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Assignment-Table-->
    <div>
        <v-row>
            <v-col>
                <h2 class="">Assignments</h2>
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
                    <v-chip>{{ item.category }}</v-chip>
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
                        <EditAssignment :keyword="item.keyword" :category="item.category" :id="item.id" :recipient="item.checkRecipient" :description="item.checkDescription"/>
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
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { API } from '../composables/API.js'
import { useAlertStore } from '../stores/AlertStore'
import { useUpdateStore } from '../stores/UpdateStore'
import EditAssignment from '../components/EditAssignment.vue'
import { watch } from 'vue'

// Operational
const keyword = ref('')
const checkMode = ref('')
const category = ref('')
const categoryItems = ref([])

// Data
const data = ref([])
const dataUnmatched = ref([])
const alertStore = useAlertStore()
const updateStore = useUpdateStore()
var conflicts = []
const checkItems = [{ 'value': 'recipient_or_description', 'title': 'Keyword must be in recipient or description' },
                    { 'value': 'recipient_only', 'title': 'Keyword must be in recipient only' },
                    { 'value': 'description_only', 'title': 'Keyword must be in description only' },
                    { 'value': 'recipient_and_description', 'title': 'Keyword must be in recipient and description' }]

// Table Variables
const headers = [
    { title: 'Keyword', value: 'keyword', sortable: true},
    { title: 'Category', value: 'category', sortable: true},
    { title: 'Recipient', value: 'checkRecipient', sortable: true, align: 'center'},
    { title: 'Description', value: 'checkDescription', sortable: true, align: 'center'},
    { title: 'Action', value: 'action', sortable: false, align: 'center'},
]

const headersUnmatched = [
    { title: 'Date', value: 'date', sortable: true },
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true, align: 'center'},

]


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


// Lifecycle
onMounted(async () => {
    loadConflicts()
    loadTable()
    loadDataUnmatched()
    loadCategoryItems()
})

watch(() => updateStore.dialogTrigger, () => {
    loadConflicts()    
    loadTable()
    loadDataUnmatched()
})
</script>