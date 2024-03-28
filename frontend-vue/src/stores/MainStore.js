import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
    state: () => ({
        app: {
            refresh: false
        },
        alert: {
            show: false,
            title: 'Error',
            message: 'Test Message',
            type: 'error'
        },
        settings: {
            trigger: false,
        },
        delete: {
            trigger: false,
            title: null,
            itemID: null,
            resource: null
        }
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
        },
        openSettings() {
            this.settings.trigger = !this.settings.trigger
        },
        refreshApp() {
            this.app.refresh = !this.app.refresh
        },
        openDelete(resource, itemID, title) {
            this.delete.trigger = !this.delete.trigger
            this.delete.title = title
            this.delete.itemID = itemID
            this.delete.resource = resource
        },
    }
})