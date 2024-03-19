import { createRouter, createWebHistory } from 'vue-router'
import CSV_View from '../views/CSV_View.vue'
import CategoriesView from '../views/CategoriesView.vue'
import AssignmentsView from '../views/AssignmentsView.vue'
import ReviewView from '../views/ReviewView.vue'
import StatisticsView from '../views/StatisticsView.vue'

const routes = [
  { path: '/', redirect: '/csvmanagement' },
  {
    path: '/csvmanagement',
    name: 'csvmanagement',
    component: CSV_View
  }
  ,
  {
    path: '/import',
    name: 'import',
    component: CSV_View
  },
  {
    path: '/categories',
    name: 'categories',
    component: CategoriesView
  },
  {
    path: '/assignments',
    name: 'assignments',
    component: AssignmentsView
  },
  {
    path: '/review',
    name: 'review',
    component: ReviewView
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: StatisticsView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
