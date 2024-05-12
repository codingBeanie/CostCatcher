import { defineStore } from 'pinia'

export const useComponentStore = defineStore('component', {
    state: () => ({
        app: {
            refresh: false,
            version: '0.9.0',
            date: '2024-04-13',
            screen: 'dektop'
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
        updateEmail: {
            trigger: false,
        },
        resetPassword: {
            trigger: false,
        },
        newPassword: {
            trigger: false,
        },
        dataProtection: {
            trigger: false,
        },
        tutorial: {
            trigger: false,
            type: null
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
        openUpdateEmail() {
            this.updateEmail.trigger = !this.updateEmail.trigger
        },
        openPasswordReset() {
            this.resetPassword.trigger = !this.resetPassword.trigger
        },
        openNewPassword() {
            this.newPassword.trigger = !this.newPassword.trigger
        },
        openDataProtection() {
            this.dataProtection.trigger = !this.dataProtection.trigger
        },
        openTutorial(type) {
            this.tutorial.trigger = !this.tutorial.trigger
            this.tutorial.type = type
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