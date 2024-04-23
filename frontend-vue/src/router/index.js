import { createRouter, createWebHistory } from 'vue-router'
import CSV_View from '../views/CSV_View.vue'
import AssignmentsView from '../views/AssignmentsView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import WelcomeView from '../views/WelcomeView.vue'
import GraphsView from '../views/GraphsView.vue'

const routes = [
  { path: '/', name: 'welcome', component: WelcomeView},
  { path: '/csvmanagement', name: 'csvmanagement', component: CSV_View},
  { path: '/import', name: 'import', component: CSV_View},
  { path: '/categories', name: 'categories', component: AssignmentsView},
  { path: '/assignments',name: 'assignments', component: AssignmentsView},
  { path: '/review',name: 'review', component: StatisticsView},
  { path: '/statistics', name: 'statistics', component: StatisticsView },
  { path: '/graphs', name: 'graphs', component: GraphsView}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
