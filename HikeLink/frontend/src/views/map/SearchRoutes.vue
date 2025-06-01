<template>
    <div class="main-container">
        <div class="filter-container">
            <h1>Filtrar Por</h1>
            <form @submit.prevent="filterRoutes">
                <input type="text" v-model="title" placeholder="Buscar Ruta" />
                
                <div class="type">
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

                <div class="difficulty">
                    <label for="difficulty">Dificultad </label>
                    <select id="difficulty" name="difficulty" v-model="difficulty">
                        <option value="Todas">Todas</option>
                        <option value="Fácil">Fácil</option>
                        <option value="Moderada">Moderada</option>
                        <option value="Difícil">Difícil</option>
                    </select>
                </div>

                <div class="origin">
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

                <div class="slider">
                    <label>Duración (horas):</label>
                    <Slider 
                        class="slider-component"    
                        v-model="durationRange" 
                        :min="0" :max="24" 
                        :step="1" :range="true" 
                    />
                    <span>{{ durationRange[0] }}h - {{ durationRange[1] }}h</span>
                </div>

                <div class="slider">
                    <label>Longitud (km):</label>
                    <Slider 
                        class="slider-component"    
                        v-model="distanceRange"
                        :min="0" :max="100"
                        :step="1" :range="true"
                    />
                    <span>{{ distanceRange[0] }}km - {{ distanceRange[1] }}km</span>
                </div>

                <button type="submit">Buscar</button>
            </form> 
        </div>

        <div v-if="routes.length" class="routes-container">
            <RouteCard 
                :routes="routes"
                :current-page="currentPage"
                :total-pages="totalPages"
                @change-page="loadRoutes"
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
    import Slider from '@vueform/slider'
    import '@vueform/slider/themes/default.css'

    // VARIABLES
    const title = ref('')
    const type = ref('Todas')
    const difficulty = ref('Todas')
    const origin = ref('Todos')
    const durationRange = ref([0, 24])
    const distanceRange = ref([0, 100])
    
    const routes = ref([])

    // Paginar
    const totalPages = ref(1)
    const currentPage = ref(1)
    const pageSize = 5

    const isFiltering = ref(false)
    const currentFilters = ref({})

    // METODOS
    // Funcion que recarga las rutas si hay filtro o si no hay filtro
    const loadRoutes = async (page = 1) => {
        try {
            let response

            if (isFiltering.value) {
                const params = new URLSearchParams(currentFilters.value)
                params.append('page', page)
                params.append('page_size', pageSize)

                response = await api.get(`/filter-routes/?${params.toString()}`)
            } else {
                response = await api.get(`/all-routes/?page=${page}&page_size=${pageSize}`)
            }

            routes.value = response.data.results
            totalPages.value = Math.ceil(response.data.count / pageSize)
            currentPage.value = page
        } catch (error) {
            console.error("Error al cargar las rutas:", error)
        }
    }

    // Funcion para buscar las rutas
    const filterRoutes = async () => {
        const params = new URLSearchParams()
        
        if (title.value) params.append('title', title.value)
        if (type.value !== 'Todas') params.append('type', type.value)
        if (difficulty.value !== 'Todas') params.append('difficulty', difficulty.value)
        if (origin.value !== 'Todos') params.append('origin', origin.value)
        
        params.append('duration_min', durationRange.value[0] * 3600)
        params.append('duration_max', durationRange.value[1] * 3600)
        params.append('distance_min', distanceRange.value[0] * 1000)
        params.append('distance_max', distanceRange.value[1] * 1000)

        currentFilters.value = Object.fromEntries(params.entries()) 
        isFiltering.value = true

        await loadRoutes(1)
    }
    
    // Para cargar todas las rutas al principio o al recargar la pagina
    onMounted(async () => {
        try {   
            loadRoutes()
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
        height: 35rem;
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

            .type, .difficulty, .origin {
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

            .slider {
                width: 100%;
                margin: 0 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;

                label {
                    font-family: "Montserrat-Bold";
                    color: var(--color-green);
                    align-self: flex-start;
                }

                .slider-component {
                    width: 70%;
                    margin-top: 1rem;
                }
   
                span {
                    margin-top: 0.25rem;
                    font-weight: bold;
                    color: var(--color-black);
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

<style lang="scss">
    .slider-tooltip {
        background-color: var(--color-green) !important;
        border-color: var(--color-green);
        color: var(--color-white) !important;
        padding: 1px 5px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.75rem;

        opacity: 0;
        transition: opacity 0.2s ease;
        pointer-events: none;
    }

    .slider-connect {
        background-color: var(--color-light-green) !important;
    }

    .slider-handle {
        border: 2px solid var(--color-green) !important;
        background-color: var(--color-white) !important;

        &:hover, &:focus, &:active {
            .slider-tooltip {
                opacity: 1;
            }
        }
    }
</style>