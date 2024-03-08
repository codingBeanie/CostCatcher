<template>
  <v-dialog v-model="active" max-width="600px">

    <template v-slot:activator="{ props: activatorProps }">
      <v-btn v-bind="activatorProps" icon="mdi-pencil" density="compact">
      </v-btn>
    </template>

    <v-card>
        <v-card-title>
            <h2>Edit Category</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field v-model="newCategory" label="Category Name"></v-text-field>
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
import { ref } from 'vue'
import { API } from '../composables/API.js'
import { useUpdateStore } from '../stores/UpdateStore';

const active = ref(false)
const props = defineProps({
  id: Number,
  inputCategory: String
})
const newCategory = ref(props.inputCategory)
const updateStore = useUpdateStore()

const close = () => {
    active.value = false
}

const save = async () => {
    const data = {
        id: props.id,
        name: newCategory.value,
    }
    await API('categories', 'PUT', data) 
    updateStore.closeDialog()
    active.value = false
}

</script>
