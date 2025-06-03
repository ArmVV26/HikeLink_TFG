<template>
    <div v-if="authStore.isAuthResolved">
        <CommonButton 
            v-if="!authStore.isAuthenticated"
            :header="false"
            :text="'Iniciar Sesión'"
            :route="'/login'"
            class="login-button"
        />
        <div v-else class="user-menu">
            <img :src="getIconUserImg"
                @error="handleImgError" 
                class="avatar" 
                ref="userImg"
                @click="toggleMenu" />
            <transition name="fade-dropdown">
                <div v-if="menuOpen" class="dropdown">
                    <h1>{{ authStore.user.username }}</h1>
                    <router-link :to="`/profile/${authStore.user.username}-${authStore.user.id}`"> Mi Perfil </router-link>
                    <router-link to="/upload-route"> Subir Ruta </router-link>
                    <router-link @click="authStore.logout" to="/">Cerrar Sesión</router-link>
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { ref, watch } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import { useRoute } from 'vue-router';
    import { useUserImage } from '@/composables/useUserImage';
    import CommonButton from '../common/CommonButton.vue';

    // VARIABLES
    const authStore = useAuthStore()
    const menuOpen = ref(false)    
    const route = useRoute()

    const emit = defineEmits(['toggle-user-menu'])
    
    // METODOS
    // Si cambia de pagina se cierra el menu
    watch(() => route.fullPath, () => {
        menuOpen.value = false;
    });
    
    // Imagen de usuario
    const { getIconUserImg, handleImgError, userImg } = useUserImage();
    
    // Para abrir o cerrar el menu
    const toggleMenu = () => {
        menuOpen.value = !menuOpen.value
        
        if (menuOpen.value) {
            emit('toggle-user-menu', true); 
        } else {
            emit('toggle-user-menu', false); 
        }
    }
</script>

<style lang="scss" scoped>
    .login-button {
        color: var(--color-white);
        font-size: 1.75rem;
        margin: 0 2.5rem 0 1rem;
    }

    .user-menu {
        .avatar {
            width: 5rem;
            height: 5rem;
            border: 2px solid transparent;
            border-radius: 25px;
            margin: 0 5rem 0 1rem;
            cursor: pointer;
            transition: all 0.15s;
        }
        .avatar:hover {
            border: 2px solid var(--color-light-green);
        }
    
        .dropdown {
            position: absolute;
            right: 0;
            top: 100%;
            display: flex;
            flex-direction: column;
            gap: 1rem;
    
            background-color: var(--color-black-opacity);
            border-bottom-left-radius: 25px;
            color: var(--color-white);
            font-size: 1.25rem;
            transition: all 0.15s;
        }
    
        .dropdown h1 {
            font-family: "Montserrat-Bold";
            font-weight: 900;
            font-size: 1rem;
            text-align: center;
            color: var(--color-light-green);
            border-bottom: 2px solid var(--color-grey);
            line-height: 0.75;
            padding: 0.5rem 0 0.25rem;
        }
    
        .dropdown a {
            font-family: "Montserrat-Bold";
            padding: 0 1rem;
            line-height: 1;
            cursor: pointer;
            transition: all 0.25s;

            &:last-child {
                padding-bottom: 1rem;
            }
        }
    
        .dropdown a:hover {
            color: var(--color-light-green);
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