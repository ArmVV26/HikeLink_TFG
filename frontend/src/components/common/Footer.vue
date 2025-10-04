<template>
  <footer class="flex flex-col">
    <section class="bg-brown flex flex-col items-center justify-center gap-8 py-8 lg:flex-row">
      <router-link to="/">
        <ResponsiveImage
          :info="['footer-LogoHikelink', 'logo']"
          :formats="['svg', 'png']"
          alt="Logo Footer"
          class="h-auto w-55"
        />
      </router-link>

      <nav class="flex flex-col items-center justify-center lg:items-start">
        <h2 class="font-montserrat-bold text-2xl text-white text-shadow-lg/30 sm:text-4xl">
          Explora
        </h2>
        <article class="flex flex-col items-center text-lg sm:text-xl lg:items-start lg:pl-4">
          <router-link
            to="/map"
            class="text-grey font-bold transition-all duration-300 hover:text-white hover:text-shadow-lg/30"
            >Mapa</router-link
          >
          <router-link
            to="/search-routes"
            class="text-grey font-bold transition-all duration-300 hover:text-white hover:text-shadow-lg/30"
            >Buscar Ruta</router-link
          >
          <router-link
            to="/foro"
            class="text-grey font-bold transition-all duration-300 hover:text-white hover:text-shadow-lg/30"
            >Foro</router-link
          >
        </article>
      </nav>

      <nav class="flex flex-col items-center justify-center lg:items-start">
        <h2 class="font-montserrat-bold text-2xl text-white text-shadow-lg/30 sm:text-4xl">
          HikeLink
        </h2>
        <article class="flex flex-col items-center pl-4 text-lg sm:text-xl lg:items-start">
          <router-link
            to="/about-us"
            class="text-grey font-bold transition-all duration-300 hover:text-white hover:text-shadow-lg/30"
            >Sobre Nosotros</router-link
          >
          <a
            href="mailto:hikelink.soporte@gmail.com"
            class="text-grey font-bold transition-all duration-300 hover:text-white hover:text-shadow-lg/30"
            >Contacta con Nosotros</a
          >
          <router-link
            to="/help"
            class="text-grey font-bold transition-all duration-300 hover:text-white hover:text-shadow-lg/30"
            >Ayuda</router-link
          >
        </article>
      </nav>

      <nav class="grid grid-cols-2">
        <a href="https://www.instagram.com/hikelink" target="_blank">
          <i
            class="fa-brands fa-instagram hover:text-light-green text-6xl text-white transition-all duration-300"
          ></i>
        </a>
        <a href="https://www.youtube.com/hikelink" target="_blank">
          <i
            class="fa-brands fa-youtube hover:text-light-green text-6xl text-white transition-all duration-300"
          ></i>
        </a>
        <a href="https://es.pinterest.com/hikelink" target="_blank">
          <i
            class="fa-brands fa-pinterest hover:text-light-green text-6xl text-white transition-all duration-300"
          ></i>
        </a>
        <a href="https://www.facebook.com/hikelink" target="_blank">
          <i
            class="fa-brands fa-facebook hover:text-light-green text-6xl text-white transition-all duration-300"
          ></i>
        </a>
      </nav>
    </section>

    <section
      class="bg-vanille text-brown flex flex-col items-center justify-center px-5 py-2 text-sm sm:text-base md:flex-row md:justify-between"
    >
      <p><span class="font-bold">© HikeLink</span> - Todos los derechos reservados.</p>

      <nav class="flex gap-6">
        <router-link to="/condition-use" class="hover:font-bold hover:underline"
          >Condiciones de Uso</router-link
        >
        <router-link to="/privacity" class="hover:font-bold hover:underline"
          >Política de Privacidad</router-link
        >
      </nav>
    </section>
  </footer>
</template>

<script setup>
// IMPORTS
import ResponsiveImage from "@/components/images/ResponsiveImage.vue";
</script>
