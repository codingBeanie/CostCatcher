import { createApp, h } from 'vue';
import Modal from '../components/Modal.vue'

export function modal(title, content, ok, cancel) {
    setTexts(title, content)
    toggleVisibility()

    return new Promise((resolve, reject) => {
        // setup interactivity
        const okButton = document.getElementById("okButton")
        const cancelButton = document.getElementById("cancelButton")

        const okHandler = () => { 
            toggleVisibility()
            okButton.removeEventListener("click", okHandler)
            cancelButton.removeEventListener("click", cancelHandler)
            resolve(true)
        }
        const cancelHandler = () => {
            toggleVisibility()
            okButton.removeEventListener("click", okHandler)
            cancelButton.removeEventListener("click", cancelHandler)
            resolve(false)
        }
        okButton.addEventListener("click", okHandler)
        cancelButton.addEventListener("click", cancelHandler)
    })

}

function setTexts(title, content) {
    const modalTitle = document.getElementById("modalTitle")
    const modalContent = document.getElementById("modalContent")
    modalTitle.innerHTML = title
    modalContent.innerHTML = content
}

function toggleVisibility() {
    const modal = document.getElementById("modal")
    const background = document.getElementById("modalBackground")

    if (modal.classList.contains("visible")) {
        modal.classList.remove("visible")
        modal.classList.add("invisible")
        background.classList.remove("visible")
        background.classList.add("invisible")
        
    } else {
        modal.classList.remove("invisible")
        modal.classList.add("visible")
        background.classList.remove("invisible")
        background.classList.add("visible")
    }
}