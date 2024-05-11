<template>
    <v-dialog v-model="active" transition="none" fullscreen>

        <v-card color="secondary">
            <v-container>
                <v-row class="padding">
                    <v-col cols="10">
                        <p class="text-h5">COSTCATCHER</p>
                    </v-col>
                    <v-col cols="2">
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
import { onMounted, ref} from 'vue'
import { useUserStore } from '../stores/UserStore.js'
import { useComponentStore } from '../stores/ComponentStore'
import { useRoute } from 'vue-router'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const userStore = useUserStore()
const componentStore = useComponentStore()
const active = ref(true)
const route = useRoute()

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
onMounted(() => {
    if(route.params.token){
        componentStore.openNewPassword()
    }
}
)
</script>

<style scoped>
.padding {
    padding-bottom: 20vh;
}
.wrap-text {
    width: 680px;
}
</style>