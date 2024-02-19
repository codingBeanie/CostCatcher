<template>
         <router-link :to="link" class="text-secondary-100"><slot></slot></router-link>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  link: String
})
</script>

<style>
    .router-link-active {
        text-decoration: solid underline;
    }
</style>
