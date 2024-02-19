<template>
    <!--Background-->
    <div id="modalBackground" class="fixed inset-0 invisible w-screen h-full bg-black opacity-70">
        
    </div>
    <!--Modal Box-->
    <div id="modal" class="fixed invisible h-40 p-2 -translate-x-1/2 shadow-xl rounded-xl left-1/2 w-96 top-1/3 bg-primary-300 text-secondary-100">
       <div class="flex flex-col items-center justify-center h-full">
            <div class="mb-2">
                <h2 id="modalTitle" class="text-secondary-100">{{ title }}</h2>
            </div>
            <div id="modalContent">
                {{ content }}
            </div>
            <div class="flex">
                <div v-if="ok" id="okButton" class="p-2">
                    <Button>OK</Button>
                </div>
                <div v-if="cancel" id="cancelButton" class="p-2">
                    <Button>Cancel</Button>
                </div>
            </div>

       </div>

    </div>    

</template>


<script setup>
import Button from './Button.vue'

const props = defineProps({
    title: String,
    content: String,
    ok: Boolean,
    cancel: Boolean
})

const ok = () => {

}

const cancel = () => {

}
</script>