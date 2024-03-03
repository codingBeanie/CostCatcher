<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Assignments</h1>
        <p class="mb-4 text-h7">Create rules for automatic assignment of categories to your transactions.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Create Form-->
    <div>
        <v-row>
            <v-col>
                <h3 class="">Create a category</h3>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <h4 class="font-weight-regular">Choose a keyword which is then checked for the fields recipients and/or description. If the rule is true, the category will be applied.</h4>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="3">
                <v-text-field v-model="keyword" label="Keyword"></v-text-field>
            </v-col>
            <v-col cols="3">
                <v-select label="Category" v-model="category" :items="categoryItems"></v-select>
            </v-col>
            <v-col cols="2">
                <v-checkbox v-model="recipient" label="Recipient"/>
            </v-col>
            <v-col cols="2">
                <v-checkbox v-model="description" label="Description"/>
            </v-col>
            <v-col cols="2" class="mt-2">
                <v-btn class="" color="accent" @click="createAssignment" prependIcon="mdi-plus">Create</v-btn>
            </v-col>
        </v-row>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Assignment-Table-->
    <div>
        <v-row>
            <v-col>
                <h3 class="">Assignments</h3>
            </v-col>
        </v-row>
        <v-row>
            <v-data-table :items="data">
                <template v-slot:item.action="{ item }">
                    <EditAssignment :keyword="item.keyword" :category="item.category" :recipient="item.checkRecipient" :description="item.checkDescription"/>
                    <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="deleteItem(item)">
                    </v-btn>
                </template>
            </v-data-table>
        </v-row>
    </div>
    <v-divider class="mt-8"></v-divider>
    
    <!--Not assigned-Table-->
    <div>
        <v-row>
            <v-col>
                <h3 class="mt-8">Transactions without a category</h3>
            </v-col>
        </v-row>
        <v-row>
            <v-data-table :items="dataUnmatched">
            </v-data-table>
        </v-row>
    </div>
    <v-divider class="mt-8"></v-divider>    
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getData, deleteData, postData } from '../composables/API.js'
import { useAlertStore } from '../stores/AlertStore'
import { useUpdateStore } from '../stores/UpdateStore'
import EditAssignment from '../components/EditAssignment.vue'
import { watch } from 'vue'

const keyword = ref('')
const recipient = ref(true)
const description = ref(true)
const category = ref('')
const categoryItems = ref([])

const data = ref([])
const dataUnmatched = ref([])
const alertStore = useAlertStore()
const updateStore = useUpdateStore()

// Methods
const loadTable = async () => {
    const rawData = await getData('assignments')
    data.value = rawData.map(item => ({ ...item, action: null }))
}

const loadCategoryItems = async () => {
    const rawData = await getData('categories')
    categoryItems.value = rawData.map(item => item.name)
}

const loadDataUnmatched = async () => {
    const rawData = await getData('transactions/without_category')
    dataUnmatched.value = rawData.map(item => ({ ...item, action: null }))
}

const createAssignment = async () => {
    if (keyword.value === '' || category.value === '' || (!recipient.value && !description.value)) {
        alertStore.showAlert('Input Failure', 'Please check your input fields', 'error', 4000)
        return
    } else {
        const assignment = {
            keyword: keyword.value,
            checkRecipient: recipient.value,
            checkDescription: description.value,
            category: category.value
        }
        await postData(assignment, 'assignments')
        keyword.value = ''
        category.value = ''
        loadTable()
    }
}

const editItem = async () => { }

const deleteItem = async (item) => {
    deleteData(item, 'assignments')
    loadTable()
}


// Lifecycle
onMounted(async () => {
    loadTable()
    loadDataUnmatched()
    loadCategoryItems()
})

watch(() => updateStore.editAssignmentClosed, () => {
    loadTable()
    loadDataUnmatched()
})
</script>