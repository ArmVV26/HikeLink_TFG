<template>
    <div class="foro-wrapper">
        <div class="foro-card" v-for="thread in paginatedThreads" :key="thread.id">
            <router-link :to="{ name: 'ThreadDetail', params: {id: thread.id, slug: thread.slug } }">
                <div class="card-left">
                    <img :src="getIconUserThread(thread.user)"
                        @error="handleImgError"
                        class="avatar-thread"
                        alt="Imagen del Usuario"
                    />
                    <h1>{{ thread.user.username }}</h1>
                </div>

                <div class="card-center">
                    <h1>{{ thread.title }}</h1>
                    <p>{{ thread.content }}</p>
                    <p class="created-date">{{ formatDate(thread.created_date) }}</p>
                </div>

                <div class="card-right">
                    <i class="fa-solid fa-comment"></i>
                    <p>{{ thread.comments_count }}</p>
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
    import { useUserThreadImage } from '@/composables/useUserImage'

    // PROPS
    const props = defineProps({
        threads: {
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

    const { getIconUserThread, handleImgError } = useUserThreadImage()

    // Paginas a mostrar en una pagina
    const paginatedThreads = computed(() => props.threads )

    // WATCHER
    watch(() => props.threads.length, () => {
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
    .foro-wrapper {
        display: flex;
        flex-direction: column;
        gap: 1rem;

        .foro-card {
            padding: 0.5rem;
            border-radius: 25px;
            box-shadow: 2px 2px 5px 1px var(--color-black);  
            background-color: var(--color-white);  
            transition: all 0.25s;

            &:hover {
                transform: scale(0.995);
            }

            a {
                display: grid;
                grid-template-columns: 10rem 1fr 10rem;
                gap: 1rem;

                .card-left {
                    display: flex;
                    align-items: center;
                    flex-direction: column;
                    gap: 0.5rem;

                    .avatar-thread {
                        width: 6rem;
                        height: 6rem;
                        object-fit: cover;
                        border-radius: 25px;
                        border: 2px solid var(--color-green);
                    }

                    h1 {
                        font-family: "Montserrat-Bold";
                        font-size: 1.5rem;
                        color: var(--color-green);
                    }
                }

                .card-center {
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

                    p {
                        margin: 0.5rem 0;
                        max-width: 100%;
                        display: -webkit-box;
                        line-clamp: 3;
                        -webkit-line-clamp: 3;       
                        -webkit-box-orient: vertical;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    }

                    .created-date {
                        position: absolute;
                        font-weight: 900;
                        bottom: 0;
                        left: 0;
                        color: var(--color-light-green);
                        text-align: right;
                    }
                }

                .card-right {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 1rem;

                    i {
                        font-size: 3rem;
                        color: var(--color-green);
                        filter: drop-shadow(4px 4px 0px var(--color-light-green));
                    }

                    p {
                        font-size: 1.5rem;
                        font-weight: 900;
                        font-style: italic;
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
            background-color: var(--color-white);
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