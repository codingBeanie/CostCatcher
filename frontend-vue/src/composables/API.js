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
        
        console.log(data)
        const payload = JSON.stringify(data)
        console.log(payload)
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