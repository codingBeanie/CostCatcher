<template>

<!--Descriptions-->
<div>
    <p class="mb-4 text-h5">Please check your data. If you encounter problems try to adjust the import schema.</p>
</div>

<!--Selectors-->
<v-row>
    <v-col><v-text-field type="number" density="compact" label="First Row" v-model="selectFirst"/></v-col>
    <v-col><v-text-field type="number" density="compact" label="Last Row" v-model="selectLast"/></v-col>
    <v-col><v-text-field type="number" density="compact" label="Column Date" v-model="selectDate" class="text-red-darken-4"/></v-col>
    <v-col><v-text-field type="number" density="compact" label="Column Recipient" v-model="selectRecipient" class="text-pink-darken-1"/></v-col>
    <v-col><v-text-field type="number" density="compact" label="Column Description" v-model="selectDescription" class="text-blue-darken-3"/></v-col>
    <v-col><v-text-field type="number" density="compact" label="Column Amount" v-model="selectAmount"/></v-col>
</v-row>

<!--Table-->
<div>
    <v-data-table :items="arrayData" headers="">
    </v-data-table>
    <v-table :key="selectDate" height="500" hover density fixed-header >
    <thead class="">
        <tr>
            <th class="">#</th>
            <th v-for="i in maxColumns" :key="i" class="">
                <div v-if="i == selectDate" class="pl-2 bg-red-darken-1">
                    Date
                </div>
                <div v-else-if="i == selectRecipient" class="pl-2 bg-pink-darken-3">
                    Recipient
                </div>
                <div v-else-if="i == selectAmount" class="pl-2 bg-green-darken-4">
                    Amount
                </div>
                <div v-else-if="i == selectDescription" class="pl-2 bg-blue-darken-4">
                    Description
                </div>
                <div v-else>
                    {{ i }}
                </div>
            </th>
        </tr>
    </thead>
        <tbody>
            <tr v-for="(line, rowIndex) in arrayData" :key="line" class="">
                <th scope="row">{{ rowIndex + 1 }}</th>
                <td v-for="(value, colIndex) in maxColumns" :key="value" class="">
                    <div v-if="rowIndex + 1 < selectFirst || rowIndex + 1 > selectLast" class="bg-grey-lighten-2">
                        (/)
                    </div>
                    <div v-else-if="colIndex + 1 == selectDate" class="justify-start d-flex grow bg-red-lighten-4">
                        {{ line[value - 1] }}
                    </div>
                    <div v-else>
                        {{ line[value - 1] }}
                    </div>
                </td>
            </tr>
        </tbody>
    </v-table>
</div>


<!-- <div class="flex">
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
</div> -->

</template>

<script setup>
import { computed, ref } from 'vue'
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