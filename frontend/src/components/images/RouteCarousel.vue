<template>
  <section v-if="!imgCarousel" class="my-6 flex w-full flex-col items-center justify-center">
    <h1 class="font-montserrat-bold text-green mb-2 text-3xl">Rutas Destacadas</h1>
    <article class="relative flex w-full items-center justify-center overflow-hidden">
      <button
        v-if="showButton"
        class="bg-green border-light-green hover:text-green z-6 mx-4 flex h-12 w-12 cursor-pointer items-center justify-center rounded-3xl border-2 text-2xl font-bold text-white transition-all duration-250 hover:bg-white max-[550px]:absolute max-[550px]:top-[30%] max-[550px]:left-0"
        @click="prevSlide(routes || imgUrls)"
      >
        <i class="fa-solid fa-arrow-left"></i>
      </button>

      <section
        class="carousel-overlay overflow-hidden p-1 max-[1150px]:p-[2px] max-[800px]:p-[1px]"
        :class="[
          'w-[calc(320px*3+2rem)] max-[1150px]:w-[calc(320px*2+1rem)] max-[800px]:w-[320px]',
        ]"
      >
        <section class="flex gap-3 will-change-transform" :style="trackStyle">
          <article
            class="carousel-card w-80 shrink-0 p-1 transition-all duration-250"
            v-for="route in routes"
            :key="route.id"
          >
            <router-link :to="{ name: 'RouteDetail', params: { id: route.id, slug: route.slug } }">
              <article class="relative overflow-hidden rounded-3xl">
                <div class="border-green h-40 overflow-hidden rounded-t-3xl border-4">
                  <img
                    :src="getRouteImg(route)"
                    @error="handleImgError"
                    class="block h-full w-full object-cover brightness-100 contrast-110 saturate-110 sepia-[0.1] filter transition-transform duration-250"
                    alt="Imagen de ruta"
                  />
                </div>
                <p
                  :title="route.title"
                  class="bg-green m-w-full overflow-hidden rounded-b-3xl px-4 text-xl font-bold text-nowrap text-ellipsis text-white text-shadow-lg/30"
                >
                  {{ route.title }}
                </p>
              </article>

              <article class="p-2">
                <p class="text-brown overflow-hidden text-base font-bold text-nowrap text-ellipsis">
                  Ruta de {{ route.user.username }}
                </p>
                <p
                  :title="`★ ${route.average_rating?.toFixed(1) || 'N/A'} · ${route.difficulty} · ${(route.distance / 1000).toFixed(1)} km · Est. ${formatDuration(route.duration)}`"
                  class="text-brown overflow-hidden text-base font-bold text-nowrap text-ellipsis"
                >
                  ★ {{ route.average_rating?.toFixed(1) || "N/A" }} · {{ route.difficulty }} ·
                  {{ (route.distance / 1000).toFixed(1) }} km · Est.
                  {{ formatDuration(route.duration) }}
                </p>
              </article>
            </router-link>
          </article>
        </section>
      </section>

      <button
        v-if="showButton"
        class="bg-green border-light-green hover:text-green z-6 mx-4 flex h-12 w-12 cursor-pointer items-center justify-center rounded-3xl border-2 text-2xl font-bold text-white transition-all duration-250 hover:bg-white max-[550px]:absolute max-[550px]:top-[30%] max-[550px]:right-0"
        @click="nextSlide(routes || imgUrls)"
      >
        <i class="fa-solid fa-arrow-right"></i>
      </button>
    </article>
  </section>

  <section v-else-if="imgUrls && imgUrls.length > 0" class="flex flex-col">
    <article class="flex items-center justify-between">
      <h1 class="font-montserrat-bold text-green text-left text-2xl font-bold">Fotos de la Ruta</h1>
      <div class="text-center">
        <button
          @click="openLightbox(0)"
          class="font-montserrat-bold bg-green border-light-green hover:text-green hover:bg-light-green hover:border-green mb-2 cursor-pointer rounded-3xl border-2 px-4 py-2 text-xl text-white transition-all duration-250"
        >
          <i class="fa-solid fa-expand"></i> Ver en grande
        </button>
      </div>
    </article>
    <article class="flex justify-center">
      <div
        class="border-green relative flex w-[calc(320px*3+7rem)] items-center overflow-hidden rounded-3xl border-5"
      >
        <div
          class="flex cursor-grab overflow-x-auto will-change-transform select-none [&::-webkit-scrollbar]:hidden"
          ref="carouselTrack"
          @mousedown="onDragStart"
          @mousemove="onDragging"
          @mouseup="onDragEnd"
          @mouseleave="onDragEnd"
          @touchstart="onTouchStart"
          @touchmove="onTouchMove"
          @touchend="onTouchEnd"
        >
          <div
            class="border-green flex h-60 w-90 flex-none border-r-4 last:border-r-0"
            v-for="imgUrl in imgUrls || []"
            :key="imgUrl"
          >
            <img
              :src="imgUrl"
              alt="Imagen de la Ruta"
              draggable="false"
              @dragstart.prevent
              class="pointer-events-none aspect-video h-full w-full object-cover"
            />
          </div>
        </div>
      </div>
    </article>
  </section>

  <VueEasyLightbox
    :visible="visible"
    :imgs="imgUrls"
    :index="lightboxIndex"
    @hide="visible = false"
  />
