<template>
  <section v-if="authStore.isAuthResolved">
    <CommonButton
      v-if="!authStore.isAuthenticated"
      :header="false"
      :text="'Iniciar Sesión'"
      :route="'/login'"
      class="color-white mr-2 ml-2 text-2xl sm:mr-4 sm:ml-4"
    />

    <article v-else>
      <button
        class="m-4 flex cursor-pointer items-center justify-center gap-2"
        @click="toggleMenu"
        @mouseenter="isHovered = true"
        @mouseleave="isHovered = false"
      >
        <img
          :src="getIconUserImg"
          @error="handleImgError"
          :class="[
            'h-12 w-12 rounded-3xl border-2 object-cover transition-all duration-200',
            {
              'border-light-green': isHovered || props.menuOpen,
              'border-transparent': !isHovered && !props.menuOpen,
            },
          ]"
          ref="userImg"
        />

        <i
          class="fa-solid fa-chevron-down text-xl transition-transform duration-300"
          :class="[{ 'rotate-180': isHovered || props.menuOpen }, menuTheme.icon]"
        ></i>
      </button>

      <transition name="fade-dropdown">
        <nav
          v-if="menuOpen"
          :class="[menuTheme.background]"
          class="absolute top-21 right-1 flex w-46 flex-col rounded-3xl pb-2 transition-all duration-200"
        >
          <h1
            :class="[menuTheme.username]"
            class="font-montserrat-bold pt-1 text-center text-lg font-bold"
          >
            {{ authStore.user.username }}
          </h1>

          <router-link
            :to="`/profile/${authStore.user.username}-${authStore.user.id}`"
            :class="[menuTheme.text]"
            class="font-montserrat-bold hover:text-light-green cursor-pointer transition-all duration-300"
          >
            Mi Perfil
          </router-link>

          <router-link
            to="/upload-route"
            :class="[menuTheme.text]"
            class="font-montserrat-bold hover:text-light-green cursor-pointer transition-all duration-300"
          >
            Subir Ruta
          </router-link>

          <router-link
            @click="authStore.logout"
            to="/"
            :class="[menuTheme.text]"
            class="font-montserrat-bold hover:text-light-green cursor-pointer transition-all duration-300"
          >
            Cerrar Sesión
          </router-link>
        </nav>
      </transition>
    </article>
  </section>
</template>

<script setup>
// IMPORTS
import { computed, ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useUserImage } from "@/composables/useUserImage";
import { useRoute } from "vue-router";
import CommonButton from "@/components/common/CommonButton.vue";

// PROPS
const route = useRoute();

const props = defineProps({
  menuOpen: Boolean,
});

// VARIABLES
const authStore = useAuthStore();
const emit = defineEmits(["toggle-user-menu"]);

// Imagen de usuario
const { getIconUserImg, handleImgError, userImg } = useUserImage();

// Hover
const isHovered = ref(false);

// METODOS
// Para abrir o cerrar el menu
const toggleMenu = () => {
  emit("toggle-user-menu", !props.menuOpen);
};

// Configuracion del estilo del menu
const menuTheme = computed(() => {
  const currentRoute = route.name;

  if (currentRoute === "Home" || currentRoute === "AboutUs") {
    return {
      background: "bg-black backdrop-blur-md shadow-[0px_0px_8px_0px_rgb(0,_0,_0)]",
      text: "text-white pl-6 py-1 text-base",
      username: "border-b-2 border-b-grey text-green",
      icon: "text-white",
    };
  } else {
    return {
      background: "bg-white backdrop-blur-md shadow-[0px_0px_8px_0px_rgb(0,_0,_0)]",
      text: "text-black pl-6 py-1 text-base",
      username: "border-b-grey border-b-2 text-brown",
      icon: "text-green",
    };
  }
});
</script>

<style lang="scss" scoped>
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
