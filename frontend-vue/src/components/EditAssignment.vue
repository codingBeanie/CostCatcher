<template>
  <v-dialog v-model="active" max-width="600px">

    <template v-slot:activator="{ props: activatorProps }">
      <v-btn v-bind="activatorProps" icon="mdi-pencil" density="compact">
      </v-btn>
    </template>

    <v-card>
        <v-card-title>
            <h2>Edit Assignment</h2>
        </v-card-title>

        <v-card-text>
            <v-container>
                <v-row>
                    <v-col>
                        <v-text-field v-model="newKeyword" label="Keyword"></v-text-field>
                    </v-col>
                    <v-col>
                        <v-select v-model="newCategory" label="Category" :items="categories"></v-select>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-checkbox v-model="newRecipient" label="Recipient"/>
                    </v-col>
                    <v-col>
                        <v-checkbox v-model="newDescription" label="Description"/>
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
import { ref, onMounted } from 'vue'
import { updateData } from '../composables/API.js'
import { useUpdateStore } from '../stores/UpdateStore'
import { getData } from '../composables/API.js'

const active = ref(false)
const props = defineProps({
    keyword: String,
    category: String,
    recipient: Boolean,
    description: Boolean
})
const newCategory = ref(props.category)
const newKeyword = ref(props.keyword)
const newRecipient = ref(props.recipient)
const newDescription = ref(props.description)
const updateStore = useUpdateStore()

const categories = ref([])


const close = () => {
    active.value = false
}

const save = async () => {
    const data = {
        oldKeyword: props.keyword,
        newKeyword: newKeyword.value,
        category: newCategory.value,
        recipient: newRecipient.value,
        description: newDescription.value
    }
    await updateData(data, 'assignments') 
    updateStore.closeAssignment()
    active.value = false
}

onMounted(async () => {
    const rawData = await getData('categories')
    categories.value = rawData.map(item => item.name)
})

</script>../stores/UpdateStore.js
