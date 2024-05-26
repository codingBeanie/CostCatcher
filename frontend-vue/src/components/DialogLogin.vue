<template>
  <v-dialog v-model="active" max-width="500px">

    <v-card>
        <v-card-title>
            <DialogTitle title="Welcome back!"></DialogTitle>   
        </v-card-title>

        <v-card-text>
            <v-container>
               <v-text-field v-model="username" @keydown.enter="login" label="Username"></v-text-field>
                <v-text-field v-model="password" @keydown.enter="login" type="password" label="Password"></v-text-field>
                <p v-if="failedLogin" class="text-error">Name or password is wrong!</p>
                <v-btn variant="plain" @click="componentStore.openPasswordReset">Forgot Password?</v-btn>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Login" variant="tonal" color="accent" @click="login"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { loginUser } from '../composables/UserAuth.js'
import { useRouter } from 'vue-router'
import DialogTitle from './DialogTitle.vue'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()
const failedLogin = ref(false)
const router = useRouter()

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
    const response = await loginUser(username.value, password.value)

    if (response == true) {
        active.value = false
        failedLogin.value = false
        router.push('/welcome')
    }   
    else {
        failedLogin.value = true
    }
}


////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => componentStore.login.trigger, () => {
    active.value = true  
})

</script>
../composables/UserAuth.js