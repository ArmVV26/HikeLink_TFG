<template>
    <div class="route-wrapper">
        <div class="route-card" v-for="route in paginatedRoutes" :key="route.id">
            <router-link :to="{name: 'RouteDetail', params: {id: route.id, slug: route.slug } }">
                <div class="card-left">
                    <img :src="getImageUrl(route)" alt="Imagen de la Ruta" class="route-img" />
                    <div>
                        <img :src="getIconUserImg(route.user)" alt="Imagen del Usuario" class="avatar-route">
                        <p>{{ route.user.username }}</p> 
                    </div>
                </div>
                <div class="card-right">
                    <h1>{{ route.title }}</h1>
                    <p class="type">{{ route.type }}</p>
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
                            {{ route.average_rating }}
                        </p>
                    </div>
                    <p class="created_date">{{ formatDate(route.created_date) }}</p>
                </div>
            </router-link>
        </div>

        <div v-if="paginated && totalPages > 1" class="pagination">
            <button @click="currentPage--" :disabled="currentPage === 1" class="nav-btn">
                <i class="fa-solid fa-less-than"></i>
            </button>

            <button v-for="page in paginationPages" :key="page"
                :disabled="page === '...'"
                :class="['page-btn', {'active': page === currentPage}]"
                @click="typeof page === 'number' && (currentPage = page)">
                {{ page }}
            </button>

            <button @click="currentPage++" :disabled="currentPage === totalPages" class="nav-btn">
                <i class="fa-solid fa-greater-than"></i>
            </button>
        </div>
    </div>
</template>

<script setup>
    import { computed, ref, watch } from 'vue'
    import { getMediaUrl } from '@/api/media';

    const props = defineProps({
        routes: {
            type: Array,
            required: true
        },
        paginated: {
            type: Boolean,
            default: false
        },
        pageSize: {
            type: Number,
            default: 5
        }
    })

    // Paginar
    const currentPage = ref(1)

    watch(() => props.routes, () => {
        currentPage.value = 1
    })

    const totalPages = computed(() => {
        return Math.ceil(props.routes.length / props.pageSize) || 1
    })

    // Paginas a mostrar en una pagina
    const paginatedRoutes = computed(() => {
        if (!props.paginated) return props.routes
        const start = (currentPage.value - 1) * props.pageSize
        const end = start + props.pageSize
        return props.routes.slice(start, end)
    })

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

    // Obtener la URl de la imagen de la ruta
    const getImageUrl = (route) => {
        return getMediaUrl(`/${route.user.username}/${route.slug}/${route.img?.[1] || route.img?.[0]}`)
    }

    // Obtener el icono del usuario
    const getIconUserImg = (manage) => {
        return getMediaUrl(`${manage.username}/${manage.profile_picture}`)
    }

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
                        border-bottom: 5px solid var(--color-green);                            
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
                    h1 {
                        font-family: "Montserrat-Bold";
                        color: var(--color-green);
                        font-size: 2rem;
                        line-height: 1;
                        text-align: left;
                    }

                    .type {
                        font-family: "Montserrat-Bold";
                        font-size: 1.25rem;
                        color: var(--color-grey);
                    }

                    .description {
                        margin: 1rem 0;
                        max-width: 100%;
                        display: -webkit-box;
                        line-clamp: 3;
                        -webkit-line-clamp: 3;       
                        -webkit-box-orient: vertical;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    }

                    .origin {
                        font-family: "Montserrat-Bold";
                    }

                    .route-stats {
                        display: flex;
                        gap: 10%;
                        font-weight: 900;
                        i {
                            color: var(--color-green);
                        }
                        
                        .rating i {
                            color: gold;
                            text-shadow: 0px 0px 2px var(--color-black);
                        }
                    }

                    .created_date {
                        position: absolute;
                        font-weight: 900;
                        bottom: 1rem;
                        right: 1rem;
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
</style>