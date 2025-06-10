<template>
    <nav :class="[{ 'hero-nav': route.name === 'Home' || route.name === 'AboutUs' }]">
        <router-link to="/" class="logo-wrapper">
            <ResponsiveImage
                :info="['LogoHikelink', 'logo']"
                :formats="['svg', 'png']"
                figureClass="logo-container"
                alt="Logo Header"
            />
        </router-link>

        
        <div class="links-container">
            <button class="menu-toggle" v-if="isMobile" @click="toggleMainMenu">
                <i class="fa-solid fa-bars"></i>
            </button>

            <transition name="fade-dropdown">
                <div v-if="!isMobile || showMainMenu" class="links">
                    <router-link to="/map">Mapa</router-link>
                    <router-link to="/search-routes">Buscar Ruta</router-link>    
                    <router-link to="/foro">Foro</router-link>    
                </div>
            </transition>
            
            <LoginButton :menuOpen="showUserMenu" @toggle-user-menu="handleUserMenuToggle" />
        </div>
    </nav>
</template>
  
<script setup>
    // IMPORTS
    import { onMounted, onBeforeUnmount, ref, watch } from 'vue';
    import { useRoute } from 'vue-router';
    import ResponsiveImage from '../images/ResponsiveImage.vue';
    import LoginButton from '../auth/LoginButton.vue';

    // VARIABLES
    const route = useRoute();
    
    const showMainMenu = ref(false);
    const showUserMenu = ref(false);
    const isMobile = ref(window.innerWidth <= 940);

    // METODOS
    // Funcion que detecta cuando se reduce el tamaño
    const updateIsMobile = () => {
        isMobile.value = window.innerWidth <= 940;
        if (!isMobile.value) {
            showMainMenu.value = false;
            showUserMenu.value = false;
        }
    };

    onMounted(() => {
        window.addEventListener('resize', updateIsMobile);
    });

    onBeforeUnmount(() => {
        window.removeEventListener('resize', updateIsMobile);
    });

    watch(() => route.fullPath, () => {
        showMainMenu.value = false;
        showUserMenu.value = false;
    });

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
        min-height: 112px;
        
        &.hero-nav {
            background: var(--color-black-opacity);
            box-shadow: none;
            transition: background 0.5s ease;
        }

        .logo-wrapper {
            padding: 1rem;
            align-self: center;

            .logo-container {
                width: 9rem;
                height: auto;
            }
        }
        
        .links-container {
            display: flex;
            justify-content: center;
            align-items: center;
            
            .menu-toggle {
                display: none;
                background: none;
                border: none;
                color: var(--color-white);
                font-size: 3.5rem;
                cursor: pointer;
            }

            .links {
                display: flex;
                align-items: center;
                justify-content: flex-end;
                
                a {
                    font-family: "Montserrat-Bold";
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

    @media (max-width: 940px) { 
        nav {
            &.hero-nav {
                .links-container {
                    .links {
                        background-color: var(--color-black-opacity);
                    }
                }
            }
            .links-container {
                .menu-toggle {
                    display: flex;
                    align-items: center;
                    justify-content: flex-end;
                    cursor: pointer;
                    transition: all 0.25s;

                    &:hover {
                        transform: scale(0.85);
                    }
                }
                
                .links {
                    display: flex;
                    flex-direction: column;
                    background: var(--color-black);
                    position: absolute;
                    top: 7rem;
                    right: 0;
                    padding: 0.25rem;
                    border-bottom-left-radius: 25px;
                    box-shadow: 0 5px 15px var(--color-black-opacity);

                    a {
                        margin: 1rem 1rem 0;
                    }
                }
            }
        }
    }

    @media (max-width: 500px) {
        nav {
            .logo-wrapper {
                padding: 0.25rem;

                .logo-container {
                    width: 6.5rem;
                }
            }

            .links-container {
                .links {
                    a {
                        font-size: 1.25rem;
                    }
                }
            }
        }
    } 
</style>  