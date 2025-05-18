<template>
    <div v-if="route">
        <div class="header-info main-container">
            <div class="route-type" v-html="routeType(route)"></div>
            <h1>{{ route.title }}</h1>
            <div>
                <p>{{ formatDate(route.created_date) }}</p>
                <CommonButton 
                    :text="'Favoritos'"
                    :icon="'fa-solid fa-bookmark'"
                    :thin="true"
                    :route="'/'"
                />
                <CommonButton 
                    v-if="isOwner"
                    :text="'Modificar'"
                    :icon="'fa-solid fa-pen-to-square'"
                    :thin="true"
                    :route="`/update-route/${route.slug}-${route.id}`"
                />
            </div>
        </div>

        <div class="map-container-detail">
            <ShowMap
                :detailed-map="false"
            ></ShowMap>
            
            <div>
                <div class="user-container">
                    <img :src="getIconUserImg(route)" class="avatar" />
                    <p>{{ route.user.username }}</p>
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
                                @rating-submitted="refreshRouteData"
                            />
                            <p>{{ route.average_rating }} / 5</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <RouteCarousel 
            :img-carousel="true"
            :img-urls="imgRoute"
        />

        <div class="description-route">
            <h1>Descripción del Itinerario</h1>
            <div v-html="route.description_html"></div>
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
    
    <div v-else>
        <h1>Error al Cargar la Ruta</h1>
    </div>
</template>
  
<script setup>
    import { computed, onMounted, ref } from 'vue'
    import { DOMParser } from 'xmldom'
    import { gpx } from '@tmcw/togeojson'
    import { getMediaUrl } from '@/api/media'
    import { useAuthStore } from '@/stores/authStore'

    import api from '@/api/api'
    
    import ShowMap from '@/components/ShowMap.vue'
    import CommonButton from '@/components/common/CommonButton.vue'
    import RouteCarousel from '@/components/images/RouteCarousel.vue'
    import RatingButton from '@/components/auth/RatingButton.vue'
    import AddComment from '@/components/auth/AddComment.vue'

    const props = defineProps({
        id: String,
        slug: String
    })

    // Funcion que permite actualizar los datos de la Ruta
    const refreshRouteData = async () => {
        try {
            const response = await api.get(`/routes/${props.id}/`)
            route.value = response.data
            elevationData.value = await parseGPX(getGPXUrl(route.value))
            imgRoute.value = await getImgRoute(route.value)
        } catch (error) {
            console.error('Error recargando los datos de la ruta:', error)
        }
    }

    // Realiza la llamada a la API para obtener los datos de la Ruta
    onMounted(async () => {
        refreshRouteData()
    })

    const route = ref(null)
    const elevationData = ref(null)
    const lastCoord = ref(null)
    const imgRoute = ref(null)

    // Compruebo si el usuario es el dueño de la ruta
    const authStore = useAuthStore()
    const currentUserId = computed(() => authStore.user?.id ?? null)
    const isOwner = computed(() => {
        return route.value && currentUserId.value === route.value.user.id
    })

    // Obtener las imagenes de las Rutas
    const getImgRoute = (route) => {
        const arrayImg = []
        for (let i = 0; i < route.img.length; i++) {
            const img = getMediaUrl(`/${route.user.username}/${route.slug}/${route.img?.[i]}`)
            arrayImg.push(img)
        }
        return arrayImg;
    }
    
    // Obtener el icono del usuario de la Ruta
    const getIconUserImg = (route) => {
        return getMediaUrl(`/${route.user.username}/${route.user.profile_picture}`)
    }

    // Obtener el icono del usuario que ha puesto el comentario
    const getIconUserComment = (comment) => {
        return getMediaUrl(`${comment.user.username}/${comment.user.profile_picture}`)
    }
    function handleImgError(event) {
        event.target.src = getMediaUrl('/sample_user_icon.png');
    }

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
</script>  

<style lang="scss" scoped>
    .main-container {
        margin: 2rem 40rem 0 10rem;    
    }

    .map-container-detail {
        margin: 0.25rem 0 0 10rem;
        display: flex;
        align-items: center;
        gap: 4rem;
    }

    .header-info {
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

        div:last-child {
            display: flex;
            align-items: center;
            gap: 1rem;

            p {
                flex: 1;
                font-size: 1rem;
                font-weight: 900;
                color: var(--color-dark-grey);
            }
        }
    }

    .user-container {
        display: flex;
        align-items: center;
        gap: 2rem;
        padding: 0.5rem;
        background-color: var(--color-vanille);
        border-radius: 25px;

        img {
            width: auto;
            height: 8rem;
            border-radius: 25px;
        }

        p {
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

    .description-route {
        display: flex;
        flex-direction: column;
        margin: 0 10rem 2rem;
        
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
        gap: 1rem;
        margin: 0 10rem 2rem;
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