<template>
  <v-dialog v-model="active" max-width="500px">

    <v-card>
        <v-card-title>
             <DialogTitle title="Change Password"></DialogTitle>  
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-text-field v-model="oldPassword" type="password" @keydown.enter="changePassword" label="Old Password"></v-text-field>
                <v-text-field v-model="password" type="password" @keydown.enter="changePassword" label="New Password"></v-text-field>
                <v-text-field v-model="repeatPassword" type="password" @keydown.enter="changePassword" label="Repeat Password"></v-text-field>
                <p v-if="errorMessage" class="text-error">{{ errorMessage }}</p>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Change" variant="tonal" color="accent" @click="changePassword"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { updatePassword } from '../composables/UserAuth.js'
import DialogTitle from './DialogTitle.vue'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()

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

const changePassword = async () => {
    if (password.value != repeatPassword.value) {
        errorMessage.value = 'Password does not match.'
        return
    }

    const response = await updatePassword(oldPassword.value, password.value)
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
watch(() => componentStore.updatePassword.trigger, () => {
    active.value = true  
})

</script>