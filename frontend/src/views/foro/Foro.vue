<template>
  <main class="mx-auto w-full py-10 sm:w-[90%] lg:w-[80%] 2xl:w-[70%]">
    <section class="mx-2 mt-4 mb-2 flex items-center justify-between sm:mx-0">
      <form @submit.prevent="filterThreads">
        <input
          type="text"
          v-model="title"
          class="border-brown hover:border-green w-[70%] rounded-lg border-2 px-2 py-2 text-xs text-black sm:w-[90%] sm:text-base"
          placeholder="Buscar Hilo"
        />
      </form>

      <CommonButton
        :text="'Nuevo Hilo'"
        :icon="'fa-solid fa-plus'"
        :thin="true"
        :route="'/new-thread'"
        :disabled="!isAuthenticated"
      />
    </section>

    <article
      v-if="threads && threads.length"
      class="bg-vanille-50 py-4 shadow-[2px_2px_5px_1px_rgb(0,_0,_0)] sm:rounded-3xl sm:p-2"
    >
      <ThreadCard
        :threads="threads"
        :currentPage="currentPage"
        :totalPages="totalPages"
        @change-page="loadThreads"
      />
    </article>

    <article v-else class="flex flex-col items-center justify-center">
      <i
        class="fa-solid fa-comment text-green text-[6rem] drop-shadow-[8px_5px_0px_rgb(129,_199,_132)]"
      ></i>
      <h1 class="font-montserrat-bold text-green text-3xl">¡No se han encontrado hilos!</h1>
      <p class="mb-2">Modifica el filtro para buscar tus hilos deseadas</p>
    </article>
  </main>
</template>

<script setup>
// IMPORTS
import { onMounted, ref, computed } from "vue";
import api from "@/utils/api";
import ThreadCard from "@/components/foro/ThreadCard.vue";
import CommonButton from "@/components/common/CommonButton.vue";
import { useAuthStore } from "@/stores/authStore";

// VARIABLES
const title = ref("");

const threads = ref([]);

// Paginar
const totalPages = ref(1);
const currentPage = ref(1);
const pageSize = 5;

const isFiltering = ref(false);
const currentFilters = ref({});

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);

// METODOS
// Funcion que recarga los hilos si hay filtro o si no hay filtro
const loadThreads = async (page = 1) => {
  try {
    let response;

    if (isFiltering.value) {
      const params = new URLSearchParams(currentFilters.value);
      params.append("page", page);
      params.append("page_size", pageSize);

      response = await api.get(`/filter-threads/?${params.toString()}`);
    } else {
      response = await api.get(`/all-threads/?page=${page}&page_size=${pageSize}`);
    }

    threads.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / pageSize);
    currentPage.value = page;
  } catch (error) {
    console.error("Error al cargar los hilos:", error);
  }
};

// Funcion para buscar los hilos
const filterThreads = async () => {
  const params = new URLSearchParams();

  if (title.value) params.append("title", title.value);

  currentFilters.value = Object.fromEntries(params.entries());
  isFiltering.value = true;

  await loadThreads(1);
};

// Para cargar todos los hilos al principio o al recargar la pagina
onMounted(async () => {
  try {
    loadThreads();
  } catch (error) {
    console.error("Error al cargar los hilos: ", error);
  }
});
</script>
