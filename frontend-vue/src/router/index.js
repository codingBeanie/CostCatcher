import { createRouter, createWebHistory } from 'vue-router'
import ImportView from '../views/ImportView.vue'
import FilesView from '../views/FilesView.vue'

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
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
