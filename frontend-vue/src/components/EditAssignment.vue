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
                        <v-select v-model="category" label="Category" :items="categories"></v-select>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-select v-model="checkMode" label="Check Mode" :items="checkModes"></v-select>
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

// Control Variables
const active = ref(false)
const updateStore = useMainStore()
const dialogStore = useMainStore()

// Data Variables
const id = ref(dialogStore.assignmentEditId)
const keyword = ref('')
const category = ref('')
const categories = ref([])
const checkMode = ref([])
const checkModes = ref([])

// Dialog Controls
const close = () => {
    updateStore.refresh = !updateStore.refresh
    active.value = false
}

const save = async () => {
    const data = {
    }
    await API('assignments', 'PUT', data) 
    active.value = false
    updateStore.refresh = !updateStore.refresh
}

// Lifecycle
const load = async () => {
    const data = await API(`assignments/?id=${id.value}`, 'GET')
    keyword.value = data.keyword
    category.value = data.categoryName
    checkMode.value = data.checkMode
}

watch(() => dialogStore.assignmentEdit, () => {
    id.value = dialogStore.assignmentEditId
    load()
    active.value = true  
})


</script>
../stores/MainStore