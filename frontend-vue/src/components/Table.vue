<template>
<table class="table">
    <thead>
        <tr>
            <th class="bg-secondary text-primary" v-for="key in Object.keys(jsonData[0])" :key="key">
                {{ translations[key] || key}}
            </th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="entry in jsonData" :key="entry.id">
            <td v-for="value in Object.values(entry)" :key="value">
                {{ value }}
            </td>
        </tr>
    </tbody>
</table> 
</template>

<script setup>

import { onMounted, ref } from 'vue';

const props = defineProps({
  jsonData: Object
})
const translations = ref({
    sourceFile: 'Name of File',
    sourceFileDate: 'Date of Upload',
    undefined: 'Undefined'
})


</script>