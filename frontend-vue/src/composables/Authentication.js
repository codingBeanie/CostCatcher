import { useMainStore } from "../stores/MainStore"
import { useUserStore } from "../stores/UserStore"
import { storeUserdata } from "./LocalStorage"

export async function Authentication(type, payload) {
    const userStore = useUserStore()
    const mainStore = useMainStore()
    
    try {
        const url = `http://localhost:8000/auth/${type}/`
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
        mainStore.showAlert('Error', error, 'error', 5000)
        return false
    }
}


