import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        username: null,
        token: null, 
    }),
    actions: {
        logout() {
            this.username = null
            this.token = null
            localStorage.removeItem('username')
            localStorage.removeItem('token')
        }
    }
})