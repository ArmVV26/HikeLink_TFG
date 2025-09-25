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
      <img
        :src="getIconUserImg"
        @error="handleImgError"
        class="hover:border-light-green mr-2 ml-2 h-22 w-22 cursor-pointer rounded-3xl border-2 border-transparent object-cover transition-all duration-200 sm:mr-4 sm:ml-4"
        ref="userImg"
        @click="toggleMenu"
      />

      <transition name="fade-dropdown">
        <nav
          v-if="menuOpen"
          :class="[
            {
              'bg-black-50 shadow-transparent transition-all duration-500':
                route.name === 'Home' || route.name === 'AboutUs',
            },
          ]"
          class="absolute top-full right-0 flex flex-col rounded-bl-3xl bg-black pb-4 text-center text-xl text-white transition-all duration-200"
        >
          <h1
            class="font-montserrat-bold text-light-green border-b-grey border-b-2 pt-1 pb-1 text-center text-2xl font-bold"
          >
            {{ authStore.user.username }}
          </h1>
          <router-link
            :to="`/profile/${authStore.user.username}-${authStore.user.id}`"
            class="font-montserrat-bold hover:text-light-green cursor-pointer px-2 py-2 transition-all duration-300"
          >
            Mi Perfil
          </router-link>
          <router-link
            to="/upload-route"
            class="font-montserrat-bold hover:text-light-green cursor-pointer px-2 py-2 transition-all duration-300"
          >
            Subir Ruta
          </router-link>
          <router-link
            @click="authStore.logout"
            to="/"
            class="font-montserrat-bold hover:text-light-green cursor-pointer px-2 py-2 transition-all duration-300"
            >Cerrar Sesión</router-link
          >
        </nav>
      </transition>
    </article>
  </section>
</template>

<script setup>
// IMPORTS
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

// METODOS
// Para abrir o cerrar el menu
const toggleMenu = () => {
  emit("toggle-user-menu", !props.menuOpen);
};
</script>

<style lang="scss" scoped>
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
