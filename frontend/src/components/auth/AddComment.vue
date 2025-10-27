<template>
  <section class="mx-2 mb-5 flex gap-2 sm:mx-10 sm:gap-4">
    <img
      v-if="isAuthenticated"
      :src="getIconUserImg"
      @error="handleImgError"
      class="border-light-green h-16 w-16 rounded-3xl border-2 object-cover"
      ref="userImg"
    />
    <img
      v-else
      :src="getMediaUrl('/_common/sample_user_icon.png')"
      class="border-light-green h-16 w-16 rounded-3xl border-2 object-cover"
    />
    <article class="flex-1" :class="{ disabled: !isAuthenticated }">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <h1 class="font-montserrat-bold text-green text-left text-base sm:text-2xl">
          Añade un comentario
        </h1>
        <p v-if="!isAuthenticated" class="text-xs font-bold text-red-500 sm:text-base">
          Debes iniciar sesión para comentar
        </p>
      </div>
      <form @submit.prevent="submitComment" class="flex flex-col">
        <textarea
          :class="[
            'min-h-50 w-full resize-none rounded-3xl border-2 border-black px-4 py-2',
            { 'bg-grey': !isAuthenticated },
          ]"
          id="addComment"
          name="addComment"
          placeholder="Escribe un comentario"
          v-model="commentText"
          :disabled="!isAuthenticated"
        ></textarea>

        <CommonButton
          :text="'Enviar Comentario'"
          :route="''"
          :thin="true"
          :asButton="true"
          :disabled="!isAuthenticated"
          @click="submitComment"
          class="mt-2 self-end"
        />
      </form>
    </article>
  </section>
</template>

<script setup>
// IMPORTS
import { ref, computed, toRefs } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { getMediaUrl } from "@/utils/media";
import { useUserImage } from "@/composables/useUserImage";
import { commentRouteServices, commentThreadServices } from "@/services/UserServices";
import CommonButton from "@/components/common/CommonButton.vue";

// PROPS
const props = defineProps({
  routeId: {
    type: Number,
    required: false,
  },
  threadId: {
    type: Number,
    required: false,
  },
});

// VARIABLES
const { routeId, threadId } = toRefs(props);

const emit = defineEmits(["comment-submitted"]);

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
const commentText = ref("");

// METODOS
// Imagen de usuario
const { getIconUserImg, handleImgError, userImg } = useUserImage();

// Metodo que permite guardar el comentario y llamar a la funcion refreshRouteData para actualizar los datos
async function submitComment() {
  if (!isAuthenticated.value || !commentText.value.trim()) return;

  try {
    if (props.routeId) {
      await commentRouteServices({ content: commentText.value, route: routeId.value });
    } else if (props.threadId) {
      await commentThreadServices({ content: commentText.value, thread: threadId.value });
    }

    commentText.value = "";
    emit("comment-submitted");
  } catch (error) {
    console.error("Error al enviar comentario:", error);
  }
}
</script>
