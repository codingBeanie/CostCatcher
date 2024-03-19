import { defineStore } from 'pinia'

export const useUpdateStore = defineStore('update', {
    state: () => ({
        dialogTrigger: false,
        settingsOpen: false,
    }),
    actions: {
        closeDialog() {
            this.dialogTrigger = !this.dialogTrigger
        },
        openSettings() {
            this.settingsOpen = !this.settingsOpen
        }
    }
})