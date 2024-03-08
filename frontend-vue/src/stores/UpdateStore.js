import { defineStore } from 'pinia'

export const useUpdateStore = defineStore('update', {
    state: () => ({
        dialogTrigger: false,
    }),
    actions: {
        closeDialog() {
            this.dialogTrigger = !this.dialogTrigger
        }
    }
})