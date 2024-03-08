<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Review</h1>
        <p class="mb-4 text-h7">Review your data. Override category assignments or edit transactions.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Search-->
    <div class="mb-3">
        <v-text-field
        v-model="search"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        hide-details
        single-line
        ></v-text-field>
    </div>

    <!--File-Table-->
    <div>
        <v-data-table :items="data" :headers="headers" :search="search">
            <template v-slot:item.date="{ item }">
                {{ new Date(item.date).toLocaleDateString() }}
            </template>

            <template v-slot:item.category=" { item }">
                {{ item.category }}
            </template>

            <template v-slot:item.action="{ item }">
                <v-btn density="compact" icon="mdi-delete" color="" @click="deleteItem(item)">
                </v-btn>
            </template>
        </v-data-table>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { API } from '../composables/API.js'

const data = ref([])
const search = ref('')

const headers = [
    { title: 'Date', value: 'date', sortable: true},
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true},
    { title: 'Category', value: 'categoryName', sortable: true},
    { title: 'Action', value: 'action' }
]

// Methods
const loadTable = async () => {
    const rawData = await API('transactions', 'GET')
    const categories = await API('categories', 'GET')

    data.value = rawData.map(item => ({ ...item, action: null, categoryName: categories.find(category => category.id === item.category)?.name }))
}

const deleteItem = async (item) => {
    await API('transactions', 'DELETE', item)
    loadTable()
}


// Lifecycle
onMounted(async () => {
    loadTable()
})
</script>