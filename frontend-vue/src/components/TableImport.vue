<template>
<div class="flex flex-col">
    <h2>Preview of data</h2>
    <h3 class="mb-5">Review your import data and set the the rows and coloumns that should be imported</h3>
    <div class="flex items-center">
        <div class="mr-3">
            <div>
                <h4>First Row</h4>
            </div>
            <div class="">
                <input type="number" v-model="selectFirst" min="1" :max="maxRows" class="w-32 p-1 text-right rounded-lg bg-light-100">
            </div>     
        </div>
        <div class="mr-3">
            <div>
                <h4>Last Row</h4>
            </div>
            <div>
                <input type="number" v-model="selectLast" min="1" :max="maxRows" class="w-32 p-1 text-right rounded-lg bg-light-100">
            </div>     
        </div>
    
        <div class="mr-3">
            <div>
                <h4>Column Date</h4>   
            </div>
            <div>
                <input type="number" v-model="selectDate" min="1" :max="maxColumns" class="w-32 p-1 text-right rounded-lg bg-light-100">
            </div>     
        </div>

        <div class="mr-3">
            <div>
                <h4>Column Recipient</h4>       
            </div>
            <div>
                <input type="number" v-model="selectRecipient" min="1" :max="maxColumns" class="w-32 p-1 text-right rounded-lg bg-light-100">
            </div>     
        </div>

        <div class="mr-3">
            <div>
               <h4>Column Description</h4>     
            </div>
            <div>
                <input type="number" v-model="selectDescription" min="1" :max="maxColumns" class="w-32 p-1 text-right rounded-lg bg-light-100">
            </div>     
        </div>

        <div class="mr-3">
            <div>
                <h4>Column Amount</h4>    
            </div>
            <div>
                <input type="number" v-model="selectAmount" min="1" :max="maxColumns" class="w-32 p-1 text-right rounded-lg bg-light-100">
            </div>     
        </div>           
    </div>
</div>

<div class="mt-2">
    <Button @click="confirm">Confirm and Upload</Button>
</div>

<div class="relative mt-5 overflow-auto h-96">
<table class="w-full overflow-scroll table-auto">
    <thead class="">
        <tr class="sticky top-0 text-left bg-light-300 ">
            <th class="">#</th>
            <th v-for="i in maxColumns" :key="i" class="pl-2">
                <div v-if="i === selectDate" class="bg-highlight-100">
                    Date
                </div>
                <div v-else-if="i === selectRecipient" class="bg-highlight-200">
                    Recipient
                </div>
                <div v-else-if="i === selectAmount" class="bg-highlight-300">
                    Amount
                </div>
                <div v-else-if="i === selectDescription" class="bg-highlight-400">
                    Description
                </div>
                <div v-else>
                    {{ i }}
                </div>
            </th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(line, rowIndex) in arrayData" :key="line" class="border bg-light-100">
            <th scope="row">{{ rowIndex + 1 }}</th>
            <td v-for="(value, colIndex) in maxColumns" :key="value" class="h-px">
                <div v-if="rowIndex + 1 < selectFirst || rowIndex + 1 > selectLast" class="h-8 text-center bg-light-300">
                    (/)
                </div>
                <div v-else>
                    {{ line[value - 1] }}
                </div>
            </td>
        </tr>
    </tbody>

</table>
</div>

</template>

<script setup>
import { computed, ref } from 'vue'
import Button from '../components/Button.vue'
import { sendData } from '../composables/ImportManager.js'


const selectFirst = ref(1)
const selectLast = ref(10)
const selectDate = ref(1)
const selectRecipient = ref(2)
const selectAmount = ref(3)
const selectDescription = ref(4)

const props = defineProps({
    arrayData: Array
})

// Calculate Min and Maxs for input fields
const maxColumns = computed(() => {
    const max = Math.max(...props.arrayData.map(line => line.length))
    if (isFinite(max)) {
        return max
    }
    else {
        return 0
    }
})

const maxRows = computed(() => {
    return props.arrayData.length
})
selectLast.value = maxRows.value

// Button Action
const confirm = (() => {
    sendData(props.arrayData, selectFirst, selectLast, selectDate, selectRecipient, selectDescription, selectAmount)
})


</script>