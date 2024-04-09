import { createRouter, createWebHistory } from 'vue-router'
import CSV_View from '../views/CSV_View.vue'
import AssignmentsView from '../views/AssignmentsView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import LandingView from '../views/LandingView.vue'

const routes = [
  { path: '/', redirect: '/landing' },
  { path: '/landing', name: 'landing', component: LandingView},
  { path: '/csvmanagement', name: 'csvmanagement', component: CSV_View},
  { path: '/import', name: 'import', component: CSV_View},
  { path: '/categories', name: 'categories', component: AssignmentsView},
  { path: '/assignments',name: 'assignments', component: AssignmentsView},
  { path: '/review',name: 'review', component: StatisticsView},
  { path: '/statistics', name: 'statistics', component: StatisticsView}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
