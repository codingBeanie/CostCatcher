<template>
  <v-app class="bg-primary">
    <!--Header-->
    <div v-if="display.mdAndUp.value">
      <MenuDesktop></MenuDesktop>
    </div>
    <div v-else>
      <HeaderMobile></HeaderMobile>
    </div>


    <!--Main Content-->
    <v-main>
      <v-container class="">

         <router-view/>
      </v-container>
    </v-main>

    <!--Footer-->
    <div v-if="display.mdAndUp.value">
      <FooterDesktop></FooterDesktop>
    </div>
    <div v-else>
      <MenuMobile></MenuMobile>
    </div>

  </v-app>

<!--Dialogs and Alerts-->
<Alert></Alert>
<div v-if="display.smAndDown.value">
  <Ouch></Ouch>
</div>

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
import { useDisplay } from 'vuetify'

import { getUserdata } from './composables/LocalStorage'
import { useUserStore } from './stores/UserStore'

import Alert from './components/Alert.vue'
import MenuDesktop from './components/MenuDesktop.vue'
import MenuMobile from './components/MenuMobile.vue'
import FooterDesktop from './components/FooterDesktop.vue'
import HeaderMobile from './components/HeaderMobile.vue'

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
const userStore = useUserStore()
const username = ref(null)
const windowWidth = ref(window.innerWidth)
const windowHeight = ref(window.innerHeight)
const router = useRouter()
const display = useDisplay()

const version = ref(process.env.VUE_APP_VERSION)
const date = ref(process.env.VUE_APP_DATE)

////////////////////////////////////////////////////////////////
// Methods //


////////////////////////////////////////////////////////////////
// Lifecycle Hooks //
onMounted(() => {
  getUserdata()
  username.value = userStore.username
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
