import { useAlertStore } from "../stores/AlertStore"

export async function getData(type) { 
    const alertStore = useAlertStore()
    try {
        const url = `http://127.0.0.1:8000/api/${type}`
        const response = await fetch(url)
        const data = await response.json()
        return data
        
    } catch (error) {
        alertStore.showAlert('Error', 'Could not fetch data. Database is probably not available.', 'error', 5000)
    }
    
}

export async function postData(data, type) {
    const alertStore = useAlertStore()
    try {
        const url = `http://127.0.0.1:8000/api/${type}/`
        const payload = JSON.stringify(data)
        const call = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload
        })
        const response = await call.json()
        if (call.status == 200) {
            alertStore.showAlert('Success', 'Data uploaded successfully.', 'success', 5000)
        } else {
            alertStore.showAlert('Error', `Could not upload data. ${JSON.stringify(response)}`, 'error', 5000)
        }
    }
    catch (error) {
        console.log(error) 
    }
}

export async function updateData(data, type) {
    const alertStore = useAlertStore()
    try {
        const url = `http://127.0.0.1:8000/api/${type}/`
        const payload = JSON.stringify(data)
        const call = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload   
        })
        const response = await call.json()
        if (call.status == 201) {
            alertStore.showAlert('Success', 'Data updated successfully.', 'success', 5000)
        } else {
            alertStore.showAlert('Error', `Could not update data. ${JSON.stringify(response)}`, 'error', 5000)
        }
    }
    catch (error) {
        alertStore.showAlert('Error', 'Could not update data. Database is unavailable', 'error', 5000)
    }
}

export async function deleteData(id, type) {
    const alertStore = useAlertStore()
    try {
        const url = `http://127.0.0.1:8000/api/${type}/`
        const call = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({id: id})
        })
        const response = await call.json()
        if (call.status == 200) {
            alertStore.showAlert('Success', 'Data deleted successfully.', 'success', 5000)
        } else {
            alertStore.showAlert('Error', `Could not delete data. ${JSON.stringify(response)}`, 'error', 5000)
        }
    }
    catch (error) {
        console.log(error) 
    }
}