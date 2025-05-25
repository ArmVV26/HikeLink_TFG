// Js para hacer la peticion de la API a cosas relacionadas con los usuarios
import { apiWithAuth } from "@/utils/api";
import api from "@/utils/api";

// COMMENTS
export async function commentServices({ content, route }) {
  return apiWithAuth().post('/comments/', { content, route });
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

// USER