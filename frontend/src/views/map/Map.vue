<template>
  <ShowMap />

  <main class="bg-vanille-50 flex flex-col items-center justify-center p-6">
    <h1 class="font-montserrat-bold text-green text-2xl italic">Explora el mapa sin límites</h1>
    <p class="text-brown w-full text-center text-base font-bold md:w-160">
      El mapa es el corazón de HikeLink. Desde aquí podrás descubrir rutas increíbles, acceder a la
      información más relevante de cada punto y visualizar todo de una forma clara e interactiva.
      Para que saques el máximo partido a esta herramienta, te explicamos brevemente las funciones
      más destacadas del mapa:
    </p>

    <section class="mb-4 flex flex-wrap justify-center gap-6">
      <article class="w-full text-center sm:w-100">
        <span class="text-green flex h-30 items-center justify-center text-[3rem]">
          <i class="fa-solid fa-circle-info"></i>
        </span>
        <h1 class="font-montserrat-bold text-green text-xl">Información del Mapa</h1>
        <p class="text-brown text-center text-base font-bold">
          Este botón despliega un menú que muestra diferente información sobre el mapa como: el
          estilo del mapa actual, las fuentes del mapa, la licencia, etc.
        </p>
      </article>

      <article class="w-full text-center sm:w-100">
        <span class="text-green flex h-30 items-center justify-center text-[3rem]">
          <i class="fa-solid fa-layer-group"></i>
        </span>
        <h1 class="font-montserrat-bold text-green text-xl">Tipos de Mapa</h1>
        <p class="text-brown text-center text-base font-bold">
          Este botón permite cambiar entre diferentes vistas del mapa.
        </p>
      </article>

      <article class="w-full text-center sm:w-100">
        <span class="text-green flex h-30 items-center justify-center text-[3rem]">
          <i class="fa-solid fa-expand"></i>
        </span>
        <h1 class="font-montserrat-bold text-green text-xl">Pantalla Completa</h1>
        <p class="text-brown text-center text-base font-bold">
          Este botón permite activar el modo pantalla completa para navegar por el mapa sin
          distracciones y mayor comodidad
        </p>
      </article>

      <article class="w-full text-center sm:w-100">
        <header class="text-green flex h-30 items-center justify-center text-base">
          <article class="border-light-green rounded-3xl border-2 bg-white px-3">
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-location-dot text-green-600"></i>
              <p class="font-black">Wikiloc</p>
            </div>
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-location-dot text-orange-600"></i>
              <p class="font-black">Strava</p>
            </div>
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-location-dot text-yellow-600"></i>
              <p class="font-black">OutdoorActive</p>
            </div>
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-location-dot text-purple-600"></i>
              <p class="font-black">AllTrails</p>
            </div>
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-location-dot text-blue-600"></i>
              <p class="font-black">Komoot</p>
            </div>
          </article>
        </header>
        <h1 class="font-montserrat-bold text-green text-xl">Leyenda del Mapa</h1>
        <p class="text-brown text-center text-base font-bold">
          Leyenda para identificar rápidamente los distintos tipos de rutas.
        </p>
      </article>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import ShowMap from "@/components/map/ShowMap.vue";
</script>
