import { useAlertStore } from "../stores/AlertStore"


export async function API(resource, method, payload=null) {
    const alertStore = useAlertStore()
    try {
        const url = `http://127.0.0.1:8000/api/${resource}/`
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
