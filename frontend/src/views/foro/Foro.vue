<template>
    <div class="foro-container">
        <div class="top-options">
            <form @submit.prevent="filterThreads" >
                <input type="text" v-model="title" placeholder="Buscar Hilo" />
            </form>

            <CommonButton
                :text="'Nuevo Hilo'"
                :icon="'fa-solid fa-plus'"
                :thin="true"
                :route="'/new-thread'"
                :disabled="!isAuthenticated"
            />
        </div>
        
        <div v-if="threads && threads.length" class="threads-container">
            <ThreadCard 
                :threads="threads"
                :currentPage="currentPage"
                :totalPages="totalPages"
                @change-page="loadThreads"
            />
        </div>

        <div v-else class="no-threads">
            <i class="fa-solid fa-comment"></i>
            <h1>¡No se han encontrado hilos!</h1>
            <p>Modifica el filtro para buscar tus hilos deseadas</p>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { onMounted, ref, computed } from 'vue'
    import api from '@/utils/api'
    import ThreadCard from '@/components/foro/ThreadCard.vue'
    import CommonButton from '@/components/common/CommonButton.vue'
    import { useAuthStore } from '@/stores/authStore'

    // VARIABLES
    const title = ref('')

    const threads = ref([])

    // Paginar
    const totalPages = ref(1)
    const currentPage = ref(1)
    const pageSize = 5  

    const isFiltering = ref(false)
    const currentFilters = ref({})

    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)

    // METODOS
    // Funcion que recarga los hilos si hay filtro o si no hay filtro
    const loadThreads = async (page = 1) => {
        try {
            let response

            if (isFiltering.value) {
                const params = new URLSearchParams(currentFilters.value)
                params.append('page', page)
                params.append('page_size', pageSize)

                response = await api.get(`/filter-threads/?${params.toString()}`)
            } else {
                response = await api.get(`/all-threads/?page=${page}&page_size=${pageSize}`)
            }

            threads.value = response.data.results
            totalPages.value = Math.ceil(response.data.count / pageSize)
            currentPage.value = page
        } catch (error) {
            console.error("Error al cargar los hilos:", error)
        }
    }

    // Funcion para buscar los hilos
    const filterThreads = async () => {
        const params = new URLSearchParams()
        
        if (title.value) params.append('title', title.value)

        currentFilters.value = Object.fromEntries(params.entries()) 
        isFiltering.value = true

        await loadThreads(1)
    }
    
    // Para cargar todos los hilos al principio o al recargar la pagina
    onMounted(async () => {
        try {   
            loadThreads()
        } catch (error) {
            console.error("Error al cargar los hilos: ", error)
        }
    })
</script>

<style lang="scss" scoped>
    .foro-container {
        width: 70%;
        margin: 0 auto 2rem;

        .top-options {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 2rem 0 0.5rem;

            form {
                input[type="text"] {
                    width: 90%;
                    padding: 0.5rem 0.75rem;
                    margin: auto;
                    font-size: 1rem;
                    color: var(--color-black);
                    border: 2px solid var(--color-brown);
                    border-radius: 10px;
    
                    &:hover {
                        border: 2px solid var(--color-green);
                    }
                }
            }
        }

        .threads-container {
            padding: 1rem;
            border-radius: 25px;
            background-color: var(--color-vanille-opacity);
            box-shadow: 2px 2px 5px 1px var(--color-black); 
        }
    }

    .no-threads {
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

    @media (max-width: 1024px) {
        .foro-container {
            width: 100%;
            padding: 0 2rem;
        }
    }

    @media (max-width: 500px) {
        .foro-container {
            padding: 0;

            .top-options {
                padding: 0 0.5rem;

                form {
                    width: 10rem;
                }
            }

            .threads-container {
                padding: 1rem 0;
                border-radius: 0;
                border-top: 5px solid var(--color-brown);
                border-bottom: 5px solid var(--color-brown);
            }
        }
    }
</style>