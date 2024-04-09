import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {
            id: null,
            name: null,
            email: null,
            currency: null,
            locale: null,
        }
    })
})