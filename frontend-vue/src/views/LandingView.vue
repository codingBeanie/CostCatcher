<template>
    <v-dialog v-model="active" transition="none" fullscreen>

        
        <v-card color="secondary">
            <v-container>

                <!--HEADER-->
                <v-row class="padding">

                    <!--LOGO-->
                    <v-col cols="2">
                        <v-img src="@/assets/logo_trans_light.webp" max-height="50"></v-img>
                    </v-col>

                    <v-col></v-col>

                    <!--LOGIN BUTTON-->
                    <v-col v-if!="device.mobile" cols="2" class="mt-2">
                        <v-btn color="info" prepend-icon="mdi-login" @click="componentStore.openLogin">Login</v-btn>
                    </v-col>

                </v-row>

                <!--STATEMENT-->
                <v-row class="mb-16">

                    <!--LOGO-->
                    <v-col cols="3">
                        <v-img src="@/assets/logo2.webp" max-height="250"></v-img>
                    </v-col>

                    <!--TEXT-->
                    <v-col cols="8" class="mt-6">

                        <!--TITLE-->
                        <v-row v-if!="device.mobile" class="mb-4">
                            <p class="text-h2 font-weight-bold">Say goodbye to your spreadsheets!</p>
                        </v-row>

                        <!--SUBTITLE-->
                        <v-row v-if!="device.mobile" class="">
                            <p class="text-h6">Upload your transactions, set your categorization rules, and enjoy automatic sorting for instant, easy-to-understand financial insights.</p>
                        </v-row>

                        <!--Mobile Text-->
                        <v-row v-if="device.mobile">
                            <v-img src="@/assets/logo_trans_light.webp"></v-img>
                        </v-row>
                        <v-row v-if="device.mobile" class="">
                            <p class="text-h6">This site is not optimised for mobile devices. Please switch to a desktop PC.</p>
                        </v-row>


                        <!--BUTTON-->
                        <v-row v-if!="device.mobile" class="mt-10">
                            <v-btn size="large" min-width="200px" max-width="300px" color="accent" @click="componentStore.openRegister">Register for free</v-btn>
                        </v-row> 

                    </v-col>

                </v-row>

                <!--FEATURES-->
                <v-row class="mt-16">

                    <v-col>
                        <v-carousel hide-delimiters show-arrows="hover" cycle>
                            <v-carousel-item src="@/assets/upload.webp"></v-carousel-item>
                            <v-carousel-item src="@/assets/categorization.webp"></v-carousel-item>
                            <v-carousel-item src="@/assets/tableau.webp"></v-carousel-item>
                            <v-carousel-item src="@/assets/graphs.webp"></v-carousel-item>
                        </v-carousel>
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
import { createDeviceDetector } from "next-vue-device-detector"
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const userStore = useUserStore()
const componentStore = useComponentStore()
const active = ref(true)
const route = useRoute()
const device = createDeviceDetector()

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