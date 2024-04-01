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
            tab: 'general',
        },
        delete: {
            trigger: false,
            title: null,
            itemID: null,
            resource: null
        },
        categories: {
            trigger: false,
        },
        categoryEdit: {
            trigger: false,
            id: null,
        },
        assignmentEdit: {
            trigger: false,
            id: null,
        },
        transactionEdit: {
            trigger: false,
            id: null,
        },
        review: {
            trigger: false,
            period: null,
            category: null
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
        openSettings(tab) {
            this.settings.trigger = !this.settings.trigger
            this.settings.tab = tab
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
        openCategories() {
            this.categories.trigger = !this.categories.trigger
        },
        openCategoryEdit(id) {
            this.categoryEdit.trigger = !this.categoryEdit.trigger
            this.categoryEdit.id = id
        },
        openAssignmentEdit(id) {
            this.assignmentEdit.trigger = !this.assignmentEdit.trigger
            this.assignmentEdit.id = id
        },
        openTransactionEdit(id) {
            this.transactionEdit.trigger = !this.transactionEdit.trigger
            this.transactionEdit.id = id
        },
        openReview(category, period) {
            this.review.trigger = !this.review.trigger
            this.review.period = period
            this.review.category = category
        }
    }
})