<template>
    <v-row justify="center">
        <v-dialog v-model="active" max-width="400px">

            <v-card>

                <v-card-title>
                    <h4 class="font-weight-thin">Are you sure you?</h4>
                </v-card-title>

                <v-card-text>
                    <h4>This will delete all data you uploaded!</h4>
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
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { deleteUser } from '../composables/UserAuth'

////////////////////////////////////////////////////////////////
// State Management
////////////////////////////////////////////////////////////////
const componentStore = useComponentStore()
const userStore = useUserStore()
const active = ref(false)


////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const confirm = async () => {
    active.value = false
    await deleteUser()
    userStore.logout()
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
watch(() => componentStore.deleteAccount.trigger, () => {
    active.value = true
})

</script>