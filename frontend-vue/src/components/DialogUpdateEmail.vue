<template>
  <v-dialog v-model="active" max-width="500px">

    <v-card>
        <v-card-title>
            <h2>Change Email</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-text-field v-model="email" @keydown.enter="changeEmail" label="Change Email"></v-text-field>
                <p v-if="errorMessage" class="text-error">{{ errorMessage }}</p>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Change" color="accent" @click="changeEmail"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore'
import { updateEmail } from '../composables/UserAuth.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()
const userStore = useUserStore()

// Error Message
const errorMessage = ref('')

// Input
const email = ref('')

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const changeEmail = async () => {
    // E-Mail correct format
    if (email.value != "") {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(email.value)) {
            errorMessage.value = 'E-Mail is not valid.'
            return
        }     
    }
    errorMessage.value = ''
    updateEmail(email.value)
    active.value = false
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => componentStore.updateEmail.trigger, () => {
    active.value = true  
    email.value = userStore.email
})

</script>