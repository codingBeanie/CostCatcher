import { defineStore } from 'pinia'

export const useFilterStore = defineStore('filter', {
    state: () => ({
        tableau: {
            type: 'monthly',
            from: null,
            to: null,
        }
    }),
}
)   