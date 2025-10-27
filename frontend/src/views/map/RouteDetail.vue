<template>
  <div v-if="route">
    <main class="flex flex-col gap-4 py-10 min-[701px]:mx-16 xl:grid xl:grid-cols-[1fr_25rem]">
      <section>
        <span
          class="text-dark-grey ml-4 flex items-center gap-2 text-base font-bold sm:text-xl"
          v-html="routeType(route)"
        ></span>
        <h1 class="font-montserrat-bold ml-4 text-left text-xl font-bold sm:text-3xl">
          {{ route.title }}
        </h1>

        <article class="mb-2 flex flex-col items-center gap-2 sm:mx-4 sm:flex-row">
          <p class="text-dark-grey flex-1 text-base font-bold">
            {{ formatDate(route.created_date) }}
          </p>
          <div class="flex flex-row gap-2">
            <CommonButton
              :text="isFavorite ? 'Quitar Favorito' : 'Añadir a Favoritos'"
              :icon="'fa-solid fa-bookmark'"
              :thin="true"
              :route="''"
              :asButton="true"
              :disabled="!isAuthenticated"
              @click="toggleFavorite"
            />
            <CommonButton
              v-if="isOwner"
              :text="'Modificar'"
              :icon="'fa-solid fa-pen-to-square'"
              :thin="true"
              :route="`/update-route/${route.slug}-${route.id}`"
            />
          </div>
        </article>

        <ShowMap :detailed-map="false"></ShowMap>
      </section>

      <section class="self-center xl:self-end">
        <aside
          class="bg-vanille-50 mx-0 flex flex-col items-center p-2 shadow-[0px_0px_5px_0px_rgb(0,_0,_0)] min-[529px]:rounded-3xl sm:mx-4 sm:flex-row md:mx-0 xl:flex-col"
        >
          <article
            class="border-brown flex h-full w-30 flex-col items-center justify-center gap-2 pr-2 pb-2 sm:w-60 xl:w-full xl:border-b-2 xl:pr-0"
          >
            <img
              :src="getUserRouteIcon(route)"
              @error="handleImgError"
              class="border-green h-30 w-30 rounded-3xl border-2 object-cover xl:h-16 xl:w-16"
            />
            <p
              :title="route.user.username"
              class="font-montserrat-bold text-green text-base leading-none sm:text-lg"
            >
              {{ route.user.username }}
            </p>
          </article>

          <article class="w-full">
            <h1
              class="font-montserrat-bold mt-4 mb-1 pl-2 text-center text-base sm:text-left sm:text-lg xl:pl-0 xl:text-center"
            >
              Estadísticas de la ruta
            </h1>

            <section class="border-grey grid grid-cols-2 border-t-2 text-center xl:grid-cols-1">
              <div class="table-detail grid grid-cols-2">
                <!-- Fila 1 -->
                <article class="max-[1280px]:h-19">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">Distancia</h1>
                  <p class="text-sm">{{ (route.distance / 1000).toFixed(1) }} km</p>
                </article>

                <article class="max-[1280px]:h-19">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                    Dificultad
                  </h1>
                  <p class="text-sm">{{ route.difficulty }}</p>
                </article>

                <!-- Fila 2 -->
                <article class="max-[1280px]:h-19">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                    Desnivel Positivo
                  </h1>
                  <p v-if="elevationData" class="text-sm">{{ elevationData.ascent }} m</p>
                </article>

                <article class="max-[1280px]:h-19">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                    Desnivel Negativo
                  </h1>
                  <p v-if="elevationData" class="text-sm">{{ elevationData.descent }} m</p>
                </article>

                <!-- Fila 3 -->
                <article class="max-[1280px]:h-19">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                    Altitud Max.
                  </h1>
                  <p v-if="elevationData" class="text-sm">{{ elevationData.maxElevation }} m</p>
                </article>

                <article class="max-[1280px]:h-19">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                    Altitud Min.
                  </h1>
                  <p v-if="elevationData" class="text-sm">{{ elevationData.minElevation }} m</p>
                </article>
              </div>

              <div class="grid grid-cols-1">
                <!-- Fila 4 -->
                <article class="border-grey border-b-2 border-l-2 max-[1280px]:h-19 xl:border-l-0">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                    Coordenadas Salida
                  </h1>
                  <p class="text-sm">
                    <strong class="text-green">Lat: </strong>{{ route.start_latitude }}
                  </p>
                  <p class="text-sm">
                    <strong class="text-green">Lon: </strong>{{ route.start_longitude }}
                  </p>
                </article>

                <!-- Fila 5 -->
                <article class="border-grey border-b-2 border-l-2 max-[1280px]:h-19 xl:border-l-0">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                    Coordenadas Llegada
                  </h1>
                  <p v-if="lastCoord" class="text-sm">
                    <strong class="text-green">Lat: </strong>{{ lastCoord.lat }}
                  </p>
                  <p v-if="lastCoord" class="text-sm">
                    <strong class="text-green">Lon: </strong>{{ lastCoord.lon }}
                  </p>
                </article>

                <!-- Fila 6 -->
                <article class="border-grey border-b-2 border-l-2 max-[1280px]:h-19 xl:border-l-0">
                  <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">Tiempo</h1>
                  <p class="text-sm">{{ formatDuration(route.duration) }}</p>
                </article>
              </div>

              <!-- Fila 7 -->
              <article class="max-[1280px]:col-span-2">
                <h1 class="text-green text-sm leading-6 font-semibold sm:text-base">
                  Valorar Ruta
                </h1>
                <RatingButton
                  :route-id="route.id"
                  :route-user-id="route.user.id"
                  @rating-updated="refreshRouteData"
                />
                <p class="text-sm">{{ route.average_rating }} / 5</p>
              </article>
            </section>
          </article>
        </aside>
      </section>
    </main>

    <section class="mx-6 sm:mx-16">
      <RouteCarousel :img-carousel="true" :img-urls="imgRoute" />

      <article class="mt-4 flex flex-col">
        <h1 class="font-montserrat-bold text-green text-left text-lg sm:text-2xl">
          Descripción del Itinerario
        </h1>
        <span class="description-route text-sm sm:text-base" v-html="route.description_html"></span>
      </article>

      <article class="border-t-light-green my-6 flex flex-col gap-2 border-t-3 pt-4">
        <h1 class="font-montserrat-bold text-green text-left text-lg sm:text-2xl">Comentarios</h1>

        <section
          class="border-b-grey mb-4 flex gap-4 border-b-5 border-dotted pb-2"
          v-for="comment in route.comments"
          :key="comment"
        >
          <img
            :src="getIconUserComment(comment)"
            @error="handleImgError"
            class="border-light-green h-16 min-w-16 rounded-3xl border-2 object-cover"
            ref="userImg"
          />

          <article>
            <div class="mb-2 flex flex-col sm:mb-0 sm:flex-row sm:items-center sm:gap-6">
              <h1 class="text-light-green font-montserrat-bold text-base sm:text-lg">
                {{ comment.user.username }}
              </h1>
              <p class="text-grey text-sm font-bold sm:text-base">
                {{ formatDate(comment.created_date) }}
              </p>
            </div>

            <p class="text-sm sm:text-base">{{ comment.content }}</p>
          </article>
        </section>
      </article>

      <AddComment :route-id="route.id" @comment-submitted="refreshRouteData" />
    </section>
  </div>

  <main v-else>
    <h1>Error al Cargar la Ruta</h1>
  </main>
