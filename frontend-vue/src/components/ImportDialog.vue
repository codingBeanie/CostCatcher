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
                                    <v-text-field label="CSV delimeter" v-model="delimiter"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field label="Thousands seperator" v-model="thousandsSeparator"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field label="Decimal seperator" v-model="decimalSeparator"></v-text-field>
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
import { onMounted } from 'vue';
import { ref } from 'vue'
import { getData, updateData } from '../composables/API.js'

const active = ref(false)

const rowFirst = ref(1)
const rowLast = ref(0)

const colDate = ref(1)
const colRecipient = ref(2)
const colDescription = ref(3)
const colAmount = ref(4)

const delimiter = ref(';')
const thousandsSeparator = ref('.')
const decimalSeparator = ref(',')

const close = () => {
    active.value = false
}
const save = () => {
    const data = {
        rowFirst: rowFirst.value,
        rowLast: rowLast.value,
        colDate: colDate.value,
        colRecipient: colRecipient.value,
        colDescription: colDescription.value,
        colAmount: colAmount.value,
        delimiter: delimiter.value,
        thousandsSeparator: thousandsSeparator.value,
        decimalSeparator: decimalSeparator.value
    }
    updateData(data, 'schema')
    active.value = false
}

onMounted(async () => {
    const schema = await getData('schema')
    console.log(schema[0].delimeter)
    rowFirst.value = schema[0].rowFirst
    rowLast.value = schema[0].rowLast
    colDate.value = schema[0].colDate
    colRecipient.value = schema[0].colRecipient
    colDescription.value = schema[0].colDescription
    colAmount.value = schema[0].colAmount
    delimiter.value = schema[0].delimiter
    thousandsSeparator.value = schema[0].thousandsSeparator
    decimalSeparator.value = schema[0].decimalSeparator

     })

</script>
