<template>
  <v-app class="bg-primary">
    <v-app-bar flat color="primary">
        <v-app-bar-title>
          COSTCATCHER
        </v-app-bar-title>

        <template v-slot:append>
         <DialogSettings/>
        </template>
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
</template>


<script setup>
import DialogSettings from './components/DialogSettings.vue'
import Alert from './components/Alert.vue'
</script>

