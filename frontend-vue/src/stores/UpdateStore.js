import { defineStore } from 'pinia'

export const useUpdateStore = defineStore('update', {
    state: () => ({
        fired: false
    }),
    actions: {
        fire() {
            this.fired = !this.fired
        }
    }
})