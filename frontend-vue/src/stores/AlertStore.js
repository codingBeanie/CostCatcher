import { defineStore } from 'pinia'

export const useAlertStore = defineStore('alert', {
    state: () => ({
        alert: {
            show: false,
            title: 'Error',
            message: 'Test Message',
            type: 'error'
        },
        appState: 'normal'
    }),
    actions: {
        showAlert(title, message, type, timeout) {
            this.alert.show = true
            this.alert.title = title
            this.alert.message = message
            this.alert.type = type

            setTimeout(() => {
                this.alert.show = false
            }, timeout)
        }
    }
})