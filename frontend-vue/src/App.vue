<template>
  <LandingPage></LandingPage>
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

            <!--End Button-->
            <div class="w-25 text-end">

              <!--Settings-->
              <v-btn class="mr-4" icon @click="mainStore.openSettings('general')">
                <v-icon>mdi-cog</v-icon>
              </v-btn>

               <!--USER-->
              <v-menu open-on-hover class="mr-4">
                <template v-slot:activator="{ props }">
                  <v-btn icon="mdi-account-circle" color="primary" v-bind="props"></v-btn>
                </template>

                <v-list>
                  <v-list-item>
                    <p class="font-weight-bold">Welcome {{ username }}</p>
                  </v-list-item>
                  <v-list-item value="changePassword" @click="changePassword">
                    <v-list-item-title><v-icon class="mr-2">mdi-lock-reset</v-icon>Change Password</v-list-item-title>
                  </v-list-item>
                  <v-list-item value="logout" @click="logout">
                    <v-list-item-title><v-icon class="mr-2">mdi-logout</v-icon>Logout</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
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
<DialogRegister></DialogRegister>
<DialogLogin></DialogLogin>

</template>

<script setup>
import { useMainStore } from './stores/MainStore.js'
import DialogLogin from './components/DialogLogin.vue'
import DialogSettings from './components/DialogSettings.vue'
import Alert from './components/Alert.vue'
import DialogDelete from './components/DialogDelete.vue'
import DialogCategories from './components/DialogCategories.vue'
import EditCategory from './components/EditCategory.vue'
import EditAssignment from './components/EditAssignment.vue'
import EditTransaction from './components/EditTransaction.vue'
import DialogReview from './components/DialogReview.vue'
import DialogRegister from './components/DialogRegister.vue'
import LandingPage from './views/LandingPage.vue'
import { onMounted } from 'vue'
import { getUserdata } from './composables/LocalStorage'
import { useUserStore } from './stores/UserStore'
import { ref } from 'vue'
////////////////////////////////////////////////////////////////
// Variables //
// State Management
const mainStore = useMainStore()
const userStore = useUserStore()
const username = ref(userStore.username)
////////////////////////////////////////////////////////////////
// Methods //
const changePassword = () => {
  console.log('Change Password')
}

const logout = () => {
  userStore.logout()
}
////////////////////////////////////////////////////////////////
// Lifecycle Hooks //
onMounted(() => {
  getUserdata()
  username.value = userStore.username
})
</script>
