import { createRouter, createWebHistory } from 'vue-router'
import ImportView from '../views/ImportView.vue'

const routes = [
  { path: '/', redirect: '/import' },
  {
    path: '/import',
    name: 'import',
    component: ImportView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
