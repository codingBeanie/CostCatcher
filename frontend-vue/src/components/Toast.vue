<template>
    <div id="toast" class="fixed flex justify-center invisible p-3 transition-all duration-500 ease-in-out -translate-x-1/2 rounded-md shadow-lg opacity-0 bottom-5 left-1/2 w-96 bg-secondary-100 text-primary-300">
        <h3 id="toastContent"> {{ content }}</h3>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  content: String
})
</script>