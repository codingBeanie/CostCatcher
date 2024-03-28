import { defineStore } from 'pinia'

export const useDialogStore = defineStore('dialog', {
    state: () => ({
        settings: {
            trigger: false,
        },
        delete: {
            trigger: false,
            title: null,
            itemID: null,
            resource: null
        }
    })
})