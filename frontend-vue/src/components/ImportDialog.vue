<template>
    <v-row justify="center">
        <v-dialog v-model="active" max-width="600px">
            <template v-slot:activator="{ props }">
                <v-btn v-bind="props" prepend-icon="mdi-cog" color="accent" class="mt-3">Import Schema</v-btn>
            </template>

            <template v-slot:default="{ active }">
                <v-card>
                    <v-card-title>
                        <h2>Manage import schema</h2>
                    </v-card-title>

                    <v-card-text>
                        <v-container>
                            <v-row>
                                <h4>Row settings</h4>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field label="Ignore # first rows" v-model="rowFirst" type="number"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field label="Ignore # last rows" v-model="rowLast" type="number"></v-text-field>
                                </v-col>
                            </v-row>

                            <v-row>
                                <h4>Column settings</h4>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field label="Column # Date" v-model="colDate" type="number"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field label="Column # Recipient" v-model="colRecipient" type="number"></v-text-field>
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-col>
                                    <v-text-field label="Column # Description" v-model="colDescription" type="number"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field label="Column # Amount" v-model="colAmount" type="number"></v-text-field>
                                </v-col>
                            </v-row>

                            <v-row>
                                <h4>Data settings</h4>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field label="Delimeter" v-model="delimeter"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-select label="Value type" v-model="valueType" :items="valueTypes"></v-select>
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
            </template>
        </v-dialog>
    </v-row>

</template>

<script setup>
import { ref } from 'vue'
const active = ref(false)

const rowFirst = ref(1)
const rowLast = ref(0)

const colDate = ref(1)
const colRecipient = ref(2)
const colDescription = ref(3)
const colAmount = ref(4)

const delimeter = ref(';')
const valueType = ref('European (#.##0,00)')

const valueTypes = [
    'European (#.##0,00)',
    'American (#,##0.00)'
]
const close = () => {
    active.value = false
}
const save = () => {
    active.value = false
}

</script>
