<template>
    <div class="main-container">
        <div class="filter-container">
            <h1>Filtrar Por</h1>
            <form @submit.prevent="filterRoutes">
                <input type="text" v-model="title" placeholder="Buscar Ruta" />
                
                <div>
                    <label for="type">Tipo </label>
                    <select id="type" name="type" v-model="type">
                        <option value="Todas">Todas</option>
                        <option value="Para-Todos">Para Todos</option>
                        <option value="Senderismo">Senderismo</option>
                        <option value="Ciclismo">Ciclismo</option>
                        <option value="Trail-Running">Trail-Running</option>
                        <option value="Alpinismo">Alpinismo</option>
                    </select>
                </div>

                <div>
                    <label for="difficulty">Dificultad </label>
                    <select id="difficulty" name="difficulty" v-model="difficulty">
                        <option value="Todas">Todas</option>
                        <option value="Fácil">Fácil</option>
                        <option value="Moderada">Moderada</option>
                        <option value="Difícil">Difícil</option>
                    </select>
                </div>

                <div>
                    <label for="origin">Origen </label>
                    <select id="origin" name="origin" v-model="origin">
                        <option value="Todos">Todos</option>
                        <option value="Wikiloc">Wikiloc</option>
                        <option value="Strava">Strava</option>
                        <option value="OutdoorActive">OutdoorActive</option>
                        <option value="AllTrails">AllTrails</option>
                        <option value="Komoot">Komoot</option>
                    </select>
                </div>

                <div>
                    <label>Duración (horas):</label>
                    <input type="range" min="0" max="24" v-model.number="durationMin" />
                    <input type="range" min="0" max="24" v-model.number="durationMax" />
                    <span>{{ durationMin }}h - {{ durationMax }}h</span>
                </div>

                <div>
                    <label>Longitud (km):</label>
                    <input type="range" min="0" max="100" v-model.number="distanceMin" />
                    <input type="range" min="0" max="100" v-model.number="distanceMax" />
                    <span>{{ distanceMin }}km - {{ distanceMax }}km</span>
                </div>

                <button type="submit">Buscar</button>
            </form> 
        </div>

        <div v-if="routes.length" class="routes-container">
            <RouteCard 
                :routes="routes"
                :current-page="currentPage"
                :total-pages="totalPages"
                @change-page="loadAllRoutes"
            />
        </div>

        <div v-else class="no-routes">
            <i class="fa-solid fa-mountain-sun"></i>
            <h1>¡No se han encontrado rutas!</h1>
            <p>Modifica el filtro para buscar tus rutas deseadas</p>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { onMounted, ref } from 'vue';
    import api from '@/utils/api';
    import RouteCard from '@/components/map/RouteCard.vue';

    // VARIABLES
    const title = ref('')
    const type = ref('Todas')
    const difficulty = ref('Todas')
    const origin = ref('Todos')
    const durationMin = ref(0)
    const durationMax = ref(24)
    const distanceMin = ref(0)
    const distanceMax = ref(1000)

    const routes = ref([])

    // METODOS
    // Funcion para buscar las rutas
    const filterRoutes = async () => {
        const params = new URLSearchParams()
        
        if (title.value) params.append('title', title.value)
        if (type.value !== 'Todas') params.append('type', type.value)
        if (difficulty.value !== 'Todas') params.append('difficulty', difficulty.value)
        if (origin.value !== 'Todos') params.append('origin', origin.value)
        
        params.append('duration_min', durationMin.value * 3600)
        params.append('duration_max', durationMax.value * 3600)
        params.append('distance_min', distanceMin.value * 1000)
        params.append('distance_max', distanceMax.value * 1000)

        try {
            const response = await api.get(`/filter-routes/?${params.toString()}`)
            routes.value = response.data.results
            totalPages.value = Math.ceil(response.data.count / pageSize)
            currentPage.value = 1
        } catch (error) {
            console.error('Error al filtrar rutas:', error)
        }
    }

    // Paginar
    const totalPages = ref(1)
    const currentPage = ref(1)
    const pageSize = 5

    const loadAllRoutes = async (page = 1) => {
        try {
            const response = await api.get(`all-routes/?page=${page}&page_size=${pageSize}`)
            routes.value = response.data.results
            totalPages.value = Math.ceil(response.data.count / pageSize)
            currentPage.value = page
        } catch (error) {
            console.error("Error obteniendo rutas paginadas: ", error)
        }
    }
    
    // Para cargar todas las rutas al principio o al recargar la pagina
    onMounted(async () => {
        try {   
            loadAllRoutes()
        } catch (error) {
            console.error("Error al cargar las rutas: ", error)
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

    .filter-container {
        height: 30rem;
        padding: 1rem;
        background-color: var(--color-vanille-opacity);
        border-radius: 25px;
        box-shadow: 5px 5px 0px 2px var(--color-brown);
        
        h1 {
            font-family: "Montserrat-Bold";
            font-size: 1.75rem;
            font-style: italic;
            margin-bottom: 1rem;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            font-family: "Lato";

            input[type="text"] {
                width: 90%;
                padding: 0.5rem 0.75rem;
                margin: auto;
                font-size: 1rem;
                color: var(--color-black);
                border: 2px solid var(--color-brown);
                background-color: var(--color-white);
                border-radius: 10px;

                &:hover {
                    border: 2px solid var(--color-green);
                }
            }

            div {
                margin: 0 1rem;
                display: flex;
                align-items: center;
                justify-content: space-between;

                label {
                    font-family: "Montserrat-Bold";
                    color: var(--color-green);
                }

                select {
                    margin-left: 1rem;
                    padding: 0.5rem 0.75rem;
                    color: var(--color-black);
                    border: 2px solid var(--color-brown);
                    background-color: var(--color-white);
                    border-radius: 25px;
                    
                    &:hover {
                        border: 2px solid var(--color-green);
                    }
                }
            }
            
            button {
                width: 90%;
                padding: 0.5rem 0.75rem;
                margin: auto;
                font-size: 1rem;
                font-weight: 900;
                color: var(--color-white);
                background-color: var(--color-green);
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.25s;
    
                &:hover {
                    background-color: var(--color-light-green);
                    color: var(--color-green);
                }
            }
        } 
    }

    .routes-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
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