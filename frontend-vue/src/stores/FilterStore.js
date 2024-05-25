import { defineStore } from 'pinia'

export const useFilterStore = defineStore('filter', {
    state: () => ({
        tableau: {
            type: 'monthly',
            from: null,
            to: null,
        },
        bargraph: {
            type: 'monthly',
            from: null,
            to: null,
            filter: 'both',
        },
        piechart: {
            type: 'all',
            from: null,
            to: null,
        },
    }),
}
)   