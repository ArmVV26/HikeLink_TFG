<template>
    <div class="main-container">
        <div class="route-form">
            <h1>Modificar Perfil</h1>
            <h2>{{ username }}</h2>
            
            <form @submit.prevent="updateProfile">
                <input type="email" v-model="email" placeholder="Correo Electrónico" required />
                <input type="text" v-model="full_name" placeholder="Nombre y Apellidos" required />
                
                <div class="password-wrapper">
                    <input :type="showOldPassword ? 'text' : 'password'"
                        v-model="old_password" 
                        placeholder="Contraseña Actual" 
                    />
                    <span class="toggle-password" @click="showOldPassword = !showOldPassword">
                        <i :class="showOldPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                </div>

                <div class="password-wrapper">
                    <input :type="showNewPassword ? 'text' : 'password'"
                            v-model="new_password"
                            placeholder="Nueva contraseña (opcional)" />
                    <span class="toggle-password" @click="showNewPassword = !showNewPassword">
                        <i :class="showNewPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                </div>

                <textarea v-model="bio" placeholder="Biografía (Opcional)"></textarea>

                <div class="img-profile">
                    <img :src="getIconUserImg(username, profile_picture)" alt="Imagen de Perfil del Usuario">
                    <input type="file" @change="handleFiles" accept="image/*" />
                </div>

                <p class="error" v-if="error">{{ error }}</p>
                <p class="success" v-if="success">{{ success }}</p>
                <button type="submit">Guardar Cambios</button>
            </form>
        </div>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import { getMediaUrl } from '@/api/media';
    import { useRoute } from 'vue-router';
    import { useAuthStore } from '@/stores/authStore'

    import api from '@/api/api';

    const router = useRoute()
    const authStore = useAuthStore()

    const username = ref('')
    const email = ref('')
    const full_name = ref('')
    const bio = ref('')
    const profile_picture = ref('')
    const old_password = ref('')
    const new_password = ref('')

    const new_image = ref([])
    const success = ref('')
    const error = ref('')

    const showOldPassword = ref(false)
    const showNewPassword = ref(false)

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const accessToken = computed(() => authStore.accessToken)

    // Obtener los datos del usuario
    onMounted( async () => {
        if (!isAuthenticated.value) return

        try {
            const { data } = await api.get(`users/${router.params.id}`)
            
            username.value = data.username
            email.value = data.email
            full_name.value = data.full_name
            bio.value = data.bio || ''
            profile_picture.value = data.profile_picture || ''
        } catch(err) {
            error.value = 'Error al cargar los datos del usuario'
        }
    })

    // Obtener el icono del usuario
    const getIconUserImg = (username, profile_picture) => {
        return getMediaUrl(`${username}/${profile_picture}`)
    }

    // Manejo imagen subida
    const handleFiles = (e) => {
        const file = e.target.files[0]
        if (file) {
            new_image.value = file
        }
    }

    // Metodo para actualizar los datos del usuario
    const updateProfile = async () => {
        error.value = ''
        success.value = ''

        if (!isAuthenticated) return

        const formData = new FormData()
        formData.append('email', email.value)
        formData.append('full_name', full_name.value)
        formData.append('bio', bio.value)
        if (new_image.value) formData.append('profile_picture', new_image.value)

        if (new_password.value) {
            if (!old_password.value) {
                error.value = 'Debes introducir tu contraseña actual para establecer una nueva.'
                return
            }
            formData.append('old_password', old_password.value)
            formData.append('new_password', new_password.value)
        }

        try {
            await api.put(`/profile/edit-profile/${router.params.id}/`, formData, {
                headers: {
                    Authorization: `Bearer ${accessToken.value}`,
                    'Content-Type': 'multipart/form-data'
                }
            })
            success.value = 'Perfil actualizado correctamente.'
            authStore.fetchUser()
        }catch (err) {
            error.value = 'Error al actualizar el Usuario'
        }
    }
</script>

<style lang="scss" scoped>
    .main-container {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0 2rem;
    }

    .route-form {
        width: 35rem;
        padding: 2rem 1.5rem;
        background-color: var(--color-white);
        border-radius: 25px;
        box-shadow: 0px 0px 10px 0px var(--color-black);

        display: flex;
        flex-direction: column;
        justify-content: center;
        
        h1 {
            font-family: "Montserrat-Bold";
            font-size: 2rem;
            color: var(--color-green);
            text-shadow: none;
            line-height: 1;
        }

        h2 {
            font-family: "Montserrat-Bold";
            font-size: 1.5rem;
            font-style: 900;
            color: var(--color-brown);
            text-shadow: none;
            margin-bottom: 1rem;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            font-family: "Lato";

            input[type="text"], input[type="email"],
            input[type="password"], textarea{
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

            .password-wrapper {
                position: relative;
                width: 90%;
                margin: auto;

                input {
                    width: 100%;
                    padding-right: 2.5rem;
                }

                .toggle-password {
                    position: absolute;
                    top: 50%;
                    right: 0.75rem;
                    color: var(--color-brown);
                    transform: translateY(-50%);
                    transition: all 0.25s;
                    cursor: pointer;
                    
                    &:hover {
                        color: var(--color-green);
                    }
                }
            }

            textarea {
                resize: none;
                min-height: 20rem;
            }

            .img-profile {
                display: flex;
                flex-direction: column;
                align-items: center;

                    img {
                        width: 9rem;
                        border-radius: 25px;
                        border: 2px solid var(--color-green);
                    }
            }

            input[type="file"] {
                padding: 0.5rem 0.75rem;
                margin: auto;
                font-size: 0.75rem;
                color: var(--color-black);

                &::file-selector-button {
                    font-size: 1rem;
                    padding: 0.5rem 0.5rem;
                    border: 2px solid var(--color-brown);
                    border-radius: 25px;
                    cursor: pointer;
                    transition: all 0.25s;

                    &:hover {
                        border: 2px solid var(--color-green);
                    }
                }
            }

            .error {
                color: var(--color-red-400);
                font-size: 1rem;
                font-weight: 900;
                text-align: center;
            }

            .success {
                color: var(--color-green);
                font-size: 1rem;
                font-weight: 900;
                text-align: center;
            }

            button[type="submit"] {
                width: 90%;
                padding: 0.5rem 0.75rem;
                margin: auto;
                font-size: 1rem;
                font-weight: 900;
                color: var(--color-white);
                background-color: var(--color-green);
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.25s;

                &:hover {
                    background-color: var(--color-light-green);
                    color: var(--color-green);
                }
            }
        }    
    }
</style>