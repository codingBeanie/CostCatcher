import { defineStore } from 'pinia'

export const useUpdateStore = defineStore('update', {
    state: () => ({
        schemaClosed: false,
        editCategoryClosed: false,
        editAssignmentClosed: false,
        editTransactionClosed: false,
    }),
    actions: {
        closeSchema() {
            this.schemaClosed = !this.schemaClosed
        },
        closeEditCategory() {
            this.editCategoryClosed = !this.editCategoryClosed
        },
        closeAssignment() {
            this.editAssignmentClosed = !this.editAssignmentClosed
        },
        closeTransaction() {
            this.editTransactionClosed = !this.editTransactionClosed
        }
    }
})