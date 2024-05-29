<template>
    <v-dialog v-model="active" transition="none" fullscreen>

        <v-card color="secondary">
            <v-container>
                <v-row class="padding text-center">
                    <v-col cols="">
                        <v-img src="@/assets/logo_trans_light.webp" max-height="50"></v-img>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col class="mr-10 ml-10">
                        <v-row class="mb-4">
                            <p class="text-h2 font-weight-bold">OUCH....!</p>
                        </v-row>

                        <v-row class="mr-10">
                            <p class="text-h6 font-weight-light">You are trying to view this website on a small or zoomed in screen. Sorry, but the developer did not optimised it for small spaces. Switch to a desktop PC or zoom out a bit.</p>
                        </v-row>

                    </v-col>
                </v-row>


            </v-container>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { createDeviceDetector } from "next-vue-device-detector"
////////////////////////////////////////
// Variables //
// State Management
const active = ref(true)
const componentStore = useComponentStore()
const device = createDeviceDetector()

////////////////////////////////////////
// Lifecylce //
onMounted(() => { 
    if (device.mobile == true) {
        active.value = true
    }
    if (componentStore.app.screen == 0) {
        active.value = true
    }
})

watch(componentStore.app, () => {

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