import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL + "/api";

// Principal sin auth
const api = axios.create({
  baseURL: API_URL,
});

// Secundaria con auth y manejo de refresh
export function apiWithAuth() {
  const instance = axios.create({
    baseURL: API_URL,
  })

  // Interceptor para incluir el token
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  // Interceptor para manejar la expiracion del token
  instance.interceptors.response.use(
    response => response,
    async error => {
      const originalRequest = error.config
      const refresh = localStorage.getItem('refresh')

      if(error.response?.status === 401 && refresh && !originalRequest._retry) {
        originalRequest._retry = true
        try {
          const res = await api.post('/token/refresh/', {refresh})
          const newAccess = res.data.access
          localStorage.setItem('access', newAccess)
          
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
          return instance(originalRequest)
        } catch (e) {
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
          window.location.href = '/login'
        }
      }
     
      return Promise.reject(error)
    }
  )

  return instance
}

export function validateResetToken(uidb64, token) {
  return api.get(`auth/validate-reset/${uidb64}/${token}`)
}

export default api;