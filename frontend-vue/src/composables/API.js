import { useMainStore } from "../stores/MainStore"


export async function API(resource, method, payload=null) {
    const mainStore = useMainStore()
    let url = null
    try {
        // If there is a query string in the resource, do not add a trailing slash
        if (resource.includes('?')) {
            url = `http://127.0.0.1:8000/api/${resource}`
        }
        else {
            url = `http://127.0.0.1:8000/api/${resource}/`
        }
        let request = null

        if (method === 'GET') {
            request = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
            })
        }
        else {
            request = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })  
        }

        const response = await request.json()

        // SUCESS
        if (request.status == 200) {
            if (method != 'GET') {
                mainStore.showAlert('Success', response, 'success', 5000)
            }
            else {
                return response
            }
        }
        // ERROR
        else {
            mainStore.showAlert('Error', response, 'error', 5000)
            return []
        }

    }
    catch (error) {
        console.log(error)
        mainStore.showAlert('Error', error, 'error', 5000)
    }
}
