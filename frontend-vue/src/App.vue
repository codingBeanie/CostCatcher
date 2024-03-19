<template>
  <v-app class="bg-primary">
    <v-app-bar flat color="primary">
        <v-app-bar-title>
          COSTCATCHER
        </v-app-bar-title>

        <template v-slot:append>
          <v-btn icon @click="openSettings">
            <v-icon>mdi-cog</v-icon>
          </v-btn>
        </template>
    </v-app-bar>
    
    <v-card>
      <v-navigation-drawer permanent rail expand-on-hover class="bg-secondary">
          <v-divider></v-divider>
          <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-file-multiple" title="CSV Management" to="/import">
            </v-list-item>
            <v-list-item prepend-icon="mdi-bookmark-check" title="Categories" to="/categories">
            </v-list-item>
            <v-list-item prepend-icon="mdi-marker" title="Assignments" to="/assignments">
            </v-list-item>
            <v-list-item prepend-icon="mdi-book-search" title="Review" to="/review">
            </v-list-item>
            <v-list-item prepend-icon="mdi-chart-bar" title="Statistics" to="/statistics">
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
<Alert></Alert>
<DialogSettings></DialogSettings>
</template>


<script setup>
import DialogSettings from './components/DialogSettings.vue';
import { useDialogStore } from './stores/DialogStore'
import Alert from './components/Alert.vue'

// Operations
const dialogStore = useDialogStore()

// Methods
const openSettings = () => {
    dialogStore.settings = !dialogStore.settings
 }
</script>

