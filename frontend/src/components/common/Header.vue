<template>
  <nav
    :class="[{ 'hero-nav': route.name === 'Home' || route.name === 'AboutUs' }]"
    class="relative z-5 flex min-h-30 justify-between bg-black shadow-xl/30 transition-colors duration-500"
  >
    <router-link to="/" class="self-center p-1 sm:p-4">
      <ResponsiveImage
        :info="['LogoHikelink', 'logo']"
        :formats="['svg', 'png']"
        alt="Logo Header"
        class="w-30 transition-all duration-250 hover:scale-95 sm:w-40"
      />
    </router-link>

    <div class="flex items-center justify-center">
      <button
        class="flex cursor-pointer items-center justify-center border-none bg-none text-5xl text-white transition-all duration-250 hover:scale-85"
        v-if="isMobile"
        @click="toggleMainMenu"
      >
        <i class="fa-solid fa-bars"></i>
      </button>

      <transition name="fade-dropdown">
        <div
          v-if="!isMobile || showMainMenu"
          class="links bg-black-50 absolute top-30 right-0 flex flex-col items-center rounded-bl p-1 shadow-xl/30 lg:relative lg:top-0 lg:flex-row lg:justify-end lg:rounded-none lg:bg-transparent lg:p-0 lg:shadow-none"
        >
          <router-link to="/map" class="font-montserrat-bold text-xl">Mapa</router-link>
          <router-link to="/search-routes" class="font-montserrat-bold text-xl"
            >Buscar Ruta</router-link
          >
          <router-link to="/foro" class="font-montserrat-bold text-xl">Foro</router-link>
        </div>
      </transition>

      <LoginButton :menuOpen="showUserMenu" @toggle-user-menu="handleUserMenuToggle" />
    </div>
  </nav>
</template>

<script setup>
// IMPORTS
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import { useRoute } from "vue-router";
import ResponsiveImage from "../images/ResponsiveImage.vue";
import LoginButton from "../auth/LoginButton.vue";

// VARIABLES
const route = useRoute();

const showMainMenu = ref(false);
const showUserMenu = ref(false);
const isMobile = ref(window.innerWidth <= 1024);

// METODOS
// Funcion que detecta cuando se reduce el tamaño
const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 1024;
  if (!isMobile.value) {
    showMainMenu.value = false;
    showUserMenu.value = false;
  }
};

onMounted(() => {
  window.addEventListener("resize", updateIsMobile);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateIsMobile);
});

watch(
  () => route.fullPath,
  () => {
    showMainMenu.value = false;
    showUserMenu.value = false;
  },
);

const toggleMainMenu = () => {
  showMainMenu.value = !showMainMenu.value;
  if (showMainMenu.value) showUserMenu.value = false;
};

const handleUserMenuToggle = (isOpen) => {
  showUserMenu.value = isOpen;
  if (isOpen) showMainMenu.value = false;
};
</script>

<style lang="scss" scoped>
.hero-nav {
  background: var(--color-black-opacity);
  box-shadow: none;
  transition: background 0.5s ease;
}

.links {
  a {
    display: inline-block;
    position: relative;
    color: var(--color-white);
    text-decoration: none;
    margin: 1rem 2rem;
    transition: all 0.25s;

    &:hover {
      color: var(--color-light-green);
    }

    &::after {
      content: "";
      position: absolute;
      width: 100%;
      transform: translateX(-50%) scaleX(0);
      height: 2px;
      bottom: 0;
      left: 50%;
      background-color: var(--color-light-green);
      transform-origin: bottom center;
      transition: transform 0.25s ease-out;
    }

    &:hover::after {
      transform: translateX(-50%) scaleX(1);
      transform-origin: bottom center;
    }
  }
}

.fade-dropdown-enter-active,
.fade-dropdown-leave-active {
  transition: all 0.25s ease;
}

.fade-dropdown-enter-from,
.fade-dropdown-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.fade-dropdown-enter-to,
.fade-dropdown-leave-from {
  opacity: 1;
  transform: translateX(0);
}
</style>
