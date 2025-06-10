<template>
    <div v-if="user.id" class="main-container">
        <div class="user-container">
            <div>
                <img :src="getIconUserImg" alt="Imagen del Usuario" 
                    class="avatar" @error="handleImgError" ref="userImg">
                <h1>{{ user.username }}</h1>
                <p>Miembro desde el {{ formatDate(user.created_date) }}</p>
            </div>
    
            <div>
                <p>{{ user.full_name }}</p>
                <p>{{ user.email }}</p>
                <p><span>Nº de Rutas: </span>{{ allRoutes }}</p>
                <p class="bio">{{ user.bio }}</p>
                <CommonButton 
                    :text="'Editar Perfil'"
                    :route="`/profile/edit-profile/${authStore.user.username}-${authStore.user.id}`"
                    :thin="true"
                />
            </div>
        </div>
    
        
        <div class="route-tab-container">
            <div class="tab-menu">
                <button :class="{'active': view === 'myRoutes'}" @click="view = 'myRoutes'">Mis Rutas</button>
                <button :class="{'active': view === 'favorites'}" @click="view ='favorites'; fetchFavorites()">Favoritos</button>
            </div>
            
            <div v-if="displayedRoutes.length" class="routes-container">
                <RouteCard 
                    v-if="view === 'myRoutes'"
                    :routes="displayedRoutes"
                    :current-page="currentPage"
                    :total-pages="totalPages"
                    @change-page="paginationFetch"
                />
                
                <RouteCard
                    v-else
                    :routes="favorites" 
                    :current-page="currentPage"
                    :total-pages="totalPages"
                    @change-page="paginationFetch"
                />
            </div>

            <div v-else class="no-routes">
                <i class="fa-solid fa-mountain-sun"></i>
                <div v-if="view === 'myRoutes'">
                    <h1>¡Comienza a incluir tus rutas!</h1>
                    <p>Todavía no has subido ninguna ruta. Subelas para compartir tus experiencias.</p>
                    <CommonButton 
                        :text="'Subir Ruta'"
                        :route="'/upload-route'"
                        :thin="true"
                    />
                </div>
                <div v-else>
                    <h1>¡Añade alguna ruta a Favoritos!</h1>
                    <p>Todavía no has añadido ninguna ruta a favoritos, dale al botón de abajo para buscar tus rutas favoritas.</p>
                    <CommonButton 
                        :text="'Buscar Ruta'"
                        :route="'/search-routes'"
                        :thin="true"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { computed, onMounted, ref } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import { useUserImage } from '@/composables/useUserImage';
    
    import api from '@/utils/api';
    import { apiWithAuth } from '@/utils/api';
    import CommonButton from '@/components/common/CommonButton.vue';
    import RouteCard from '@/components/map/RouteCard.vue';

    // VARIABLES
    const routes = ref([])
    const favorites = ref([])
    const view = ref('myRoutes')
    const allRoutes = computed(() => routes.value.length)
    
    const authStore = useAuthStore()
    const user = computed(() => authStore.user)
    const isAuthenticated = computed(() => authStore.isAuthenticated)

    const { getIconUserImg, handleImgError, userImg } = useUserImage();

    const displayedRoutes = computed(() => {
        return view.value === 'myRoutes' ? routes.value : favorites.value
    })
    
    // Paginar
    const totalPages = ref(1)
    const currentPage = ref(1)
    const pageSize = 5

    // METODOS
    // Transformar la fecha en "10 de marzo de 2026"
    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('es-ES', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        }).format(date)
    }

    // Para hacer que las rutas se pongan en paginas
    const paginationFetch = async (page = 1) => {
        try {
            const response = await api.get(`/routes/user/${user.value.id}?page=${page}&page_size=${pageSize}`)
            routes.value = response.data.results
            totalPages.value = Math.ceil(response.data.count / pageSize)
            currentPage.value = page 
        } catch (error) {
            console.error("Error obteniendo rutas paginadas: ", error)
        }
    }

    // Funcion para obtener las rutas que tiene un usuario en favoritos
    const fetchFavorites = async () => {
        if (!isAuthenticated.value) return

        try {
            const response = await apiWithAuth().get(`favorites/?user=${user.value.id}`)
            const favoriteIds = response.data.map(fav => fav.route)
            
            const promises = favoriteIds.map(id => apiWithAuth().get(`/routes/${id}/`))
            const routeDetails = await Promise.all(promises)

            favorites.value = routeDetails.map(r => r.data)
            totalPages.value = Math.ceil(favorites.value.length / pageSize);
            currentPage.value = 1;
        } catch (error) {
            console.error("Error obteniendo favoritos:", error)
        }
    }

    // Funcion que se llama al cargar todo
    onMounted(async () => {
        if (!isAuthenticated.value) return
        await paginationFetch(1)
    })
