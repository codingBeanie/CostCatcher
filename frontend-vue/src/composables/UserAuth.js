import { useUserStore } from "../stores/UserStore"
import { useAlertStore } from "../stores/AlertStore"
import { storeUserdata } from "./LocalStorage"

export async function registerUser(username, password, email) {
    let urlBase = process.env.VUE_APP_API_URL
    const url = `${urlBase}/auth/register/`
    const userStore = useUserStore()
    const alertStore = useAlertStore()
    const payload = { username: username, password: password, email: email}
    
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
            userStore.email = payload.email
            storeUserdata(payload.username, response, payload.email)
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
    let urlBase = process.env.VUE_APP_API_URL
    const url = `${urlBase}/auth/login/`
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
            userStore.token = response.token
            userStore.email = response.email
            storeUserdata(payload.username, response.token, response.email)
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
    let urlBase = process.env.VUE_APP_API_URL
    const url = `${urlBase}/auth/deleteUser/`
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
    let urlBase = process.env.VUE_APP_API_URL
    const url = `${urlBase}/auth/updatePassword/`
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

export async function setNewPassword(password, token) {
    let urlBase = process.env.VUE_APP_API_URL
    const url = `${urlBase}/auth/setnewpassword/`
    const alertStore = useAlertStore()
    try {
        const request = await fetch(url, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
            body: JSON.stringify({ 'password': password})
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

export async function passwordReset(username) {
    let urlBase = process.env.VUE_APP_API_URL
    const url = `${urlBase}/auth/passwordReset/`
    const alertStore = useAlertStore()
    try {
        const request = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'username': username })
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

export async function updateEmail(email) {
    let urlBase = process.env.VUE_APP_API_URL
    const url = `${urlBase}/auth/updateEmail/`
    const userStore = useUserStore()
    const alertStore = useAlertStore()
    const username = userStore.username
    const token = userStore.token
    try {
        const request = await fetch(url, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
            body: JSON.stringify({ 'email': email })
        })
        const response = await request.json()
        if (request.status !== 200) {
            alertStore.showAlert('Error', response, 'error', 5000)
            return false
        }
        else {
            alertStore.showAlert('Success', response, 'success', 5000)
            userStore.email = email
            return true
        }
    }
    catch (error) {
        alertStore.showAlert('Error', error, 'error', 5000)
        return false
    }
}