![Costcatcher Logo](https://github.com/codingBeanie/CostCatcher/blob/main/frontend-vue/src/assets/costcatcher_logo_prim.webp)


Costcatcher is a small application utilizing a Django-Backend and a Vue.js-Frontend for analysing personal financial information. The goal is to get an overview over your spendings, as well as manage the types or categories of your spendings for a deeper analysis.
Visit the website: [Costcatcher](costcatcher.cbeanie.com).

## Features
Because this is just a hobby project, the features a bit limited and tailored to my personal needs.

### Upload
The upload of Data is done via a csv-file import. The specific import schema can be altered to fit various formatting styles of csv-files. 

### Categorization
Besides simple Categories, the user can create rulesets for automatic assignment. This allows to only define a certain rule ones, and in the future transactions get automatically assigned to categories based on the ruleset.

### Visualisation
There is a basic tableau available, that pretty much sums up all the transaction in a overview. The user can click on each displayed amount to get further information how a value is calculated.