</script>

<style lang="scss" scoped>
    .main-container {
        width: 95%;
        margin: 2rem auto;
        display: grid;
        grid-template-columns: 20rem 1fr;
        gap: 2rem;
    }

    .user-container {
        height: 30rem;
        padding: 1rem;
        background-color: var(--color-vanille-opacity);
        border-radius: 25px;
        box-shadow: 5px 5px 0px 2px var(--color-brown);
        
        div:first-child {
            border-bottom: 2px solid var(--color-brown);
            padding-bottom: 1rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: center;

            .avatar {
                align-self: center;
                width: auto;
                height: 10rem;
                object-fit: cover;
                border-radius: 25px;
            }
    
            h1 {
                font-family: "Montserrat-Bold";
                font-size: 1.75rem;
                font-style: italic;
                line-height: 1;
                margin-top: 1rem;
            }
    
            p {
                color: var(--color-light-green);
                font-weight: 900;
                text-align: center;
            }
        }

        div:last-child {
            font-weight: 900;
            line-height: 1.5;
            text-align: center;

            p {
                text-align: left;
            }

            span {
                color: var(--color-green);
            }

            .bio {
                text-align: center;
                color: var(--color-light-green);
                margin: 1rem 0;
            }

            a {
                display: inline-block;
                margin: 0 auto;
            }
        }
    }

    .route-tab-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;

        .tab-menu {
            display: flex;
            gap: 1rem;
            border-bottom: 5px solid var(--color-black);

            button {
                font-family: "Montserrat-Bold";
                font-size: 1.5rem;
                cursor: pointer;

                &:hover {
                    color: var(--color-green);
                }
            }

            .active {
                color: var(--color-light-green);
                border-bottom: 5px solid var(--color-green);

                &:hover {
                    color: var(--color-light-green);
                }
            }
        }
    }

    .no-routes {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        div {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        i {
            font-size: 6rem;
            color: var(--color-green);
            filter: drop-shadow(8px 5px 0px var(--color-light-green));
        }

        h1 {
            font-family: "Montserrat-Bold";
            font-size: 2.5rem;
            color: var(--color-green);
        }

        p {
            margin-bottom: 1rem;
        }
    }

    @media (max-width: 1300px) {
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .user-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 2rem;
            width: 30rem;
            height: 20rem;
            
            div:first-child {
                border-bottom: none;
                border-right: 2px solid var(--color-brown);
                padding: 0;
            }
        }

        .no-routes {
            text-align: center;
        }
    }

    @media (max-width: 500px) {
        .main-container {
            width: 100%;
            margin: 2rem 0;
        }

        .user-container {
            width: 100%;
            height: 100%;
            padding: 1rem 0;
            border-radius: 0;
            box-shadow: none;
            border-top: 5px solid var(--color-brown);
            border-bottom: 5px solid var(--color-brown);

            flex-direction: column;
            gap: 0;

            div:first-child {
                width: 100%;
                border-right: 0;
                border-bottom: 5px solid var(--color-brown);
                padding-bottom: 1rem;
            }

            div:last-child {
                p {
                    text-align: center;
                }
            }
        }
    }
</style>