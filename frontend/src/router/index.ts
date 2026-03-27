import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Players from '../views/Players.vue'
import Media from '../views/Media.vue'
import Playlists from '../views/Playlists.vue'
import MainLayout from '../layouts/MainLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'players',
        name: 'Players',
        component: Players
      },
      {
        path: 'media',
        name: 'Media',
        component: Media
      },
      {
        path: 'playlists',
        name: 'Playlists',
        component: Playlists
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Basic Auth Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.name !== 'Login' && !token) next({ name: 'Login' })
  else next()
})

export default router
