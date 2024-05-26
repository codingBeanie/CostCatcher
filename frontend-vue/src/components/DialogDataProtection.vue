<template>
  <v-dialog v-model="active" max-width="1000px">

    <v-card>
        <v-card-text>
            <v-container>
                <v-row v-for="chapter in DataPolicy" class="mb-8">
                    <v-col>
                        <v-row class="">
                            <p class="text-h5 font-weight-bold">{{ chapter.title }}</p>
                        </v-row>
                        <v-row v-if="chapter.description">
                            <p>{{ chapter.description }}</p>
                        </v-row>
                        <v-row v-if="chapter.bullets">
                            <v-list>
                                <v-list-item v-for="bullet in chapter.bullets" :key="bullet" prepend-icon="mdi-circle-small">
                                    <v-list-item-title>{{ bullet }}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-row>
                    </v-col>

                </v-row>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="OK" color="success" variant="tonal" @click="close"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { DataPolicy } from '../composables/DataPolicy.js'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const active = ref(false)
const componentStore = useComponentStore()

// Input

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watch(() => componentStore.dataProtection.trigger, () => {
    active.value = true  
})

</script>