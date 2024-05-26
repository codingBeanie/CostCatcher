<template>
    <v-row no-gutters :class="['mt-' + spacing]">
        <v-col cols="1">
        </v-col>
        <v-col class="text-center" cols="10">
            <p class="text-overline text-secondary">{{ title }}</p>
        </v-col>
        <v-col cols="1">
            <v-btn v-if="showToggle && showStateRef" @click="toggleVisibility" prepend-icon="mdi-eye-off" variant="plain" color="info">hide</v-btn>
            <v-btn v-if="showToggle && !showStateRef" @click="toggleVisibility" prepend-icon="mdi-eye" variant="plain" color="info">show</v-btn>
        </v-col>
    </v-row>
    <v-row no-gutters>
        <v-col class="">
            <v-divider color="info" thickness="3"></v-divider>
        </v-col>
    </v-row>
    
</template>

<script setup>
import {ref, watchEffect } from 'vue';
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const props = defineProps({
    title: {
        type: String,
        default: ''
    },
    spacing: {
        type: String,
        default: "0"
    },
    showToggle: {
        type: Boolean,
        default: false
    },
    showState: {
        type: Boolean,
        default: true
    }
})
const showStateRef = ref(true)
const emit = defineEmits(['toggle'])
////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const toggleVisibility = () => {
    showStateRef.value = !showStateRef.value
    emit('toggle', showStateRef.value)
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
watchEffect(() => {
    if (props.showState) {
        showStateRef.value = props.showState
    }
})
</script>