import { createRouter, createWebHashHistory } from 'vue-router'
import CSV_View from '../views/CSV_View.vue'
import AssignmentsView from '../views/AssignmentsView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import WelcomeView from '../views/WelcomeView.vue'
import GraphsView from '../views/GraphsView.vue'
import LandingView from '../views/LandingView.vue'
import notFound404 from '../views/notFound404.vue'
import ReviewView from '../views/ReviewView.vue'
//

const routes = [
  { path: '/', name: 'landing', component: LandingView },
  { path: '/welcome', name:'weclome', component: WelcomeView},
  { path: '/csvmanagement', name: 'csvmanagement', component: CSV_View},
  { path: '/import', name: 'import', component: CSV_View},
  { path: '/categories', name: 'categories', component: AssignmentsView},
  { path: '/assignments', name: 'assignments', component: AssignmentsView },
  { path: '/review', name: 'review', component: ReviewView},
  { path: '/statistics', name: 'statistics', component: StatisticsView },
  { path: '/graphs', name: 'graphs', component: GraphsView},
  { path: '/:pathMatch(.*)*', name: 'not-found', component: notFound404 },
  { path: '/resetpassword/:token', name: 'resetpassword', component: LandingView},
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})

export default router
