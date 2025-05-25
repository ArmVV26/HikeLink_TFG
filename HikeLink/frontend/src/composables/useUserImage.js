// Js para obtener el icono/imagen de perfil del usuario
import { computed, ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { getMediaUrl } from '@/utils/media';

// Usuario Autenticado
export function useUserImage() {
  const authStore = useAuthStore();
  const userImg = ref(null);

  const getIconUserImg = computed(() => {
    const user = authStore.user;
    if (!user) return null;
    return getMediaUrl(`/${user.username}/${user.profile_picture}`);
  });

  function handleImgError() {
    if (userImg.value) {
      userImg.value.src = getMediaUrl('/_common/sample_user_icon.png');
    }
  }

  return {
    getIconUserImg,
    handleImgError,
    userImg
  };
}

// Usuario Dueño Ruta
export function useUserRouteImage() {
    function getIconRouteImg(user) {
      return getMediaUrl(`/${user.username}/${user.profile_picture}`)
    }

    function handleImgUserError(event) {
      event.target.src = getMediaUrl(`/_common/sample_user_icon.png`);
    }

    return {
      getIconRouteImg,
      handleImgUserError
    }
}

// Usuario Especifico Imagen
export function useUserSpecificImage() {
    function getIconUserImg(username, profile_picture) {
      return getMediaUrl(`/${username}/${profile_picture}`)
    }

    function handleImgError(event) {
      event.target.src = getMediaUrl('/_common/sample_user_icon.png')
    }

    return {
      getIconUserImg,
      handleImgError
    }
}

// Icono del usuario que a puesto un comentario
export function useUserCommentImage() {
  function getIconUserComment(comment) {
    return getMediaUrl(`${comment.user.username}/${comment.user.profile_picture}`)
  }

  function handleImgError(event) {
    event.target.src = getMediaUrl('/_common/sample_user_icon.png')
  }

  return {
    getIconUserComment,
    handleImgError
  }
}