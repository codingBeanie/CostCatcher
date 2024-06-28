<template>
<v-app-bar flat color="secondary">
    <v-app-bar-title>
        <v-row no-gutters class="d-flex align-center">
        <!--LOGO-->
            <v-col cols="8" class="text-start justify-start">
                <router-link to="/welcome">
                <v-img src="../assets/logo_trans_light.webp" max-height="120px" max-width="120px"></v-img>
                </router-link>
            </v-col>

            <!--MENU-->
             <v-col cols="4" v-if="username" class="text-end">

                <!--Settings-->
                <v-btn class="" icon @click="componentStore.openSettings('general')">
                <v-icon>mdi-cog</v-icon>
                </v-btn>

                <!--USER-->
                <v-menu open-on-hover class="">
                <template v-slot:activator="{ props }">
                    <v-btn class="" icon="mdi-account-circle" color="primary" v-bind="props"></v-btn>
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
</template>

<script setup>
import {ref, onMounted } from 'vue'
import { getUserdata } from '../composables/LocalStorage'
import { useUserStore } from '../stores/UserStore.js'
import { useComponentStore } from '../stores/ComponentStore.js'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const username = ref(null)
const userStore = useUserStore()
const componentStore = useComponentStore()

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////
const logout = () => {
  userStore.logout()
  router.push('/')
}

////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////
onMounted(() => {
  getUserdata()
  username.value = userStore.username
})
</script>