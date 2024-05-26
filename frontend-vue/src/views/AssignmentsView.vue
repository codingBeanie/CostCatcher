<template>
    <!--Titles-->
    <Title title="Categorization" tutorial="categorization"></Title>

    <!--Create Form-->
    <div>
        <Divider title="Create Ruleset" spacing=0></Divider>
        <v-row class="mt-2">
            <!--Keyword-->
            <v-col class="d-flex" cols="3">
                <v-text-field  density="comfortable" v-model="keyword" label="Keyword"></v-text-field>
                <v-tooltip :text="infoKeyword">
                    <template v-slot:activator="{ props }">
                        <v-icon color="info" v-bind="props" density="compact" class="mt-3 ml-2">mdi-information</v-icon>
                    </template>
                </v-tooltip>
            </v-col>
            
            <!--CheckMode-->
            <v-col cols="2" class="d-flex">
                <v-select density="comfortable" v-model="checkMode" label="Check-Mode" :items="checkItems" item-title="title" item-value="value"/>
                    <v-tooltip :text="infoCheckMode">
                        <template v-slot:activator="{ props }">
                            <v-icon color="info" v-bind="props" density="compact" class="mt-3 ml-2">mdi-information</v-icon>
                        </template>
                </v-tooltip>
            </v-col>

            <!--Category-->
            <v-col cols="3" class="d-flex">
                <v-select  density="comfortable" label="Category" v-model="category" :items="categories" item-title="name" item-value="id"></v-select>
                <v-tooltip :text="infoCategory">
                    <template v-slot:activator="{ props }">
                        <v-icon color="info" v-bind="props" density="compact" class="mt-3 ml-2">mdi-information</v-icon>
                    </template>
                </v-tooltip>
            </v-col>

            <!--Category Button-->
            <v-col cols="2" class="mt-2 text-start">
                <v-btn v-if="display.mdAndDown.value" color="info" @click="componentStore.openCategories()" icon="mdi-bookshelf"></v-btn>
                <v-btn v-else class="" color="info" @click="componentStore.openCategories()">Edit Categories</v-btn>
            </v-col>
            
            <!--Button-->
            <v-col cols="2" class="mt-2 text-center">
                <v-btn v-if="display.mdAndDown.value" class="" color="accent" @click="createAssignment" icon="mdi-plus"></v-btn>
                <v-btn v-else class="" color="accent" @click="createAssignment">Create</v-btn>
            </v-col>
        </v-row>

    </div>

    <!--Assignment-Table-->
    <div>
        <Divider title="Created rulesets" spacing=16 :showToggle=true :showState=showAssignments @toggle="(state) => showAssignments = state"></Divider>    
        <v-row class="mt-4" v-show="showAssignments">
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
                            <v-btn variant="text" @click="componentStore.openAssignmentEdit(item.id)">{{ item.keyword }}</v-btn>
                        </div>
                    </v-row>
                </template>

                <!--Category-->
                <template v-slot:item.category="{ item }">
                    <v-chip :color="item.color" link @click="componentStore.openCategoryEdit(item.category)">{{ item.categoryName }}</v-chip>
                </template>

                <!--Recipient-->
                <template v-slot:item.checkMode="{ item }">
                    <v-row class="justify-start">
                        <v-btn v-if="item.checkMode==='recipient_or_description'" variant="plain" @click="componentStore.openAssignmentEdit(item.id)">Recipient OR Description</v-btn>
                        <v-btn v-if="item.checkMode==='recipient_only'" variant="plain" @click="componentStore.openAssignmentEdit(item.id)">Recipient</v-btn>
                        <v-btn v-if="item.checkMode==='description_only'" variant="plain" @click="componentStore.openAssignmentEdit(item.id)">Description</v-btn>
                        <v-btn v-if="item.checkMode==='recipient_and_description'" variant="plain" @click="componentStore.openAssignmentEdit(item.id)">Recipient AND Description</v-btn>
                    </v-row>
               </template>

               <!--Number of Transactions-->
                <template v-slot:item.numberOfAssignments="{ item }">
                    <div v-if="item.numberOfAssignments === 0" class="text-error">
                        <v-tooltip text="No transaction is assigend due to this rule!">
                            <template v-slot:activator="{ props }">
                                <v-btn color="error" v-bind="props" density="compact" icon="mdi-alert-circle" variant="tonal"></v-btn>
                            </template>
                        </v-tooltip>
                        {{ item.numberOfAssignments }}
                    </div>
                    <div v-else>
                      {{ item.numberOfAssignments }}
                    </div>
                </template>

                <!--Action-->
                <template v-slot:item.action="{ item }">
                    <v-row class="justify-center">
                        <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="componentStore.openAssignmentEdit(item.id)"></v-btn>  
                        <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="componentStore.openDelete('assignments', item.id, item.keyword)">
                        </v-btn>                   
                    </v-row>

                </template>
            </v-data-table>
        </v-row>
        <v-row v-if="waitingAssignments">
            <v-progress-linear
                color="accent"
                indeterminate
            ></v-progress-linear>
        </v-row>
    </div>
    
    <!--Not assigned-Table-->
    <div>
        <Divider title="transactions without categorization" spacing=16></Divider>    
        <v-row class="mt-4">
            <v-data-table :items="dataNoCategory" :headers="headersNoCategory">
                <!--Date-->
                <template v-slot:item.date="{ item }">
                    {{ new Date(item.date).toLocaleDateString(locale) }}
                </template>

                <!--Amount-->
                <template v-slot:item.amount="{ item }">
                    <v-row class="justify-end mr-12">
                        <div v-if="item.amount < 0" class="text-error">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</div>
                        <div v-if="item.amount >= 0" class="text-success">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</div>
                    </v-row>
                </template>

                <template v-slot:item.action="{ item }">
                    <v-row class="justify-center">
                        <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="componentStore.openTransactionEdit(item.id)"></v-btn>  
                        <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="componentStore.openDelete('transactions', item.id, `${item.recipient} | ${item.description}`)">
                        </v-btn>                   
                    </v-row>
                </template>
                
            </v-data-table>
        </v-row>
        <v-row v-if="waitingNoCategories">
            <v-progress-linear
                color="accent"
                indeterminate
            ></v-progress-linear>
        </v-row>
    </div>

