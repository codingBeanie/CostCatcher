<template>
    <!--Footer-->
    <v-footer app color="info" class="text-center">
      <v-row>
        <v-col v-if="version == 'DEV'">
          <p class="mt-1">V{{ version }} ({{ date }}) [{{ display.name }}]</p>
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
</template>

<script setup>
import { ref } from 'vue'
import { useDisplay } from 'vuetify'
////////////////////////////////////////////////////////////////
// Variables
////////////////////////////////////////////////////////////////
const version = ref(process.env.VUE_APP_VERSION)
const date = ref(process.env.VUE_APP_DATE)
const display = useDisplay()

////////////////////////////////////////////////////////////////
// Methods
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
// Lifecycle
////////////////////////////////////////////////////////////////

</script>