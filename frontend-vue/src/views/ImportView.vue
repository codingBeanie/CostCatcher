<template>
    <div class="d-flex flex-column align-items-center">
        <h1>Import</h1>
        <h4>Import your CSV-File here</h4>
        <BasicTable v-if="data" :jsonData="data" />
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getData } from '../composables/API.js'
import BasicTable from '../components/BasicTable.vue'

const data = ref(null)

onMounted(async () => {
    data.value = await getData('files')
})

</script>