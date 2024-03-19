<template>
    <v-row justify="center">
        <v-dialog v-model="active" max-width="400px">

            <v-card>

                <v-card-title>
                    <h3>Are you sure you want to delete?</h3>
                </v-card-title>

                <v-card-text>
                    <h4>{{ props.itemName }}</h4>
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
import { ref, watch, defineProps } from 'vue'
import { useDialogStore } from '../stores/DialogStore.js'
import { API } from '../composables/API.js'

// Operational Variables
const dialogStore = useDialogStore()
const active = ref(false)

// Props
const props = defineProps({
    item: Object,
    itemName: String,
    resource: String
})

// Methods
const close = () => {
    active.value = false
}

const confirm = async () => {
    await API(props.resource, 'DELETE', props.item)
    active.value = false
    dialogStore.dialog = !dialogStore.dialog
}

// Lifecycle
watch(() => dialogStore.delete, () => {
    active.value = true
})
</script>