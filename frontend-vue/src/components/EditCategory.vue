<template>
  <v-dialog v-model="active" max-width="700px">

    <v-card>
        <v-card-title>
            <DialogTitle title="Edit Category"></DialogTitle>   
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field v-model="newCategory" label="Category Name" clearable></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col cols="12" md="6">
                         <h4 class="mb-1 font-weight-thin">Color</h4>
                        <v-color-picker v-model="newColor" hide-inputs></v-color-picker>
                    </v-col>

                    <v-col cols="12" md="6">
                         <h4 class="mb-1 font-weight-thin">Preview</h4>
                        <v-chip :color="newColor" size="large">{{ newCategory }}</v-chip>
                    </v-col>
                </v-row>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Save" variant="tonal" color="accent" @click="save"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { API } from '../composables/API.js'
import { useComponentStore } from '../stores/ComponentStore.js'
import DialogTitle from './DialogTitle.vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()

// Input
const newCategory = ref('')
const newColor = ref('')
const id = ref('')

////////////////////////////////////////////////////////////////
// Loads
////////////////////////////////////////////////////////////////
const loadData = async () => {
    id.value = componentStore.categoryEdit.id
    const data = await API(`categories/?id=${id.value}`, 'GET')
    newCategory.value = data[0].name
    newColor.value = data[0].color
}

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
    newCategory.value = ''
    newColor.value = ''
}

const save = async () => {
    const data = {
        id: id.value,
        name: newCategory.value,
        color: newColor.value
    }
    await API('categories', 'PUT', data) 
    componentStore.refreshApp()
    active.value = false
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
const load = () => {
    loadData()
}

watch(() => componentStore.categoryEdit.trigger, () => {
    load()
    active.value = true  
})



</script>
