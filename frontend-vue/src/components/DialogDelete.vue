<template>
    <v-row justify="center">
        <v-dialog v-model="active" max-width="400px">

            <v-card>

                <v-card-title>
                    <h4 class="font-weight-thin">Are you sure you want to delete?</h4>
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
import { useMainStore} from '../stores/MainStore.js'
import { API } from '../composables/API.js'

////////////////////////////////////////////////////////////////
// State Management
////////////////////////////////////////////////////////////////
const mainStore = useMainStore()
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
    mainStore.refreshApp()
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
watch(() => mainStore.delete.trigger, () => {
    title.value = mainStore.delete.title
    itemID.value = mainStore.delete.itemID
    resource.value = mainStore.delete.resource
    active.value = true
})

</script>