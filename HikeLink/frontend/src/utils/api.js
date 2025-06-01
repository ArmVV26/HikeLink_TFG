import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

export function apiWithAuth() {
  const token = localStorage.getItem('access');
  return axios.create({
    baseURL: API_URL,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function validateResetToken(uidb64, token) {
  return api.get(`auth/validate-reset/${uidb64}/${token}`)
}

export default api;