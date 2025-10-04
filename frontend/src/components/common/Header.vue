<template>
  <nav
    :class="[
      {
        'bg-gradient-to-b from-black/40 to-transparent':
          route.name === 'Home' || route.name === 'AboutUs',
        'bg-black shadow-xl/30': route.name !== 'Home' && route.name !== 'AboutUs',
      },
    ]"
    class="relative z-5 flex min-h-20 justify-between transition-all duration-500"
  >
    <router-link
      to="/"
      class="flex items-center self-center p-1 transition-all duration-300 select-none hover:scale-95 sm:p-4"
    >
      <ResponsiveImage
        :info="['header-LogoHikelink', 'logo']"
        :formats="['svg', 'png']"
        alt="Logo Header"
        class="w-22"
      />
      <h1 class="font-montserrat-bold ml-[-16px] hidden text-2xl text-white sm:block">HIKELINK</h1>
    </router-link>

    <section class="flex items-center justify-center">
      <button
        class="flex cursor-pointer items-center justify-center border-none bg-none text-5xl text-white transition-all duration-300 hover:scale-85"
        v-if="isMobile"
        @click="toggleMainMenu"
      >
        <i class="fa-solid fa-bars"></i>
      </button>

      <transition name="fade-dropdown">
        <nav
          v-if="!isMobile || showMainMenu"
          :class="[
            {
              'backdrop-blur-sm': (route.name === 'Home' || route.name === 'AboutUs') && isMobile,
              'bg-black shadow-lg/30': route.name !== 'Home' && route.name !== 'AboutUs',
            },
          ]"
          class="links absolute top-20 right-0 flex flex-col items-center rounded-bl-3xl p-1 lg:relative lg:top-0 lg:flex-row lg:justify-end lg:rounded-none lg:bg-transparent lg:p-0 lg:shadow-none"
        >
          <router-link to="/map" class="font-montserrat-bold text-xl">Mapa</router-link>
          <router-link to="/search-routes" class="font-montserrat-bold text-xl"
            >Buscar Ruta</router-link
          >
          <router-link to="/foro" class="font-montserrat-bold text-xl">Foro</router-link>
        </nav>
      </transition>

      <LoginButton :menuOpen="showUserMenu" @toggle-user-menu="handleUserMenuToggle" />
    </section>
  </nav>
</template>

<script setup>
// IMPORTS
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import { useRoute } from "vue-router";
import ResponsiveImage from "@/components/images/ResponsiveImage.vue";
import LoginButton from "@/components/auth/LoginButton.vue";

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
  transform: translateY(-10px);
}

.fade-dropdown-enter-to,
.fade-dropdown-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
