<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Categories</h1>
        <p class="mb-4 text-h7">Create, edit and delete custom categories for your transactions.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--Create Form-->
    <div>
        <v-row>
            <v-col cols="4">
                <v-text-field v-model="inputCategory" label="Category Name"></v-text-field>
            </v-col>
            <v-col cols="2" class="mt-2">
                <v-btn class="" color="accent" @click="createCategory" prependIcon="mdi-plus">Create</v-btn>
            </v-col>
        </v-row>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--File-Table-->
    <div>
        <v-data-table :items="data">
            <template v-slot:item.action="{ item }">
                <EditCategory :inputCategory="item.name" :id="item.id"/>
                <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="deleteItem(item)">
                </v-btn>
            </template>
        </v-data-table>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { API } from '../composables/API.js'
import { useAlertStore } from '../stores/AlertStore'
import { useUpdateStore } from '../stores/UpdateStore'
import EditCategory from '../components/EditCategory.vue'
import { watch } from 'vue'

const inputCategory = ref('')
const data = ref([])
const alertStore = useAlertStore()
const updateStore = useUpdateStore()

// Methods
const loadTable = async () => {
    const rawData = await API('categories', 'GET')
    data.value = rawData.map(item => ({ ...item, action: null }))
}

const createCategory = async () => {
    if(inputCategory.value === '') {
        alertStore.showAlert('Input Failure', 'Please enter a category name.', 'error', 4000)
        return
    } else {
        const category = {
            name: inputCategory.value,
        }
        await API('categories', 'POST', category)
        inputCategory.value = ''
        loadTable()
    }
}

const deleteItem = async (item) => {
    await API('categories', 'DELETE', item)
    loadTable()
}


// Lifecycle
onMounted(async () => {
    loadTable()
})

watch(() => updateStore.editCategoryClosed, () => {
    loadTable()
})
</script>