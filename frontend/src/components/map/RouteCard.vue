<template>
  <main class="flex flex-col gap-4">
    <section
      class="rounded-3xl p-2 shadow-[2px_2px_5px_1px_rgb(0,_0,_0)] transition-all duration-300 hover:scale-99"
      v-for="route in paginatedRoutes"
      :key="route.id"
    >
      <router-link
        :to="{ name: 'RouteDetail', params: { id: route.id, slug: route.slug } }"
        class="flex flex-col-reverse gap-2 lg:grid lg:grid-cols-[25rem_1fr]"
      >
        <article class="relative flex flex-col gap-2">
          <img
            :src="getRouteImg(route)"
            @error="handleImgError"
            class="border-green h-60 w-full rounded-3xl border-4 object-cover md:h-80 lg:h-40"
            alt="Imagen de la Ruta"
          />
          <article
            class="bg-green absolute right-2 bottom-2 flex items-center gap-2 rounded-3xl px-2 py-1 shadow-xl lg:relative lg:right-auto lg:bottom-auto lg:bg-transparent lg:p-0 lg:shadow-transparent"
          >
            <img
              :src="getIconRouteImg(route.user)"
              @error="handleImgUserError"
              class="border-light-green lg:border-green h-10 w-10 rounded-3xl border-2 object-cover lg:h-20 lg:w-20"
              alt="Imagen del Usuario"
            />
            <p class="font-montserrat-bold kg:text-base text-sm text-white lg:text-black">
              {{ route.user.username }}
            </p>
          </article>
        </article>

        <article class="relative flex min-w-0 flex-col">
          <h1
            :title="route.title"
            class="font-montserrat-bold text-green truncate text-center text-2xl leading-tight max-sm:text-xl lg:text-left"
          >
            {{ route.title }}
          </h1>
          <p class="font-montserrat-bold text-grey text-center text-lg lg:text-left">
            {{ route.type }}
          </p>
          <p class="text-light-green text-center font-bold lg:absolute lg:right-4 lg:bottom-2">
            {{ formatDate(route.created_date) }}
          </p>
          <span
            class="mt-4 mb-1 line-clamp-3 max-w-full overflow-hidden indent-6 text-ellipsis"
            v-html="route.description_html"
          ></span>
          <p
            :style="{ color: getColorByOrigin(route.origin) }"
            class="font-montserrat-bold text-base"
          >
            {{ route.origin }}
          </p>

          <article
            class="mt-2 flex flex-wrap justify-around gap-2 text-sm font-bold sm:text-base lg:justify-start lg:gap-8"
          >
            <p>{{ route.difficulty }}</p>
            <p>
              <i class="fa-solid fa-route text-green"></i>
              {{ (route.distance / 1000).toFixed(1) }} km
            </p>
            <p>
              <i class="fa-regular fa-clock"></i>
              {{ formatDuration(route.duration) }}
            </p>
            <p class="flex items-center">
              <i
                v-for="(star, index) in getRanting(route.average_rating)"
                :key="index"
                :class="star"
                class="text-amber-300 text-shadow-sm/30"
              ></i>
              <span class="ml-2">{{ route.average_rating }}</span>
            </p>
          </article>
        </article>
      </router-link>
    </section>

    <!-- Paginacion -->
    <section class="my-4 flex items-center justify-center gap-2">
      <button
        @click="emit('change-page', props.currentPage - 1)"
        :disabled="props.currentPage === 1"
        class="border-green hover:bg-green cursor-pointer rounded-3xl border-2 bg-white px-2 py-1 text-sm transition-all duration-300 hover:text-white disabled:hidden sm:px-4 sm:py-2 sm:text-lg"
      >
        <i class="fa-solid fa-less-than"></i>
      </button>

      <button
        v-for="page in paginationPages"
        :key="page"
        :disabled="page === '...'"
        :class="[
          'text-sm transition-all duration-300 sm:text-lg',
          {
            'bg-green text-white': page === props.currentPage,
            'bg-white': page !== props.currentPage && page !== '...',
            'text-brown cursor-default border-0 p-0 font-bold': page === '...',
            'border-green hover:bg-green cursor-pointer rounded-3xl border-2 px-2 py-1 hover:text-white sm:px-4 sm:py-2':
              page !== '...',
          },
        ]"
        @click="typeof page === 'number' && emit('change-page', page)"
      >
        {{ page }}
      </button>

      <button
        @click="emit('change-page', props.currentPage + 1)"
        :disabled="props.currentPage === props.totalPages"
        class="border-green hover:bg-green cursor-pointer rounded-3xl border-2 bg-white px-2 py-1 text-sm transition-all duration-300 hover:text-white disabled:hidden sm:px-4 sm:py-2 sm:text-lg"
      >
        <i class="fa-solid fa-greater-than"></i>
      </button>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { computed, watch } from "vue";
import { useRouteImage } from "@/composables/useRouteImage";
import { useUserRouteImage } from "@/composables/useUserImage";

// PROPS
const props = defineProps({
  routes: {
    type: Array,
    required: true,
  },
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
});

// VARIABLES
const maxVisiblePages = 5;

const emit = defineEmits(["change-page"]);

const { getIconRouteImg, handleImgUserError } = useUserRouteImage();
const { getRouteImg, handleImgError } = useRouteImage();

// Paginas a mostrar en una pagina
const paginatedRoutes = computed(() => props.routes);

// WATCHER
watch(
  () => props.routes.length,
  () => {
    const page = Math.min(props.currentPage, props.totalPages);
    emit("change-page", page < 1 ? 1 : page);
  },
);

// METODOS
// Funcion para determinar el numero de paginas que se muestran en el pagination
const paginationPages = computed(() => {
  const pages = [];
  const total = props.totalPages;
  const current = props.currentPage;

  if (total <= maxVisiblePages) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    pages.push(1);

    if (current > 3) {
      pages.push("...");
    }

    const start = Math.max(2, current - 1);
    const end = Math.min(total - 1, current + 1);

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }

    if (current < total - 2) {
      pages.push("...");
    }

    pages.push(total);
  }

  return pages;
});

// Obtener el Origen reformulado de la ruta
const getColorByOrigin = (origin) => {
  switch (origin) {
    case "Wikiloc":
      return "green";
    case "Strava":
      return "red";
    case "OutdoorActive":
      return "orange";
    case "AllTrails":
      return "violet";
    case "Komoot":
      return "blue";
    default:
      return "gray";
  }
};

// Transformar la fecha en "1h 10min"
const formatDuration = (seconds) => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return h > 0 ? `${h}h ${m}min` : `${m}min`;
};

// Obtener el numero de estrellas que tiene la ruta en funcion del average_rating
const getRanting = (rating) => {
  const stars = [];
  const rounded = Math.round(rating * 2) / 2;

  for (let i = 1; i <= 5; i++) {
    if (i <= rounded) {
      stars.push("fas fa-star");
    } else if (i - 0.5 === rounded) {
      stars.push("fas fa-star-half-alt");
    } else {
      stars.push("far fa-star");
    }
  }
  return stars;
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
</script>
