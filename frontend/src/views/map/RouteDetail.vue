<template>
    <div v-if="route">
        <div class="main-container">
            <div class="map-container">
                <div class="route-type" v-html="routeType(route)"></div>
                <h1>{{ route.title }}</h1>
                <div class="date-buttons">
                    <p>{{ formatDate(route.created_date) }}</p>
                    <CommonButton 
                        :text="isFavorite ? 'Quitar Favorito' : 'Añadir a Favoritos'"
                        :icon="'fa-solid fa-bookmark'"
                        :thin="true"
                        :route="''"
                        :asButton="true"
                        :disabled="!isAuthenticated"
                        @click="toggleFavorite"
                    />
                    <CommonButton 
                        v-if="isOwner"
                        :text="'Modificar'"
                        :icon="'fa-solid fa-pen-to-square'"
                        :thin="true"
                        :route="`/update-route/${route.slug}-${route.id}`"
                    />
                </div>
                
                <ShowMap
                    :detailed-map="false"
                ></ShowMap>
            </div>
            
            <div class="user-container">
                <div class="user-wrapper">
                    <div class="user-detail">
                        <img :src="getUserRouteIcon(route)" @error="handleImgError" class="avatar" />
                        <p :title="route.user.username">{{ route.user.username }}</p>
                    </div>
                    <div class="route-detail-container">
                        <h1 class="route-head">Estadísticas de la ruta</h1>
                        <div class="table">
                            <div class="row">
                                <div>
                                    <h1>Distancia</h1>
                                    <p>{{ (route.distance / 1000).toFixed(1) }} km</p>
                                </div>
                                 <div>
                                    <h1>Dificultad</h1>
                                    <p>{{ route.difficulty }}</p>
                                </div>
                            </div>
                            <div class="row">
                                <div>
                                    <h1>Desnivel Positivo</h1>
                                    <p v-if="elevationData">{{ elevationData.ascent }} m</p>
                                </div>
                                <div>
                                    <h1>Desnivel Negativo</h1>
                                    <p v-if="elevationData">{{ elevationData.descent }} m</p>
                                </div>
                            </div>
                            <div class="row">
                                <div>
                                    <h1>Altitud Max.</h1>
                                    <p v-if="elevationData">{{ elevationData.maxElevation }} m</p>
                                </div>
                                <div>
                                    <h1>Altitud Min.</h1>
                                    <p v-if="elevationData">{{ elevationData.minElevation }} m</p>
                                </div>
                            </div>
                            <div class="row-single">
                                <h1>Coordenadas Salida</h1>
                                <p><strong>Lat: </strong>{{ route.start_latitude }}</p>
                                <p><strong>Lon: </strong>{{ route.start_longitude }}</p>
                            </div>
                            <div class="row-single">
                                <h1>Coordenadas Llegada</h1>
                                <p v-if="lastCoord"><strong>Lat: </strong>{{ lastCoord.lat }}</p>
                                <p v-if="lastCoord"><strong>Lon: </strong>{{ lastCoord.lon }}</p>
                            </div>
                            <div class="row-single">
                                <h1>Tiempo</h1>
                                <p>{{ formatDuration(route.duration) }}</p>
                            </div>
                            <div class="row-single">
                                <h1>Valorar Ruta</h1>
                                <RatingButton 
                                    :route-id="route.id"
                                    :route-user-id="route.user.id"
                                    @rating-updated="refreshRouteData"
                                />
                                <p>{{ route.average_rating }} / 5</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="content-wrapper">
            <RouteCarousel 
                :img-carousel="true"
                :img-urls="imgRoute"
            />
    
            <div class="description-route">
                <h1>Descripción del Itinerario</h1>
                <div class="description-text" v-html="route.description_html"></div>
            </div>
    
            <div class="comment-container">
                <h1>Comentarios</h1>
                <div class="comment-card" v-for="comment in route.comments" :key="comment">
                    <img :src="getIconUserComment(comment)" @error="handleImgError" class="avatar" ref="userImg" />
                    <div class="comment">
                        <div>
                            <h1>{{ comment.user.username }}</h1>
                            <p>{{ formatDate(comment.created_date) }}</p>
                        </div>
                        <p>{{ comment.content }}</p>
                    </div>
                </div>
    
            </div>
            
            <AddComment 
                :route-id="route.id"
                @comment-submitted="refreshRouteData"
            />
        </div>
    </div>
    
    <div v-else>
        <h1>Error al Cargar la Ruta</h1>
    </div>
