<template>
  <v-dialog v-model="active" max-width="800px">

    <v-card>
        <v-card-title>
            <v-row>
                <v-col cols="1">
                    <v-icon class="">mdi-school</v-icon>
                </v-col>
                <v-col cols="9">
                    <p class="text-h4">{{ content.title }}</p>
                </v-col>
            </v-row>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row v-for="chapter in content.chapter" class="mb-6">
                    <p class="text-h6 font-weight-bold">{{ chapter.title }}</p>
                    <p>{{ chapter.text }}</p>
                </v-row>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="OK" color="accent" @click="close"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore'
import { Tutorials } from '../composables/Tutorials.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()
const userStore = useUserStore()
const content = ref([])

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const load = () => {
    content.value = Tutorials.filter(tutorial => tutorial.id == componentStore.tutorial.type)[0]
 }

const close = () => {
    active.value = false
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => componentStore.tutorial.trigger, () => {
    active.value = true  
    load()
})

</script>