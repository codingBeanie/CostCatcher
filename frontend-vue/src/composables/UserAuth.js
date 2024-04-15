import { useUserStore } from "../stores/UserStore"
import { useAlertStore } from "../stores/AlertStore"
import { storeUserdata } from "./LocalStorage"

export async function registerUser(username, password) {
    const url = `http://localhost:8000/auth/register/`
    const userStore = useUserStore()
    const alertStore = useAlertStore()
    const payload = { username: username, password: password }
    
    try {
        const request = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        const response = await request.json()

        if (request.status === 200) {
            userStore.username = payload.username
            userStore.token = response
            storeUserdata(payload.username, response)
            return true
        }
        else {
            return false
        }
    }
    catch (error) {
        alertStore.showAlert('Error', error, 'error', 5000)
        return false
    }
}

export async function loginUser(username, password) {
    const url = `http://localhost:8000/auth/login/`
    const userStore = useUserStore()
    const alertStore = useAlertStore()
    const payload = { username: username, password: password }
    
    try {
        const request = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        const response = await request.json()

        if (request.status === 200) {
            userStore.username = payload.username
            userStore.token = response
            storeUserdata(payload.username, response)
            return true
        }
        else {
            return false
        }
    }
    catch (error) {
        alertStore.showAlert('Error', error, 'error', 5000)
        return false
    }
}

export async function deleteUser() {
    const url = `http://localhost:8000/auth/deleteUser/`
    const userStore = useUserStore()
    const alertStore = useAlertStore()
    const username = userStore.username
    const token = userStore.token
    try {
        const request = await fetch(url, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
        })
        const response = await request.json()
        if (request.status !== 200) {
            alertStore.showAlert('Error', response, 'error', 5000)
            return false
        }
        else {
            alertStore.showAlert('Success', response , 'success', 5000)
            return true
        }
    }
    catch (error) {
        alertStore.showAlert('Error', error, 'error', 5000)
        return false
    }
}

export async function updatePassword(currentPassword, newPassword) {
    const url = `http://localhost:8000/auth/updatePassword/`
    const userStore = useUserStore()
    const alertStore = useAlertStore()
    const username = userStore.username
    const token = userStore.token
    try {
        const request = await fetch(url, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
            body: JSON.stringify({ 'currentPassword': currentPassword, 'newPassword': newPassword })
        })
        const response = await request.json()
        if (request.status !== 200) {
            alertStore.showAlert('Error', response, 'error', 5000)
            return false
        }
        else {
            alertStore.showAlert('Success', response, 'success', 5000)
            return true
        }
    }
    catch (error) {
        alertStore.showAlert('Error', error, 'error', 5000)
        return false
    }
}