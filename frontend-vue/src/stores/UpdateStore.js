import { defineStore } from 'pinia'

export const useUpdateStore = defineStore('update', {
    state: () => ({
       refresh: false, 
    }),
})