</template>

<script setup>
// IMPORTS
import { onMounted, onUnmounted, ref, computed, toRefs } from "vue";
import { useRouteImage } from "@/composables/useRouteImage";
import VueEasyLightbox from "vue-easy-lightbox";

// PROPS
const props = defineProps({
  imgCarousel: {
    type: Boolean,
    default: false,
  },
  routes: {
    type: Array,
  },
  imgUrls: {
    type: Array,
    default: [],
  },
});

// VARIABLES
const { imgCarousel, routes, imgUrls } = toRefs(props);

const currentIndex = ref(0);
const cardWidth = computed(() => (imgCarousel.value ? 490 : 336));
const cardGap = computed(() => (imgCarousel.value ? 4 : 1));
const visibleCount = ref(3);

const { getRouteImg, handleImgError } = useRouteImage();

const visible = ref(false);
const lightboxIndex = ref(0);

const carouselTrack = ref(null);
let isDragging = false;
let startX = 0;
let scrollLeft = 0;

// Permtie determinar si muestra o no los botones para mover el carousel
const showButton = computed(() => {
  if (imgCarousel.value && Array.isArray(imgUrls.value) && imgUrls.value.length <= 3) {
    return false;
  } else {
    return true;
  }
});

// Determina el estilo del carousel
const trackStyle = computed(() => {
  const totalOffset = currentIndex.value * (cardWidth.value + cardGap.value - 5);
  return {
    transform: `translateX(-${totalOffset}px)`,
    transition: "transform 0.5s ease-in-out",
  };
});

// METODOS
// Funciones para desplazar el corusel de imagenes con el raton
const onDragStart = (e) => {
  isDragging = true;
  startX = e.pageX;
  scrollLeft = carouselTrack.value.scrollLeft;
  carouselTrack.value.style.cursor = "grabbing";
};

const onDragging = (e) => {
  if (!isDragging) return;
  e.preventDefault();
  const x = e.pageX;
  const walk = (x - startX) * 1.5;
  carouselTrack.value.scrollLeft = scrollLeft - walk;
};

const onDragEnd = () => {
  isDragging = false;
  carouselTrack.value.style.cursor = "grab";
};

// Soporte móvil:
const onTouchStart = (e) => {
  isDragging = true;
  startX = e.touches[0].pageX - carouselTrack.value.offsetLeft;
  scrollLeft = carouselTrack.value.scrollLeft;
};

const onTouchMove = (e) => {
  if (!isDragging) return;
  const x = e.touches[0].pageX - carouselTrack.value.offsetLeft;
  const walk = (x - startX) * 1.5;
  carouselTrack.value.scrollLeft = scrollLeft - walk;
};

const onTouchEnd = () => {
  isDragging = false;
};

// Funcion para el lightbox
const openLightbox = (index) => {
  lightboxIndex.value = index;
  visible.value = true;
};

// Funcion que permite pasar de imagenes a la derecha
const nextSlide = (itemCount) => {
  if (itemCount.length <= visibleCount.value) return;

  currentIndex.value += 1;
  if (currentIndex.value > itemCount.length - visibleCount.value) {
    currentIndex.value = 0;
  }
};

// Funcion que permite pasar de imagenes a la izquierda
const prevSlide = (itemCount) => {
  if (itemCount.length <= visibleCount.value) return;

  currentIndex.value -= 1;
  if (currentIndex.value < 0) {
    currentIndex.value = itemCount.length - visibleCount.value;
  }
};

// Para reformular la duracion de la Ruta
const formatDuration = (seconds) => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return h > 0 ? `${h}h ${m}min` : `${m}min`;
};

// Funcion que actualiza las rutas visibles
const updateVisibleCount = () => {
  const width = window.innerWidth;
  if (width <= 800) {
    visibleCount.value = 1;
  } else if (width <= 1150) {
    visibleCount.value = 2;
  } else {
    visibleCount.value = 3;
  }
};

onMounted(() => {
  updateVisibleCount();
  window.addEventListener("resize", updateVisibleCount);
});

onUnmounted(() => {
  window.removeEventListener("resize", updateVisibleCount);
});
</script>

<style lang="scss" scoped>
.carousel-card {
  &:hover img {
    transform: scale(1.05);
  }
}

.carousel-overlay {
  position: relative;
  overflow: hidden;
}

.carousel-overlay::before,
.carousel-overlay::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 10px;
  pointer-events: none;
  z-index: 5;
}

.carousel-overlay::before {
  left: 0;
  background: linear-gradient(to right, white, transparent);
}

.carousel-overlay::after {
  right: 0;
  background: linear-gradient(to left, white, transparent);
}
</style>
