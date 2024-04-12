<template>
  <v-dialog v-model="active" max-width="400px">

    <v-card>
        <v-card-title>
            <h2>Heyho, welcome back!</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
               <v-text-field v-model="username" @keydown.enter="login" label="Name"></v-text-field>
                <v-text-field v-model="password" @keydown.enter="login" label="Password"></v-text-field>
                <p v-if="failedLogin" class="text-error">Name or password is wrong!</p>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Login" color="accent" @click="login"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useMainStore } from '../stores/MainStore.js'
import { Authentication } from '../composables/Authentication.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const mainStore = useMainStore()
const failedLogin = ref(false)

// Input
const username = ref('')
const password = ref('')

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const login = async () => {
    const payload = {
        username: username.value,
        password: password.value
    }
    const response = await Authentication('login', payload)

    if (response == true) {
        active.value = false
        failedLogin.value = false
    }   
    else {
        failedLogin.value = true
    }
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => mainStore.login.trigger, () => {
    active.value = true  
})

</script>
