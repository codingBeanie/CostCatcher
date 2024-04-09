<template>
  <v-dialog v-model="active" max-width="700px">

    <v-card>
        <v-card-title>
            <h2>Register</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
               
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="info" @click="close"></v-btn>
            <v-btn text="Register" color="success" @click="register"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { API } from '../composables/API.js'
import { useMainStore } from '../stores/MainStore.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const mainStore = useMainStore()

// Input
const name = ref('')
const email = ref('')
const password = ref('')

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const register = async () => {
    active.value = false
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => mainStore.register.trigger, () => {
    active.value = true  
})

</script>
