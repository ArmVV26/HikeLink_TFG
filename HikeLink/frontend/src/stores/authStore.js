import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthResolved = ref(false)
  const isAuthenticated = computed(() => user.value !== null);
  const accessToken = computed(() => localStorage.getItem('access'))
  const refreshToken = computed(() => localStorage.getItem('refresh'))

  function login(userData) {
    user.value = userData
    isAuthResolved.value = true
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
      const response = await api.get('user/', {
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      })
      user.value = response.data
    } catch (error) {
      console.error('Error al obtener el usuario:', error)
      logout() 
    }
  }
  return { user, isAuthResolved, isAuthenticated, login, logout, 
           setResolved, accessToken, refreshToken, fetchUser }
})