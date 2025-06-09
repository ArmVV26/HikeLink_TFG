<template>
    <div class="route-wrapper">
        <div class="route-card" v-for="route in paginatedRoutes" :key="route.id">
            <router-link :to="{name: 'RouteDetail', params: {id: route.id, slug: route.slug } }">
                <div class="card-left">
                    <img :src="getRouteImg(route)"
                        @error="handleImgError" 
                        class="route-img"
                        alt="Imagen de la Ruta"
                    />
                    <div>
                        <img :src="getIconRouteImg(route.user)"
                            @error="handleImgUserError"
                            class="avatar-route" 
                            alt="Imagen del Usuario"    
                        />
                        <p>{{ route.user.username }}</p> 
                    </div>
                </div>
                <div class="card-right">
                    <h1 :title="route.title">{{ route.title }}</h1>
                    <p class="type">{{ route.type }}</p>
                    <p class="created-date">{{ formatDate(route.created_date) }}</p>
                    <div class="description" v-html="route.description_html"></div>
                    <p :style="{color: getColorByOrigin(route.origin)}" class="origin">{{ route.origin }}</p>
                    <div class="route-stats">
                        <p>{{ route.difficulty }}</p>
                        <p>
                            <i class="fa-solid fa-route"></i>
                            {{ (route.distance / 1000).toFixed(1) }} km
                        </p>
                        <p>
                            <i class="fa-regular fa-clock"></i>
                            {{ formatDuration(route.duration) }}
                        </p>
                        <p class="rating">
                            <i v-for="(star, index) in getRanting(route.average_rating)" :key="index" :class="star"></i>
                            <div>{{ route.average_rating }}</div>
                        </p>
                    </div>
                </div>
            </router-link>
        </div>

        <div class="pagination">
            <button @click="emit('change-page', props.currentPage - 1)" :disabled="props.currentPage === 1" class="nav-btn">
                <i class="fa-solid fa-less-than"></i>
            </button>

            <button v-for="page in paginationPages" :key="page"
                :disabled="page === '...'"
                :class="['page-btn', {'active': page === props.currentPage}]"
                @click="typeof page === 'number' && emit('change-page', page)">
                {{ page }}
            </button>

            <button @click="emit('change-page', props.currentPage + 1)" :disabled="props.currentPage === props.totalPages" class="nav-btn">
                <i class="fa-solid fa-greater-than"></i>
            </button>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { computed, watch } from 'vue'
    import { useRouteImage } from '@/composables/useRouteImage' 
    import { useUserRouteImage } from '@/composables/useUserImage'

    // PROPS
    const props = defineProps({
        routes: {
            type: Array,
            required: true
        },
        currentPage: {
            type: Number,
            required: true
        },
        totalPages: {
            type: Number,
            required: true
        }
    })

    // VARIABLES
    const maxVisiblePages = 5   

    const emit = defineEmits(['change-page'])

    const { getIconRouteImg, handleImgUserError } = useUserRouteImage()
    const { getRouteImg, handleImgError } = useRouteImage()
    
    // Paginas a mostrar en una pagina
    const paginatedRoutes = computed(() => props.routes )

    // WATCHER
    watch(() => props.routes.length, () => {
        const page = Math.min(props.currentPage, props.totalPages)
        emit('change-page', page < 1 ? 1 : page)
    });

    // METODOS
    // Funcion para determinar el numero de paginas que se muestran en el pagination
    const paginationPages = computed(() => {
        const pages = []
        const total = props.totalPages
        const current = props.currentPage

        if (total <= maxVisiblePages) {
            for (let i = 1; i <= total; i++) {
                pages.push(i)
            }
        } else {
            pages.push(1)

            if (current > 3) {
                pages.push('...')
            }

            const start = Math.max(2, current - 1)
            const end = Math.min(total - 1, current + 1)

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

    // Obtener el Origen reformulado de la ruta
    const getColorByOrigin = (origin) => {
        switch(origin) {
            case 'Wikiloc': return 'green';
            case 'Strava': return 'red'
            case 'OutdoorActive': return 'orange';
            case 'AllTrails': return 'violet';
            case 'Komoot': return 'blue';
            default: return 'gray'; 
        }
    }

    // Transformar la fecha en "1h 10min"
    const formatDuration = (seconds) => {
        const h = Math.floor(seconds / 3600)
        const m = Math.floor((seconds % 3600) / 60)
        return h > 0 ? `${h}h ${m}min` : `${m}min`
    }

    // Obtener el numero de estrellas que tiene la ruta en funcion del average_rating
    const getRanting = (rating) => {
        const stars = [];
        const rounded = Math.round(rating * 2) / 2;

        for (let i = 1; i <= 5; i++) {
            if (i <= rounded) {
                stars.push('fas fa-star'); 
            } else if (i - 0.5 === rounded) {
                stars.push('fas fa-star-half-alt'); 
            } else {
                stars.push('far fa-star'); 
            }
        }
        return stars;
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
</script>

<style lang="scss" scoped>
    .route-wrapper {
        display: flex;
        flex-direction: column;
        gap: 1rem;

        .route-card {
            padding: 0.5rem;
            border-radius: 25px;
            box-shadow: 2px 2px 5px 1px var(--color-black);    
            transition: all 0.25s;

            &:hover {
                transform: scale(0.995);
            }

            a {
                display: grid;
                grid-template-columns: 25rem 1fr;
                gap: 1rem;
                
                .card-left {
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;

                    .route-img {
                        width: 100%;
                        height: 12rem;
                        object-fit: cover;
                        border-radius: 25px;
                        border: 2px solid var(--color-green);                            
                    }

                    div {
                        display: flex;
                        align-items: center;
                        gap: 1rem;

                        .avatar-route {
                            width: 5rem;
                            height: 5rem;
                            object-fit: cover;
                            border-radius: 25px;
                            border: 2px solid var(--color-green);
                        }

                        p {
                            font-family: "Montserrat-Bold";
                        }
                    }
                }

                .card-right {
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    min-width: 0;

                    h1 {
                        font-family: "Montserrat-Bold";
                        color: var(--color-green);
                        font-size: 2rem;
                        line-height: 1;
                        text-align: left;
                        white-space: nowrap;         
                        overflow: hidden;             
                        text-overflow: ellipsis; 
                        max-width: 100%;
                        display: block;
                    }

                    .type {
                        font-family: "Montserrat-Bold";
                        font-size: 1.25rem;
                        color: var(--color-grey);
                    }

                    .description {
                        margin: 1rem 0 0.25rem;
                        max-width: 100%;
                        display: -webkit-box;
                        line-clamp: 3;
                        -webkit-line-clamp: 3;       
                        -webkit-box-orient: vertical;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        text-indent: 2rem;
                    }

                    .origin {
                        font-family: "Montserrat-Bold";
                    }

                    .route-stats {
                        display: flex;
                        justify-self: flex-end;
                        gap: 3rem;
                        margin-top: 3.5rem;
                        font-weight: 900;
                        font-size: 1rem;

                        i {
                            color: var(--color-green);
                        }
                        
                        .rating {
                            display: flex;
                            align-items: center;
                            
                            i {
                                color: gold;
                                text-shadow: 0px 0px 2px var(--color-black);
                            }

                            div {
                                margin-left: 0.25rem;
                            }
                        }

                    }

                    .created-date {
                        position: absolute;
                        font-weight: 900;
                        bottom: 0.25rem;
                        right: 0.5rem;
                        color: var(--color-light-green);
                        text-align: right;
                    }
                }
            }
        }
    }

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

    @media (max-width: 930px) {
        .route-wrapper {
            .route-card {
                a {
                    grid-template-columns: 15rem 1fr;
                }
            }
        }
    }

    @media (max-width: 768px) {
        .route-wrapper {
            .route-card {
                a {
                    display: flex;
                    flex-direction: column-reverse;

                    .card-left {
                        position: relative;
                        justify-content: center;
                        align-items: center;

                        .route-img {
                            height: 20rem;
                        }

                        div {
                            flex-direction: row-reverse;
                            gap: 0.5rem;
                            position: absolute;
                            bottom: 0.5rem;
                            right: 0.5rem;

                            background-color: var(--color-green);
                            border-radius: 25px;
                            padding: 0.25rem 0.25rem;
                            box-shadow: 2px 2px 5px 1px var(--color-black);

                            .avatar-route {
                                width: 3.5rem;
                                height: 3.5rem;
                                border-color: var(--color-light-green);
                            }

                            p {
                                color: var(--color-white);
                            }
                        }
                    }

                    .card-right {
                        h1 {
                            font-size: 1.5rem;
                            text-align: center;
                            display: -webkit-box;
                            line-clamp: 2;
                            -webkit-line-clamp: 2;       
                            -webkit-box-orient: vertical;
                            white-space: wrap;
                        }

                        .type {
                            text-align: center;
                        }

                        .description {
                            margin: 0 0 0.25rem;
                        }

                        .route-stats {
                            justify-content: space-around;
                            margin-top: 0.5rem;
                        }

                        .created-date {
                            position: relative;
                            text-align: left;
                            padding-left: 0.5rem;
                            margin-top: 1rem;
                        }
                    }
                }
            }
        }
    }

    @media (max-width: 500px) {
        .route-wrapper {
            padding: 0 0.5rem;

            .route-card {
                a {
                    .card-left {
                        .route-img {
                            height: 10rem;
                        }

                        div {
                            .avatar-route {
                                width: 2rem;
                                height: 2rem;
                            }

                            p {
                                font-size: 0.75rem;
                            }
                        }
                    }

                    .card-right {
                        .route-stats {
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            margin: auto;
                            text-align: center;
                            gap: 1rem;
                        }
                    }
                }
            }
        }

        .pagination {
            gap: 0.5rem;

            .nav-btn, .page-btn {
                font-size: 1rem;
                padding: 0.25rem 0.5rem;
            }
        }
    }
</style>