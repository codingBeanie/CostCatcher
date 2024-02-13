<template>
<div class="">
        <div class="">
            <div>
                First Row of Data:    
            </div>
            <div>
                <input type="number" v-model="selectFirst" min="1" :max="maxRows">
            </div>     
        </div>

        <div class="">
            <div>
                Last Row of Data:    
            </div>
            <div>
                <input type="number" v-model="selectLast" min="1" :max="maxRows">
            </div>     
        </div>

        <div class="">
            <div>
                Column of Date:     
            </div>
            <div>
                <input type="number" v-model="selectDate" min="1" :max="maxColumns">
            </div>     
        </div>

        <div class="">
            <div>
                Column of Recipient:     
            </div>
            <div>
                <input type="number" v-model="selectRecipient" min="1" :max="maxColumns">
            </div>     
        </div>

        <div class="">
            <div>
                Column of Description:     
            </div>
            <div>
                <input type="number" v-model="selectDescription" min="1" :max="maxColumns">
            </div>     
        </div>

                <div class="">
            <div>
                Column of Amount:     
            </div>
            <div>
                <input type="number" v-model="selectAmount" min="1" :max="maxColumns">
            </div>     
        </div>
    </div>

   <div class="d-flex flex-column align-items-start overflow-auto p-2 mt-4">
    <table class="table table-bordered table-responsive">
        <thead>
            <tr>
                <th>#</th>
                <th v-for="i in maxColumns" :key="i">
                    <div v-if="i === selectDate" class="">
                        Date
                    </div>
                    <div v-else-if="i === selectRecipient" class="">
                        Recipient
                    </div>
                    <div v-else-if="i === selectAmount" class="">
                        Amount
                    </div>
                    <div v-else-if="i === selectDescription" class="">
                        Description
                    </div>
                    <div v-else>
                        {{ i }}
                    </div>
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(line, index) in arrayData" :key="line">
                <th scope="row">{{ index + 1 }}</th>
                <td v-for="value in maxColumns" :key="value">
                    <div v-if="index + 1 === selectFirst" class="">
                        _{{ line[value - 1] }} 
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
import { computed, ref } from 'vue';

const selectFirst = ref(1)
const selectLast = ref(2)
const selectDate = ref(4)
const selectRecipient = ref(5)
const selectAmount = ref(6)
const selectDescription = ref(7)

const props = defineProps({
    arrayData: Array
})
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
</script>