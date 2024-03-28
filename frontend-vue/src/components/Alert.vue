<template>
    <div class="">
        <v-alert :title="mainStore.alert.title" :type="mainStore.alert.type" v-model="mainStore.alert.show" class="text-h7" :closable="true">
            {{ mainStore.alert.message }}
        </v-alert>
    </div>

</template>

<script setup>
import { useMainStore } from '../stores/MainStore.js'

const mainStore = useMainStore()

</script>

<style scoped>
.v-alert {
  position: fixed;
  left: 50%;
  bottom: 50px;
  transform: translate(-50%, -50%);
  margin: 0 auto;
  z-index: 9999; 
}
</style>