const MEDIA_URL = import.meta.env.VITE_MEDIA_URL;

export function getMediaUrl(path) {
  return `${MEDIA_URL}/${path}`;
}