import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        username: null,
        token: null, 
        email: null,
    }),
    actions: {
        logout() {
            this.username = null
            this.token = null
            this.email = null
            localStorage.removeItem('username')
            localStorage.removeItem('token')
            localStorage.removeItem('email')
        },
    }
})