import { defineStore } from 'pinia'

export const useFilterStore = defineStore('filter', {
    state: () => ({
        tableau: {
            type: 'monthly',
            categories: null,
            from: null,
            to: null,
            statistics: false,
            ignoreZero: false,
        },
        bargraph: {
            type: 'monthly',
            from: null,
            to: null,
            filter: 'both',
        },
        piechart: {
            type: 'single',
            from: null,
            to: null,
            filter: 'expense',
        },
        import: {
            mode: 'csv'
        },
    }),
}
)   