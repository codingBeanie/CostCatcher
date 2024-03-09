<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Uploads</h1>
        <p class="mb-4 text-h7">Manage your uploaded files here. Delete all corresponding transactions of a previous file upload.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--File-Table-->
    <div>
        <v-data-table :items="data" :headers="headers">
            <!--Date-->
            <template v-slot:item.fileDate="{ item }">
                {{ new Date(item.fileDate).toLocaleString() }}
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
const headers = [
    { title: 'File Name', value: 'fileName' },
    { title: 'Upload Date', value: 'fileDate' },
    { title: 'Actions', value: 'action', align: 'center'}
]

// Methods
const loadTable = async () => {
    const rawData = await API('files', 'GET')
    data.value = rawData.map(item => ({ ...item, action: null }))
}

const deleteItem = async (item) => {
    await API('files', 'DELETE', item)
    loadTable()
}


// Lifecycle
onMounted(async () => {
    loadTable()
})
</script>