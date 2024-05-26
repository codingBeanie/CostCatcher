<template>
    <v-row justify="center">
        <v-dialog v-model="active" transition="dialog-bottom-transition" fullscreen>

            <v-card color="primary">
                <v-toolbar color="secondary">
                    <v-btn icon @click="close">
                        <v-icon>mdi-arrow-collapse-left</v-icon>
                    </v-btn>
                    <v-toolbar-title>Category Management</v-toolbar-title>
                </v-toolbar>

                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col>
                                <p class="text-h5 font-weight-bold text-secondary">Create new category</p>
                            </v-col>
                            <v-col>
                                <p class="text-h5 font-weight-bold text-secondary">Edit categories</p>
                            </v-col>
                        </v-row>
                        <v-row>
                        <v-col class="mr-4">
                        <!--Create Section-->
                        <v-row>
                            <v-col cols="8">
                                <v-text-field clearable v-model="inputCategory" label="Category Name"></v-text-field>
                            </v-col>
                            <v-col cols="2" class="mt-2 text-center">
                                    <v-chip v-if="inputCategory" :color="inputColor" size="large">{{ inputCategory }}</v-chip>
                                    <v-chip v-else color="grey" size="large">Preview</v-chip>
                            </v-col>
                            <v-col cols="2" class="mt-2">
                                <v-btn class="" color="accent" @click="createCategory" prependIcon="mdi-plus">Create</v-btn>
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
                            <v-col class="">
                                <v-row class="">

                                </v-row>
                            </v-col>
                        </v-row>

                        </v-col>

                        <v-col class="ml-4">
                        <!--Edit Section-->
                        <v-row>
                            <v-data-table :items="data" :headers="headers">
                                <!--Category-->
                                <template v-slot:item.name="{ item }">
                                <v-chip :color="item.color" link @click="componentStore.openCategoryEdit(item.id)"> {{ item.name }}</v-chip> 
                                </template>
                                <template v-slot:item.action="{ item }">
                                    <v-btn density="compact" icon="mdi-pencil" class="ml-3" @click="componentStore.openCategoryEdit(item.id)">
                                    </v-btn>
                                    <v-btn density="compact" icon="mdi-delete" class="ml-3" @click="componentStore.openDelete('categories', item.id, item.name)">
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
                    <v-btn text="Close" color="accent" variant="tonal" @click="close"></v-btn>
                </v-card-actions>

            </v-card>
        </v-dialog>
    </v-row>

</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { API } from '../composables/API.js'

////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const active = ref(false)

// Data
const data = ref([])
const inputCategory = ref('')
const inputColor = ref('#444444')
const itemEdit = ref('0')

// Table Headers
const headers = [
    { title: 'Category', value: 'name', sortable: true },
    { title: 'Action', value: 'action', sortable: false, align: 'center'}
]

////////////////////////////////////////////////////////////////
// Load Data
////////////////////////////////////////////////////////////////
const loadTable = async () => {
    const originalData = await API('categories', 'GET')
    data.value = originalData.map(item => ({ ...item, action: null }))
}

////////////////////////////////////////////////////////////////
// CRUD Operations
////////////////////////////////////////////////////////////////
const createCategory = async () => {
    const body = {
        name: inputCategory.value,
        color: inputColor.value
    }
    await API('categories', 'POST', body)
    inputCategory.value = ''
    inputColor.value = '#444444'
    load()
}

////////////////////////////////////////////////////////////////
// Actions
////////////////////////////////////////////////////////////////
const close = () => {
    componentStore.refreshApp()
    active.value = false
}
////////////////////////////////////////////////////////////////
// Lifecycle Hooks
////////////////////////////////////////////////////////////////
const load = () => {
    loadTable()
}

onMounted(async () => {
    load()
})

watch(() => componentStore.categories.trigger, () => {
    load()
    active.value = true
})

watch(() => componentStore.app.refresh, () => {
    load()
})

watch(() => userStore.username, () => {
    load()
})
</script>