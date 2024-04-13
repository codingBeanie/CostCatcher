<template>
    <div>
        <h1 class="">{{ title }}</h1>
        <p class="mb-4 text-h6 font-weight-light">{{ subtitle }}</p>
    </div>
    <v-divider class="mb-2"></v-divider>
</template>

<script setup>
const props = defineProps({
    title: String,
    subtitle: String
})
</script>