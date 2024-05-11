<template>
  <v-dialog v-model="active" max-width="500px">

    <v-card>
        <v-card-title>
            <h2>Set your new password</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-text-field v-model="password" type="password" @keydown.enter="submitPassword" label="New Password"></v-text-field>
                <v-text-field v-model="repeatPassword" type="password" @keydown.enter="submitPassword" label="Repeat Password"></v-text-field>
                <p v-if="errorMessage" class="text-error">{{ errorMessage }}</p>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Change" color="accent" @click="submitPassword"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { setNewPassword } from '../composables/UserAuth.js'
import { useRoute } from 'vue-router'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()
const route = useRoute()

// Error Message
const errorMessage = ref('')

// Input
const oldPassword = ref('')
const password = ref('')
const repeatPassword = ref('')

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const submitPassword = async () => {
    if (password.value != repeatPassword.value) {
        errorMessage.value = 'Password does not match.'
        return
    }

    const response = await setNewPassword(password.value, route.params.token)
    if (response) {
        active.value = false
    }
    else {
        active.value = true
    }
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => componentStore.newPassword.trigger, () => {
    active.value = true  
})

</script>