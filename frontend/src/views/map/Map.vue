<template>
    <ShowMap />

    <div class="tutorial-map">
        <h1>Explora el mapa sin límites</h1>
        <p>
            El mapa es el corazón de HikeLink. Desde aquí podrás descubrir rutas increíbles, acceder a la 
            información más relevante de cada punto y visualizar todo de una forma clara e interactiva. Para
            que saques el máximo partido a esta herramienta, te explicamos brevemente las funciones más destacadas
            del mapa:
        </p>
        <div class="cards-map">
            <div>
                <div class="icon-wrapper">
                    <i class="fa-solid fa-circle-info"></i>
                </div>
                <h1>Información del Mapa</h1>
                <p>
                    Este botón despliega un menú que muestra diferente información sobre el mapa como: el estilo del mapa
                    actual, las fuentes del mapa, la licencia, etc.
                </p>
            </div>
            <div>
                <div class="icon-wrapper">
                    <i class="fa-solid fa-layer-group"></i>
                </div>
                <h1>Tipos de Mapa</h1>
                <p>
                    Este botón permite cambiar entre diferentes vistas del mapa.
                </p>
            </div>
            <div>
                <div class="icon-wrapper">
                    <i class="fa-solid fa-expand"></i>
                </div>
                <h1>Pantalla Completa</h1>
                <p>
                    Este botón permite activar el modo pantalla completa para navegar por el mapa sin distracciones
                    y mayor comodidad
                </p>
            </div>
            <div>
                <div class="icon-wrapper">
                    <div class="legend-map">
                        <div>
                            <i class="fa-solid fa-location-dot text-green-600"></i>
                            <p class="font-black">Wikiloc</p>
                        </div>
                        <div>
                            <i class="fa-solid fa-location-dot text-orange-600"></i>
                            <p>Strava</p>
                        </div>
                        <div>
                            <i class="fa-solid fa-location-dot text-yellow-600"></i>
                            <p>OutdoorActive</p>
                        </div>
                        <div>
                            <i class="fa-solid fa-location-dot text-purple-600"></i>
                            <p>AllTrails</p>
                        </div>
                        <div>
                            <i class="fa-solid fa-location-dot text-blue-600"></i>
                            <p>Komoot</p>
                        </div>
                    </div>
                </div>
                <h1>Leyenda del Mapa</h1>
                <p>Leyenda para identificar rápidamente los distintos tipos de rutas.</p>
            </div>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import ShowMap from '@/components/map/ShowMap.vue';
</script>

<style lang="scss" scoped>
    /* Estilo del tutorial del mapa */
    .tutorial-map {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        background-color: var(--color-vanille-opacity);
        padding: 1rem;
        
        h1 {
            font-family: "Montserrat-Bold";
            font-size: 1.5rem;
            font-style: italic;
            color: var(--color-green);
            text-shadow: 0px 0px 1px var(--color-black);
        }

        p {
            font-weight: 900;
            color: var(--color-brown);
            text-align: center;
        }
        
        .cards-map {
            display: flex;
            justify-content: center;
            flex-wrap: wrap ;
            gap: 1.5rem;
            margin-bottom: 2rem;
            
            div {
                width: 20rem;
                text-align: center;
                
                .icon-wrapper {
                    height: 9rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    
                    .legend-map {
                        display: flex;
                        flex-direction: column;
                        align-items: flex-start;
                        width: 10rem !important;
                
                        padding: 0.5rem;
                        background-color: var(--color-white);
                        border: 2px solid var(--color-light-green);
                        border-radius: 25px;
                        
                        div {
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                            width: 100%;
                        }
                    }
                }
            }
        }
    }
    
    .tutorial-map > p:nth-child(2) {
        width: 50%;
    }

    .icon-wrapper > i {
        color: var(--color-green);
        font-size: 2rem;
        background-color: var(--color-white);
        border: 2px solid var(--color-light-green);
        border-radius: 10rem;
        padding: 1rem;
    }

    @media (max-width: 1250px) {
        .tutorial-map > p:nth-child(2) {
            width: 100%;
        }
        
        .tutorial-map {
            h1 {
                font-size: 1.25rem;
            }
        }
    }
</style>