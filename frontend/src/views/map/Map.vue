<template>
  <main class="relative h-full w-full">
    <ShowMap />

    <button
      class="question border-light-green absolute top-2 left-12 z-1 hidden cursor-pointer rounded-full border-2 bg-white px-3 py-2 text-white shadow-lg transition-all duration-200 lg:block"
      @click="openInfo"
    >
      <i class="fa-solid fa-circle-question text-green text-base transition-all duration-200"></i>
    </button>

    <transition name="fade">
      <section
        v-if="showInfo"
        class="absolute inset-0 z-2 flex flex-col items-center justify-center bg-black/50 p-6"
      >
        <div
          class="border-grey relative w-220 rounded-3xl border-2 bg-white text-center shadow-2xl"
        >
          <button
            class="text-brown hover:text-green absolute top-4 right-4 cursor-pointer"
            @click="closeInfo"
          >
            <i class="fa-solid fa-xmark text-2xl"></i>
          </button>

          <h1
            class="font-montserrat-bold border-dark-grey border-b-2 pt-4 pb-2 text-2xl text-black"
          >
            Consejos del Mapa
          </h1>

          <article class="bg-vanille-50 rounded-b-3xl pt-4">
            <h1 class="font-montserrat-bold text-green text-center text-lg italic">
              Explora el mapa sin límites
            </h1>
            <p class="w-full px-28 text-center text-sm text-black">
              El mapa es el corazón de HikeLink. Desde aquí podrás descubrir rutas increíbles,
              acceder a la información más relevante de cada punto y visualizar todo de una forma
              clara e interactiva. Para que saques el máximo partido a esta herramienta, te
              explicamos brevemente las funciones más destacadas del mapa:
            </p>

            <section class="mt-6 flex flex-wrap justify-center gap-6 pb-4">
              <article class="mt-18 w-100 text-center">
                <span class="text-green flex items-center justify-center text-[2rem]">
                  <i class="fa-solid fa-layer-group"></i>
                </span>
                <h1 class="font-montserrat-bold text-green text-base">Tipos de Mapa</h1>
                <p class="text-center text-sm text-black">
                  Este botón permite cambiar entre diferentes vistas del mapa.
                </p>
              </article>

              <article class="w-100 text-center">
                <header class="text-green flex items-center justify-center text-base">
                  <article class="border-light-green rounded-3xl border-2 bg-white px-3 text-sm">
                    <div class="flex items-center gap-2 font-bold text-green-600">
                      <i class="fa-solid fa-location-dot"></i>
                      <p>Wikiloc</p>
                    </div>
                    <div class="flex items-center gap-2 font-bold text-orange-600">
                      <i class="fa-solid fa-location-dot"></i>
                      <p>Strava</p>
                    </div>
                    <div class="flex items-center gap-2 font-bold text-yellow-600">
                      <i class="fa-solid fa-location-dot"></i>
                      <p>OutdoorActive</p>
                    </div>
                    <div class="flex items-center gap-2 font-bold text-purple-600">
                      <i class="fa-solid fa-location-dot"></i>
                      <p>AllTrails</p>
                    </div>
                    <div class="flex items-center gap-2 font-bold text-blue-600">
                      <i class="fa-solid fa-location-dot"></i>
                      <p>Komoot</p>
                    </div>
                  </article>
                </header>
                <h1 class="font-montserrat-bold text-green text-base">Leyenda del Mapa</h1>
                <p class="text-center text-sm text-black">
                  Leyenda para identificar rápidamente los distintos tipos de rutas.
                </p>
              </article>

              <article class="w-100 text-center">
                <span class="text-green flex items-center justify-center text-[2rem]">
                  <i class="fa-solid fa-circle-info"></i>
                </span>
                <h1 class="font-montserrat-bold text-green text-base">Información del Mapa</h1>
                <p class="text-center text-sm text-black">
                  Este botón despliega un menú que muestra diferente información sobre el mapa como:
                  el estilo del mapa actual, las fuentes del mapa, la licencia, etc.
                </p>
              </article>

              <article class="w-100 text-center">
                <span class="text-green flex items-center justify-center text-[2rem]">
                  <i class="fa-solid fa-expand"></i>
                </span>
                <h1 class="font-montserrat-bold text-green text-base">Pantalla Completa</h1>
                <p class="text-center text-sm text-black">
                  Este botón permite activar el modo pantalla completa para navegar por el mapa sin
                  distracciones y mayor comodidad
                </p>
              </article>
            </section>
          </article>
        </div>
      </section>
    </transition>
  </main>
</template>

<script setup>
// IMPORTS
import { ref, onMounted, onBeforeUnmount } from "vue";
import ShowMap from "@/components/map/ShowMap.vue";

// VARIABLES
const showInfo = ref(false);
const isDesktop = ref(window.innerWidth >= 1024);

// METODOS
const openInfo = () => (showInfo.value = true);
const closeInfo = () => (showInfo.value = false);

const handleKey = (e) => {
  if (e.key === "Escape" && showInfo.value) closeInfo();
};

const handleResize = () => {
  const wasDesktop = isDesktop.value;
  isDesktop.value = window.innerWidth >= 1024;

  if (!isDesktop.value) {
    showInfo.value = false;
  }
};

onMounted(() => {
  if (isDesktop.value) {
    showInfo.value = true;
  }

  window.addEventListener("keydown", handleKey);
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleKey);
  window.removeEventListener("resize", handleResize);
});
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

main {
  .question {
    &:hover {
      background-color: var(--color-brown);
      border: 2px solid var(--color-vanille);

      i {
        color: var(--color-white);
      }
    }
  }
}
</style>
