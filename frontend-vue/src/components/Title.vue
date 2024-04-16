<template>
    <div>
        <h1 class="text-h3">{{ title }}</h1>
        <p class="mb-10 ml-1 mt-1 text-h6 font-weight-light">{{ subtitle }}</p>
    </div>
</template>

<script setup>

const props = defineProps({
    title: String,
    subtitle: String
})
</script>