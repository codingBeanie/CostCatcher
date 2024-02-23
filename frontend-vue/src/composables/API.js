export async function getData(type) { 
    try {
        const url = `http://127.0.0.1:8000/api/${type}`
        const response = await fetch(url)
        const data = await response.json()
        return data
        
    } catch (error) {
       console.log(error) 
    }
    
}

export async function postData(data, type) {
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
    }
    catch (error) {
        console.log(error) 
    }
}

export async function deleteData(id, type) {
    try {
        const url = `http://127.0.0.1:8000/api/${type}/`
        const call = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({id: id})
        })
    }
    catch (error) {
        console.log(error) 
    }
}