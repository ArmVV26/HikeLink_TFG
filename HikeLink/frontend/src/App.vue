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
  import Header from './components/common/Header.vue'
  import Footer from './components/common/Footer.vue'

  import { onMounted } from 'vue'
  import axios from 'axios'
  import { useAuthStore } from './stores/authStore'

  const authStore = useAuthStore()

  onMounted(async () => {
    const token = localStorage.getItem('access')
    if (token && !authStore.user) {
      try {
        const response = await axios.get('http://localhost:8000/api/user', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        authStore.login(response.data)
      } catch (error) {
        console.error('Error al recuperar el usuario al iniciar:', error)
        authStore.logout()
      }
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
