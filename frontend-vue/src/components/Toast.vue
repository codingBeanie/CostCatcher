<template>
    <div class="fixed top-0 flex justify-center invisible p-3 rounded-md shadow-lg w-96 bg-secondary-100 text-primary-300">
        <h3> {{ content }}</h3>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  content: String
})
</script>