<template>
    <p :class="['text-center', 'text-overline', 'mt-' + spacing]">{{ title }}</p>
    <v-divider color="info" thickness="3" class="mb-2"></v-divider>
    
</template>

<script setup>
const props = defineProps({
    title: String,
    spacing: Number
})
</script>