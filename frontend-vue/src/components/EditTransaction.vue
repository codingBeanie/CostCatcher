<template>
  <v-dialog v-model="active" max-width="600px">

    <template v-slot:activator="{ props: activatorProps }">
      <v-btn v-bind="activatorProps" icon="mdi-pencil" density="compact">
      </v-btn>
    </template>

    <v-card>
        <v-card-title>
            <h2>Edit Transaction</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field label="Recipient" v-model="newRecipient"></v-text-field>
                    </v-col>
                </v-row>
                
                <v-row>
                    <v-col>
                        <v-text-field label="Description" v-model="newDescription"></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-text-field type="Date" label="Date" v-model="newDate"></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field type="Number" label="Amount" v-model="newAmount"></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-select
                            v-model="newCategory"
                            :items="props.categories"
                            label="Category"
                        ></v-select>
                    </v-col>
                </v-row>

            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Cancel" color="sucess" @click="close"></v-btn>
            <v-btn text="Save" color="sucess" @click="save"></v-btn>
        </v-card-actions>
    </v-card>
        
  </v-dialog> 
</template>

<script setup>
import { ref } from 'vue'
import { API } from '../composables/API.js'
import { useMainStore } from '../stores/MainStore.js'

const updateStore = useMainStore()

const active = ref(false)
const props = defineProps({
    id: Number,
    date: String,
    recipient: String,
    description: String,
    amount: Number,
    category: String,
    categories: Array
})
const newDate = ref(props.date)
const newRecipient = ref(props.recipient)
const newDescription = ref(props.description)
const newAmount = ref(props.amount)
const newCategory = ref(props.category)

const close = () => {
    active.value = false
}

const save = async () => {
    const data = {
        id: props.id,
        date: newDate.value,
        recipient: newRecipient.value,
        description: newDescription.value,
        amount: newAmount.value,
        category: newCategory.value
    }
    await API('transactions', 'PUT', data) 
    updateStore.closeDialog()
    active.value = false
}

</script>
