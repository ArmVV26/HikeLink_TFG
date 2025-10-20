<template>
  <HeroImage name="PaginaPrincipal">
    <h1>Explora. Comparte. Conecta.</h1>
    <h2>¿Quieres saber como funciona HikeLink?</h2>
    <CommonButton :samePage="true" :header="true" :text="'Saber Más'" :route="'#tutorial'" />
  </HeroImage>

  <RouteCarousel :routes="topRoutes" />

  <section class="bg-light-green-50 my-10 w-full py-16">
    <article
      class="mx-6 flex flex-col justify-center gap-2 lg:mx-auto lg:grid lg:grid-cols-[38rem_20rem] lg:gap-6"
    >
      <ResponsiveImage
        :info="['decorative-PaginaPrincipal', 'img-decorative']"
        :formats="['jpg', 'webp']"
        imgClass=" rounded-3xl shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] saturate-90 brightness-95 contrast-120 sepia-10"
        alt="Imagen Historia HikeLink"
      />

      <aside class="flex flex-col items-center justify-center">
        <article class="flex flex-col text-center">
          <h1 class="font-montserrat-bold text-green text-xl sm:text-3xl">Nuestra Historia</h1>
          <p class="mt-4 mb-10 text-sm sm:text-base">
            HikiLink nació de la pasión por la montaña y la necesidad de tener un lugar donde
            compartir y descubrir rutas reales, contadas por quienes las han vivido. ¿Quieres saber
            cómo empezó todo?
          </p>
        </article>

        <article>
          <CommonButton :text="'Conoce Nuestra Historia'" :route="'/about-us'" />
        </article>
      </aside>
    </article>
  </section>

  <section
    id="tutorial"
    class="mx-4 mb-10 flex flex-col items-center justify-center gap-8 lg:flex-row"
  >
    <article
      class="border-grey bg-light-green-50 flex h-110 w-auto flex-col items-center justify-center rounded-3xl border-2 px-4 py-6 text-center shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:w-90"
    >
      <i class="fa-solid fa-map-location-dot text-green text-8xl"></i>
      <h1 class="font-montserrat-bold text-green text-2xl">Crea tu cuenta</h1>
      <p class="mt-6 text-sm sm:text-base">
        Regístrate gratis, crea tu perfil y únete a una comunidad de amantes de la montaña. Podrás
        explorar rutas subidas por otros usuarios y guardarlas en favoritos.
      </p>
    </article>

    <article
      class="border-grey bg-light-green-50 flex h-110 w-auto flex-col items-center justify-center rounded-3xl border-2 px-4 py-6 text-center shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:w-90 lg:mb-20"
    >
      <i class="fa-solid fa-file-arrow-up text-green text-8xl"></i>
      <h1 class="font-montserrat-bold text-green text-2xl">Sube tus rutas</h1>
      <p class="mt-6 text-sm sm:text-base">
        Guarda tus recorridos subiendo archivos GPX desde tu app favorita. Añade descripciones,
        fotos y deja tu huella en el mapa.
      </p>
    </article>

    <article
      class="border-grey bg-light-green-50 flex h-110 w-auto flex-col items-center justify-center rounded-3xl border-2 px-4 py-6 text-center shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:w-90"
    >
      <i class="fa-solid fa-people-group text-green text-8xl"></i>
      <h1 class="font-montserrat-bold text-green text-2xl">Descubre y Conecta</h1>
      <p class="mt-6 text-sm sm:text-base">
        Busca nuevas rutas, comenta en el foro, deja valoraciones y comparte experiencias. HikiLink
        es una comunidad donde todos sumamos.
      </p>
    </article>
  </section>
</template>

<script setup>
// IMPORTS
import { ref, onMounted, computed } from "vue";
import HeroImage from "@/components/images/HeroImage.vue";
import CommonButton from "@/components/common/CommonButton.vue";
import RouteCarousel from "@/components/images/RouteCarousel.vue";
import ResponsiveImage from "@/components/images/ResponsiveImage.vue";
import api from "@/utils/api";

// VARIABLES
const routes = ref(null);
const topRoutes = computed(() => {
  return routes.value ? routes.value.slice(0, 5) : [];
});

// METODOS
// Funcion para obtener ordenadas por mayor rating
onMounted(async () => {
  try {
    const response = await api.get("/routes/");
    const sortedRoutes = response.data.sort((a, b) => b.average_rating - a.average_rating);
    routes.value = sortedRoutes;
  } catch (error) {
    console.error("Error cargando rutas:", error);
  }
});
</script>
