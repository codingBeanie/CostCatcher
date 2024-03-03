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
                    <v-col>
                        <v-select v-model="newType" label="Expense Type" :items="['Expense', 'Income']"></v-select>
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
import { updateData } from '../composables/API.js'
import { useUpdateStore } from '../stores/UpdateStore';

const active = ref(false)
const props = defineProps({
  inputCategory: String,
  inputType: String
})
const newCategory = ref(props.inputCategory)
const newType = ref(props.inputType)
const updateStore = useUpdateStore()

const close = () => {
    active.value = false
}

const save = async () => {
    const data = {
        oldName: props.inputCategory,
        newName: newCategory.value,
        newType: newType.value
    }
    await updateData(data, 'categories') 
    updateStore.closeEditCategory()
    active.value = false
}

</script>
