<template>
  <main v-if="thread" class="xl:w-[70%]container w-full py-10 sm:m-auto sm:w-[90%] lg:w-[80%]">
    <section
      class="bg-vanille-50 mb-4 flex flex-col gap-2 py-4 shadow-[2px_2px_5px_1px_rgb(0,_0,_0)] sm:m-4 sm:rounded-3xl sm:p-4"
    >
      <article
        class="bg-light-green-50 relative grid grid-cols-[4rem_1fr] gap-4 p-2 shadow-[2px_2px_5px_1px_rgb(0,_0,_0)] sm:grid-cols-[6rem_1fr] sm:rounded-3xl"
      >
        <aside class="flex flex-col items-center gap-2">
          <img
            :src="getIconUserThread(thread.user)"
            @error="handleImgError"
            class="border-green h-18 w-18 rounded-3xl border-2 object-cover sm:h-24 sm:w-24"
            alt="Imagen del Usuario"
          />

          <button
            v-if="isOwner"
            @click="showDeleteModal = true"
            class="cursor-pointer rounded-3xl bg-red-500 px-2 py-2 text-sm font-bold text-white transition-all duration-300 hover:bg-red-300 hover:text-black sm:text-base"
          >
            Eliminar
          </button>
        </aside>

        <article class="flex flex-col">
          <header class="mr-6 flex flex-col sm:mb-2 sm:flex-row sm:items-center sm:justify-between">
            <h1 class="font-montserrat-bold text-green text-base sm:text-xl">
              {{ thread.user.username }}
            </h1>
            <p class="text-brown mb-2 text-sm leading-2 font-bold sm:mb-0 sm:text-base">
              {{ formatDate(thread.created_date) }}
            </p>
          </header>
          <h1 class="font-montserrat-bold text-green text-left text-xl leading-8 sm:text-3xl">
            {{ thread.title }}
          </h1>
          <p class="max-w-full indent-8 text-sm sm:text-base">{{ thread.content }}</p>
        </article>
      </article>

      <section class="mt-6 flex flex-col gap-3">
        <article v-for="comment in thread.comments" :key="comment.id">
          <article
            class="grid grid-cols-[4rem_1fr] gap-4 bg-white p-2 shadow-[2px_2px_5px_1px_rgb(0,_0,_0)] sm:rounded-3xl"
          >
            <img
              :src="getIconUserThread(comment.user)"
              @error="handleImgError"
              class="border-green h-16 w-18 rounded-3xl border-2 object-cover"
              alt="Imagen del Usuario"
            />

            <aside class="flex flex-col">
              <article class="mr-6 flex flex-col sm:flex-row sm:items-center sm:justify-between">
                <h1 class="font-montserrat-bold text-green text-base sm:text-xl">
                  {{ comment.user.username }}
                </h1>
                <p class="text-brown mb-2 text-sm leading-2 font-bold sm:mb-0 sm:text-base">
                  {{ formatDate(comment.created_date) }}
                </p>
              </article>
              <p class="max-w-full text-sm sm:text-base">{{ comment.content }}</p>
            </aside>
          </article>
        </article>
      </section>
    </section>

    <AddComment :thread-id="thread.id" @comment-submitted="refreshThreadData" />

    <transition name="fade">
      <DeleteModal
        v-if="showDeleteModal"
        :title="'¿Quieres eliminar el Hilo?'"
        :message="'Si eliminas el Hilo no podras acceder más a este hilo. Piensatelo 2 veces.'"
        @confirm="confirmDeleteThread"
        @cancel="showDeleteModal = false"
      />
    </transition>
  </main>

  <main v-else>
    <h1>Error al Cargar el Hilo</h1>
  </main>
</template>

<script setup>
// IMPORTS
import { computed, onMounted, ref } from "vue";
import { useUserThreadImage } from "@/composables/useUserImage";
import { useAuthStore } from "@/stores/authStore";
import { deleteThreadServices } from "@/services/ThreadServices";
import { useRouter } from "vue-router";

import DeleteModal from "@/components/modal/DeleteModal.vue";
import AddComment from "@/components/auth/AddComment.vue";
import api from "@/utils/api";

// PROPS
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  slug: {
    type: String,
    required: true,
  },
});

// VARIABLES
const showDeleteModal = ref(false);
const router = useRouter();

const thread = ref(null);

const { getIconUserThread, handleImgError } = useUserThreadImage();

// Compruebo si el usuario es el dueño deL hilo
const authStore = useAuthStore();
const currentUserId = computed(() => authStore.user?.id ?? null);
const isOwner = computed(() => {
  return thread.value && currentUserId.value === thread.value.user.id;
});

// METODOS
// Transformar la fecha en "10 de marzo de 2026"
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("es-ES", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(date);
};

// Funcion para eliminar el hilo
const confirmDeleteThread = async () => {
  try {
    await deleteThreadServices(props.id);
    showDeleteModal.value = false;
    router.push("/foro");
  } catch (error) {
    console.error("Error al eliminar el hilo:", error);
  }
};

// Funcion que permite actualizar los datos del Hilo
const refreshThreadData = async () => {
  try {
    const response = await api.get(`/threads/${props.id}/`);
    thread.value = response.data;
  } catch (error) {
    console.error("Error recargando los datos del hilo:", error);
  }
};

// Realiza la llamada a la API para obtener los datos del Hilo
onMounted(async () => {
  await refreshThreadData();
});
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
