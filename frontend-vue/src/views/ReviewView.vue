<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Review</h1>
        <p class="mb-4 text-h7">Review your data. Override category assignments or edit transactions.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <v-row>
        <v-col>
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
        </v-col>
        <v-col>
            <v-select
                v-model="selectedCategories"
                 :items="categories.map(category => category.name)"
                clearable
                chips
                multiple
                variant="outlined"
                label="Categories"        
                ></v-select>
        </v-col>
    </v-row>


    <!--File-Table-->
    <div>
        <v-data-table :items="data" :headers="headers" :search="search">
            <!--Category-->
            <template v-slot:item.date="{ item }">
                {{ new Date(item.date).toLocaleDateString() }}
            </template>

            <!--Category-->
            <template v-slot:item.categoryName="{ item }">
                <v-chip v-if="item.categoryName"> {{ item.categoryName }} </v-chip>
            </template>

            <!--Amount-->
            <template v-slot:item.amount="{ item }">
                <v-row class="justify-end mr-12">
                    {{ item.amount.toFixed(2) }}
                </v-row>
            </template>

            <!--Action-->
            <template v-slot:item.action="{ item }">
                <v-btn density="compact" icon="mdi-delete" color="" @click="deleteItem(item)">
                </v-btn>
            </template>
        </v-data-table>
    </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { API } from '../composables/API.js'

const data = ref([])
const search = ref('')
let categories = ref(['Test'])
const selectedCategories = ref([])

const headers = [
    { title: 'Date', value: 'date', sortable: true},
    { title: 'Recipient', value: 'recipient', sortable: true},
    { title: 'Description', value: 'description', sortable: true},
    { title: 'Amount', value: 'amount', sortable: true, align: 'center'},
    { title: 'Category', value: 'categoryName', sortable: true},
    { title: 'Action', value: 'action' }
]

// Methods
const loadTable = async () => {
    const categoryQuery = selectedCategories.value.map(category => category).join('%')  
    const rawData = await API(`transactions/?categories=${categoryQuery}&datefrom=asdf&dateto=asdf`, 'GET')
    categories.value = await API('categories', 'GET')
    data.value = rawData.map(item => ({ ...item, action: null, categoryName: categories.value.find(category => category.id === item.category)?.name }))
}

const deleteItem = async (item) => {
    await API('transactions', 'DELETE', item)
    loadTable()
}



// Lifecycle
onMounted(async () => {
    loadTable()
})

watch(selectedCategories, () => {
    loadTable()
})
</script>