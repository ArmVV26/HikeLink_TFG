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

            <button class="fullscreen-btn" @click="toggleFullscreen">
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
            <div v-if="detailedMap" class="legend">
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
            <button v-if="!detailedMap" class="fullscreen-btn-map" @click="toggleFullscreen">
                <i class="fa-solid fa-expand"></i>
            </button>

            <!-- Mostrar info del mapa -->
            <div class="map-info-button">
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
                    <p><strong>Última actualización:</strong> Abril 2025</p>
                </div>
            </transition>

            <transition v-if="detailedMap " name="fade-slide">
                <div v-if="selectedRoute" class="route-info-container">
                    <div class="route-imgs">
                        <img :src="getImageUrl(selectedRoute)" alt="Imagen de ruta">
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

<script>
    import { useRoute } from 'vue-router'
    import L from 'leaflet';
    import 'leaflet-gpx';
    import 'leaflet.fullscreen';
    import 'leaflet.fullscreen/Control.FullScreen.css';
    import api from '@/api/api';
    import { getMediaUrl } from '@/api/media';

    export default {
        name: 'MapComponent',
        props: {
            detailedMap : {
                type: Boolean,
                default: true
            },
        },

        data() {
            return {
                map: null,
                tileLayer: null,
                menuVisible: false,
                showInfo: false,
                currentStyleName: 'OpenStreetMap',
                shownRoutes: new Set(),
                routeMarkers: new Map(),
                gpxLayers: new Map(),
                selectedRoute: null,

                suggestions: [],
                highlightedIndex: -1,

                vueRoute: useRoute(),
            }
        },

        computed: {
            isSingleRoute() {
                const self = this;
                return !!self.vueRoute.params.id;
            }  
        },

        methods: {
            // Menu desplegable
            toggleMenu() {
                const self = this;
                self.menuVisible = !self.menuVisible;
            },

            // Para cambiar el tipo de mapa
            changeTile(style) {
                const self = this;
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

                if (self.tileLayer) {
                    self.map.removeLayer(self.tileLayer);
                }

                self.tileLayer = L.tileLayer(tileURLs[style], {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                }).addTo(self.map);

                this.currentStyleName = tileNames[style];
                self.menuVisible = false;
            },
            
            // Metodo para cargar las rutas
            async loadRoutes() {
                const self = this;
                try {
                    const response = await api.get('/routes/');
                    const routes = response.data;

                    routes.forEach(route => {
                        const color = self.getColorByOrigin(route.origin);
                        const icon = L.icon ({
                            iconUrl: self.getIconUrl(color),
                            iconSize: [25,41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        });

                        const marker = L.marker([route.start_latitude, route.start_longitude], { icon })
                            .addTo(self.map);

                        // Al hacer clic en el marcador, mostrara la ruta GPX
                        marker.on('click', function() {
                            self.selectedRoute = route;
                            self.toggleRoute(route);
                        });

                        self.routeMarkers.set(route.id, marker)
                    });
                } catch (error) {
                    console.error('Error cargado rutas:', error)
                }
            },

            // Metodo para generar el color del icono
            getColorByOrigin(origin) {
                switch (origin) {
                    case 'Wikiloc': return 'green';
                    case 'Strava': return 'red'
                    case 'OutdoorActive': return 'orange';
                    case 'AllTrails': return 'violet';
                    case 'Komoot': return 'blue';
                    default: return 'gray';
                }
            },

            // Metodo para genear la URl
            getIconUrl(color) {
                return `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`;
            },

            // Metodo para desactivar o activar una ruta
            toggleRoute(route) {
                const self = this;

                if (self.isSingleRoute) {
                    const color = self.getColorByOrigin(route.origin);
                    const gpxURL = getMediaUrl(`/${route.user.username}/${route.slug}/${route.gpx_file}`);

                    const gpx = new L.GPX(gpxURL, {
                        async: true,
                            markers: {
                                startIcon: self.getIconUrl('green'),
                                endIcon: self.getIconUrl('red')
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
                    });

                    gpx.on('loaded', function (e) {
                    const bounds = e.target.getBounds();
                    self.map.fitBounds(bounds);
                    self.map.setMaxBounds(bounds.pad(0.2));
                    self.map.setMinZoom(self.map.getZoom());
                    self.map.setMaxZoom(self.map.getZoom() + 3);
                    });

                    gpx.addTo(self.map);
                    self.gpxLayers.set(route.id, gpx);
                    self.shownRoutes.add(route.id);
                } else {
                    if (self.shownRoutes.has(route.id)) {
                        const layer = self.gpxLayers.get(route.id);
                        if (layer) self.map.removeLayer(layer);
    
                        self.shownRoutes.delete(route.id);
                        self.gpxLayers.delete(route.id);
                    } else {
    
                        self.shownRoutes.forEach((routeId) => {
                            const layer = self.gpxLayers.get(routeId);
                            if (layer) self.map.removeLayer(layer);
                            self.gpxLayers.delete(routeId);
                        });
    
                        self.shownRoutes.clear();
    
                        const color = self.getColorByOrigin(route.origin);
                        const gpxURL = getMediaUrl(`/${route.user.username}/${route.slug}/${route.gpx_file}`);
    
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
                        });
    
                        // Para hacer zoom in a la ruta seleccionada
                        // gpx.on('loaded', function (e) {
                        //     self.map.fitBounds(e.target.getBounds());
                        // });
    
                        gpx.on('addLine', function (e) {
                            const polyline = e.line;
                            polyline.on('mouseover', () => polyline.setStyle({ weight: 6, opacity: 1 }));
                            polyline.on('mouseout', () => polyline.setStyle({ weight: 4, opacity: 0.75 }));
                        });
    
                        gpx.addTo(self.map);
                        self.gpxLayers.set(route.id, gpx);
                        self.shownRoutes.add(route.id);
                    }
                }
            },

            // Metodo para mostrar la duracion de forma correcta
            formatDuration(seconds) {
                const h = Math.floor(seconds / 3600);
                const m = Math.floor((seconds % 3600) / 60);
                return h > 0 ? `${h}h ${m}min` : `${m}min`;
            },

            // Metodo para buscar por ubicacion
            async handleInput(e) {
                const self = this;

                const query = e.target.value;

                if (query.length < 3) {
                    self.suggestions = [];
                    return;
                }

                const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&addressdetails=1&limit=5`;

                try {
                    const res = await fetch(url);
                    const data = await res.json();
                    self.suggestions = data;
                    self.highlightedIndex = -1;
                } catch (err) {
                    console.error("Error buscando sugerencias:", err);
                }
            },

            selectSuggestion(suggestion) {
                const self = this;

                self.suggestions = [];
                self.map.setView([parseFloat(suggestion.lat), parseFloat(suggestion.lon)], 13);
                document.getElementById("location-search").value = suggestion.display_name;
            },

            highlightNext() {
                const self = this;

                if (self.highlightedIndex < self.suggestions.length - 1) {
                    self.highlightedIndex++;
                }
            },

            highlightPrev() {
                const self = this;
                if (self.highlightedIndex > 0) {
                    self.highlightedIndex--;
                }
            },

            selectHighlighted() {
                const self = this;
                if (self.highlightedIndex >= 0) {
                    self.selectSuggestion(self.suggestions[self.highlightedIndex]);
                }
            },

            // Metodo para mostrar en pantalla completa el mapa
            toggleFullscreen() {
                const mapContainer = document.getElementById('map');

                if (!document.fullscreenElement) {
                    mapContainer.requestFullscreen().catch(err => {
                        console.error(`Error al entrar en pantalla completa: ${err.message}`);
                    });
                } else {
                    document.exitFullscreen();
                }
            },

            // Metodo para obtener la imagen para mostrar en los detalles de la ruta
            getImageUrl(route) {
                return getMediaUrl(`/${route.user.username}/${route.slug}/${route.img?.[1] || route.img?.[0]}`)
            },

            // Funcion que permite borrar las rutas del mapa y cerrar los detalles de la ruta
            closeRouteDetails() {
                const self = this;

                if (self.selectedRoute && self.gpxLayers.has(self.selectedRoute.id)) {
                    const layer = self.gpxLayers.get(self.selectedRoute.id);
                    if (layer) self.map.removeLayer(layer);

                    self.shownRoutes.delete(self.selectedRoute.id);
                    self.gpxLayers.delete(self.selectedRoute.id);
                }

                self.selectedRoute = null;
            },
        },

        mounted() {
            const self = this;
            self.map = L.map('map' || 'map-detail').setView([37.1773, -3.5986], 13);

            self.tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            }).addTo(self.map);

            if (!self.isSingleRoute) {
                L.control.scale({ position: 'topleft', imperial: true, metric: true}).addTo(self.map)
            }

            // Detectar cambio de pantalla completa
            document.addEventListener('fullscreenchange', () => {
                const mapElement = document.getElementById('map');
                if (document.fullscreenElement) {
                    mapElement.classList.add('fullscreen-border');
                } else {
                    mapElement.classList.remove('fullscreen-border');
                }
            });

            if (self.isSingleRoute) {
                api.get(`/routes/${self.vueRoute.params.id}`)
                    .then(response => {
                        self.selectedRoute = response.data;
                        self.toggleRoute(self.selectedRoute);
                    })
                    .catch(error => {
                        console.error('Error cargando ruta individual:', error);
                    })
            } else {
                self.loadRoutes();
            }
        },
    };
</script>

<style scoped>
    .map-container {
        position: relative;
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
    }

    .map-detailed {
        width: 69rem;
        height: 43.5rem;
        /* margin: 0.5rem 0; */

        border: 5px solid var(--color-green);
        border-radius: 25px;
    }
    
    .fullscreen-border {
        border-top-left-radius: 25px;
        border-top-right-radius: 25px;
        border-top: 5px solid var(--color-green);
    }

    .map-style-toggle {
        position: absolute;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
    }

    .map-style-toggle button {
        background: var(--color-white);
        border: 2px solid var(--color-light-green);
        padding: 0.5rem 1rem 0.5rem;
        border-radius: 10rem;
        cursor: pointer;

        font-size: 2rem;
        color: var(--color-green);

        transition: all 0.25s;
    }

    .map-style-toggle button:hover {
        color: var(--color-white);
        background-color: var(--color-brown);
        border: 2px solid var(--color-vanille);
    }

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

    /* Estilo de la Leyenda */
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
    }

    .legend i {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1rem;
        font-weight: 900;
        line-height: 1.25;
    }

    .legend i p {
        font-family: "Lato";
        font-size: 1.25rem;
    }

    /* Estilo Informacion del Mapa */
    .map-info-button {
        position: absolute;
        bottom: 1rem;
        left: 1rem;
        z-index: 1000;
    }

    .map-info-button button {
        background: var(--color-white);
        border: 2px solid var(--color-light-green);
        padding: 0.5rem 1rem 0.5rem;
        border-radius: 10rem;
        cursor: pointer;

        font-size: 2rem;
        color: var(--color-green);

        transition: all 0.25s;
    }

    .map-info-button button:hover {
        color: var(--color-white);
        background-color: var(--color-brown);
        border: 2px solid var(--color-vanille);
    }

    .hide {
        display: none;
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
    }

    .close-btn {
        position: absolute;
        top: 0.25rem;
        left: 0.75rem;
        font-size: 1.25rem;
        color: var(--color-green);
        cursor: pointer;
        transition: all 0.25s;
    }
    
    .close-btn:hover {
        color: var(--color-brown);
    }

    .map-info-panel h1 {
        font-size: 2rem;
    }

    .map-info-panel p {
        text-align: justify;
    }

    .map-info-panel p:first-of-type {
        margin: 0.15rem 0 0.5rem;
    }

    .map-info-panel strong {
        color: var(--color-brown);
        font-weight: 900;
    }

    /* Estilo del top del mapa */
    .map-top-container {
        width: 70%;
        margin: 2rem auto 0;
        background-color: var(--color-vanille);
        padding: 0.75rem;
        display: flex;
        justify-content: space-between;

        border-top-left-radius: 25px;
        border-top-right-radius: 25px;
        
        border-top: 5px solid var(--color-green);
        border-left: 5px solid var(--color-green);
        border-right: 5px solid var(--color-green);
    }

    #location-search {
        width: 80%;
        margin-left: 2rem;
        background-color: var(--color-white);
        border: 2px solid var(--color-grey);
        outline: none;
        padding: 0.5rem 1rem;
        border-radius: 25px;    
    }

    .suggestions-list {
        position: absolute;
        top: 4rem;
        left: 21rem;
        width: 30%;
        background: var(--color-white);
        border: 5px solid var(--color-green);
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        max-height: 10rem;
        overflow-y: auto;
        z-index: 1001;
        list-style: none;
    }
    
    .suggestions-list li {
        padding: 0.5rem;
        cursor: pointer;
        transition: all 0.25s;
    }

    .suggestions-list li:hover,
    .suggestions-list li.highlighted {
        background-color: var(--color-vanille);
    }

    .fullscreen-btn {
        color: var(--color-green);
        background-color: var(--color-white);
        border: 2px solid var(--color-light-green);
        font-size: 2rem;
        padding: 0.25rem 1rem;
        border-radius: 20rem;
        margin-right: 2rem;
        cursor: pointer;
        transition: all 0.25s;
    }

    .fullscreen-btn:hover {
        color: var(--color-white);
        background-color: var(--color-brown);
        border: 2px solid var(--color-vanille);
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
    }

    .fullscreen-btn-map:hover {
        color: var(--color-white);
        background-color: var(--color-brown);
        border: 2px solid var(--color-vanille);
    }

    /* Estilos para mostrar los detalles de la ruta */
    .route-info-container {
        position: absolute;
        z-index: 1000;
        bottom: 1rem;
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
    }

    .route-imgs {
        padding: 0.25rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .route-imgs img {
        width: 8rem;
        height: 8rem;
        border-radius: 25px;
    }

    .route-info {
        width: 65%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        cursor: default;
        margin-bottom: 1rem;
    }

    .route-info p {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--color-brown);
    }

    .route-info p strong {
        font-weight: 900;
    }

    .route-info h1 {
        font-family: "Montserrat-Bold";
        font-size: 1.5rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        color: var(--color-green);
    }

    .route-info-container .close-btn {
        right: 0.75rem;
        left: initial;
    }

    /* Estilo del link para ver la ruta */
    .route-link {
        position: absolute;
        bottom: 0.25rem;
        right: 0.75rem;
        font-size: 0.85rem;
        font-weight: 900;
        color: var(--color-green);
        cursor: pointer;
        transition: all 0.25s;
    }

    .route-link:hover {
        color: var(--color-brown);
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