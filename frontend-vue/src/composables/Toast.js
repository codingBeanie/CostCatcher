import { createApp, h } from 'vue';
import Toast from '../components/Toast.vue'

export function toast(content) {
    const container = document.createElement('div')
    container.id = "toast"
    document.body.appendChild(container)

    const app = createApp({
        render() {
            return h(Toast, { content })
        }
    })
    app.mount(container)

    setTimeout(() => {
        app.unmount(container)
        document.body.removeChild(container)
    }, 3000)

}