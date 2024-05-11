<template>
    <div class="d-flex justify-center text-center align-center">
        <p class="mb-10 ml-1 mt-1 text-h6 font-weight-light">Hint: {{ text }}</p>
    </div>
</template>

<script setup>

const props = defineProps({
    text: String
})
</script>