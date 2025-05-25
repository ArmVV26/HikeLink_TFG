<template>
    <div v-if="!imgCarousel" class="carousel-container">
        <h1>Rutas Destacadas</h1>
        <div class="carousel-wrapper">
            <button v-if="showButton" class="carousel-btn" @click="prevSlide(routes || imgUrls)">
                <i class="fa-solid fa-arrow-left"></i>
            </button>

            <div class="carousel-viewport">
                <div class="carousel-track" :style="trackStyle">
                    <div class="carousel-card" v-for="route in routes" :key="route.id">
                        <router-link :to="{name: 'RouteDetail', params: {id: route.id, slug: route.slug } }">
                            <div class="route-card-top">
                                <div class="img-wrapper">
                                    <img :src="getRouteImg(route)" 
                                        @error="handleImgError"
                                        class="route-img"
                                        alt="Imagen de ruta" 
                                    />
                                </div>
                                <p :title="route.title">{{ route.title }}</p>
                            </div>

                            <div class="route-info">
                                <p class="route-meta">Ruta de {{ route.user.username }}</p>
                                <p class="route-meta">
                                    ★ {{ route.average_rating?.toFixed(1) || 'N/A' }} ·
                                    {{ route.difficulty }} ·
                                    {{ (route.distance / 1000).toFixed(1) }} km ·
                                    Est. {{ formatDuration(route.duration) }}
                                </p>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>

            <button v-if="showButton" class="carousel-btn" 
                @click="nextSlide(routes || imgUrls)">
                <i class="fa-solid fa-arrow-right"></i>
            </button>
        </div>
    </div>

    <div v-else-if="imgUrls && imgUrls.length > 0" class="carousel-img-container">
        <h1>Fotos de la Ruta</h1>
        <div class="carousel-img-wrapper">
            <div class="carousel-img-viewport">
                <button v-if="showButton" class="carousel-img-btn" @click="prevSlide(routes || imgUrls)">
                    <i class="fa-solid fa-arrow-left"></i>
                </button>
    
                <div class="carousel-img-track" :style="trackStyle">
                    <div class="carousel-img-card" v-for="imgUrl in imgUrls || []" :key="imgUrl">
                        <img :src="imgUrl" alt="Imagen de la Ruta">
                    </div>
                </div>
    
                <button v-if="showButton" class="carousel-img-btn" 
                    @click="nextSlide(routes || imgUrls)">
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { ref, computed, toRefs } from 'vue'
    import { useRouteImage } from '@/composables/useRouteImage'

    // PROPS
    const props = defineProps({
        imgCarousel: {
            type: Boolean,
            default: false
        },
        routes: {
            type: Array,
        },
        imgUrls: {
            type: Array,
            default: []
        }
    })

    // VARIABLES
    const { imgCarousel, routes, imgUrls } = toRefs(props)

    const currentIndex = ref(0)
    const cardWidth = computed(() => imgCarousel.value ? 490 : 336)
    const cardGap = computed(() => imgCarousel.value ? 4 : 1 )
    const visibleCount = 3

    const { getRouteImg, handleImgError } = useRouteImage();
    
    // Permtie determinar si muestra o no los botones para mover el carousel
    const showButton = computed(() =>{
         if (imgCarousel.value && Array.isArray(imgUrls.value) && imgUrls.value.length <= 3) {
            return false
        } else {
            return true
        } 
    });
    
    // Determina el estilo del carousel
    const trackStyle = computed(() => {
        const totalOffset = currentIndex.value * (cardWidth.value + cardGap.value)
        return {
            transform: `translateX(-${totalOffset}px)`,
            transition: 'transform 0.5s ease-in-out',
        }
    });

    // METODOS
    // Funcion que permite pasar de imagenes a la derecha
    const nextSlide = (itemCount) => {
        if (itemCount.length <= visibleCount) return

        currentIndex.value += 1
        if (currentIndex.value > itemCount.length - visibleCount) {
            currentIndex.value = 0
        }
    }

    // Funcion que permite pasar de imagenes a la izquierda
    const prevSlide = (itemCount) => {
        if (itemCount.length <= visibleCount) return

        currentIndex.value -= 1
        if (currentIndex.value < 0) {
            currentIndex.value = itemCount.length - visibleCount
        }
    }

    // Para reformular la duracion de la Ruta
    const formatDuration = (seconds) => {
        const h = Math.floor(seconds / 3600)
        const m = Math.floor((seconds % 3600) / 60)
        return h > 0 ? `${h}h ${m}min` : `${m}min`
    }
