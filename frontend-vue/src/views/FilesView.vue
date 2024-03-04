<template>
    <!--Titles-->
    <div>
        <h1 class="mb-3 text-h3 font-weight-bold">Uploads</h1>
        <p class="mb-4 text-h7">Manage your uploaded files here.</p>
    </div>
    <v-divider class="mb-8"></v-divider>

    <!--File-Table-->
    <div>
        <v-data-table :items="data" :headers="headers.value">
            <template v-slot:item.action="{ item }">
                <v-btn density="compact" icon="mdi-delete" color="" @click="deleteItem(item)">
                </v-btn>
            </template>
        </v-data-table>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getData } from '../composables/API.js'
import { deleteData } from '../composables/API.js'
import { useAlertStore } from '../stores/AlertStore';

const data = ref([])
const headers = [
    { text: 'File Name', value: 'fileName' },
    { text: 'File Date', value: 'fileDate' },
    { text: 'Actions', value: 'action'}
]
const alertStore = useAlertStore()

// Methods
const loadTable = async () => {
    const rawData = await getData('files')
    data.value = rawData.map(item => ({ ...item, action: null }))
}

const deleteItem = async (item) => {
    await deleteData(item, 'files')
    loadTable()
}


// Lifecycle
onMounted(async () => {
    loadTable()
})
</script>