</template>

<script setup>
// IMPORTS
import { computed, onMounted, ref } from "vue";
import { DOMParser } from "xmldom";
import { gpx } from "@tmcw/togeojson";
import { getMediaUrl } from "@/utils/media";
import { useAuthStore } from "@/stores/authStore";
import { useRouteImage } from "@/composables/useRouteImage";
import { useUserCommentImage } from "@/composables/useUserImage";

import { apiWithAuth } from "@/utils/api";
import api from "@/utils/api";

import ShowMap from "@/components/map/ShowMap.vue";
import CommonButton from "@/components/common/CommonButton.vue";
import RouteCarousel from "@/components/images/RouteCarousel.vue";
import RatingButton from "@/components/auth/RatingButton.vue";
import AddComment from "@/components/auth/AddComment.vue";

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
const route = ref(null);
const elevationData = ref(null);
const lastCoord = ref(null);
const imgRoute = ref(null);

const isFavorite = ref(false);
const favoriteId = ref(null);

// Compruebo si el usuario es el dueño de la ruta
const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
const currentUserId = computed(() => authStore.user?.id ?? null);
const isOwner = computed(() => {
  return route.value && currentUserId.value === route.value.user.id;
});

const { getRouteAllImgURL, getUserRouteIcon } = useRouteImage();
const { getIconUserComment, handleImgError } = useUserCommentImage();

// METODOS
// Obtener la URL del GPX de la Ruta
const getGPXUrl = (route) => {
  return getMediaUrl(`/${route.user.username}/${route.slug}/${route.gpx_file}`);
};

// Transformar la fecha en "10 de marzo de 2026"
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("es-ES", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(date);
};

