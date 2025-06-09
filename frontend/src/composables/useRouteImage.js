// Js para obtener la imagen de una routa
import { getMediaUrl } from '@/utils/media';

// Imagen de un Ruta
export function useRouteImage() {
    function getRouteImg(route) {
        return getMediaUrl(`/${route.user.username}/${route.slug}/${route.img?.[0]}`)
    }

    function getRouteAllImg(route, img) {
        return getMediaUrl(`/${route.user.username}/${route.slug}/${img}`)
    }

    function getRouteAllImgURL(route) {
        const arrayImg = []
        for (let i = 0; i < route.img.length; i++) {
            const img = getMediaUrl(`/${route.user.username}/${route.slug}/${route.img?.[i]}`)
            arrayImg.push(img)
        }
        return arrayImg
    }

    function getUserRouteIcon(route) {
        return getMediaUrl(`/${route.user.username}/${route.user.profile_picture}`)
    }

    function handleImgError(event) {
        event.target.src = getMediaUrl('/_common/sample_route_img.png');
    }

    return {
        getRouteImg,
        getRouteAllImg,
        getRouteAllImgURL,
        getUserRouteIcon,
        handleImgError
    }
}