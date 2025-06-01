<template>
    <div class="comment-add-container">
        <img v-if="isAuthenticated" :src="getIconUserImg" @error="handleImgError" class="avatar" ref="userImg" />
        <img v-else :src="getMediaUrl('/_common/sample_user_icon.png')" class="avatar avatar-disabled">
        <div class="comment-add" :class="{ 'disabled': !isAuthenticated }">
            <div>
                <h1>Añade un comentario</h1>
                <p v-if="!isAuthenticated" class="auth-warning">
                    Debes iniciar sesión para comentar
                </p>
            </div>
            <form @submit.prevent="submitComment">
                <textarea :class="{'textarea-disabled': !isAuthenticated}" 
                    id="addComment" 
                    name="addComment" 
                    placeholder="Escribe un comentario"
                    v-model="commentText"
                    :disabled="!isAuthenticated" 
                ></textarea>
                <CommonButton 
                    :text="'Enviar Comentario'"
                    :route="''"
                    :thin="true"
                    :asButton="true"
                    :disabled="!isAuthenticated"
                    @click="submitComment"
                />
            </form>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { ref, computed, toRefs } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import { getMediaUrl } from '@/utils/media';
    import { useUserImage } from '@/composables/useUserImage';
    import { commentRouteServices, commentThreadServices } from '@/services/UserServices';
    import CommonButton from '../common/CommonButton.vue';

    // PROPS
    const props = defineProps({
        routeId: {
            type: Number,
            required: false
        },
        threadId: {
            type: Number,
            required: false
        }
    })
    
    // VARIABLES
    const { routeId, threadId } = toRefs(props);
    
    const emit = defineEmits(['comment-submitted'])

    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const commentText = ref('')

    // METODOS
    // Imagen de usuario
    const { getIconUserImg, handleImgError, userImg } = useUserImage();

    // Metodo que permite guardar el comentario y llamar a la funcion refreshRouteData para actualizar los datos
    async function submitComment() {
        if (!isAuthenticated.value || !commentText.value.trim()) return
        
        try {
            if (props.routeId) {
                await commentRouteServices({ content: commentText.value, route: routeId.value });
            } else if (props.threadId) {
                await commentThreadServices({ content: commentText.value, thread: threadId.value });
            } 

            commentText.value = ''
            emit('comment-submitted')
        } catch (error) {
            console.error('Error al enviar comentario:', error)
        }
    }
</script>

<style lang="scss" scoped>
    .comment-add-container {
        display: flex;
        flex-direction: row;
        gap: 1rem;
        margin: 0 10rem 2rem;
        
        .avatar {
            width: 4rem;
            height: 4rem;
            border-radius: 25px;
            object-fit: cover;
            border: 2px solid var(--color-light-green);
        }

        .avatar-disabled {
            filter: grayscale(100%);
            opacity: 0.5;
        }

        .comment-add {
            flex: 1;
            
            .comment-add {
                opacity: 0.5;
                pointer-events: none;
            }

            div {
                display: flex;
                align-items: center;
                gap: 1rem;
            }

            h1 {
                font-family: "Montserrat-Bold";
                font-size: 1.5rem;
                text-align: left;
                color: var(--color-green);
            }

            textarea {
                width: 100%;
                min-height: 12rem;
                border-radius: 25px;
                padding: 0.25rem 1rem;
                border: 2px solid var(--color-black);
                resize: none;
            }

            .textarea-disabled {
                background-color: var(--color-grey);
            }

            .auth-warning {
                margin-top: 0.25rem;
                font-size: 1rem;
                font-weight: 900;
                color: red;
            }

            form {
                display: flex;
                flex-direction: column;

                button { 
                    margin-top: 1rem;
                    align-self: flex-end;
                }
            }
        }
    }
</style>