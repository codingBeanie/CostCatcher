<template>
  <v-dialog v-model="active" max-width="600px">

    <v-card>
        <v-card-title>
            <DialogTitle title="Edit Transaction"></DialogTitle>    
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field label="Recipient" v-model="recipient"></v-text-field>
                    </v-col>
                </v-row>
                
                <v-row>
                    <v-col>
                        <v-text-field label="Description" v-model="description"></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-text-field type="Date" label="Date" v-model="date"></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field type="Number" label="Amount" v-model="amount"></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-select
                            v-model="category"
                            :items="categories"
                            item-title="name"
                            item-value="id"
                            label="Category"
                        ></v-select>
                        <h5 class="font-weight-thin">If you change the category, the new category will be locked and will not be changed automatically by the rules of the categorization!</h5>
                    
                    </v-col>
                </v-row>

            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="sucess" @click="close"></v-btn>
            <v-btn text="Save" variant="tonal" color="accent" @click="save"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref } from 'vue'
import { API } from '../composables/API.js'
import { useComponentStore } from '../stores/ComponentStore.js'
import { watch } from 'vue';
import DialogTitle from './DialogTitle.vue'
////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const active = ref(false)

// Inputs
const id = ref('')
const date = ref('')
const recipient = ref('')
const description = ref('')
const amount = ref('')
const category = ref('')
const categories = ref([])

////////////////////////////////////////////////////////////
// Load Functions
////////////////////////////////////////////////////////////
const loadFields = async () => {
    const transaction = await API(`transactions/?id=${id.value}`, 'GET')
    date.value = transaction[0].date
    recipient.value = transaction[0].recipient
    description.value = transaction[0].description
    amount.value = transaction[0].amount / 100
    category.value = transaction[0].category
}

const loadCategories = async () => {
    categories.value = await API('categories', 'GET')
}

////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////
const close = () => {
    active.value = false
}

const save = async () => {
    const data = {
        id: id.value,
        date: date.value,
        recipient: recipient.value,
        description: description.value,
        amount: amount.value,
        category: category.value
    }
    await API('transactions', 'PUT', data) 
    componentStore.refreshApp()
    active.value = false
}

////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////
const load = async () => {
    id.value = componentStore.transactionEdit.id
    loadFields()
    loadCategories()
}

watch(() => componentStore.transactionEdit.trigger, () => {
    load()
    active.value = true
})

</script>
