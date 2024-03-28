<template>
    <v-row justify="center">
        <v-dialog v-model="active" max-width="400px">

            <v-card>

                <v-card-title>
                    <h3>Are you sure you want to delete?</h3>
                </v-card-title>

                <v-card-text>
                    <h4>{{ title }}</h4>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text="Cancel" color="sucess" @click="close"></v-btn>
                    <v-btn text="Confirm" color="error" @click="confirm"></v-btn>
                </v-card-actions>

            </v-card>
        </v-dialog>
    </v-row>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useDialogStore } from '../stores/DialogStore.js'
import { useUpdateStore } from '@/stores/UpdateStore.js';
import { API } from '../composables/API.js'

////////////////////////////////////////////////////////////////
// State Management
////////////////////////////////////////////////////////////////
const dialogStore = useDialogStore()
const updateStore = useUpdateStore()
const active = ref(false)

////////////////////////////////////////////////////////////////
// Operational Variables
////////////////////////////////////////////////////////////////
const title = ref('')
const itemID = ref('')
const resource = ref('')

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const confirm = async () => {
    console.log('Deleting item', itemID.value, 'from', resource.value)
    await API(resource.value, 'DELETE', itemID.value)
    active.value = false
    updateStore.refresh = !updateStore.refresh
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
watch(() => dialogStore.delete.trigger, () => {
    title.value = dialogStore.delete.title
    itemID.value = dialogStore.delete.itemID
    resource.value = dialogStore.delete.resource
    active.value = true
})

</script>