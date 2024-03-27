<template>
    <v-row justify="center">
        <v-dialog v-model="active" transition="dialog-bottom-transition" fullscreen>

            <v-card color="primary">
                <v-toolbar color="secondary">
                    <v-btn icon @click="close">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>Category Management</v-toolbar-title>
                </v-toolbar>

                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col>
                                <h3>Create category</h3>
                            </v-col>
                            <v-col>
                                <h3>Edit categories</h3>
                            </v-col>
                        </v-row>
                        <v-row>
                        <v-col class="mr-4">
                        <!--Create Section-->
                        <v-row>
                            <v-col cols="">
                                <v-text-field clearable v-model="inputCategory" label="Category Name"></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row cols="" class="">
                            <v-col class="mr-2">
                                <v-row>
                                    <h4 class="mb-4 ml-2 font-weight-thin">Color</h4>
                                </v-row>
                                <v-row class="mb-4">
                                    <v-color-picker v-model="inputColor" hide-inputs></v-color-picker>
                                </v-row>
                            </v-col>
                            <v-col class="ml-2">
                                <v-row>
                                    <h4 class="mb-4 ml-2 font-weight-thin">Preview</h4>
                                </v-row>
                                <v-row class="justify-center">
                                    <v-chip v-if="inputCategory" :color="inputColor" size="large">{{ inputCategory }}</v-chip>
                                    <v-chip v-else color="grey" size="large">Enter a category name above</v-chip>
                                </v-row>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="" class="mt-2 text-start">
                                <v-btn class="" color="accent" @click="createCategory" prependIcon="mdi-plus">Create</v-btn>
                            </v-col>
                        </v-row>
                        </v-col>

                        <v-col class="ml-4">
                        <!--Edit Section-->
                        <v-row>
                            <v-data-table :items="data" :headers="headers">
                                <!--Category-->
                                <template v-slot:item.name="{ item }">
                                <v-chip :color="item.color"> {{ item.name }}</v-chip> 
                                </template>
                                <template v-slot:item.action="{ item }">
                                    <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="editItem(item)">
                                    </v-btn>
                                    <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="deleteItem(item)">
                                    </v-btn>
                                </template>
                            </v-data-table>
                        </v-row>
                        </v-col>
                    </v-row>
                    </v-container>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text="Close" color="sucess" @click="close"></v-btn>
                </v-card-actions>

            </v-card>
        </v-dialog>
    </v-row>
<EditCategory :item="itemEdit"></EditCategory>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useDialogStore } from '../stores/DialogStore.js'
import { useUpdateStore } from '@/stores/UpdateStore.js'
import EditCategory from './EditCategory.vue'
import { API } from '../composables/API.js'

// Operational Variables
const dialogStore = useDialogStore()
const updateStore = useUpdateStore()
const active = ref(false)

// Data
const data = ref([])
const inputCategory = ref('')
const inputColor = ref('#444444')
const itemEdit = ref(null)

// Table Headers
const headers = [
    { title: 'Category', value: 'name', sortable: true },
    { title: 'Action', value: 'action', sortable: false, align: 'center'}
]

// Methods
const loadTable = async () => {
    const rawData = await API('categories', 'GET')
    data.value = rawData.map(item => ({ ...item, action: null }))
}

const close = () => {
    active.value = false
}


const createCategory = async () => {
    const body = {
        name: inputCategory.value,
        color: inputColor.value
    }
    await API('categories', 'POST', body)
    inputCategory.value = ''
    inputColor.value = '#444444'
    loadTable()
}

const editItem = (item) => {
    dialogStore.categoryEdit = !dialogStore.categoryEdit
    itemEdit.value = item
}

const deleteItem = async (item) => {
    await API('categories', 'DELETE', item)
    loadTable()
}

// Lifecycle
onMounted(async () => {
    loadTable()
})

watch(() => dialogStore.category, () => {
    active.value = true
})

watch(() => updateStore.refresh, () => {
    loadTable()
})
</script>