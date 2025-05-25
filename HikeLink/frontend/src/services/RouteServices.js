// JS para hacer la peticion de la API a cosas relacionadas con las rutas
import { apiWithAuth } from "@/utils/api";
import api from "@/utils/api";

// UPLOAD_ROUTE
export async function uploadRouteServices(formData) {
    const response = await apiWithAuth().post('upload-route/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    return response.data
}

// UPDATE_ROUTE
export async function updateRouteServices(routeId, formData) {
    await apiWithAuth().put(`/update-route/${routeId}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

// DELETE_ROUTE
export async function deleteRouteServices(routeId) {
    await apiWithAuth().delete(`/delete-route/${routeId}/`)
}