import { defineStore } from 'pinia'

export const useUpdateStore = defineStore('update', {
    state: () => ({
        schemaClosed: false,
        editCategoryClosed: false,
    }),
    actions: {
        closeSchema() {
            this.schemaClosed = !this.schemaClosed
        },
        closeEditCategory() {
            this.editCategoryClosed = !this.editCategoryClosed
        }
    }
})