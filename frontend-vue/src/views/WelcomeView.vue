<template>
    <v-row>
        <span class="text-h2 mt-10">Welcome to</span>
        <span class="text-h2 mt-10 ml-4 font-weight-bold text-accent">COSTCATCHER</span>
    </v-row>
    <v-row>
        <span class="text-h4 mt-10 font-weight-light">How does it work?</span>
    </v-row>
    <v-divider class="mt-4 mb-6"></v-divider>
    <v-row class="mb-10" v-for="item in items">
        <div class="flex pa-2 w-100">
            <div class="mb-2">
                <v-btn size="x-large" :to="item.link" :prepend-icon="item.icon">{{ item.title }}</v-btn>
            </div>
            <div>
                <p class="text-h6 font-weight-light w-75">{{ item.subtitle }}</p>
            </div>

        </div>
    </v-row>
</template>

<script setup>
const items = [
    {
        title: 'Upload your CSV-Files',
        subtitle: 'First you need to upload some date. This is done with a csv-file which contains your transaction data. You probably need to adjust the `import schema` for your specific csv-file, because every bank may have it´s own csv-schema.',
        icon: 'mdi-upload',
        link: '/import'
    },
    {
        title: 'Create Categories',
        subtitle: 'Categorization is a core feature of CostCatcher. Create custom categories and rulesets for an automatic assignment of categories to your transactions. In future, you won´t need to categorize your transactions manually. Just upload the most recent file and most of the transactions will be categorized automatically.',
        icon: 'mdi-tag-multiple',
        link: '/assignments'
    },
    {
        title: 'Get Basic Statistics',
        subtitle: 'CostCatcher provides a basic table with your financial statistics. The focus here lies on the categorization of your transactions. You can see how much money you spent in each category and how much money you received.',
        icon: 'mdi-sigma',
        link: '/statistics'
    }
]

</script>