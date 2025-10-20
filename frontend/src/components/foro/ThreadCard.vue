<template>
  <main class="flex flex-col gap-4">
    <section
      class="bg-white px-2 py-4 shadow-[0px_0px_6px_0px_rgb(0,_0,_0)] transition-all duration-300 hover:scale-99 sm:rounded-3xl"
      v-for="thread in paginatedThreads"
      :key="thread.id"
    >
      <router-link
        :to="{ name: 'ThreadDetail', params: { id: thread.id, slug: thread.slug } }"
        class="flex flex-col gap-1 md:grid md:grid-cols-[10rem_1fr_8rem]"
      >
        <article class="flex flex-col items-center gap-2">
          <img
            :src="getIconUserThread(thread.user)"
            @error="handleImgError"
            class="border-green h-20 w-20 rounded-3xl border-2 object-cover"
            alt="Imagen del Usuario"
          />
          <h1 class="font-montserrat-bold text-green text-lg lg:text-2xl">
            {{ thread.user.username }}
          </h1>
        </article>

        <article class="relative flex min-w-0 flex-col pb-6">
          <h1
            class="font-montserrat-bold text-green line-clamp-2 text-center text-xl leading-tight text-ellipsis sm:text-left lg:text-3xl"
          >
            {{ thread.title }}
          </h1>
          <p class="my-2 line-clamp-3 max-w-full indent-8 text-sm text-ellipsis sm:text-base">
            {{ thread.content }}
          </p>
          <p class="text-light-green absolute bottom-0 left-0 text-right text-sm font-bold">
            {{ formatDate(thread.created_date) }}
          </p>
        </article>

        <article class="flex items-center justify-center gap-2">
          <i
            class="fa-solid fa-comment text-green drop-shadow-light-green text-4xl drop-shadow-sm"
          ></i>
          <p class="text-xl font-bold italic">{{ thread.comments_count }}</p>
        </article>
      </router-link>
    </section>

    <!-- Paginacion -->
    <section class="my-4 flex items-center justify-center gap-2">
      <button
        @click="emit('change-page', props.currentPage - 1)"
        :disabled="props.currentPage === 1"
        class="border-green hover:bg-green tranext-wsition-all hover:thite cursor-pointer rounded-3xl border-2 bg-white px-2 py-1 text-sm duration-300 disabled:hidden sm:px-4 sm:py-2 sm:text-lg"
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
import { useUserThreadImage } from "@/composables/useUserImage";

// PROPS
const props = defineProps({
  threads: {
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

const { getIconUserThread, handleImgError } = useUserThreadImage();

// Paginas a mostrar en una pagina
const paginatedThreads = computed(() => props.threads);

// WATCHER
watch(
  () => props.threads.length,
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
