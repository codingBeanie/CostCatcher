<template>
    <v-dialog v-model="active" transition="none" fullscreen>

        <v-card color="secondary">
            <v-container>
                <v-row class="padding">
                    <v-col cols="11">
                        <p class="text-h5">COSTCATCHER</p>
                    </v-col>
                    <v-col cols="1">
                        <v-btn color="info" prepend-icon="mdi-login" @click="componentStore.openLogin">Login</v-btn>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col class="mr-10">
                        <v-row class="mb-4">
                            <p class="text-h2 font-weight-bold">Get an overview over your spendings</p>
                        </v-row>

                        <v-row class="">
                            <p class="text-h6 font-weight-thin">Upload csv-files with your bank transactions, categorize your expenses and analyse your spendings.</p>
                        </v-row>

                        <v-row class="mt-10">
                            <v-btn size="large" min-width="200px" max-width="200px" color="accent" @click="componentStore.openRegister">Register</v-btn>
                        </v-row> 
                    </v-col>

                    <v-col class="ml-10">
                        IMAGES
                    </v-col>

                </v-row>


            </v-container>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
////////////////////////////////////////
// Variables //
// State Management
const active = ref(true)
const componentStore = useComponentStore()
const userStore = useUserStore()

////////////////////////////////////////
// Lifecylce //
watch(() => userStore.username, () => {
    if (userStore.username != null) {
        active.value = false
    }
    else {
        active.value = true
    }
 })
</script>

<style scoped>
.padding {
    padding-bottom: 20vh;
}
.wrap-text {
    width: 680px;
}
</style>