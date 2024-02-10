<template>
    <div class="d-flex flex-column align-items-center">
        <h1>Import</h1>
        <h4>Import your CSV-File here</h4>
        {{ data }}
    </div>
</template>

<script>
import { ref } from 'vue'
export default {
    name: 'ImportView',
    setup() {

        // API Call (Files)
        const data = ref(null)
        const fetchData = async () => { 
            const response = await fetch('http://127.0.0.1:8000/api/files/')
            const responseData = await response.json()
            data.value = responseData
        }
        fetchData()
        return { data }
    }
   
}
</script>