</template>
  
<script setup> 
    // IMPORTS
    import { computed, onMounted, ref } from 'vue'
    import { DOMParser } from 'xmldom'
    import { gpx } from '@tmcw/togeojson'
    import { getMediaUrl } from '@/utils/media'
    import { useAuthStore } from '@/stores/authStore'
    import { useRouteImage } from '@/composables/useRouteImage'
    import { useUserCommentImage } from '@/composables/useUserImage'

    import { apiWithAuth } from '@/utils/api'
    import api from '@/utils/api'
    
    import ShowMap from '@/components/map/ShowMap.vue'
    import CommonButton from '@/components/common/CommonButton.vue'
    import RouteCarousel from '@/components/images/RouteCarousel.vue'
    import RatingButton from '@/components/auth/RatingButton.vue'
    import AddComment from '@/components/auth/AddComment.vue'

    // PROPS
    const props = defineProps({
        id: {
            type: String,
            required: true
        },
        slug: {
            type: String,
            required: true
        }
    })  
    
    // VARIABLES
    const route = ref(null)
    const elevationData = ref(null)
    const lastCoord = ref(null)
    const imgRoute = ref(null)

    const isFavorite = ref(false)
    const favoriteId = ref(null)

    // Compruebo si el usuario es el dueño de la ruta
    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const currentUserId = computed(() => authStore.user?.id ?? null)
    const isOwner = computed(() => {
        return route.value && currentUserId.value === route.value.user.id
    })

    const { getRouteAllImgURL, getUserRouteIcon } = useRouteImage()
    const { getIconUserComment, handleImgError } = useUserCommentImage()

    // METODOS
    // Obtener la URL del GPX de la Ruta
    const getGPXUrl = (route) => {
        return getMediaUrl(`/${route.user.username}/${route.slug}/${route.gpx_file}`)
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
    
    // Transformar la fecha en "6h 10min"
    const formatDuration = (seconds) => {
        const h = Math.floor(seconds / 3600)
        const m = Math.floor((seconds % 3600) / 60)
        return h > 0 ? `${h}h ${m}min` : `${m}min`
    }
    
    // Saber que icono de ruta poner en funcion del tipo
    const iconType = (route) => {
        switch(route.type) {
            case "Senderismo": return '<i class="fa-solid fa-person-hiking"></i>';
            case "Para-Todos": return '<i class="fa-solid fa-people-roof"></i>';
            case "Ciclismo": return '<i class="fa-solid fa-person-biking"></i>';
            case "Trail-Running": return '<i class="fa-solid fa-person-running"></i>';
            case "Alpinismo": return '<i class="fa-solid fa-mountain"></i>';
            default: return '<i class="fa-solid fa-question"></i>';
        }
    }
    
    // Mandar el HTML del icono de la Ruta
    const routeType = (route) =>{
        return `${iconType(route)} <p>${route.type}</p>`;
    }
    
    // Obtener la elevacion positiva y negativa media, las ultimas coordenadas y la elevacion max y min
    const parseGPX = async(gpxUrl) => {
        const response = await fetch(gpxUrl)
        const text = await response.text()
        const xml = new DOMParser().parseFromString(text, 'text/xml')
        const geojson = gpx(xml)
        
        const elevations = []
        
        geojson.features.forEach(feature => {
            if (feature.geometry.type === 'LineString') {
                const coords = feature.geometry.coordinates
                
                coords.forEach(coord => {
                    const ele = coord[2]
                    if (typeof ele === 'number') {
                        elevations.push(ele)
                    }
                })
                
                const last = coords[coords.length - 1]
                if (last) {
                    lastCoord.value = {
                        lat: last[1],
                        lon: last[0]
                    }
                }
            }
        })
        
        return calculateElevationGainLoss(elevations)
    }
    
    // Calcula la elevacion
    const calculateElevationGainLoss = (elevations) => {
        let gain = 0
        let loss = 0
        
        for (let i = 1; i < elevations.length; i++) {
            const diff = elevations[i] - elevations[i -1]
            if (diff > 0) gain += diff
            else if (diff < 0) loss -= diff
        }
        
        return {
            ascent: Math.round(gain),
            descent: Math.round(loss),
            maxElevation: Math.max(...elevations).toFixed(1),
            minElevation: Math.min(...elevations).toFixed(1)
        }
    }
    
    // Funcion para guardar una ruta en favoritos
    const toggleFavorite = async () => {
        try {
            // Eliminar de favoritos
            if (isFavorite.value) {
                await apiWithAuth().delete(`/favorites/${favoriteId.value}/`)
                isFavorite.value = false
                favoriteId.value = null
            
                // Añadir a favoritos
            } else {
                const response = await apiWithAuth().post(`/favorites/`, {
                    user: currentUserId.value,
                    route: route.value.id
                })
                isFavorite.value = true
                favoriteId.value = response.data.id
            }
        } catch (error) {
            console.error('Error en toggle de favoritos:', error)
        }
    }
    
    // Funcion que comprueba si una ruta esta en favoritos o no
    const checkIfFavorite = async () => {
        if (!isAuthenticated.value) return
        
        try {
            const response = await apiWithAuth().get(`/favorites/?user=${currentUserId.value}&route=${route.value.id}`)
            if (response.data.length > 0) {
                isFavorite.value = true
                favoriteId.value = response.data[0].id
            } else {
                isFavorite.value = false
                favoriteId.value = null
            }
        } catch (error) {
            console.error('Error comprobando favoritos:', error)
        }
    }

    // Funcion que permite actualizar los datos de la Ruta
    const refreshRouteData = async () => {
        try {
            const response = await api.get(`/routes/${props.id}/`)
            route.value = response.data
            elevationData.value = await parseGPX(getGPXUrl(route.value))
            imgRoute.value = await getRouteAllImgURL(route.value)
        } catch (error) {
            console.error('Error recargando los datos de la ruta:', error)
        }
    }
    
    // Realiza la llamada a la API para obtener los datos de la Ruta
    onMounted(async () => {
        await refreshRouteData()
        await checkIfFavorite()
    })
</script>  

<style lang="scss" scoped>
    .main-container {
        display: grid;
        grid-template-columns: 1fr 25rem;
        gap: 1rem;
        margin: 2rem 10rem;
        
        .map-container {
            .route-type {
                font-size: 1.5rem;
                font-weight: 900;
                color: var(--color-dark-grey);
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }        

            h1 {
                font-size: 1.75rem;
                font-family: "Montserrat-Bold";
                font-weight: 900;
                text-align: left;
            }

            .date-buttons {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 0.25rem;

                p {
                    flex: 1;
                    font-size: 1rem;
                    font-weight: 900;
                    color: var(--color-dark-grey);
                }
            }
        }

        .user-container {
            align-self: flex-end;
            
            .user-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 0.5rem;
                background-color: var(--color-vanille-opacity);
                border-radius: 25px;
                box-shadow: 2px 2px 5px 1px var(--color-black); 
                
                .user-detail {
                    display: flex;
                    align-items: center;
                    gap: 1rem;                
    
                    img {
                        max-width: 10rem;
                        height: 8rem;
                        border-radius: 25px;
                        border: 2px solid var(--color-green);
                    }
            
                    p {
                        font-family: "Montserrat-Bold";
                        font-weight: 900;
                        font-size: 1.25rem;
                    }
    
                }
    
                .route-detail-container {
                    .route-head {
                        font-size: 1.25rem;
                        text-align: left;
                        margin: 1rem 0 0.25rem;
                    }
    
                    .row {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        border-top: 2px solid var(--color-grey);
                        text-align: center;
    
                        div {
                            width: 10rem;
                            padding-top: 0.5rem;
                            margin: 0 1rem;
                        }
    
                        div:first-child {
                            border-right: 2px solid var(--color-grey);
                        }
    
                        h1 {
                            font-size: 1rem;
                            color: var(--color-green);
                            line-height: 1;
                        }
    
                        p {
                            font-weight: 900;
                        }
    
                        strong {
                            color: var(--color-green);
                        }
                    }
    
                    .row-single {
                        display: grid;
                        grid-template-columns: 1fr;
                        border-top: 2px solid var(--color-grey);
                        text-align: center;
                        padding-top: 0.5rem;
    
                        h1 {
                            font-size: 1rem;
                            color: var(--color-green);
                            line-height: 1;
                        }
    
                        p {
                            font-weight: 900;
                        }
    
                        strong {
                            color: var(--color-green);
                        }
                    }
                }
            }
        }
    }

    .content-wrapper {  
        margin: 0 10rem;

        .description-route {
            display: flex;
            flex-direction: column;
            margin-top: 1rem;
            
            h1 {
                font-family: "Montserrat-Bold";
                font-size: 1.5rem;
                color: var(--color-green);
                text-align: left;
            }
        }
    
        .comment-container {
            display: flex;
            flex-direction: column;
            margin: 1rem 0;
            gap: 1rem;
            padding-top: 1rem;
            border-top: 3px solid var(--color-light-green);
    
            h1 {
                font-family: "Montserrat-Bold";
                font-size: 1.5rem;
                color: var(--color-green);
                text-align: left;
            }
    
            .comment-card {
                display: flex;
                gap: 1rem;
                padding-bottom: 1rem;
                border-bottom: 5px dotted var(--color-grey);
    
                img {
                    width: 4rem;
                    height: 4rem;
                    border-radius: 25px;
                    object-fit: cover;
                    border: 2px solid var(--color-light-green);
                }
    
                .comment {
                    div {
                        display: flex;
                        align-items: center;
                        gap: 1rem;
    
                        h1 {
                            font-size: 1.25rem;
                            color: var(--color-light-green);
                        }
                        
                        p {
                            font-weight: 900;
                            color: var(--color-grey);
                        }
                    }
                }
            }
        }
    }

    @media (max-width: 1450px) {
        .main-container {
            display: flex;
            flex-direction: column;
            margin: 2rem;

            .user-container {
                align-self: center;

                .user-wrapper {
                    flex-direction: row;

                    .user-detail {
                        width: 12rem;
                        flex-direction: column;

                        p {
                            white-space: nowrap;         
                            overflow: hidden;             
                            text-overflow: ellipsis; 
                            max-width: 100%;
                            display: block;
                        }
                    }

                    .route-detail-container {
                        max-width: 30rem;
                        
                        .table {
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            grid-template-rows: repeat(3, 5rem);

                            
                            .row {
                                grid-template-columns: 1fr 1fr;
                                align-items: center;
                                
                                div {
                                    height: 100%;
                                    border-right: 2px solid var(--color-grey);
                                    width: auto;
                                    margin: 0;
                                    display: flex;
                                    flex-direction: column;
                                    justify-content: center;

                                }

                                &:nth-child(3) {
                                    border-bottom: 2px solid var(--color-grey);
                                }
                            }
                            
                            .row-single {
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                align-items: center;
                                padding: 0.25rem 0;
                                
                                &:nth-child(4) {
                                    grid-column: 2/3;
                                    grid-row: 1/2;
                                }
    
                                &:nth-child(5) {
                                    grid-column: 2/3;
                                    grid-row: 2/3;
                                }

                                &:nth-child(6) {
                                    border-bottom: 2px solid var(--color-grey);       
                                }

                                &:nth-child(7) {
                                    border: 0;
                                    grid-column: 1/3;
                                }
                            }
                        }
                    }
                }
            }
        }
        
        .content-wrapper {
            margin: 0 2rem;
        }
    }

    @media (max-width: 700px) {
        .main-container {
            margin: 2rem 0;

            .map-container {
                .route-type, h1, .date-buttons {
                    margin: 0.25rem 1rem;
                }

                h1 {
                    text-align: center;
                    font-size: 1.5rem;
                    line-height: 1;
                }

                .date-buttons {
                    justify-content: center;
                    margin: 0.25rem 0;
                    position: relative;
                    padding-top: 1.5rem;
                    gap: 0.15rem;

                    p {
                        position: absolute;
                        top: 0;
                    }
                }
            }

            .user-container {
                .user-wrapper {
                    flex-direction: column;
                    margin: 0 1rem;
                }

                .route-detail-container {
                    h1 {
                        font-size: 0.95rem;
                    }

                    p {
                        font-size: 0.85rem;
                    }
                }
            }
        }

        .content-wrapper {
            margin: 0 1rem;

            .description-route {
                h1 {
                    font-size: 1.25rem;
                }

                .description-text {
                    font-size: 0.95 rem;
                }
            }

            .comment-container {
                .comment-card {
                    .comment {
                        div {
                            align-items: flex-start;
                            flex-direction: column;
                            gap: 0;
                            margin-bottom: 0.5rem;

                            h1 {
                                line-height: 1;
                                font-size: 1.25rem;
                            }

                        }

                        p {
                            font-size: 0.95rem;
                        }
                    }
                }
            }
        }
    }
</style> 

<style lang="scss">
    .description-route {
        ol {
            list-style: normal;
            padding-left: 2rem;

            li {
                padding-left: 0.25rem;
            }
        }
    }
</style>