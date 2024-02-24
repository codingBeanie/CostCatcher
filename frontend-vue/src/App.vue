<template>
  <v-app class="bg-primary">
    <v-app-bar flat color="secondary">
        <v-app-bar-title>COSTCATCHER</v-app-bar-title>
    </v-app-bar>
    <v-card>
      <v-navigation-drawer rail expand-on-hover class="bg-secondary">
          <v-list>
            <v-list-item title="ME">
            </v-list-item>
          </v-list>

          <v-divider></v-divider>
          <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-upload" title="Import CSV" to="/import">
            </v-list-item>
             <v-list-item prepend-icon="mdi-file-multiple" title="Manage Files" to="/files">
            </v-list-item>
          </v-list>
      </v-navigation-drawer>
    </v-card>


    <v-main>
      <v-container fluid class="pa-6">
         <router-view/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>

</script>
