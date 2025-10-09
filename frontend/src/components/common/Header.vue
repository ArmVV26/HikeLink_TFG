<template>
  <nav
    :class="[headerTheme.background]"
    class="fixed top-0 z-50 flex h-20 w-full justify-between transition-all duration-500"
  >
    <!-- Logo -->
    <router-link to="/" class="logo m-1 flex items-center self-center p-1 select-none sm:m-4">
      <ResponsiveImage
        :info="['header-LogoHikelink', 'logo']"
        :formats="['svg', 'png']"
        alt="Logo Header"
        :figureClass="headerTheme.logo"
        imgClass="w-20 h-auto"
      />
      <h1
        :class="[headerTheme.text]"
        class="font-montserrat-bold ml-[-20px] hidden text-2xl sm:block"
      >
        HIKELINK
      </h1>
    </router-link>

    <!-- Menu -->
    <section class="flex items-center justify-center">
      <button
        :class="[headerTheme.text]"
        class="flex cursor-pointer items-center justify-center border-none bg-none text-5xl transition-all duration-300 hover:scale-85"
        v-if="isMobile"
        @click="toggleMainMenu"
      >
        <i class="fa-solid fa-bars"></i>
      </button>

      <transition name="fade-dropdown">
        <nav
          v-if="!isMobile || showMainMenu"
          :class="[menuTheme.background]"
          class="links absolute top-20 right-0 flex flex-col items-center rounded-bl-3xl p-1 transition-all duration-500 will-change-transform lg:relative lg:top-0 lg:flex-row lg:justify-end lg:rounded-none lg:p-0 lg:shadow-none"
        >
          <router-link to="/map" :class="[headerTheme.text]" class="font-montserrat-bold text-xl">
            Mapa
          </router-link>
          <router-link
            to="/search-routes"
            :class="[headerTheme.text]"
            class="font-montserrat-bold text-xl"
          >
            Buscar Ruta
          </router-link>
          <router-link to="/foro" :class="[headerTheme.text]" class="font-montserrat-bold text-xl">
            Foro
          </router-link>
        </nav>
      </transition>

      <LoginButton
        :menuOpen="showUserMenu"
        @toggle-user-menu="handleUserMenuToggle"
        :is-scrolled="isScrolled"
      />
    </section>
  </nav>
</template>

<script setup>
// IMPORTS
import { onMounted, onBeforeUnmount, ref, watch, computed } from "vue";
import { useRoute } from "vue-router";
import ResponsiveImage from "@/components/images/ResponsiveImage.vue";
import LoginButton from "@/components/auth/LoginButton.vue";

// VARIABLES
const route = useRoute();

const showMainMenu = ref(false);
const showUserMenu = ref(false);
const isMobile = ref(window.innerWidth <= 1024);
const isScrolled = ref(false);

// METODOS
// Funcion que detecta cuando se reduce el tamaño
const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 1024;
  if (!isMobile.value) {
    showMainMenu.value = false;
    showUserMenu.value = false;
  }
};

// Detectar Scroll
const handleScroll = () => {
  isScrolled.value = window.scrollY > 0;
};

onMounted(() => {
  window.addEventListener("resize", updateIsMobile);
  window.addEventListener("scroll", handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateIsMobile);
  window.addEventListener("scroll", handleScroll);
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

// Configuracion del color de fondo, los textos y el logo
const headerTheme = computed(() => {
  const currentRoute = route.name;

  if (currentRoute === "Home" || currentRoute === "AboutUs") {
    return {
      background: isScrolled.value
        ? "backdrop-blur-md bg-black/50"
        : "bg-gradient-to-b from-black/40 to-transparent",
      text: "text-white",
      logo: "",
    };
  } else {
    return {
      background: "bg-bg/50 backdrop-blur-md shadow-sm",
      text: "text-green",
      logo: "drop-shadow-[0px_0px_1px_rgb(0,0,0)]",
    };
  }
});

// Configuracion del menu desplegable
const menuTheme = computed(() => {
  const currentRoute = route.name;

  if (isMobile.value) {
    if (currentRoute === "Home" || currentRoute === "AboutUs") {
      return {
        background: isScrolled.value ? "backdrop-blur-md bg-black" : "bg-transparent",
      };
    } else {
      return {
        background: "bg-bg backdrop-blur-md shadow-sm",
      };
    }
  }

  return { background: "" };
});
</script>

<style lang="scss" scoped>
.links {
  a {
    display: inline-block;
    position: relative;
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

.fade-dropdown-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.fade-dropdown-enter-to {
  opacity: 1;
  transform: translateX(0);
}

.fade-dropdown-leave-from {
  opacity: 1;
  transform: translateX(0);
}

.fade-dropdown-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>

<style lang="scss">
#fullsun {
  opacity: 0;
  visibility: hidden;
  transform: translateX(0);
  transition:
    opacity 0.25s ease,
    visibility 0.3s ease,
    transform 0.3s ease;
}

.logo:hover #fullsun {
  opacity: 1;
  visibility: visible;
  transform: translateX(-70px);
}

#sun {
  opacity: 1;
  visibility: visible;
  transition:
    opacity 0.3s ease,
    visibility 0.3s ease,
    transform 0.3s ease;
}

.logo:hover #sun {
  opacity: 0;
  visibility: hidden;
  transform: translateX(-70px);
}
</style>
