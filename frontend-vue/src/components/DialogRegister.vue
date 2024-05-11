<template>
  <v-dialog v-model="active" max-width="500px">

    <v-card>
        <v-card-title>
            <h2>Register</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
               <v-text-field v-model="username" @keydown.enter="register" label="Name"></v-text-field>
               <v-text-field v-model="email" @keydown.enter="register" label="E-Mail (optional)"></v-text-field>
                <v-text-field v-model="password" type="password" @keydown.enter="register" label="Password"></v-text-field>
                <v-text-field v-model="repeatPassword" type="password" @keydown.enter="register" label="Repeat Password"></v-text-field>
                <v-row class="d-flex align-center">
                    <v-col>
                        <v-checkbox v-model="checkPrivacyStatement" label="I acknowledge that I have read and agree to the privacy policy.">
                        </v-checkbox>
                    </v-col>
                    <v-col>
                        <v-btn @click="componentStore.openDataProtection">privacy policy</v-btn>
                    </v-col>
                </v-row>
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
import { registerUser } from '../composables/UserAuth.js'
import { useRouter } from 'vue-router'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()
const router = useRouter()

// Error Message
const errorMessage = ref('')

// Input
const username = ref('')
const password = ref('')
const email = ref('')
const repeatPassword = ref('')
const checkPrivacyStatement = ref(false)

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const register = async () => {
    // Validation
    // Checkmarks are set
    if (checkPrivacyStatement.value == false) {
        errorMessage.value = 'You need to agree to the privacy policy.'
        return
    }

    // Passwords match
    if (password.value != repeatPassword.value) {
        errorMessage.value = 'Password does not match.'
        return
    }

    // E-Mail correct format
    if (email.value != "") {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(email.value)) {
            errorMessage.value = 'E-Mail is not valid.'
            return
        }
    }

    const response = await registerUser(username.value, password.value, email.value)

    if (response == true) {
        active.value = false
        router.push('/welcome')
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