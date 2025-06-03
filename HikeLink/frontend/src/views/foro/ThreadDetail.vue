<template>
    <div v-if="thread" class="main-container">
        <div class="thread-container">
            <div class="thread-main">
                <img :src="getIconUserThread(thread.user)"
                    @error="handleImgError"
                    class="avatar-thread"
                    alt="Imagen del Usuario"
                /> 
    
                <div class="content">
                    <div class="user-date">
                        <h1>{{ thread.user.username }}</h1>
                        <p>{{ formatDate(thread.created_date) }}</p>
                    </div>
                    <h1>{{ thread.title }}</h1>
                    <p>{{ thread.content }}</p>
                </div>

                <div v-if="isOwner" class="delete-button">
                    <p @click="showDeleteModal = true">Eliminar Hilo</p>
                </div>
            </div>
    
            <div class="comment-wrapper">
                <div class="comment-card" v-for="comment in thread.comments" :key="comment.id">
                    <div class="comment-main">
                        <img :src="getIconUserThread(comment.user)"
                            @error="handleImgError"
                            class="avatar-thread"
                            alt="Imagen del Usuario"
                        />
                        
                        <div class="content">
                            <div class="user-date">
                                <h1>{{ comment.user.username }}</h1>
                                <p>{{ formatDate(comment.created_date) }}</p>
                            </div>
                            <p>{{ comment.content }}</p>
                        </div>
                    </div>
                </div>
            </div>
    
        </div>
        
        <AddComment 
            :thread-id="thread.id"
            @comment-submitted="refreshThreadData"
        />

        <transition name="fade">
            <DeleteModal
                v-if="showDeleteModal"
                :title="'¿Quieres eliminar el Hilo?'"
                :message="'Si eliminas el Hilo no podras acceder más a este hilo. Piensatelo 2 veces.'"
                @confirm="confirmDeleteThread"
                @cancel="showDeleteModal = false"
            />
        </transition>
    </div>

    <div v-else>
        <h1>Error al Cargar el Hilo</h1>
    </div>
</template>

<script setup>
    // IMPORTS
    import { computed, onMounted, ref } from 'vue'
    import { useUserThreadImage } from '@/composables/useUserImage'
    import { useAuthStore } from '@/stores/authStore'
    import { deleteThreadServices } from '@/services/ThreadServices'
    import { useRouter } from 'vue-router'

    import DeleteModal from '@/components/modal/DeleteModal.vue'
    import AddComment from '@/components/auth/AddComment.vue'
    import api from '@/utils/api'

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
    const showDeleteModal = ref(false)
    const router = useRouter()

    const thread = ref(null)

    const { getIconUserThread, handleImgError } = useUserThreadImage()

    // Compruebo si el usuario es el dueño deL hilo
    const authStore = useAuthStore()
    const currentUserId = computed(() => authStore.user?.id ?? null)
    const isOwner = computed(() => {
        return thread.value && currentUserId.value === thread.value.user.id
    })

    // METODOS
    // Transformar la fecha en "10 de marzo de 2026"
    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('es-ES', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        }).format(date)
    }

    // Funcion para eliminar el hilo
    const confirmDeleteThread = async () => {
        try {
            await deleteThreadServices(props.id)
            showDeleteModal.value = false
            router.push('/foro')
        } catch (error) {
            console.error('Error al eliminar el hilo:', error)
        }
    }

    // Funcion que permite actualizar los datos del Hilo
    const refreshThreadData = async () => {
        try {
            const response = await api.get(`/threads/${props.id}/`)
            thread.value = response.data
        } catch (error) {
            console.error('Error recargando los datos del hilo:', error)
        }
    }


    // Realiza la llamada a la API para obtener los datos del Hilo
    onMounted(async () => {
        await refreshThreadData()
    })
</script>

<style lang="scss" scoped>
    .fade-enter-active, .fade-leave-active {
        transition: opacity 0.3s ease;
    }
    .fade-enter-from, .fade-leave-to {
        opacity: 0;
    }

    .main-container {
        width: 70%;
        margin: auto;

        .thread-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin: 2rem;
            padding: 1rem;
            background-color: var(--color-vanille-opacity);
            border-radius: 25px;
            box-shadow: 2px 2px 5px 1px var(--color-black); 

            .thread-main {
                position: relative;
                display: grid;
                grid-template-columns: 6rem 1fr;
                gap: 1rem;
                padding: 0.5rem;
                background-color: var(--color-light-green-opacity);
                box-shadow: 2px 2px 5px 1px var(--color-black); 
                border-radius: 25px;

                .avatar-thread {
                    width: 6rem;
                    height: 6rem;
                    object-fit: cover;
                    border-radius: 25px;
                    border: 2px solid var(--color-green);
                }

                .content {
                    display: flex;
                    flex-direction: column;

                    .user-date {
                        display: flex;
                        align-items: center;
                        gap: 1rem;

                        h1 {
                            font-family: "Montserrat-Bold";
                            font-size: 1.25rem;
                            color: var(--color-green);
                        }

                        p {
                            font-weight: 900;
                            color: var(--color-black);
                        }
                    }

                    h1 {
                        font-family: "Montserrat-Bold";
                        color: var(--color-green);
                        font-size: 2rem;
                        line-height: 1;
                        text-align: left;
                    }

                    p {
                        max-width: 100%;
                        display: -webkit-box;
                        line-clamp: 3;
                        -webkit-line-clamp: 3;       
                        -webkit-box-orient: vertical;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    }
                }

                .delete-button {
                    position: absolute;
                    top: 0.5rem;
                    right: 1rem;
                    background-color: var(--color-red-500);
                    border: 2px solid var(--color-red-700);
                    border-radius: 25px;
                    padding: 0.5rem 1rem;
                    cursor: pointer;
                    transition: all 0.25s;

                    &:hover {
                        background-color: var(--color-red-400);
                    }

                    p {
                        font-weight: 900;
                        color: var(--color-white);
                    }
                }
            }

            .comment-wrapper {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                margin-top: 1.5rem;

                .comment-card {
                    .comment-main {
                        display: grid;
                        grid-template-columns: 6rem 1fr;
                        gap: 1rem;
                        padding: 0.5rem;
                        background-color: var(--color-white);
                        box-shadow: 2px 2px 5px 1px var(--color-black); 
                        border-radius: 25px;

                        .avatar-thread {
                            width: 6rem;
                            height: 6rem;
                            object-fit: cover;
                            border-radius: 25px;
                            border: 2px solid var(--color-green);
                        }
                        .content {
                            display: flex;
                            flex-direction: column;

                            .user-date {
                                display: flex;
                                align-items: center;
                                gap: 1rem;

                                h1 {
                                    font-family: "Montserrat-Bold";
                                    font-size: 1.5rem;
                                    color: var(--color-green);
                                }

                                p {
                                    font-weight: 900;
                                    color: var(--color-black);
                                }
                            }

                            p {
                                max-width: 100%;
                                display: -webkit-box;
                                line-clamp: 3;
                                -webkit-line-clamp: 3;       
                                -webkit-box-orient: vertical;
                                overflow: hidden;
                                text-overflow: ellipsis;
                            }
                        }
                    }
                }
            }
        }
    }
</style>