// Transformar la fecha en "6h 10min"
const formatDuration = (seconds) => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return h > 0 ? `${h}h ${m}min` : `${m}min`;
};

// Saber que icono de ruta poner en funcion del tipo
const iconType = (route) => {
  switch (route.type) {
    case "Senderismo":
      return '<i class="fa-solid fa-person-hiking"></i>';
    case "Para-Todos":
      return '<i class="fa-solid fa-people-roof"></i>';
    case "Ciclismo":
      return '<i class="fa-solid fa-person-biking"></i>';
    case "Trail-Running":
      return '<i class="fa-solid fa-person-running"></i>';
    case "Alpinismo":
      return '<i class="fa-solid fa-mountain"></i>';
    default:
      return '<i class="fa-solid fa-question"></i>';
  }
};

// Mandar el HTML del icono de la Ruta
const routeType = (route) => {
  return `${iconType(route)} <p>${route.type}</p>`;
};

// Obtener la elevacion positiva y negativa media, las ultimas coordenadas y la elevacion max y min
const parseGPX = async (gpxUrl) => {
  const response = await fetch(gpxUrl);
  const text = await response.text();
  const xml = new DOMParser().parseFromString(text, "text/xml");
  const geojson = gpx(xml);

  const elevations = [];

  geojson.features.forEach((feature) => {
    if (feature.geometry.type === "LineString") {
      const coords = feature.geometry.coordinates;

      coords.forEach((coord) => {
        const ele = coord[2];
        if (typeof ele === "number") {
          elevations.push(ele);
        }
      });

      const last = coords[coords.length - 1];
      if (last) {
        lastCoord.value = {
          lat: last[1],
          lon: last[0],
        };
      }
    }
  });

  return calculateElevationGainLoss(elevations);
};

// Calcula la elevacion
const calculateElevationGainLoss = (elevations) => {
  let gain = 0;
  let loss = 0;

  for (let i = 1; i < elevations.length; i++) {
    const diff = elevations[i] - elevations[i - 1];
    if (diff > 0) gain += diff;
    else if (diff < 0) loss -= diff;
  }

  return {
    ascent: Math.round(gain),
    descent: Math.round(loss),
    maxElevation: Math.max(...elevations).toFixed(1),
    minElevation: Math.min(...elevations).toFixed(1),
  };
};

// Funcion para guardar una ruta en favoritos
const toggleFavorite = async () => {
  try {
    // Eliminar de favoritos
    if (isFavorite.value) {
      await apiWithAuth().delete(`/favorites/${favoriteId.value}/`);
      isFavorite.value = false;
      favoriteId.value = null;

      // Añadir a favoritos
    } else {
      const response = await apiWithAuth().post(`/favorites/`, {
        user: currentUserId.value,
        route: route.value.id,
      });
      isFavorite.value = true;
      favoriteId.value = response.data.id;
    }
  } catch (error) {
    console.error("Error en toggle de favoritos:", error);
  }
};

// Funcion que comprueba si una ruta esta en favoritos o no
const checkIfFavorite = async () => {
  if (!isAuthenticated.value) return;

  try {
    const response = await apiWithAuth().get(
      `/favorites/?user=${currentUserId.value}&route=${route.value.id}`,
    );
    if (response.data.length > 0) {
      isFavorite.value = true;
      favoriteId.value = response.data[0].id;
    } else {
      isFavorite.value = false;
      favoriteId.value = null;
    }
  } catch (error) {
    console.error("Error comprobando favoritos:", error);
  }
};

// Funcion que permite actualizar los datos de la Ruta
const refreshRouteData = async () => {
  try {
    const response = await api.get(`/routes/${props.id}/`);
    route.value = response.data;
    elevationData.value = await parseGPX(getGPXUrl(route.value));
    imgRoute.value = await getRouteAllImgURL(route.value);
  } catch (error) {
    console.error("Error recargando los datos de la ruta:", error);
  }
};

// Realiza la llamada a la API para obtener los datos de la Ruta
onMounted(async () => {
  await refreshRouteData();
  await checkIfFavorite();
});
</script>

<style lang="scss">
.description-route {
  ol {
    list-style: normal;
    padding-left: 2rem;

    li {
      padding-left: 0.25rem;
    }
  }
}

.table-detail {
  article {
    padding-top: 0.25rem;
    border-bottom: 2px solid var(--color-grey);

    &:nth-child(1),
    &:nth-child(3),
    &:nth-child(5) {
      border-right: 2px solid var(--color-grey);
    }
  }
}
@media (max-width: 1280px) {
  .table-detail {
    article {
      height: 70 px;
    }
  }
}
</style>
