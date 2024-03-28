import { useMainStore } from "../stores/MainStore"


export async function API(resource, method, payload=null) {
    const mainStore = useMainStore()
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