</script>

<style lang="scss" scoped>
    .carousel-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 2rem auto;
        width: 100%;

        h1 {
            font-family: "Montserrat-Bold";
            color: var(--color-green);
        }

        .carousel-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            width: 100%;
        
            .carousel-btn {
                background-color: var(--color-green);
                border: 2px solid var(--color-light-green);
                border-radius: 25px;
                color: var(--color-white);
                font-size: 2rem;
                font-weight: bold;
                width: 3rem;
                height: 3rem;
                cursor: pointer;
                z-index: 1;
        
                display: flex;
                justify-content: center;
                align-items: center;
        
                margin: 0 1rem;
                
                transition: all 0.25s;
    
                &:hover {
                    background-color: var(--color-white);
                    color: var(--color-green);
                }
            }

            .carousel-viewport {
                width: calc(320px * 3 + 2rem);
                overflow: hidden;
                
                .carousel-track {
                    display: flex;
                    gap: 1rem;
                    will-change: transform;
                    
                    .carousel-card {
                        padding: 0.5rem;
                        width: 20rem;
                        flex-shrink: 0;
                        transition: all 0.25s;
    
                        &:hover .route-img {
                            transform: scale(1.05);
                        }
                        
                        .route-card-top {
                            border-radius: 25px;
                            overflow: hidden;
                            position: relative;
    
                            .img-wrapper {
                                overflow: hidden;
                                height: 10rem;
                                border-top-right-radius: 25px;
                                border-top-left-radius: 25px;
                                border: 3px solid var(--color-green);

                                .route-img {
                                    display: block;
                                    width: 100%;
                                    height: 100%;
                                    object-fit: cover;
                                    transition: transform 0.25s ease;
                                    filter: brightness(1) contrast(110%) saturate(110%) sepia(10%);
                                }
                            }
    
                            p {
                                font-size: 1.25rem;
                                font-weight: bolder;
                                color: var(--color-white);
                                background-color: var(--color-green);
                                border-bottom-right-radius: 25px;
                                border-bottom-left-radius: 25px;
                                overflow: hidden;
                                text-overflow: ellipsis;
                                white-space: nowrap;
                                max-width: 100%;
                                padding: 0 1rem;
                                text-shadow: 1px 2px 5px var(--color-black);
                            }
                        }
    
                        .route-info {
                            padding: 0.5rem;
                            
                            p {
                                font-size: 1rem;
                                color: var(--color-brown);
                                font-weight: 900;
                                white-space: nowrap;
                                overflow: hidden;
                                text-overflow: ellipsis;
                            }
                        }
                    }
                }
            }
        }
    }
    
    /* Carousel de img route details */
    .carousel-img-container {
        display: flex;
        flex-direction: column;
        margin: 2rem 10rem;
        
        h1 {
            font-family: "Montserrat-Bold";
            font-size: 1.5rem;
            font-weight: 900;
            color: var(--color-green);
            line-height: 1;
            text-align: left;
        }

        .carousel-img-viewport {
            display: flex;
            align-items: center;
            position: relative;
            width: calc(475px * 3 + 2rem);
            overflow: hidden;
            border: 5px solid var(--color-green);
            border-radius: 25px;
            
            .carousel-img-btn {
                position: absolute;
                background-color: var(--color-green);
                border: 2px solid var(--color-light-green);
                border-radius: 25px;
                color: var(--color-white);
                font-size: 2rem;
                font-weight: bold;
                width: 3rem;
                height: 3rem;
                cursor: pointer;
                z-index: 1;
        
                display: flex;
                justify-content: center;
                align-items: center;
    
                &:first-child {
                    left: 10px;
                }
    
                &:last-child {
                    right: 10px;
                }
    
                &:hover {
                    background-color: var(--color-white);
                    color: var(--color-green);
                }
            }

            .carousel-img-track {
                display: flex;
                will-change: transform;
                
                .carousel-img-card {
                    width: 30.5rem;
                    border-right: 5px solid var(--color-green);
                    flex-shrink: 0;
                    transition: all 0.25s;
                    
                    img {
                       width: 100%;
                       height: 100%;
                       object-fit: cover;
                       aspect-ratio: 16/9;
                   }
                }
            }
        }
    }
</style>