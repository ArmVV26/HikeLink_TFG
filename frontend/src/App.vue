<template>
  <div id="app">
    <Header />
    <main class="main-content">
      <router-view />
    </main>
    <Footer v-if="route.name !== 'Map'" />
  </div>
</template>

<script setup>
// IMPORTS
import { onMounted } from "vue";
import { useAuthStore } from "./stores/authStore";
import { useRoute } from "vue-router";
import Header from "@/components/common/Header.vue";
import Footer from "@/components/common/Footer.vue";

// VARIABLES
const authStore = useAuthStore();
const route = useRoute();

// METODOS
// Metodo para cargar desde el token las sesion del usuario
onMounted(async () => {
  const token = localStorage.getItem("access");
  if (token) {
    await authStore.fetchUser();
  } else {
    authStore.setResolved();
  }
});
</script>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
  scroll-behavior: smooth;
}

#app {
  display: flex;
  flex-direction: column;
}

.main-content {
  margin-top: 80px;
  flex: 1;
}
</style>
