1111
<template>
  <main
    v-if="user.id"
    class="flex flex-col gap-6 py-10 sm:mx-2 xl:mx-6 xl:grid xl:grid-cols-[25rem_1fr]"
  >
    <section
      class="bg-vanille-50 border-brown w-full self-center border-y-6 p-6 sm:w-100 sm:rounded-3xl sm:border-0 sm:shadow-[5px_5px_0px_2px_rgb(141,_110,_99)] xl:self-start"
    >
      <article
        class="border-b-brown mb-4 flex flex-col items-center justify-center border-b-2 pb-4"
      >
        <img
          :src="getIconUserImg"
          alt="Imagen del Usuario"
          class="h-60 w-[80%] rounded-3xl object-cover"
          @error="handleImgError"
          ref="userImg"
        />
        <h1 class="font-montserrat-bold text-green mt-4 text-2xl leading-4">
          {{ user.username }}
        </h1>
        <p class="text-green text-center text-sm font-bold italic">
          Miembro desde el {{ formatDate(user.created_date) }}
        </p>
      </article>

      <article class="text-center leading-5 font-bold">
        <p class="text-left">{{ user.full_name }}</p>
        <p class="text-left">{{ user.email }}</p>
        <p class="text-left">
          Nº de Rutas: <span class="text-green">{{ allRoutes }}</span>
        </p>
        <p class="text-light-green mt-4 mb-6 text-center italic">{{ user.bio }}</p>
        <CommonButton
          :text="'Editar Perfil'"
          :route="`/profile/edit-profile/${authStore.user.username}-${authStore.user.id}`"
          :thin="true"
          class="my-auto inline-block"
        />
      </article>
    </section>

    <section class="mx-2 flex flex-col gap-6 sm:m-0">
      <article class="flex gap-4 border-b-2 border-b-black">
        <button
          class="font-montserrat-bold hover:text-green cursor-pointer text-xl"
          :class="{
            'text-light-green border-b-green hover:text-light-green border-b-5':
              view === 'myRoutes',
          }"
          @click="view = 'myRoutes'"
        >
          Mis Rutas
        </button>
        <button
          class="font-montserrat-bold hover:text-green cursor-pointer text-xl"
          :class="{
            'text-light-green border-b-green hover:text-light-green border-b-5':
              view === 'favorites',
          }"
          @click="
            view = 'favorites';
            fetchFavorites();
          "
        >
          Favoritos
        </button>
      </article>

      <article v-if="displayedRoutes.length" class="routes-container">
        <RouteCard
          v-if="view === 'myRoutes'"
          :routes="displayedRoutes"
          :current-page="currentPage"
          :total-pages="totalPages"
          @change-page="paginationFetch"
        />

        <RouteCard
          v-else
          :routes="favorites"
          :current-page="currentPage"
          :total-pages="totalPages"
          @change-page="paginationFetch"
        />
      </article>

      <article v-else class="flex flex-col items-center justify-center">
        <i
          class="fa-solid fa-mountain-sun text-green text-[6rem] drop-shadow-[8px_5px_0px_0px_rgb(129,_199,_132)]"
        ></i>
        <article
          v-if="view === 'myRoutes'"
          class="flex flex-col items-center justify-center text-center"
        >
          <h1 class="font-montserrat-bold text-green text-3xl">¡Comienza a incluir tus rutas!</h1>
          <p class="mb-4">
            Todavía no has subido ninguna ruta. Subelas para compartir tus experiencias.
          </p>
          <CommonButton :text="'Subir Ruta'" :route="'/upload-route'" :thin="true" />
        </article>
        <article v-else class="flex flex-col items-center justify-center text-center">
          <h1 class="font-montserrat-bold text-green text-3xl">¡Añade alguna ruta a Favoritos!</h1>
          <p class="mb-4">
            Todavía no has añadido ninguna ruta a favoritos, dale al botón de abajo para buscar tus
            rutas favoritas.
          </p>
          <CommonButton :text="'Buscar Ruta'" :route="'/search-routes'" :thin="true" />
        </article>
      </article>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { computed, onMounted, ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useUserImage } from "@/composables/useUserImage";

import { apiWithAuth } from "@/utils/api";
import CommonButton from "@/components/common/CommonButton.vue";
import RouteCard from "@/components/map/RouteCard.vue";

// VARIABLES
const routes = ref([]);
const favorites = ref([]);
const view = ref("myRoutes");
const allRoutes = computed(() => routes.value.length);

const authStore = useAuthStore();
const user = computed(() => authStore.user);
const isAuthenticated = computed(() => authStore.isAuthenticated);

const { getIconUserImg, handleImgError, userImg } = useUserImage();

const displayedRoutes = computed(() => {
  return view.value === "myRoutes" ? routes.value : favorites.value;
});

// Paginar
const totalPages = ref(1);
const currentPage = ref(1);
const pageSize = 5;

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

// Para hacer que las rutas se pongan en paginas
const paginationFetch = async (page = 1) => {
  try {
    const response = await apiWithAuth().get(
      `/routes/user/${user.value.id}?page=${page}&page_size=${pageSize}`,
    );
    routes.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / pageSize);
    currentPage.value = page;
  } catch (error) {
    console.error("Error obteniendo rutas paginadas: ", error);
  }
};

// Funcion para obtener las rutas que tiene un usuario en favoritos
const fetchFavorites = async () => {
  if (!isAuthenticated.value) return;

  try {
    const response = await apiWithAuth().get(`favorites/?user=${user.value.id}`);
    const favoriteIds = response.data.map((fav) => fav.route);

    const promises = favoriteIds.map((id) => apiWithAuth().get(`/routes/${id}/`));
    const routeDetails = await Promise.all(promises);

    favorites.value = routeDetails.map((r) => r.data);
    totalPages.value = Math.ceil(favorites.value.length / pageSize);
    currentPage.value = 1;
  } catch (error) {
    console.error("Error obteniendo favoritos:", error);
  }
};

// Funcion que se llama al cargar todo
onMounted(async () => {
  if (!isAuthenticated.value) return;
  await paginationFetch(1);
});
</script>
