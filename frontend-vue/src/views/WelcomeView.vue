<template>
    <UpdateBlog />
</template>

<script setup>
import { onMounted, ref} from 'vue'
import { useUserStore } from '../stores/UserStore.js'
import UpdateBlog from '../components/UpdateBlog.vue'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const userStore = useUserStore()

//
const username = ref(userStore.username)
</script>