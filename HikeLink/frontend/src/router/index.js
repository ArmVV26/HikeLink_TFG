import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import api from '@/utils/api'
import EditProfile from '@/views/auth/EditProfile.vue'
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

const requireIsProfileOwner = (to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const userId = authStore.user?.id

  if (!isAuthenticated) {
    return next('/login')
  }

  if (parseInt(to.params.id) !== userId) {
    return next('/')
  }

  next()
}

const routes = [
  { 
    path: '/profile/edit-profile/:username-:id(\\d+)',
    name:'EditProfile', component: EditProfile, 
    beforeEnter: requireIsProfileOwner, 
    meta: { title: 'HikeLink - Perfil' }
  },
  { 
    path: '/login', name:'Login', 
    component: Login, meta: { title: 'HikeLink - Iniciar Sesión' }
  },
  { 
    path: '/register', name:'Register',
    component: Register, meta: { title: 'HikeLink - Registrarse' }
  },
  { 
    path: '/update-route/:slug-:id(\\d+)',
    name:'UpdateRoute', component: UpdateRoute,
    props: true, beforeEnter: requireIsOwner,
    meta: { title: 'HikeLink - Actualizar Ruta' }
  },
  { 
    path: '/upload-route', name:'UploadRoute',
    component: UploadRoute, beforeEnter: requireAuth,
    meta: { title: 'HikeLink - Subir Ruta' }
  },
  { 
    path: '/profile/:username-:id(\\d+)',
    name:'UserProfile', component: UserProfile,
    beforeEnter: requireAuth, meta: { title: 'HikeLink - Perfil' }
  },
  { 
    path: '/foro', name:'Foro', 
    component: Foro, meta: { title: 'HikeLink - Foro' }
  },
  { 
    path: '/map', name:'Map', 
    component: Map, meta: { title: 'HikeLink - Mapa' }
  },
  { 
    path: '/routes/:slug-:id(\\d+)',
    name:'RouteDetail', component: RouteDetail,
    props: true, meta: { title: 'HikeLink - Ruta' }
  },
  { 
    path: '/search-routes', name:'SearchRoute',
    component: SearchRoutes, meta: { title: 'HikeLink - Buscar Ruta' }
  },
  { 
    path: '/about-us', name:'AboutUs', 
    component: AboutUs, meta: { title: 'HikeLink - Sobre Nosotros' }
  },
  { 
    path: '/condition-use', name:'ConditionUse', 
    component: ConditionUse, meta: { title: 'HikeLink - Uso' }
  },
  { 
    path: '/contact', name:'Contact', 
    component: Contact, meta: { title: 'HikeLink - Contacto' }
  },
  { 
    path: '/help', name:'Help', 
    component: Help, meta: { title: 'HikeLink - Ayuda' }
  },
  { 
    path: '/privacity', name:'Privacity',
    component: Privacity, meta: { title: 'HikeLink - Privacidad' }
  },
  { 
    path: '/', name:'Home', 
    component: Home, meta: { title: 'HikeLink' }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (!authStore.isAuthResolved) {
    // Esperar a que isAuthResolved sea true
    await new Promise(resolve => {
      const stopWatching = authStore.$subscribe((mutation, state) => {
        if (state.isAuthResolved) {
          stopWatching()
          resolve()
        }
      })
    })
  }

  next()
})

export default router