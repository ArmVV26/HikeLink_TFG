<template>
    <div v-if="user.id" class="main-container">
        <div class="user-container">
            <div>
                <img :src="getIconUserImg(user)" alt="Imagen del Usuario" class="avatar">
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
                    :route="`/edit-profile/${authStore.user.id}`"
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
                    :paginated="true"
                />
                
                <RouteCard
                    v-else
                    :routes="favorites" 
                    :paginated="true"
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
                        :route="'/searchroutes'"
                        :thin="true"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue';
    import { getMediaUrl } from '@/api/media';
    import { useAuthStore } from '@/stores/authStore';

    import api from '@/api/api';
    import CommonButton from '@/components/common/CommonButton.vue';
    import RouteCard from '@/components/map/RouteCard.vue';

    const user = ref({})
    const routes = ref([])
    const favorites = ref([])
    const view = ref('myRoutes')
    const allRoutes = computed(() => routes.value.length)

    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const accessToken = computed(() => authStore.accessToken)

    const displayedRoutes = computed(() => {
        return view.value === 'myRoutes' ? routes.value : favorites.value
    })

    // Obtener el icono del usuario
    const getIconUserImg = (manage) => {
        return getMediaUrl(`${manage.username}/${manage.profile_picture}`)
    }
    
    // Transformar la fecha en "10 de marzo de 2026"
    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('es-ES', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        }).format(date)
    }

    // Paginar
    const totalPages = ref(1)
    const currentPage = ref(1)
    const pageSize = 5
    
    // Para determinar el numero de paginas que se muestran en el pagination
    const maxVisiblePages = 5
    const paginationPages = computed(() => {
        const pages = []
        const total = totalPages.value
        const current = currentPage.value

        if (total <= maxVisiblePages) {
            for (let i = 1; i <= total; i++) {
                pages.push(i)
            }
        } else {
            pages.push(1)

            if (current > 3) {
                pages.push('...')
            }

            let start = Math.max(2, current - 1)
            let end = Math.min(total - 1, current + 1)

            for (let i = start; i <= end; i++) {
                pages.push(i)
            }

            if (current < total - 2) {
                pages.push('...')
            }

            pages.push(total)
        }

        return pages
    })

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
            const response = await api.get(`favorites/?user=${user.value.id}`)
            const favoriteIds = response.data.map(fav => fav.route)
            
            const promises = favoriteIds.map(id => api.get(`/routes/${id}/`))
            const routeDetails = await Promise.all(promises)

            favorites.value = routeDetails.map(r => r.data)
        } catch (error) {
            console.error("Error obteniendo favoritos:", error)
        }
    }

    // Para obtener los datos del usuario y las rutas del usuario
    onMounted(async () => {
        if (!isAuthenticated.value) return

        try {
            // Obtener datos del usuario
            const userRes = await api.get('/user/', {
                headers: {
                    Authorization: `Bearer ${accessToken.value}`
                }
            })
            user.value = userRes.data

            // Obtener rutas del usuario paginadas
            await paginationFetch(1)
        } catch (error) {
            console.error("Error cargando datos del perfil:", error)
        }
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

    .routes-container {
        flex: 1;

        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            margin: 1rem 0;

            .nav-btn, .page-btn {
                font-size: 1.25rem;
                padding: 0.35rem 0.85rem;
                border: 2px solid var(--color-green);
                border-radius: 25rem;
                cursor: pointer;
                transition: all 0.25s;

                &:hover {
                    background-color: var(--color-green);
                    color: var(--color-white);
                }

            }
            
            .nav-btn:disabled {
                display: none;
            }

            .page-btn:disabled {
                border: 0px;
                padding: 0;
                color: var(--color-brown);
                font-weight: 900;
                cursor: default;

                &:hover {
                    background-color: transparent;
                    color: var(--color-brown);
                }
            }

            .active {
                background-color: var(--color-green);
                color: var(--color-white);
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
</style>