<template>
  <div id="app">
    <Header />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
  // IMPORTS
  import Header from '@/components/common/Header.vue'
  import Footer from '@/components/common/Footer.vue'
  import { onMounted } from 'vue'
  import { useAuthStore } from './stores/authStore'

  // VARIABLES
  const authStore = useAuthStore()

  // METODOS
  // Metodo para cargar desde el token las sesion del usuario
  onMounted(async () => {
    const token = localStorage.getItem('access')
    if (token) {
      await authStore.fetchUser()
    } else {
      authStore.setResolved()
    }
  })
</script>

<style>
  html, body, #app {
    height: 100%;
    margin: 0;
  }

  #app {
    display: flex;
    flex-direction: column;
  }

  .main-content {
    flex: 1;
  }
</style>
