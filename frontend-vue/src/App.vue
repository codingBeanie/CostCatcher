<template>
  <v-app class="bg-primary">
    <v-app-bar flat color="secondary">
        <v-app-bar-title>
          <div class="text-center bg-error" v-if="alertStore.appState==='error'">The application is not working properly. Please come back later.</div>
          <div v-else>COSTCATCHER</div>
        </v-app-bar-title>
    </v-app-bar>
    <v-card>
      <v-navigation-drawer permanent rail expand-on-hover class="bg-secondary">
          <v-divider></v-divider>
          <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-upload" title="Import CSV" to="/import">
            </v-list-item>
             <v-list-item prepend-icon="mdi-file-multiple" title="Manage Files" to="/files">
            </v-list-item>
            <v-list-item prepend-icon="mdi-bookmark-check" title="Categories" to="/categories">
            </v-list-item>
            <v-list-item prepend-icon="mdi-marker" title="Assignments" to="/assignments">
            </v-list-item>
          </v-list>
      </v-navigation-drawer>
    </v-card>

    <v-main>
      <v-container class="">
         <router-view/>
      </v-container>
    </v-main>
  </v-app>
<Alert/>

</template>


<script setup>
import Alert from './components/Alert.vue'
import { useAlertStore } from './stores/AlertStore.js'
const alertStore = useAlertStore()
</script>

