<template>
<table class="bg-gray-100 shadow-sm table-auto ">
    <thead>
        <tr>
            <th class="p-1 pl-2 text-left border-b ptext-left text-primary-300" v-for="key in Object.keys(jsonData[0])" :key="key">
                {{ translations[key] || key}}
            </th>
            <th class="p-1 pl-2 text-left border-b ptext-left text-primary-300">
                Actions
            </th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="entry in jsonData" :key="entry.id">
            <td v-for="value in Object.values(entry)" :key="value" class="p-1 border-b-2 border-primary-100">
                {{ value }}
            </td>
            
            <td class="p-1 border-b-2 border-primary-100">
                DELETE
            </td>
        </tr>
    </tbody>
</table> 
</template>

<script setup>

import { ref } from 'vue';

const props = defineProps({
  jsonData: Object
})
const translations = ref({
    sourceFile: 'Name of File',
    sourceFileDate: 'Date of Upload',
    undefined: 'Undefined'
})


</script>