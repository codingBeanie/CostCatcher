<template>
  <v-dialog v-model="active" max-width="500px">

    <v-card>
        <v-card-title>
            <h2>Get an password reset mail</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
               <v-text-field v-model="username" @keydown.enter="sendMail" label="Name"></v-text-field>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Send Mail" color="accent" @click="sendMail"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { passwordReset } from '../composables/UserAuth'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()
const failedLogin = ref(false)

// Input
const username = ref('')

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const sendMail = async () => {
    const response = await passwordReset(username.value)
    active.value = false
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => componentStore.resetPassword.trigger, () => {
    active.value = true  
})

</script>
