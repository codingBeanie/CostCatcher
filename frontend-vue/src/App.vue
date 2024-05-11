<template>
  <v-app class="bg-primary">
    <!--App Bar-->
    <v-app-bar flat color="secondary">
        <v-app-bar-title>
          <v-row no-gutters class="d-flex justify-center align-center">
            <!--LOGO-->
            <v-col cols="1">
              <router-link to="/welcome">
                <v-img src="./assets/logo2.webp" max-height="50px"></v-img>
              </router-link>
            </v-col>

            <!--MENU-->
            <v-col cols="10" v-if="username">
              <v-row class="d-flex">
                <v-col></v-col>
                <v-col>
                  <v-btn to="import" width="200px" prepend-icon="mdi-upload" variant="text" size="large" stacked>Import</v-btn>
                </v-col>

                <v-col>
                  <v-btn to="assignments" width="200px" text prepend-icon="mdi-tag-multiple" variant="text" size="large" stacked>Categorization</v-btn>
                </v-col>
              
                <v-col>
                  <v-btn to="statistics" width="200px" text prepend-icon="mdi-sigma" variant="text" size="large" stacked>Statistics</v-btn>
                </v-col>

                  <v-col>
                    <v-btn to="graphs" width="200px" text prepend-icon="mdi-chart-bar" variant="text" size="large" stacked>Graphs</v-btn>
                  </v-col>
                  <v-col></v-col>
              </v-row>

            </v-col>

            <!--End Button-->
            <v-col cols="1" v-if="username">

              <!--Settings-->
              <v-btn class="mr-4" icon @click="componentStore.openSettings('general')">
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

                  <!--Change Password-->
                  <v-list-item value="changePassword" @click="componentStore.openUpdatePassword">
                    <v-list-item-title><v-icon class="mr-2">mdi-lock-reset</v-icon>Change Password</v-list-item-title>
                  </v-list-item>

                  <!--Change Email-->
                  <v-list-item value="changePassword" @click="componentStore.openUpdateEmail">
                    <v-list-item-title><v-icon class="mr-2">mdi-email-edit-outline</v-icon>Change Email</v-list-item-title>
                  </v-list-item>

                  <!--Delete-->
                  <v-list-item value="delete" @click="componentStore.openDeleteAccount">
                    <v-list-item-title><v-icon class="mr-2">mdi-fire</v-icon>Delete Account</v-list-item-title>
                  </v-list-item>
                  
                  <!--Logout-->
                  <v-list-item value="logout" @click="logout">
                    <v-list-item-title><v-icon class="mr-2">mdi-logout</v-icon>Logout</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
            
          </v-row>
        </v-app-bar-title>
    </v-app-bar>

    <!--Main Content-->
    <v-main>
      <v-container class="">
         <router-view/>
      </v-container>
    </v-main>

    <!--Footer-->
    <v-footer app color="info" class="text-center">
      <v-row>
        <v-col>
          <p class="mt-1">V{{ version }} ({{ date }})</p>
        </v-col>
        <v-col>
          <v-btn href="https://github.com/codingbeanie" color="primaryLight" variant="text" prepend-icon="mdi-github">
            codingbeanie
          </v-btn>
        </v-col>

        <v-col>
          <v-btn href="mailto:mail.costcatcher.cbeanie.com" color="primaryLight" variant="text" prepend-icon="mdi-mail">
              Contact
          </v-btn>   
        </v-col>
      </v-row>
    </v-footer>

  </v-app>

<!--Dialogs and Alerts-->
<Alert></Alert>
<Ouch></Ouch>

<DialogRegister></DialogRegister>
<DialogLogin></DialogLogin>
<DialogDeleteAccount></DialogDeleteAccount>
<DialogUpdatePassword></DialogUpdatePassword>
<DialogPasswordReset></DialogPasswordReset>
<DialogNewPassword></DialogNewPassword>
<DialogUpdateEmail></DialogUpdateEmail>
<DialogDataProtection></DialogDataProtection>

<DialogSettings></DialogSettings>
<DialogDelete></DialogDelete>

<DialogCategories></DialogCategories>
<EditCategory></EditCategory>
<EditAssignment></EditAssignment>

<DialogReview></DialogReview>
<EditTransaction></EditTransaction>

</template>

<script setup>
import { onMounted, ref, watch } from 'vue'

import { getUserdata } from './composables/LocalStorage'
import { useUserStore } from './stores/UserStore'
import { useComponentStore } from './stores/ComponentStore.js'

import Alert from './components/Alert.vue'
import Ouch from './views/Ouch.vue'

import DialogRegister from './components/DialogRegister.vue'
import DialogLogin from './components/DialogLogin.vue'
import DialogDeleteAccount from './components/DialogDeleteAccount.vue'
import DialogUpdatePassword from './components/DialogUpdatePassword.vue'
import DialogPasswordReset from './components/DialogPasswordReset.vue'
import DialogNewPassword from './components/DialogNewPassword.vue'
import DialogUpdateEmail from './components/DialogUpdateEmail.vue'
import DialogDataProtection from './components/DialogDataProtection.vue'

import DialogSettings from './components/DialogSettings.vue'
import DialogDelete from './components/DialogDelete.vue'

import DialogCategories from './components/DialogCategories.vue'
import EditCategory from './components/EditCategory.vue'
import EditAssignment from './components/EditAssignment.vue'

import DialogReview from './components/DialogReview.vue'
import EditTransaction from './components/EditTransaction.vue'
import { useRouter, useRoute } from 'vue-router'

////////////////////////////////////////////////////////////////
// Variables //
// State Management
const componentStore = useComponentStore()
const userStore = useUserStore()
const username = ref(null)
const windowWidth = ref(window.innerWidth)
const windowHeight = ref(window.innerHeight)
const router = useRouter()
const route = useRoute()

const version = ref(process.env.VUE_APP_VERSION)
const date = ref(process.env.VUE_APP_DATE)
////////////////////////////////////////////////////////////////
// Methods //
const logout = () => {
  userStore.logout()
  router.push('/')
}

const checkResize = () => {
  windowWidth.value = window.innerWidth
  windowHeight.value = window.innerHeight
  if (windowWidth.value < 1140 || windowHeight.value < 1000) {
    componentStore.app.screen = 'mobile'
  }
  else {
    componentStore.app.screen = 'desktop'
  }
}
////////////////////////////////////////////////////////////////
// Lifecycle Hooks //
onMounted(() => {
  getUserdata()
  username.value = userStore.username
  checkResize()
  window.addEventListener('resize', checkResize)
  
})

watch(() => userStore.username, () => {
  username.value = userStore.username
  if(username.value == null){
    router.push('/')
  }
  else {
    router.push('/welcome')
  }
})

</script>
