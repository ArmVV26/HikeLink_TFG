<template>
    <nav :class="[{ 'hero-nav': route.name === 'Home' || route.name === 'AboutUs' }]">
        <router-link to="/" class="px-5 py-1">
            <ResponsiveImage
                :info="['LogoHikelink', 'logo']"
                :formats="['svg', 'png']"
                figureClass="logo-container"
                alt="Logo Header"
            />
        </router-link>
        <div class="links">
            <router-link to="/map">Mapa</router-link>
            <router-link to="/search-routes">Buscar Ruta</router-link>    
            <router-link to="/foro">Foro</router-link>    
            <LoginButton />
        </div>
    </nav>
</template>
  
<script setup>
    // IMPORTS
    import { useRoute } from 'vue-router';
    import ResponsiveImage from '../images/ResponsiveImage.vue';
    import LoginButton from '../auth/LoginButton.vue';

    // VARIABLES
    const route = useRoute();
</script>

<style lang="scss" scoped>
    nav {
        display: flex;
        justify-content: space-between;
        background: var(--color-black);
        box-shadow: 0px 0px 15px 0px var(--color-black);
        width: auto;
        height: 7rem;
        transition: background-color 0.5s ease-in-out;
        position: relative;
        z-index: 5;
        
        &.hero-nav {
            background: var(--color-black-opacity);
            box-shadow: none;
            transition: background 0.5s ease;
        }
        
        .logo-container {
            width: 9rem;
            height: auto;
        }

        .links {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            
            a {
                display: inline-block;
                position: relative;
                color: var(--color-white);
                text-decoration: none;
                font-size: 1.5rem;
                font-weight: 550;
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
    }
</style>  