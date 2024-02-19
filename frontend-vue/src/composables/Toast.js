export function toast(content) {
    document.getElementById("toastContent").innerHTML = content
    const toast = document.getElementById("toast")
    toast.classList.remove("invisible", "opacity-0")
    toast.classList.add("visible", "opacity-100")

    setTimeout(() => {
        toast.classList.remove("visible", "opacity-100")
        toast.classList.add("invisible", "opacity-0")
    }, 3000)
}

