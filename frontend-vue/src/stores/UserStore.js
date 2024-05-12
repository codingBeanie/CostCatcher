import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        username: null,
        token: null, 
        email: null,
        showTutorialImport: true,
        showTutorialCategorization: true,
        showTutorialStatistics: true,
        showTutorialReview: true,
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
        setTutorialStatus(type, value) {
            if(type === 'import') {
                this.showTutorialImport = value
            }
            if(type === 'categorization') {
                this.showTutorialCategorization = value
            }
            if(type === 'statistics') {
                this.showTutorialStatistics = value
            }
            if(type === 'review') {
                this.showTutorialReview = value
            }
            localStorage.setItem('showTutorialImport', this.showTutorialImport)
            localStorage.setItem('showTutorialCategorization', this.showTutorialCategorization)
            localStorage.setItem('showTutorialStatistics', this.showTutorialStatistics)
            localStorage.setItem('showTutorialReview', this.showTutorialReview)
        }
        
    }
})