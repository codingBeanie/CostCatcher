<template>
  <v-dialog v-model="active" max-width="600px">

    <v-card>
        <v-card-title>
            <h2>Edit Assignment</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field v-model="keyword" label="Keyword"></v-text-field>
                    </v-col>
                    <v-col>
                        <v-select v-model="category" label="Category" :items="categories" item-title="name" item-value="id"></v-select>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-select v-model="checkMode" label="Check Mode" :items="checkItems" item-title="title" item-value="value"></v-select>
                    </v-col>
                </v-row>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="sucess" @click="close"></v-btn>
            <v-btn text="Save" color="sucess" @click="save"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useMainStore } from '@/stores/MainStore';
import { API } from '../composables/API.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const mainStore = useMainStore()

// Input
const id = ref('')
const keyword = ref('')
const category = ref('')
const categories = ref([])
const checkMode = ref([])
const checkItems = [{ 'value': 'recipient_or_description', 'title': 'Keyword must be in recipient or description' },
                    { 'value': 'recipient_only', 'title': 'Keyword must be in recipient only' },
                    { 'value': 'description_only', 'title': 'Keyword must be in description only' },
                    { 'value': 'recipient_and_description', 'title': 'Keyword must be in recipient and description' }]

////////////////////////////////////////////////////////////////
// Controls
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const save = async () => {
    const data = {
        id: id.value,
        keyword: keyword.value,
        category: category.value,
        checkMode: checkMode.value
    }
    await API('assignments', 'PUT', data) 
    active.value = false
    mainStore.refreshApp()
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
const load = async () => {
    id.value = mainStore.assignmentEdit.id
    const data = await API(`assignments/?id=${id.value}`, 'GET')
    keyword.value = data.keyword
    category.value = data.category
    checkMode.value = data.checkMode

    categories.value = await API('categories', 'GET')
}

watch(() => mainStore.assignmentEdit.trigger, () => {
    load()
    active.value = true  
})


</script>
../stores/MainStore