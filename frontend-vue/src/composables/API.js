import { useAlertStore } from "../stores/AlertStore"
import { useUserStore } from "../stores/UserStore"


export async function API(resource, method, payload=null) {
    const alertStore = useAlertStore()
    const userStore = useUserStore()
    const token = userStore.token
    let url = null
    if (token == null) {
        return []
    }
   // console.log('API', resource, method, payload, token)
    try {
        // If there is a query string in the resource, do not add a trailing slash
        if (resource.includes('?')) {
            url = `https://costcatcher.cbeanie.com/api/${resource}`
        }
        else {
            url = `https://costcatcher.cbeanie.com/api/${resource}/`
        }
        let request = null

        if (method === 'GET') {
            request = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
            })
        }
        else {
            request = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
                body: JSON.stringify(payload)
            })  
        }

        const response = await request.json()

        // SUCESS
        if (request.status == 200) {
            if (method != 'GET') {
                alertStore.showAlert('Success', response, 'success', 5000)
            }
            else {
                return response
            }
        }
        // ERROR
        else {
            alertStore.showAlert('Error', response, 'error', 5000)
            return []
        }

    }
    catch (error) {
        console.log(error)
        alertStore.showAlert('Error', error, 'error', 5000)
    }
}
