<template>
    <div class="overlay bg-secondary">
        <v-container>
            <v-row class="padding">
                <v-col>
                    <p class="text-h1 font-weight-bold">COSTCATCHER</p>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <p class="text-h4 font-weight-thin wrap-text">Categorize and analyse your spendings. Simply upload your data via a csv-file and start cost catching.</p>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="2">
                    <v-btn size="x-large" height="5vh" width="10vw" color="info">Login</v-btn>
                </v-col>
                <v-col cols="2">
                    <v-btn size="x-large" height="5vh" width="10vw" color="accent" @click="register">Register</v-btn>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script setup>
import { useMainStore } from '../stores/MainStore.js'

////////////////////////////////////////////////////////////
// Variables //
// State Management
const mainStore = useMainStore()

////////////////////////////////////////////////////////////
// Actions //
const register = () => {
    mainStore.openRegister()
}
</script>

<style scoped>
.overlay {
    height: 100vh;
    width: 100vw;
    z-index: 2000;
    position: fixed;
    top: 0;
    left: 0;
}
.padding {
    padding-top: 20vh;
}
.wrap-text {
    width: 45vw;
}
</style>