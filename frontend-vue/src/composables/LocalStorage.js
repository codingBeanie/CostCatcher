import { useUserStore } from '../stores/UserStore'

export function storeUserdata(username, token, email) {
    localStorage.setItem('username', username)
    localStorage.setItem('token', token)
    localStorage.setItem('email', email)
}

export function getUserdata() {
    const username = localStorage.getItem('username')
    const token = localStorage.getItem('token')
    const email = localStorage.getItem('email')
    if (username && token) {
        const userStore = useUserStore()
        userStore.username = username
        userStore.token = token
        userStore.email = email
     }
}

export function getTutorialStatus() {
    const userStore = useUserStore()

    const showTutorialImport = localStorage.getItem('showTutorialImport')
    const showTutorialCategorization = localStorage.getItem('showTutorialCategorization')
    const showTutorialStatistics = localStorage.getItem('showTutorialStatistics')
    const showTutorialReview = localStorage.getItem('showTutorialReview')

    if(showTutorialImport != null) {
        userStore.showTutorialImport = showTutorialImport
    }
    if(showTutorialCategorization != null) {
        userStore.showTutorialCategorization = showTutorialCategorization
    }
    if(showTutorialStatistics != null) {
        userStore.showTutorialStatistics = showTutorialStatistics
    }
    if(showTutorialReview != null) {
        userStore.showTutorialReview = showTutorialReview
    }
}