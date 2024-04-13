import { useUserStore } from '../stores/UserStore'

export function storeUserdata(username, token) {
    localStorage.setItem('username', username)
    localStorage.setItem('token', token)
}

export function getUserdata() {
    const username = localStorage.getItem('username')
    const token = localStorage.getItem('token')
    if (username && token) {
        const userStore = useUserStore()
        userStore.username = username
        userStore.token = token
     }
}