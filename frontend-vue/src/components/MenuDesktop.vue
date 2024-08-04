<template>
<v-app-bar flat color="secondary">
    <v-app-bar-title>
        <v-row no-gutters class="d-flex align-center">
            <!--LOGO-->
            <v-col cols="2" class="text-start justify-start">
                <router-link to="/welcome">
                <v-img src="../assets/logo2.webp" max-height="50px" max-width="50px"></v-img>

                </router-link>
            </v-col>

            <!--MENU-->
            <v-col cols="8" v-if="username">
                <v-row class="d-flex">

                    <v-col>
                        <v-btn v-if="display.lgAndUp.value == true" to="import" class="w-links" prepend-icon="mdi-upload" variant="text" size="large" stacked>Import</v-btn>
                        <v-btn v-else to="import" variant="tonal" icon="mdi-upload" size="large"></v-btn>
                    </v-col>

                    <v-col>
                        <v-btn v-if="display.lgAndUp.value == true" to="assignments" class="w-links" text prepend-icon="mdi-tag-multiple" variant="text" size="large" stacked>Categorization</v-btn>
                        <v-btn v-else to="assignments" variant="tonal" icon="mdi-tag-multiple" size="large"></v-btn>
                    </v-col>

                    <v-col>
                        <v-btn v-if="display.lgAndUp.value == true" to="review" class="w-links" text prepend-icon="mdi-text-box-search" variant="text" size="large" stacked>Review</v-btn>
                        <v-btn v-else to="review" variant="tonal" icon="mdi-text-box-search" size="large"></v-btn>
                    </v-col>
                    
                    <v-col>
                        <v-btn v-if="display.lgAndUp.value == true" to="statistics" class="w-links" text prepend-icon="mdi-sigma" variant="text" size="large" stacked>Statistics</v-btn>
                        <v-btn v-else to="statistics" variant="tonal" icon="mdi-sigma" size="large"></v-btn>
                    </v-col>

                    <v-col>
                        <v-btn v-if="display.lgAndUp.value == true" to="graphs" class="w-links" text prepend-icon="mdi-chart-bar" variant="text" size="large" stacked>Graphs</v-btn>
                        <v-btn v-else to="graphs" variant="tonal" icon="mdi-chart-bar" size="large"></v-btn>
                    </v-col>

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
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useComponentStore } from '../stores/ComponentStore.js'
import { useUserStore } from '../stores/UserStore.js'
import { getUserdata } from '../composables/LocalStorage'
import { useDisplay } from 'vuetify'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const componentStore = useComponentStore()
const userStore = useUserStore()
const username = ref(null)
const display = useDisplay()

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

<style scoped>
.w-links {
    width: 100%;
}
</style>