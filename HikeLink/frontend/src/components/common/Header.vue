<template>
    <nav :class="['flex justify-between', { 'hero-nav': route.name === 'Home' || route.name === 'AboutUs' }]">
        <router-link to="/" class="px-5 py-1">
            <ResponsiveImage
                :info="['LogoHikelink', 'logo']"
                :formats="['svg', 'png']"
                figureClass="logo-container"
                alt="Logo Header"
            />
        </router-link>
        <div class="links flex items-center text-center justify-end">
            <router-link class="links-menu" to="/map">Mapa</router-link>
            <router-link class="links-menu" to="/searchroutes">Buscar Ruta</router-link>    
            <router-link class="links-menu" to="/foro">Foro</router-link>    
            <LoginButton />
        </div>
    </nav>
</template>
  
<script setup>
    import { useRoute } from 'vue-router';
    import ResponsiveImage from '../images/ResponsiveImage.vue';
    import LoginButton from '../auth/LoginButton.vue';

    const route = useRoute();
    console.log(route)
</script>

<style scoped>
    nav {
        background: var(--color-black);
        box-shadow: 0px 0px 15px 0px var(--color-black);
        width: auto;
        height: 7rem;
        transition: background-color 0.5s ease-in-out;
        position: relative;
        z-index: 5;
    }

    .hero-nav {
        background: var(--color-black-opacity);
        box-shadow: none;
        transition: background 0.5s ease;
    }

    .logo-container {
        width: 9rem;
        height: auto;
    }

    .links .links-menu {
        color: var(--color-white);
        text-decoration: none;
        font-size: 1.5rem;
        font-weight: 550;
        padding: 1rem 2rem;
        transition: all 0.25s;
    }

    .links .links-menu:hover {
        color: var(--color-light-green);
        transform: scale(1.05);
    }

    .links .links-menu::after {
        content: "";
        position: absolute;
        top: 80%;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        width: 0;
        height: 0.2rem;
        background-color: #F1A2A2;
        transition: width 0.3s ease;
    }
</style>  