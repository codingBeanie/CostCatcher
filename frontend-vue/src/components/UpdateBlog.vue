<template>
<v-row class="mt-6">
    <v-col cols="12">
        <Title title="Info Board" subtitle="Get the latest news about the Costcatcher"/>
    </v-col>
</v-row>
<v-row>
    <v-card v-for="entry in updateBlog" class="mb-10 bg-primaryLight" width="100%">

        <!--TITLE-->
        <v-card-title>
            <p class="title text-secondary mt-4 mb-2">{{entry.title}}</p>
        </v-card-title>

        <!--SUBTITLE-->
        <v-card-subtitle>
            <p class="subtitle mb-2">{{ entry.date }}</p>
        </v-card-subtitle>

        <v-card-text class="ma-3">

            <!--DESCRIPTION-->
            <v-row v-if="entry.description" class="mb-6">
                <p class="description">{{ entry.description }}</p>
            </v-row>

            <!--CONTENT-->
            <v-row class="" v-if="entry.chapter" v-for="chapter in entry.chapter">
                <v-col>
                    <!--CHAPTER TITLE-->
                    <v-row class="mt-4">
                        <v-icon class="">{{ chapter.icon }}</v-icon><p class="ml-2 mb-2 chapter-title">{{ chapter.title }}</p>
                    </v-row>

                    <!--CHAPTER CONTENT-->
                    <v-row v-if="chapter.text">
                        <p class="chapter-text mt-1">{{ chapter.text }}</p>             
                    </v-row>  

                    <!--CHAPTER BULLETS-->
                    <v-row v-if="chapter.bullets">
                        <v-list class="bg-primaryLight">
                            <v-list-item v-for="bullet in chapter.bullets" :key="bullet" prepend-icon="mdi-circle-small">
                                    <v-list-item-title class="bullet mb-1">{{ bullet }}</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-row>

                </v-col>  

            </v-row>

        </v-card-text>
    </v-card>
</v-row>

</template>

<script setup>
import { updateBlog } from '../composables/UpdateBlog.js'
import Title from '../components/Title.vue'

</script>

<style scoped>
.title {
    font-size: 2rem;
    font-weight: 500;
}
.subtitle {
    font-size: 1rem;
    font-weight: 400;
}
.description {
    font-size: 1.25rem;
    font-weight: 400;
    line-height: 1.4;
}
.chapter-title {
    font-size: 1.2rem;
    font-weight: 500;
}
.chapter-text {
    font-size: 1rem;
}
.bullet {
    font-size: 1rem;
}
</style>