<Hint class="mt-10" v-if="!waitingNoCategories" text="You can collapse the upper table."></Hint>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useDisplay } from 'vuetify'
import { API } from '../composables/API.js'
import { useComponentStore } from '../stores/ComponentStore'
import { useUserStore } from '../stores/UserStore'
import { watch } from 'vue'

import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
import Hint from '../components/Hint.vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const waitingAssignments = ref(false)
const waitingNoCategories = ref(false)
const showAssignments = ref(true)

// Settings
const currency = ref('€')
const locale = ref('de-DE')

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

// Table Variables
const headersAssignments = [
    { title: 'Keyword', value: 'keyword', sortable: true},
    { title: 'Category', value: 'category', sortable: true},
    { title: 'Check-Mode', value: 'checkMode', sortable: true, align: 'start' },
    { title: '# of Transactions', value: 'numberOfAssignments', sortable: true, align: 'end'},
    { title: 'Action', value: 'action', sortable: false, align: 'center'},
]

const headersNoCategory = [
    { title: 'Date', value: 'date', sortable: true },
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true, align: 'center' },
    { title: 'Period', value: 'period', sortable: true, align: 'center' },
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
    locale.value = settingsData.locale
}

const loadCategories = async () => {
    categories.value = await API('categories', 'GET') 
}

const loadAssignments = async () => {
    waitingAssignments.value = true
    data.value = await API('assignments', 'GET')
    waitingAssignments.value = false
}

const loadNoCategory = async () => {
    waitingNoCategories.value = true
    dataNoCategory.value = await API("transactions/?category=0", 'GET')
    waitingNoCategories.value = false
}

////////////////////////////////////////////////////////////////
// CRUD Methods
////////////////////////////////////////////////////////////////
const createAssignment = async () => {
    if (keyword.value === '' || category.value === '' || checkMode.value === '') {
        componentStore.showAlert('Input Failure', 'Please check your input fields', 'error', 4000)
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
        componentStore.refreshApp()
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

watch([() => componentStore.app.refresh, () => componentStore.categories.trigger], () => {
    load()
})

watch(() => userStore.username, () => {
    load()
})
</script>