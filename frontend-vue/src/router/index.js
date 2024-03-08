import { createRouter, createWebHistory } from 'vue-router'
import ImportView from '../views/ImportView.vue'
import FilesView from '../views/FilesView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import AssignmentsView from '../views/AssignmentsView.vue'
import ReviewView from '../views/ReviewView.vue'

const routes = [
  { path: '/', redirect: '/import' },
  {
    path: '/import',
    name: 'import',
    component: ImportView
  }
  ,
  {
    path: '/files',
    name: 'files',
    component: FilesView
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
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
