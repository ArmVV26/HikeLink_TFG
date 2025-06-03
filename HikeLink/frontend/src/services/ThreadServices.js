// Js para hacer la peticion de la API a cosas relacionadas con los hilos
import { apiWithAuth } from "@/utils/api";
import api from "@/utils/api";

// UPLOAD_THREAD
export async function uploadThreadServices(formData) {
    const response = await apiWithAuth().post('threads/', formData)
    return response.data
}

// DELETE_THREAD
export async function deleteThreadServices(threadId) {
    await apiWithAuth().delete(`delete-thread/${threadId}/`)
}