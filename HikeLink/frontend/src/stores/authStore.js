import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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

  return { user, isAuthResolved, isAuthenticated, login, logout, setResolved, accessToken, refreshToken }
})