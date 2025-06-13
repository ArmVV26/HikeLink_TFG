<template>
    <div class="map-container">
        <div v-if="detailedMap" class="map-top-container">
            <input type="text" id="location-search" placeholder="🔍 Buscar por lugares, regiones, coordenadas y más ..."
                @input="handleInput"
                @keydown.down.prevent="highlightNext"
                @keydown.up.prevent="highlightPrev"
                @keydown.enter.prevent="selectHighlighted"
            >
            <ul v-if="suggestions.length" class="suggestions-list">
                <li 
                    v-for="(s, i) in suggestions"
                    :key="i"
                    :class="{highlighted: i === highlightedIndex}"
                    @click="selectSuggestion(s)"
                >
                    {{ s.display_name }}
                </li>
            </ul>

            <button v-if="!isMobile" class="fullscreen-btn" @click="toggleFullscreen">
                <i class="fa-solid fa-expand"></i>
            </button>
        </div>
        
        <div id="map" :class="{'map': detailedMap, 'map-detailed': !detailedMap}">

            <!-- Seleccionar el tipo de mapa -->
            <div class="map-style-toggle">
                <button @click="toggleMenu">
                    <i class="fa-solid fa-layer-group"></i>
                </button>

                <transition name="fade-slide">
                    <ul v-if="menuVisible" class="map-style-menu">
                        <li @click="changeTile('osm')">OpenStreetMap</li>
                        <li @click="changeTile('topo')">OpenTopoMap</li>
                        <li @click="changeTile('sat')">Satélite (ESRI)</li>
                        <li @click="changeTile('light')">Carto Light</li>
                        <li @click="changeTile('dark')">Carto Dark</li>
                    </ul>
                </transition>
            </div>

            <!-- Leyenda del mapa -->
            <div v-if="detailedMap" :class="['legend', {'hide-mobile': selectedRoute && detailedMap}]">
                <i class="fa-solid fa-location-dot text-green-600">
                    <p>Wikiloc</p>
                </i>
                <i class="fa-solid fa-location-dot text-orange-600">
                    <p>Strava</p>
                </i>
                <i class="fa-solid fa-location-dot text-yellow-600">
                    <p>OutdoorActive</p>
                </i>
                <i class="fa-solid fa-location-dot text-purple-600">
                    <p>AllTrails</p>
                </i>
                <i class="fa-solid fa-location-dot text-blue-600">
                    <p>Komoot</p>
                </i>
            </div>

            <!-- Poner el mapa en grande, si es una unica ruta -->
            <button v-if="!detailedMap && !isMobile" class="fullscreen-btn-map" @click="toggleFullscreen">
                <i class="fa-solid fa-expand"></i>
            </button>

            <!-- Boton para salir de pantalla completa -->
            <button v-if="isFullscreen" class="exit-fullscreen-btn" @click="exitFullscreen">
                <i class="fa-solid fa-compress"></i>
            </button>

            <!-- Mostrar info del mapa -->
            <div :class="['map-info-button', { 'hide-mobile': selectedRoute && detailedMap }]">
                <button @click="showInfo = true" :class="{'hide': showInfo}">
                    <i class="fa-solid fa-circle-info"></i>
                </button>
            </div>

            <transition name="fade-slide">
                <div v-if="showInfo" class="map-info-panel">
                    <button class="close-btn" @click="showInfo = false">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <h1>HikeLink Mapa</h1>
                    <p>
                        Este mapa muestra rutas de senderismo extraídas de datos públicos
                        geoespaciales. Incluye caminos, puntos de interés y diferentes estilos de visualización.
                    </p>
                    <p><strong>Estilo Actual:</strong> {{ currentStyleName }}</p>
                    <p><strong>Fuentes:</strong> OpenStreetMap, OpenTopoMap, ESRI, CartoDB</p>
                    <p><strong>Desarrollado por:</strong> Armando Vaquero Vargas</p>
                    <p><strong>Licencia:</strong> CC BY-SA 4.0</p>
                    <p><strong>Última actualización:</strong> Junio 2025</p>
                </div>
            </transition>

            <transition v-if="detailedMap " name="fade-slide">
                <div v-if="selectedRoute" class="route-info-container">
                    <div class="route-imgs">
                        <img :src="getRouteImg(selectedRoute)" 
                            @error="handleImgError" 
                            alt="Imagen de ruta"
                        />
                    </div>
                    <div class="route-info">
                        <h1 :title="selectedRoute.title">{{ selectedRoute.title }}</h1>
                        <p><strong :style="{color: getColorByOrigin(selectedRoute.origin)}">{{ selectedRoute.origin }}</strong></p>
                        <p>Ruta de {{ selectedRoute.user.username }}</p>
                        <p class="route-meta">
                            ★ {{ selectedRoute.average_rating?.toFixed(1) || 'N/A' }} ·
                            {{ selectedRoute.difficulty }} ·
                            {{ (selectedRoute.distance / 1000).toFixed(1) }} km ·
                            Est. {{ formatDuration(selectedRoute.duration) }}
                        </p>
                    </div>
    
                    <button class="close-btn" @click="closeRouteDetails">
                        <i class="fa-solid fa-xmark"></i>
                    </button>

                    <router-link class="route-link" :to="{name: 'RouteDetail', params: {id: selectedRoute.id, slug: selectedRoute.slug  } }">
                        <p>Ver Ruta</p>
                    </router-link>
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { defineProps, ref, onMounted, computed, onUnmounted } from 'vue';
    import { useRoute } from 'vue-router'
    import { getMediaUrl } from '@/utils/media';
    import { useRouteImage } from '@/composables/useRouteImage' 
    import L from 'leaflet';
    import 'leaflet-gpx';
    import 'leaflet.fullscreen';
    import 'leaflet.fullscreen/Control.FullScreen.css';
    import api from '@/utils/api';

    // PROPS
    const props = defineProps({
        detailedMap: {
            type: Boolean,
            default: true
        }
    })

    // VARIABLES
    const map = ref(null)
    const tileLayer = ref(null)
    const menuVisible = ref(false)
    const showInfo = ref(false)
    const currentStyleName = ref('OpenStreetMap')
    const shownRoutes = ref(new Set())
    const routeMarkers = ref(new Map())
    const gpxLayers = ref(new Map())
    const selectedRoute = ref(null)
    const isFullscreen = ref(false)
    const isMobile = ref(window.innerWidth <= 700)

    const suggestions = ref([])
    const highlightedIndex = ref(-1)

    const vueRoute = useRoute()

    const { getRouteImg, handleImgError } = useRouteImage()

    // COMPUTED
    const isSingleRoute = computed(() => !!vueRoute.params.id)

    // METODOS
    // Funcion para mostrar o no el menu visible de los layers
    const toggleMenu = () => {
        menuVisible.value = !menuVisible.value
    } 

    // Funcion para cambiar el tipo de layer del mapa
    const changeTile = (style) => {
        const tileURLs = {
            osm: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            topo: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            sat: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            light: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
            dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        };

        const tileNames = {
            osm: 'OpenStreetMap',
            topo: 'OpenTopoMap',
            sat: 'Satélite (ESRI)',
            light: 'Carto Light',
            dark: 'Carto Dark',
        };

        if (tileLayer.value) map.value.removeLayer(tileLayer.value)

        tileLayer.value = L.tileLayer(tileURLs[style], {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(map.value);

        currentStyleName.value = tileNames[style]
        menuVisible.value = false
    }

    // Funcion para obtener el color del marker en funcion del origen de la ruta
    const getColorByOrigin = (origin) => {
        switch (origin) {
            case 'Wikiloc': return 'green';
            case 'Strava': return 'red';
            case 'OutdoorActive': return 'orange';
            case 'AllTrails': return 'violet';
            case 'Komoot': return 'blue';
            default: return 'gray';
        }
    }

    const toggleRoute = (route) => {
        if (isSingleRoute.value)  {
            const color = getColorByOrigin(route.origin)
            const gpxURL = getMediaUrl(`/${route.user.username}/${route.slug}/${route.gpx_file}`)

            const gpx = new L.GPX(gpxURL, {
                async: true,
                    markers: {
                        startIcon: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png`,
                        endIcon: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png`
                    },
                    marker_options: {
                        iconSize: [20, 30],
                        iconAnchor: [10, 30]
                    },
                    polyline_options: {
                        color: color,
                        weight: 4,
                        opacity: 0.75
                    }
            })

            gpx.on('loaded', function (e) {
                const bounds = e.target.getBounds()
                map.value.fitBounds(bounds)
                map.value.setMaxBounds(bounds.pad(0.2))
                map.value.setMinZoom(map.value.getZoom())
                map.value.setMaxZoom(map.value.getZoom() + 3)
            })

            gpx.addTo(map.value)
            gpxLayers.value.set(route.id, gpx)
            shownRoutes.value.add(route.id)
        } else {
            if (shownRoutes.value.has(route.id)) {
                const layer = gpxLayers.value.get(route.id)
                if (layer) map.value.removeLayer(layer)

                shownRoutes.value.delete(route.id)
                gpxLayers.value.delete(route.id)
            } else {
                shownRoutes.value.forEach((routeId) => {
                    const layer = gpxLayers.value.get(routeId)
                    if (layer) map.value.removeLayer(layer)

                    gpxLayers.value.delete(routeId)
                })

                shownRoutes.value.clear()

                const color = getColorByOrigin(route.origin)
                const gpxURL = getMediaUrl(`/${route.user.username}/${route.slug}/${route.gpx_file}`)

                const gpx = new L.GPX(gpxURL, {
                    async: true,
                    markers: {
                        startIcon: null,
                        endIcon: null,
                        shadow: null,
                        wptIcons: false
                    },
                    polyline_options: {
                        color: color,
                        weight: 4,
                        opacity: 0.75
                    }
                })

                // Para hacer zoom in a la ruta seleccionada
                // gpx.on('loaded', function (e) {
                //      map.value.fitBounds(e.target.getBounds());
                // });

                gpx.on('addLine', function (e) {
                    const polyline = e.line
                    polyline.on('mouseover', () => polyline.setStyle({ weight: 6, opacity: 1 }))
                    polyline.on('mouseout', () => polyline.setStyle({ weight: 4, opacity: 0.75 }))
                })

                gpx.addTo(map.value)
                gpxLayers.value.set(route.id, gpx)
                shownRoutes.value.add(route.id)
            }
        }
    }

    // Funcion para cargar las rutas en el mapa
    const loadRoutes = async () => {
        try {
            const response = await api.get('/routes/')
            const routes = response.data

            routes.forEach(route => {
                const color = getColorByOrigin(route.origin)
                const icon = L.icon ({
                    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`,
                    iconSize: [25,41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                })

                const marker = L.marker([
                    route.start_latitude, route.start_longitude
                    ], { icon }).addTo(map.value);

                // Al hacer clic en el marcador, mostrar la ruta GPX
                marker.on('click', function() {
                    selectedRoute.value = route
                    toggleRoute(route)
                })

                routeMarkers.value.set(route.id, marker)
            }) 
        } catch (error) {
            console.error('Error cargando rutas: ', error)
        }
    }

    // Funcion pra mostrar la duracion de la ruta formateada
    const formatDuration = (seconds) => {
        const h = Math.floor(seconds / 3600)
        const m = Math.floor((seconds % 3600) / 60)
        return h > 0 ? `${h}h ${m}min` : `${m}min`
    }

    // Funcion para buscar por ubicacion en el buscador
    const handleInput = async (e) => {
        const query = e.target.value

        if (query.length < 3) {
            suggestions.value = []
            return
        }

        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&addressdetails=1&limit=5`

        try {
            const res = await fetch(url)
            const data = await res.json()

            suggestions.value = data
            highlightedIndex.value = -1
        } catch (err) {
            console.error("Error buscando sugerencias: ", err)
        }
    }

    // Funcion para mover el mapa hacia la ubicacion indicada
    const selectSuggestion = (suggestion) => {
        suggestions.value = [];
        map.value.setView([parseFloat(suggestion.lat), parseFloat(suggestion.lon)], 13);
        document.getElementById("location-search").value = suggestion.display_name;
    }

    // Funcion para remarca la siguiente opcion del buscador
    const highlightNext = () => {
        if (highlightedIndex.value < suggestions.value.length - 1) {
            highlightedIndex.value++;
        }
    }

    // Funcion para remarcar la anterior opcion del buscador
    const highlightPrev = () => {
        if (highlightedIndex.value > 0) {
            highlightedIndex.value--;
        }
    }

    // Funcion para remarcar y seleccionar la opcion indicada
    const selectHighlighted = () => {
        if (highlightedIndex.value >= 0) {
            selectSuggestion(suggestions.value[highlightedIndex.value]);
        }
    }

    // Funcion para mostrar el mapa en pantalla completa
    const toggleFullscreen = () => {
        const mapContainer = document.getElementById('map');

        if (!document.fullscreenElement) {
            mapContainer.requestFullscreen().catch(err => {
                console.error(`Error al entrar en pantalla completa: ${err.message}`);
            });
        } else {
            exitFullscreen();
        }
    }

    // Función para salir de pantalla completa
    const exitFullscreen = () => {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
    }

    // Función para manejar cambios en el tamaño de la ventana
    const handleResize = () => {
        isMobile.value = window.innerWidth <= 700;
    }

    // Funcion para quitar las rutas del mapa y cerrar los detalles de la ruta
    const closeRouteDetails = () => {
        if (selectedRoute.value && gpxLayers.value.has(selectedRoute.value.id)) {
            const layer = gpxLayers.value.get(selectedRoute.value.id)
            if (layer) map.value.removeLayer(layer)

            shownRoutes.value.delete(selectedRoute.value.id)
            gpxLayers.value.delete(selectedRoute.value.id)
        }

        selectedRoute.value = null
    }

    onMounted( () => {
        map.value = L.map('map' || 'map-detail').setView([37.1773, -3.5986], 13)

        tileLayer.value = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(map.value)

        if (!isSingleRoute.value) {
            L.control.scale({ position: 'topleft', imperial: true, metric: true}).addTo(map.value)
        }

        // Detectar cambio de pantalla completa
        document.addEventListener('fullscreenchange', () => {
            const mapElement = document.getElementById('map')
            isFullscreen.value = !!document.fullscreenElement;
            if (document.fullscreenElement) {
                mapElement.classList.add('fullscreen-border')
            } else {
                mapElement.classList.remove('fullscreen-border')
            }
        });

        // Añadir listener para cambios de tamaño de ventana
        window.addEventListener('resize', handleResize);

        if (isSingleRoute.value) {
            api.get(`/routes/${vueRoute.params.id}`)
                .then(response => {
                    selectedRoute.value = response.data;
                    toggleRoute(selectedRoute.value);
                })
                .catch(error => {
                    console.error('Error cargando ruta individual:', error);
                })
        } else {
            loadRoutes();
        }
    })

    onUnmounted(() => {
        // Limpiar listeners
        window.removeEventListener('resize', handleResize);
    })
</script>

<style lang="scss" scoped>
    .map-container {
        position: relative;

        .map-top-container {
            position: relative;
            width: 70%;
            margin: 2rem auto 0;
            background-color: var(--color-vanille);
            padding: 0.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;

            border-top-left-radius: 25px;
            border-top-right-radius: 25px;
            
            border-top: 5px solid var(--color-green);
            border-left: 5px solid var(--color-green);
            border-right: 5px solid var(--color-green);
            
            #location-search {
                width: 100%;
                height: 3rem;
                margin-left: 1rem;
                background-color: var(--color-white);
                border: 2px solid var(--color-grey);
                outline: none;
                border-radius: 25px;    
                padding: 0 1rem;
            }
            
            .suggestions-list {
                position: absolute;
                top: 3.5rem;
                left: 0.5rem;
                width: 55%;
                background: var(--color-white);
                border: 5px solid var(--color-green);
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                max-height: 10rem;
                overflow-y: auto;
                z-index: 1001;
                list-style: none;
                
                li {
                    padding: 0.5rem;
                    cursor: pointer;
                    transition: all 0.25s;
                    
                    &:hover, &.highlighted {
                        background-color: var(--color-vanille);
                    }
                }
            }
            
            .fullscreen-btn {
                color: var(--color-green);
                background-color: var(--color-white);
                border: 2px solid var(--color-light-green);
                font-size: 1.5rem;
                padding: 0.25rem 0.75rem;
                border-radius: 20rem;
                margin-right: 1rem;
                cursor: pointer;
                transition: all 0.25s;
        
                &:hover {
                    color: var(--color-white);
                    background-color: var(--color-light-green);
                    border: 2px solid var(--color-green);
                }
            }
        }
        
        .map {
            width: 70%;
            height: 43.5rem;
            margin: 0 auto 2rem;
    
            border-bottom-left-radius: 25px;
            border-bottom-right-radius: 25px;
            
            border-bottom: 5px solid var(--color-green);
            border-left: 5px solid var(--color-green);
            border-right: 5px solid var(--color-green);
            z-index: 1;
        }

        .map-detailed {
            width: 100%;
            height: 40.5rem;
            
            border: 5px solid var(--color-green);
            border-radius: 25px;
        }

        .map, .map-detailed {
            .map-style-toggle {
                position: absolute;
                top: 1rem;
                right: 1rem;
                z-index: 1000;
                
                button {
                    background: var(--color-white);
                    border: 2px solid var(--color-light-green);
                    padding: 0.5rem 1rem 0.5rem;
                    border-radius: 10rem;
                    cursor: pointer;
            
                    font-size: 2rem;
                    color: var(--color-green);
            
                    transition: all 0.25s;

                    &:hover {
                        color: var(--color-white);
                        background-color: var(--color-brown);
                        border: 2px solid var(--color-vanille);
                    }
                }
            }

            .legend {
                position: absolute;
                bottom: 2rem;
                right: 1rem;

                display: flex;
                flex-direction: column;
                justify-content: center;

                padding: 0.5rem;
                background-color: var(--color-white);
                border: 2px solid var(--color-light-green);
                border-radius: 25px;
                box-shadow: 0 2px 8px var(--color-black);

                z-index: 1000;

                i {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-size: 1rem;
                    font-weight: 900;
                    line-height: 1.25;
                        
                    p {
                        font-family: "Lato";
                        font-size: 1.25rem;
                    }
                }
            }

            .fullscreen-btn-map {
                z-index: 1000;
                position: absolute;
                bottom: 1.5rem;
                right: 1rem;
                color: var(--color-green);
                background-color: var(--color-white);
                border: 2px solid var(--color-light-green);
                font-size: 2rem;
                padding: 0.25rem 1rem;
                border-radius: 20rem;
                cursor: pointer;
                transition: all 0.25s;
                
                &:hover {
                    color: var(--color-white);
                    background-color: var(--color-brown);
                    border: 2px solid var(--color-vanille);
                }
            }
            
            .map-info-button {
                position: absolute;
                bottom: 1rem;
                left: 1rem;
                z-index: 1000;
                
                button {
                    background: var(--color-white);
                    border: 2px solid var(--color-light-green);
                    padding: 0.5rem 1rem 0.5rem;
                    border-radius: 10rem;
                    cursor: pointer;
            
                    font-size: 2rem;
                    color: var(--color-green);
            
                    transition: all 0.25s;

                    &:hover {
                        color: var(--color-white);
                        background-color: var(--color-brown);
                        border: 2px solid var(--color-vanille);
                    }

                    &.hide {
                        display: none;
                    }
                }
            }
            
            .map-info-panel {
                position: absolute;
                bottom: 1rem;
                left: 1rem;
                width: 22rem;
                background: var(--color-white);
                border-radius: 25px;
                box-shadow: 0 2px 8px var(--color-black);        
                padding: 1rem;
                z-index: 1000;
                
                .close-btn {
                    position: absolute;
                    top: 0.25rem;
                    left: 0.75rem;
                    font-size: 1.25rem;
                    color: var(--color-green);
                    cursor: pointer;
                    transition: all 0.25s;

                    &:hover {
                        color: var(--color-brown);
                    }
                }
                
                h1 {
                    font-size: 2rem;
                }
            
                p {
                    text-align: justify;
                    
                    &:first-of-type {
                        text-indent: 2rem;
                        margin: 0.15rem 0 0.5rem;
                    }
                }
                
                strong {
                    color: var(--color-brown);
                    font-weight: 900;
                }
            }

            .route-info-container {
                position: absolute;
                z-index: 1000;
                bottom: 1.25rem;
                margin-left: auto;
                margin-right: auto;
                left: 0;
                right: 0;
                background-color: var(--color-white);
                border-radius: 25px;
                box-shadow: 0 2px 8px var(--color-black);
                width: 30rem;
                
                display: flex;
                gap: 1rem;
                
                .route-imgs {
                    padding: 0.25rem;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    
                    img {
                        width: 8rem;
                        height: 8rem;
                        border-radius: 25px;
                        object-fit: cover;
                        border: 2px solid var(--color-green);
                    }
                }
                
                .route-info {
                    width: 65%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    cursor: default;
                    margin: 1rem 0;
                    
                    p {
                        font-size: 0.85rem;
                        font-weight: 600;
                        color: var(--color-brown);
                        
                        strong {
                            font-weight: 900;
                        }
                    }
                    
                    h1 {
                        text-align: left;
                        font-family: "Montserrat-Bold";
                        font-size: 1rem;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        color: var(--color-green);
                    }
                }
                
                .close-btn {
                    position: absolute;
                    top: 0.25rem;
                    right: 0.75rem;
                    font-size: 1.25rem;
                    color: var(--color-green);
                    cursor: pointer;
                    transition: all 0.25s;

                    &:hover {
                        color: var(--color-brown);
                    }
                }

                .route-link {
                    position: absolute;
                    bottom: 0rem;
                    right: 0rem;
                    font-size: 0.85rem;
                    font-weight: 900;
                    color: var(--color-white);
                    background-color: var(--color-green);
                    padding: 0.25rem 1rem;
                    border-top-left-radius: 25px;
                    border-bottom-right-radius: 25px;
                    cursor: pointer;
                    transition: all 0.25s;
                    
                    &:hover {
                        color: var(--color-light-green);
                    }
                }
            }

            .exit-fullscreen-btn {
                position: absolute;
                top: 1rem;
                right: 6rem;
                z-index: 1000;
                color: var(--color-green);
                background-color: var(--color-white);
                border: 2px solid var(--color-light-green);
                font-size: 1.5rem;
                padding: 0.25rem 0.75rem;
                border-radius: 20rem;
                cursor: pointer;
                transition: all 0.25s;
                
                &:hover {
                    color: var(--color-white);
                    background-color: var(--color-brown);
                    border: 2px solid var(--color-vanille);
                }
            }
        }
    }

    // Fullscreen
    .fullscreen-border {
        border-top-left-radius: 25px;
        border-top-right-radius: 25px;
        border-top: 5px solid var(--color-green);
    }

    // Menu desplegable layers
    .map-style-menu {
        position: absolute;
        top: 100%;
        right: 0;
        background: var(--color-white);
        list-style: none;
        padding: 0;
        margin-top: 0.25rem;
        border-radius: 25px;
        box-shadow: 0 2px 8px var(--color-black);
        z-index: 1000;
    }

    .map-style-menu li {
        padding: 0.5rem;
        cursor: pointer;
        transition: all 0.25s;
    }

    .map-style-menu li:first-of-type {
        border-top-left-radius: 25px;
        border-top-right-radius: 25px;
    }

    .map-style-menu li:last-of-type {
        border-bottom-left-radius: 25px;
        border-bottom-right-radius: 25px;
    }

    .map-style-menu li:hover {
        background: var(--color-grey);
    }

    // Animacion
    .fade-slide-enter-active,
    .fade-slide-leave-active {
        transition: all 0.3s ease;
    }

    .fade-slide-enter-from {
        opacity: 0;
        transform: translateY(-10px);
    }

    .fade-slide-enter-to {
        opacity: 1;
        transform: translateY(0);
    }

    .fade-slide-leave-from {
        opacity: 1;
        transform: translateY(0);
    }

    .fade-slide-leave-to {
        opacity: 0;
        transform: translateY(-10px);
    }
    
    // MEDIA QUERIES
    @media (max-width: 1250px) {
        .map-container {
            .map-top-container {
                width: 90%;
            }

            .map {
                width: 90%;

                .map-style-toggle {
                    top: 0.25rem;
                    right: 0.25rem;

                    button {
                        font-size: 1.5rem;
                        padding: 0.35rem 0.75rem;
                    }
                }

                .legend {
                    bottom: 1.25rem;
                    right: 0.25rem;

                    i {
                        font-size: 0.85rem;

                        p {
                            font-size: 1rem;
                        }
                    }
                }

                .map-info-button {
                    bottom: 0.25rem;
                    left: 0.25rem;

                    button {
                        font-size: 1.5rem;
                        padding: 0.35rem 0.75rem;
                    }
                }

                .exit-fullscreen-btn {
                    top: 0.25rem;
                    right: 4rem;
                }
            }

            .map, .map-detailed {
                .map-info-panel {
                    bottom: 0.25rem;
                    left: 0.25rem;

                    h1 {
                        font-size: 1.5rem;
                    }
                }
            }
        }
    }

    @media (max-width: 900px) {
        .hide-mobile {
            display: none !important;
        }
    }

    @media (max-width: 700px) {
        .map-container {
            .map-detailed {
                border-radius: 0;
                border: 0;
                border-top: 5px solid var(--color-green);
                border-bottom: 5px solid var(--color-green);
                height: 25rem;
            }
        }
    }

    @media (max-width: 550px) {
        .map-container {
            .map-top-container {
                width: 100%;
                border-radius: 0;
                border: none;
                border-top: 5px solid var(--color-green);

                #location-search {
                    margin-left: 0.25rem
                }

                .suggestions-list {
                    margin-right: 0.25rem;
                }
            }

            .map {
                width: 100%;
                height: 33.5rem;
                border-radius: 0;
                border: 0;
                border-bottom: 5px solid var(--color-green);

                .route-info-container {
                    width: 19.5rem;
                    flex-direction: column;
                    gap: 0.25rem;

                    .route-imgs {
                        padding: 0;

                        img {
                            width: 100%;
                            height: 7rem;
                            border: 0;
                            border-bottom: 2px solid var(--color-green);
                        }
                    }

                    .route-info {
                        width: 100%;
                        align-items: center;
                        margin: 0 0 2rem;
                        padding: 0 0.5rem;

                        h1 {
                            max-width: 100%;
                        }
                    }

                    .close-btn {
                        top: 0;
                        right: 0%;
                        color: var(--color-white);
                        background-color: var(--color-green);
                        padding: 0 0.75rem;
                        border-top-right-radius: 25px;
                        border-bottom-left-radius: 25px;
                    }
                }
            }

            .map, .map-detailed {
                .map-info-panel {
                    width: 19.5rem;

                    h1 {
                        font-size: 1rem;
                    }
                }
            }
        }
    }
</style>


<style>
    /* Estilo al control de escala */
    .leaflet-control-scale {
        padding: 0.5rem 1rem;
        background-color: var(--color-white);
        border-radius: 25px;
        box-shadow: 0 2px 8px var(--color-black);        
    }

    .leaflet-left .leaflet-control-scale {
        margin: -4rem 4rem;
    }

    .leaflet-control-scale-line {
        background-color: transparent;
        color: var(--color-black);
    }    
</style>