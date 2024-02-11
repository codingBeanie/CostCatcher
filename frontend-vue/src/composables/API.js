export async function getData(type) { 
    try {
        const url = `http://127.0.0.1:8000/api/${type}`
        const response = await fetch(url)
        const data = await response.json()
        return data
        
    } catch (error) {
        return error
    }
    
}