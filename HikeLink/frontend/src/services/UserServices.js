// Js para hacer la peticion de la API a cosas relacionadas con los usuarios
import { apiWithAuth } from "@/utils/api";
import api from "@/utils/api";

// COMMENTS_ROUTE
export async function commentRouteServices({ content, route }) {
  return apiWithAuth().post('/comments/', { content, route });
}

// COMMENTS_FORO
export async function commentThreadServices({ content, thread }) {
  return apiWithAuth().post('/foro-comments/', { content, thread });
}

// RATINGS
export async function ratingUserServices(routeId) {
  try {
    const response = await apiWithAuth().get(`/ratings/user/${routeId}/`);
    return response.data;
  } catch(error) {
    if (error.response?.status !== 404) {
      console.error("Error al obtener la valoración:", error)
    }
    if (error.response?.status === 404) {
      return {rating: 0, id: null};
    } else {
      throw error;
    }
  }
}

export async function createRatingServices(payload) {
  const response = await apiWithAuth().post('/ratings/', payload);
  return response.data;
}

export  async function updateRatingServices(userRatingId, payload) {
  await apiWithAuth().put(`/ratings/${userRatingId}/`, payload);
}

// USER_EDIT
export async function updateUserServices(userId, formData) {
  const response = await apiWithAuth().put(`/profile/edit-profile/${userId}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })

  return response.data;
}

export async function deleteUserServices(userId) {
  await apiWithAuth().delete(`/delete-account/${userId}/`)
}

// USER_RESGISTER
export async function registerUserServices(formData) {
  await api.post('/register/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// USER_FORGOT_PASSWORD
export async function forgotPasswordServices(email) {
  await api.post('/auth/forgot-password/', {
    email: email
  })
}

// USER_RECOVER_PASSWORD
export async function resetPasswordServices(uidb64, token, password) {
  await api.post('/auth/reset-password/', {
    uidb64,
    token,
    new_password: password
  })
}