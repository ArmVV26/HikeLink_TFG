import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import api from '@/api/api'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import UpdateRoute from '@/views/auth/UpdateRoute.vue'
import UploadRoute from '@/views/auth/UploadRoute.vue'
import UserProfile from '@/views/auth/UserProfile.vue'
import Foro from '@/views/foro/Foro.vue'
import Map from '@/views/map/Map.vue'
import RouteDetail from '@/views/map/RouteDetail.vue'
import SearchRoutes from '@/views/map/SearchRoutes.vue'
import AboutUs from '@/views/static/AboutUs.vue'
import ConditionUse from '@/views/static/ConditionUse.vue'
import Contact from '@/views/static/Contact.vue'
import Help from '@/views/static/Help.vue'
import Privacity from '@/views/static/Privacity.vue'
import Home from '@/views/Home.vue'

const requireAuth = (to, from, next) => {
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated) {
    next('/login') 
  } else {
    next()
  }
}

const requireIsOwner = async (to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const userId = authStore.user?.id

  if (!isAuthenticated) {
    return next('/login')
  }

  try {
    const { data } = await api.get(`/routes/${to.params.id}`)
    const routeOwnerId = typeof data.user === 'object' ? data.user.id : data.user
    if (routeOwnerId !== userId) {
      return next('/')
    }
    next()
  } catch (error) {
    next('/')
  }
}

const routes = [
  { path: '/login', name:'Login', component: Login},
  { path: '/register', name:'Register', component: Register},
  { path: '/update-route/:slug-:id(\\d+)', name:'UpdateRoute', component: UpdateRoute, props: true, beforeEnter: requireIsOwner},
  { path: '/upload-route', name:'UploadRoute', component: UploadRoute, beforeEnter: requireAuth},
  { path: '/profile', name:'UserProfile', component: UserProfile},
  { path: '/foro', name:'Foro', component: Foro },
  { path: '/map', name:'Map', component: Map },
  { path: '/routes/:slug-:id(\\d+)', name:'RouteDetail', component: RouteDetail, props: true },
  { path: '/searchroutes', name:'SearchRoute', component: SearchRoutes },
  { path: '/aboutus', name:'AboutUs', component: AboutUs },
  { path: '/conditionuse', name:'ConditionUse', component: ConditionUse },
  { path: '/contact', name:'Contact', component: Contact },
  { path: '/help', name:'Help', component: Help },
  { path: '/privacity', name:'Privacity', component: Privacity },
  { path: '/', name:'Home', component: Home },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router