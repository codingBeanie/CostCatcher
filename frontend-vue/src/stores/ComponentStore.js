import { defineStore } from 'pinia'

export const useComponentStore = defineStore('component', {
    state: () => ({
        app: {
            refresh: false,
        },
        register: {
            trigger: false,
        },
        login: {
            trigger: false,
        },
        deleteAccount: {
            trigger: false,
        },
        updatePassword: {
            trigger: false,
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
        openRegister() {
            this.register.trigger = !this.register.trigger
        },
        openLogin() {
            this.login.trigger = !this.login.trigger
        },
        openDeleteAccount() {
            this.deleteAccount.trigger = !this.deleteAccount.trigger
        },
        openUpdatePassword() {
            this.updatePassword.trigger = !this.updatePassword.trigger
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