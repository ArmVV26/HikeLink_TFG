<template>
  <main class="mx-auto my-6 flex w-[95%] flex-col gap-6 xl:grid xl:grid-cols-[20rem_1fr]">
    <article class="border-b-green flex border-b-5 xl:hidden">
      <button
        class="font-montserrat-bold bg-green hover:text-light-green flex cursor-pointer items-center gap-2 rounded-t-3xl p-2 text-xl text-white transition-all duration-300"
        @click="toggleFilters"
      >
        <i class="fa-solid fa-filter"></i>
        <p>Filtrar Rutas</p>
      </button>
    </article>

    <transition name="fade-slide">
      <section
        class="bg-vanille xl:bg-vanille-50 absolute top-48 z-10 h-124 rounded-b-3xl p-4 shadow-[3px_3px_0px_3px_rgb(141,_110,_99)] xl:relative xl:top-0 xl:h-140 xl:rounded-xl"
        :class="{ active: showFilters }"
        ref="filterRef"
        v-show="showFilters"
      >
        <article class="mb-4 hidden items-center justify-center gap-2 text-2xl xl:flex">
          <i class="fa-solid fa-filter text-green"></i>
          <h1 class="font-montserrat-bold">Filtrar Por</h1>
        </article>

        <form @submit.prevent="filterRoutes" class="flex flex-col gap-4">
          <input
            type="text"
            v-model="title"
            class="border-brown hover:border-green m-auto w-[90%] rounded-lg border-2 bg-white px-3 py-2 text-base text-black"
            placeholder="Buscar Ruta"
          />

          <article>
            <label for="type">Tipo </label>
            <select id="type" name="type" v-model="type">
              <option value="Todas">Todas</option>
              <option value="Para-Todos">Para Todos</option>
              <option value="Senderismo">Senderismo</option>
              <option value="Ciclismo">Ciclismo</option>
              <option value="Trail-Running">Trail-Running</option>
              <option value="Alpinismo">Alpinismo</option>
            </select>
          </article>

          <article>
            <label for="difficulty">Dificultad </label>
            <select id="difficulty" name="difficulty" v-model="difficulty">
              <option value="Todas">Todas</option>
              <option value="Fácil">Fácil</option>
              <option value="Moderada">Moderada</option>
              <option value="Difícil">Difícil</option>
            </select>
          </article>

          <article>
            <label for="origin">Origen </label>
            <select id="origin" name="origin" v-model="origin">
              <option value="Todos">Todos</option>
              <option value="Wikiloc">Wikiloc</option>
              <option value="Strava">Strava</option>
              <option value="OutdoorActive">OutdoorActive</option>
              <option value="AllTrails">AllTrails</option>
              <option value="Komoot">Komoot</option>
            </select>
          </article>

          <article class="mx-4 flex w-full flex-col items-center justify-center">
            <label class="font-montserrat-bold text-green self-start">Duración (horas):</label>
            <Slider
              class="mt-4 w-[70%]"
              v-model="durationRange"
              :min="0"
              :max="24"
              :step="1"
              :range="true"
            />
            <span class="mt-1 font-bold text-black"
              >{{ durationRange[0] }}h - {{ durationRange[1] }}h</span
            >
          </article>

          <article class="mx-4 flex w-full flex-col items-center justify-center">
            <label class="font-montserrat-bold text-green self-start">Longitud (km):</label>
            <Slider
              class="mt-4 w-[70%]"
              v-model="distanceRange"
              :min="0"
              :max="100"
              :step="1"
              :range="true"
            />
            <span class="mt-1 font-bold text-black"
              >{{ distanceRange[0] }}km - {{ distanceRange[1] }}km</span
            >
          </article>

          <button
            type="submit"
            class="bg-green hover:bg-light-green hover:text-green m-auto w-[90%] cursor-pointer rounded-3xl px-3 py-2 text-xl font-bold text-white transition-all duration-300"
          >
            Buscar
          </button>
        </form>
      </section>
    </transition>

    <article v-if="routes.length" class="flex flex-col gap-6">
      <RouteCard
        :routes="routes"
        :current-page="currentPage"
        :total-pages="totalPages"
        @change-page="loadRoutes"
      />
    </article>

    <article v-else class="flex flex-col items-center justify-center">
      <i
        class="fa-solid fa-mountain-sun text-green text-[6rem] drop-shadow-[8px_5px_0px_0px_rgb(129,_199,_132)]"
      ></i>
      <h1 class="font-montserrat-bold text-green text-3xl">¡No se han encontrado rutas!</h1>
      <p class="mb-4">Modifica el filtro para buscar tus rutas deseadas</p>
    </article>
  </main>
