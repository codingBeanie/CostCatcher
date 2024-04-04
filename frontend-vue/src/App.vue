<template>
  <v-app class="bg-primary">
    <!--App Bar-->
    <v-app-bar flat color="secondary">
        <v-app-bar-title>
          <div class="d-flex align-center">
            <!--LOGO-->
            <div class="w-25">
              <div>COSTCATHER</div>
            </div>

            <!--MENU-->
            <div class="justify-center w-50 d-flex">
              <div class="">
                <v-btn to="import" width="200px" prepend-icon="mdi-upload" variant="text" size="large" stacked>Import</v-btn>
              </div>
              
              <div>
                <v-btn to="assignments" width="200px" text prepend-icon="mdi-tag-multiple" variant="text" size="large" stacked>Categorization</v-btn>
              </div>
              
              <div>
                <v-btn to="statistics" width="200px" text prepend-icon="mdi-sigma" variant="text" size="large" stacked>Statistics</v-btn>
              </div>
            </div>

            <!--SETTINGS-->
            <div class="w-25 text-end">
              <v-btn class="mr-4" icon @click="mainStore.openSettings('general')">
                <v-icon>mdi-cog</v-icon>
              </v-btn>
            </div>
            
          </div>
        </v-app-bar-title>
    </v-app-bar>

    <!--Main Content-->
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
