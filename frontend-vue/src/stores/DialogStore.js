import { defineStore } from 'pinia'

export const useDialogStore = defineStore('dialog', {
    state: () => ({
        settings: false,
        delete: false, 
        dialog: false
    })
})