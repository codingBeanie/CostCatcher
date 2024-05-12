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