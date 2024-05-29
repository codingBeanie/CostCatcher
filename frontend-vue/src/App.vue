<template>
  <v-app class="bg-primary">
    <!--App Bar-->
    <v-app-bar flat color="secondary">
        <v-app-bar-title>
          <v-row no-gutters class="d-flex align-center">
            <!--LOGO-->
            <v-col cols="2" class="text-start justify-start">
              <router-link to="/welcome">
                <v-img src="./assets/logo2.webp" max-height="50px" max-width="50px"></v-img>

              </router-link>
            </v-col>

            <!--MENU-->
            <v-col cols="8" v-if="username">
              <v-row class="d-flex">
                <v-col></v-col>
                <v-col>
                  <v-btn v-if="componentStore.app.screen > 1" to="import" class="w-links" prepend-icon="mdi-upload" variant="text" size="large" stacked>Import</v-btn>
                  <v-btn v-else to="import" icon="mdi-upload" size="large"></v-btn>
                </v-col>

                <v-col>
                  <v-btn v-if="componentStore.app.screen > 1" to="assignments" class="w-links" text prepend-icon="mdi-tag-multiple" variant="text" size="large" stacked>Categorization</v-btn>
                  <v-btn v-else to="assignments" icon="mdi-tag-multiple" size="large"></v-btn>
                </v-col>
              
                <v-col>
                  <v-btn v-if="componentStore.app.screen > 1" to="statistics" class="w-links" text prepend-icon="mdi-sigma" variant="text" size="large" stacked>Statistics</v-btn>
                  <v-btn v-else to="statistics" icon="mdi-sigma" size="large"></v-btn>
                </v-col>

                  <v-col>
                    <v-btn v-if="componentStore.app.screen > 1" to="graphs" class="w-links" text prepend-icon="mdi-chart-bar" variant="text" size="large" stacked>Graphs</v-btn>
                    <v-btn v-else to="graphs" icon="mdi-chart-bar" size="large"></v-btn>
                  </v-col>
                  <v-col></v-col>
              </v-row>

            </v-col>

            <!--End Button-->
            <v-col cols="2" v-if="username" class="text-end">

              <!--Settings-->
              <v-btn class="" icon @click="componentStore.openSettings('general')">
                <v-icon>mdi-cog</v-icon>
              </v-btn>

               <!--USER-->
              <v-menu open-on-hover class="mr-4">
                <template v-slot:activator="{ props }">
                  <v-btn class="mr-8" icon="mdi-account-circle" color="primary" v-bind="props"></v-btn>
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
        <v-col v-if="version == 'DEV'">
          <p class="mt-1">V{{ version }} ({{ date }}) [{{ componentStore.app.screen }}] {{ windowWidth }} x {{ windowHeight }}</p>
        </v-col>
        <v-col v-else>
          <p class="mt-1">V{{ version }} ({{ date }})</p>
        </v-col>
        <v-col>
          <v-btn href="https://github.com/codingbeanie" color="primaryLight" variant="text" prepend-icon="mdi-github">
            codingbeanie
          </v-btn>
        </v-col>

        <v-col>
          <v-btn href="mailto:mail@costcatcher.cbeanie.com" color="primaryLight" variant="text" prepend-icon="mdi-mail">
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

<Tutorial></Tutorial>

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

import Tutorial from './components/Tutorial.vue'

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
  if (windowWidth.value < 750 || windowHeight.value < 700) {
    componentStore.app.screen = 0
  }
  else if (windowWidth.value < 1100)
  {
    componentStore.app.screen = 1
  }
  else if (windowWidth.value < 1300)
  {
    componentStore.app.screen = 2
  }
  else if (windowWidth.value < 1600)
  {
    componentStore.app.screen = 3
  }
  else {
    componentStore.app.screen = 4
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
<style scoped>
.w-links {
  min-width: 150px;
  max-width: 150px;
}
</style>