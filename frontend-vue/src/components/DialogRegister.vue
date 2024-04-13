<template>
  <v-dialog v-model="active" max-width="500px">

    <v-card>
        <v-card-title>
            <h2>Register</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
               <v-text-field v-model="username" @keydown.enter="register" label="Name"></v-text-field>
                <v-text-field v-model="password" type="password" @keydown.enter="register" label="Password"></v-text-field>
                <v-text-field v-model="repeatPassword" type="password" @keydown.enter="register" label="Repeat Password"></v-text-field>
                <v-checkbox v-model="checkDevMode" label="I understand that this is just a hobby project and i may encounter bugs and problem."></v-checkbox>
                <p v-if="errorMessage" class="text-error">{{ errorMessage }}</p>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Register" color="accent" @click="register"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { RegisterUser } from '../composables/UserAuth.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()

// Error Message
const errorMessage = ref('')

// Input
const username = ref('')
const password = ref('')
const repeatPassword = ref('')
const checkDevMode = ref(false)

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const register = async () => {
    // Validation
    if (checkDevMode.value == false) {
        errorMessage.value = 'You need to agree to the terms and conditions.'
        return
    }

    if (password.value != repeatPassword.value) {
        errorMessage.value = 'Password does not match.'
        return
    }

    const response = await RegisterUser(username.value, password.value)

    if (response == true) {
        active.value = false
    }   
    else {
        errorMessage.value = 'Username already exist.'
    }
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => componentStore.register.trigger, () => {
    active.value = true  
})

</script>