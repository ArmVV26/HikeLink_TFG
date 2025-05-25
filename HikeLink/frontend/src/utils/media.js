// JS que permite obtener las imagenes de la API
const MEDIA_URL = import.meta.env.VITE_MEDIA_URL;

// Funcion para obtener una imagen de la API
export function getMediaUrl(path) {
  return `${MEDIA_URL}/${path}`;
}