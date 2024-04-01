<template>
  <v-app class="bg-primary">
    <v-app-bar flat color="primary">
        <v-app-bar-title>
          COSTCATCHER
        </v-app-bar-title>

        <template v-slot:append>
          <v-btn icon @click="mainStore.openSettings('general')">
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

<!--Dialogs and Alerts-->
<Alert></Alert>
<DialogSettings></DialogSettings>
<DialogDelete></DialogDelete>
<DialogCategories></DialogCategories>
<DialogReview></DialogReview>
<EditCategory></EditCategory>
<EditAssignment></EditAssignment>
<EditTransaction></EditTransaction>

</template>

<script setup>
import { useMainStore } from './stores/MainStore.js'
import DialogSettings from './components/DialogSettings.vue'
import Alert from './components/Alert.vue'
import DialogDelete from './components/DialogDelete.vue'
import DialogCategories from './components/DialogCategories.vue'
import EditCategory from './components/EditCategory.vue'
import EditAssignment from './components/EditAssignment.vue'
import EditTransaction from './components/EditTransaction.vue'
import DialogReview from './components/DialogReview.vue'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const mainStore = useMainStore()

</script>
