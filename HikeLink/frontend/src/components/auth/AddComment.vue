<template>
    <div class="comment-add-container">
        <img v-if="isAuthenticated" :src="getIconUserImg" @error="handleImgError" class="avatar" ref="userImg" />
        <img v-else :src="getMediaUrl('/sample_user_icon.png')" class="avatar avatar-disabled">
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
    import { ref, computed, toRefs } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import { getMediaUrl } from '@/api/media';
    import CommonButton from '../common/CommonButton.vue';
    import api from '@/api/api';

    const props = defineProps({
        routeId: {
            type: Number,
            required: true
        },
    })
    
    const {routeId} = toRefs(props);
    
    const emit = defineEmits(['comment-submitted'])

    const authStore = useAuthStore()
    const commentText = ref('')
    const userImg = ref(null);
    const accessToken = computed(() => authStore.accessToken)

    const isAuthenticated = computed(() => authStore.isAuthenticated)

    const getIconUserImg = computed(() => {
        const user = authStore.user;
        if (!user) return null
        return getMediaUrl(`/${user.username}/${user.profile_picture}`)
    });

    function handleImgError() {
        userImg.value.src = getMediaUrl('/sample_user_icon.png');
    }

    async function submitComment() {
        if (!isAuthenticated.value || !commentText.value.trim()) return
        
        try {
            await api.post('/comments/', {
                content: commentText.value,
                route: routeId.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${accessToken.value}`
                }
            })
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