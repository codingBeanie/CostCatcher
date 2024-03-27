<template>
  <v-dialog v-model="active" max-width="700px">

    <v-card>
        <v-card-title>
            <h2>Edit Category</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field v-model="newCategory" label="Category Name" clearable></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <h4 class="mb-1 font-weight-thin">Color</h4>
                    </v-col>
                    <v-col>
                        <h4 class="mb-1 font-weight-thin">Preview</h4>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-color-picker v-model="newColor" hide-inputs></v-color-picker>
                    </v-col>
                    <v-col class="text-center">
                        <v-chip :color="newColor" size="large">{{ newCategory }}</v-chip>
                    </v-col>
                </v-row>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Save" color="success" @click="save"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { API } from '../composables/API.js'
import { useDialogStore } from '../stores/DialogStore.js'
import { useUpdateStore } from '../stores/UpdateStore.js'

const active = ref(false)
const props = defineProps({
    item: Object,
})
const newCategory = ref('')
const newColor = ref('')
const dialogStore = useDialogStore()
const updateStore = useUpdateStore()

const close = () => {
    active.value = false
    newCategory.value = ''
    newColor.value = ''
}

const save = async () => {
    const data = {
        id: props.item.id,
        name: newCategory.value,
        color: newColor.value
    }
    await API('categories', 'PUT', data) 
    dialogStore.category = !dialogStore.category
    updateStore.refresh = !updateStore.refresh
    active.value = false
}

watch(() => dialogStore.categoryEdit, () => {
    active.value = true
    newCategory.value = props.item.name
    newColor.value = props.item.color
})

</script>
