<template>
    <v-row justify="center">
        <v-dialog v-model="active" max-width="400px">

            <v-card>

                <v-card-title>
                    <DialogTitle title="Delete Item"></DialogTitle>
                </v-card-title>

                <v-card-text class="text-center">
                    <p class="text-h5 text-error font-weight-bold">{{ title }}</p>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text="Cancel" color="sucess" @click="close"></v-btn>
                    <v-btn text="Confirm" variant="tonal" color="error" @click="confirm"></v-btn>
                </v-card-actions>

            </v-card>
        </v-dialog>
    </v-row>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { API } from '../composables/API.js'
import DialogTitle from './DialogTitle.vue'

////////////////////////////////////////////////////////////////
// State Management
////////////////////////////////////////////////////////////////
const componentStore = useComponentStore()
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
    await API(resource.value, 'DELETE', itemID.value)
    active.value = false
    componentStore.refreshApp()
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
watch(() => componentStore.delete.trigger, () => {
    title.value = componentStore.delete.title
    itemID.value = componentStore.delete.itemID
    resource.value = componentStore.delete.resource
    active.value = true
    
})

</script>