</template>

<script setup>
// IMPORTS
import { onMounted, onBeforeUnmount, ref } from "vue";
import api from "@/utils/api";
import RouteCard from "@/components/map/RouteCard.vue";
import Slider from "@vueform/slider";
import "@vueform/slider/themes/default.css";

// VARIABLES
const title = ref("");
const type = ref("Todas");
const difficulty = ref("Todas");
const origin = ref("Todos");
const durationRange = ref([0, 24]);
const distanceRange = ref([0, 100]);

const routes = ref([]);

const showFilters = ref(false);
const filterRef = ref(null);

// Paginar
const totalPages = ref(1);
const currentPage = ref(1);
const pageSize = 5;

const isFiltering = ref(false);
const currentFilters = ref({});

// METODOS
// Funcion que detecta la redimension de la pagina para mostrar el menu de los filtros
const handleResize = () => {
  if (window.innerWidth > 1279) {
    showFilters.value = true;
  }
};

// Funcion para detectar si se clica fuera del contenedor
const handleClickOutside = (event) => {
  const filterEl = filterRef.value;
  const toggleEl = document.querySelector(".filter-toggle");

  if (
    window.innerWidth < 1279 &&
    filterEl &&
    !filterEl.contains(event.target) &&
    toggleEl &&
    !toggleEl.contains(event.target)
  ) {
    showFilters.value = false;
  }
};

// Funcion para mostrar o ocultar las rutas
const toggleFilters = () => {
  showFilters.value = !showFilters.value;
};

// Funcion que recarga las rutas si hay filtro o si no hay filtro
const loadRoutes = async (page = 1) => {
  try {
    let response;

    if (isFiltering.value) {
      const params = new URLSearchParams(currentFilters.value);
      params.append("page", page);
      params.append("page_size", pageSize);

      response = await api.get(`/filter-routes/?${params.toString()}`);
    } else {
      response = await api.get(`/all-routes/?page=${page}&page_size=${pageSize}`);
    }

    routes.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / pageSize);
    currentPage.value = page;

    if (window.innerWidth < 1279) showFilters.value = false;
  } catch (error) {
    console.error("Error al cargar las rutas:", error);
  }
};

// Funcion para buscar las rutas
const filterRoutes = async () => {
  const params = new URLSearchParams();

  if (title.value) params.append("title", title.value);
  if (type.value !== "Todas") params.append("type", type.value);
  if (difficulty.value !== "Todas") params.append("difficulty", difficulty.value);
  if (origin.value !== "Todos") params.append("origin", origin.value);

  params.append("duration_min", durationRange.value[0] * 3600);
  params.append("duration_max", durationRange.value[1] * 3600);
  params.append("distance_min", distanceRange.value[0] * 1000);
  params.append("distance_max", distanceRange.value[1] * 1000);

  currentFilters.value = Object.fromEntries(params.entries());
  isFiltering.value = true;

  await loadRoutes(1);
};

// Para cargar todas las rutas al principio o al recargar la pagina
onMounted(async () => {
  window.addEventListener("resize", handleResize);
  document.addEventListener("click", handleClickOutside);
  handleResize();

  try {
    loadRoutes();
  } catch (error) {
    console.error("Error al cargar las rutas: ", error);
  }
});

// Funcion para detectar si se clica fuera del menu de filtros
onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style lang="scss" scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.main-container {
  width: 95%;
  margin: 2rem auto;
  display: grid;
  grid-template-columns: 20rem 1fr;
  gap: 2rem;
}

form {
  article {
    margin: 0 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;

    label {
      font-family: "Montserrat-Bold";
      color: var(--color-green);
    }

    select {
      margin-left: 1rem;
      padding: 0.5rem 0.75rem;
      color: var(--color-black);
      border: 2px solid var(--color-brown);
      background-color: var(--color-white);
      border-radius: 25px;

      &:hover {
        border: 2px solid var(--color-green);
      }
    }
  }
}
</style>

<style lang="scss">
.slider-tooltip {
  background-color: var(--color-green);
  border-color: var(--color-green);
  color: var(--color-white);
  padding: 1px 5px;
  border-radius: 5px;
  font-weight: bold;
  font-size: 0.75rem;

  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.slider-connect {
  background-color: var(--color-light-green);
}

.slider-handle {
  border: 2px solid var(--color-green);
  background-color: var(--color-white);

  &:hover,
  &:focus,
  &:active {
    .slider-tooltip {
      opacity: 1;
    }
  }
}
</style>
