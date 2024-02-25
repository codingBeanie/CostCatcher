<template>
    
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getData } from '../composables/API.js'

const data = ref(null)

onMounted(async () => {
    data.value = await getData('files')
})
</script>