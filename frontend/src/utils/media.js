// JS que permite obtener las imagenes de la API
const MEDIA_URL = import.meta.env.VITE_API_URL + "/media";

// Funcion para obtener una imagen de la API
export function getMediaUrl(path) {
  const base = MEDIA_URL.replace(/\/$/, '');
  const cleanPath = path.replace(/^\/+/, '');
  return `${base}/${cleanPath}`;
}