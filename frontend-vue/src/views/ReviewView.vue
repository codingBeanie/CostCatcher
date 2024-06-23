<template>
    <Title title="Review" subtitle="Look through your transactions and edit them if needed" />
    <Divider title="Overview" spacing="8"/>

    <!--Search-->
    <v-text-field
        v-model="search"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        hide-details
        single-line
        class="mt-4"
      ></v-text-field>
    <!--Data Table-->
    <v-data-table :items="data" :headers="header" :search="search" class="mt-4">
        <!--Date-->
        <template v-slot:item.date="{ item }">
            {{ new Date(item.date).toLocaleDateString(locale) }}
        </template>

        <!--Category-->
        <template v-slot:item.categoryName="{ item }">
            <v-chip :color="item.color" link @click="componentStore.openCategoryEdit(item.category)">{{ item.categoryName }}</v-chip>
        </template>

        <!--Amount-->
        <template v-slot:item.amount="{ item }">
            <v-row class="justify-end mr-12">
                <div v-if="item.amount < 0" class="text-error">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</div>
                <div v-if="item.amount >= 0" class="text-success">{{ parseFloat(item.amount / 100).toLocaleString(locale, {minimumFractionDigits: 2})}} {{ currency }}</div>
            </v-row>
        </template>

        <!--Action-->
        <template v-slot:item.action="{ item }">
            <v-row class="justify-center">
                <v-tooltip v-if="item.overruled" text="Category is locked. Click to unlock.">
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" density="compact" icon="mdi-lock" @click="unlock(item)" ></v-btn>
                    </template>
                </v-tooltip>
                <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="componentStore.openTransactionEdit(item.id)"></v-btn>  
                <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="componentStore.openDelete('transactions', item.id, `${item.recipient} | ${item.description}`)">
                </v-btn>                   
            </v-row>
        </template>
    </v-data-table>

</template>

<script setup>
import { onMounted, ref} from 'vue'
import { useUserStore } from '../stores/UserStore.js'
import { useComponentStore } from '../stores/ComponentStore.js'
import Title from '../components/Title.vue'
import Divider from '../components/Divider.vue'
import { API } from '../composables/API.js'
import { watch } from 'vue'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const userStore = useUserStore()
const componentStore = useComponentStore()
const data = ref([])
const header = [
    { title: 'Date', value: 'date' },
    { title: 'Recipient', value: 'recipient'},
    { title: 'Description', value: 'description' },
    { title: 'Category', value: 'categoryName'},
    { title: 'Amount', value: 'amount' },
    { title: 'Actions', value: 'action', sortable: false },
]
const search = ref('')
////////////////////////////////////////////////////////////////
// Methods
const load = async () => {
    data.value = await API('transactions', 'GET')
}

const unlock = async (item) => {
    item.overruled = false
    item.amount = item.amount / 100
    await API('transactions', 'PUT', item)
    load()
}

////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
onMounted(() => {
    load()
})

watch([() => componentStore.app.refresh], () => {
    load()
})
</script>