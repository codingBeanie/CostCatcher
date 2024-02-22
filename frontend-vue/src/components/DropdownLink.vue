<template>
    <div>
        <button @click="toggleDropdown" class="text-lg font-bold text-secondary-100"> {{ title }}</button>
        <div :id="title" class="text-secondary-100">
            <router-link v-for="link in links" :key="link.title" :to="link.url" class="block ml-4">
                 {{link.title }}
            </router-link>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    title: String,
    links: Object
})

const toggleDropdown = () => {
    const dropdown = document.getElementById(props.title)
    dropdown.classList.toggle('hidden')
}
</script>