<template>
    <div class="">
        <v-alert :title="alertStore.alert.title" :type="alertStore.alert.type" v-model="alertStore.alert.show" class="text-h7" :closable="true">
            {{ alertStore.alert.message }}
        </v-alert>
    </div>

</template>

<script setup>
import { useAlertStore } from '../stores/AlertStore.js'

const alertStore = useAlertStore()

</script>

<style scoped>
.v-alert {
  position: fixed;
  left: 50%;
  bottom: 50px;
  transform: translate(-50%, -50%);
  margin: 0 auto; 
}
</style>