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
                    <router-link to="/profile"> Mi Perfil </router-link>
                    <router-link to="/upload-route"> Subir Ruta </router-link>
                    <router-link @click="authStore.logout" to="/">Cerrar Sesión</router-link>
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, watch } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import CommonButton from '../common/CommonButton.vue';
    import { getMediaUrl } from '@/api/media';
    import { useRouter } from 'vue-router';

    const authStore = useAuthStore()
    const menuOpen = ref(false)    
    const userImg = ref(null)
    const route = useRouter()

    // Si cambia de pagina se cierra el menu
    watch(() => route.fullPath, () => {
        menuOpen.value = false;
    });

    const getIconUserImg = computed(() => {
        const user = authStore.user;
        if (!user) return null
        return getMediaUrl(`/${user.username}/${user.profile_picture}`)
    });
    
    function handleImgError() {
        userImg.value.src = getMediaUrl('/sample_user_icon.png');
    }

    const toggleMenu = () => {
        menuOpen.value = !menuOpen.value
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
            border-radius: 25px;
            cursor: pointer;
            margin: 0 5rem 0 1rem;
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