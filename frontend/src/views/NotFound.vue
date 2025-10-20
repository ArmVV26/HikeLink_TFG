<template>
  <main class="flex h-full items-center justify-center py-10">
    <section
      class="w-full bg-white px-1 py-8 text-center shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:w-120 sm:rounded-3xl sm:px-4"
    >
      <h1 class="text-green text-6xl sm:text-8xl">404</h1>
      <h2 class="text-xl sm:text-3xl">¡Ups! Página no encontrada</h2>
      <p class="my-2 text-sm sm:text-base">
        Lo sentimos, la página que estás buscando no existe o ha sido movida. Puedes volver a la
        página principal o intentar buscar lo que necesitas.
      </p>
      <router-link
        to="/"
        class="bg-green mt-6 inline-flex items-center gap-2 rounded-3xl px-4 py-2 text-white transition-all duration-300 hover:translate-y-[-2px] hover:shadow-[0px_4px_8px_rgba(0,_0,_0,_0.1)]"
      >
        <i class="fa-solid fa-house text-xl"></i>
        Volver al inicio
      </router-link>
    </section>
  </main>
</template>
