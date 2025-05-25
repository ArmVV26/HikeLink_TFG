import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiWithAuth} from '@/utils/api'
import api from '@/utils/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthResolved = ref(false)
  const isAuthenticated = computed(() => user.value !== null);
  const accessToken = computed(() => localStorage.getItem('access'))
  const refreshToken = computed(() => localStorage.getItem('refresh'))

  async function login(username, password) {
    try {
      const { data: token } = await api.post('/token/', {
        username,
        password
      })

      localStorage.setItem('access', token.access)
      localStorage.setItem('refresh', token.refresh)

      const userRes = await apiWithAuth().get('/user/')
      user.value = userRes.data
      isAuthResolved.value = true
    } catch(error) {
      throw error
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    isAuthResolved.value = true
  }

  function setResolved() {
    isAuthResolved.value = true
  }

  async function fetchUser() {
    try {
      const response = await apiWithAuth().get('/user/')
      user.value = response.data
    } catch (error) {
      console.error('Error al obtener el usuario:', error)
      logout() 
    } finally {
      isAuthResolved.value = true
    }
  }
  return { user, isAuthResolved, isAuthenticated, login, logout, 
           setResolved, accessToken, refreshToken, fetchUser }
})