<template>
    <div class="main-container">
        <div class="route-form">
            <h1>Modificar Perfil</h1>
            <h2>{{ username }}</h2>
            
            <form @submit.prevent="updateProfile">
                <input type="text" v-model="email" placeholder="Correo Electrónico" />
                <input type="text" v-model="full_name" placeholder="Nombre y Apellidos" />
                
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
                    <img :src="getIconUserImg(username, profile_picture)"
                        @error="handleImgError"
                        alt="Imagen de Perfil del Usuario"
                    />
                    <input type="file" @change="handleFiles" accept="image/*" />
                </div>

                <ul>
                    <li class="error" v-for="err in fieldErrors">{{ err }}</li>
                </ul>
                <p class="error" v-if="error">{{ error }}</p>
                <p class="success" v-if="success">{{ success }}</p>
                <p class="success-deleted" v-if="successMessage">{{ successMessage }}</p>

                <div class="buttons-container">
                    <button type="submit">Guardar Cambios</button>
                    <button type="button" class="deleted" @click="showDeleteModal = true">Borrar Cuenta</button> 
                </div>
            </form>
        </div>

        <transition name="fade">
            <DeleteModal
                v-if="showDeleteModal"
                :title="'¿Quieres eliminar el Usuario?'"
                :message="'Si eliminas el Usuario no podras acceder más a esta web con esta cuenta. Piensatelo 2 veces.'"
                @confirm="confirmDeleteUser"
                @cancel="showDeleteModal = false"
            />
        </transition>
    </div>
</template>

<script setup>
    // IMPORTS
    import { computed, onMounted, ref } from 'vue'
    import { useRouter, useRoute } from 'vue-router';
    import { useAuthStore } from '@/stores/authStore'
    import { useUserSpecificImage } from '@/composables/useUserImage';
    import { updateUserServices, deleteUserServices } from '@/services/UserServices';
    import { useFormValidation } from '@/composables/useValidation';
    
    import DeleteModal from '@/components/modal/DeleteModal.vue';
    import api from '@/utils/api';

    // VARIABLES
    const showDeleteModal = ref(false)
    const successMessage = ref('')

    const router = useRouter()
    const route = useRoute()
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

    const { 
        fieldErrors,
        resetErrors,
        validateEmail,
        validatePassword,
        validateName,
    } = useFormValidation()

    // Imagen de usuario
    const { getIconUserImg, handleImgError } = useUserSpecificImage();

    const isAuthenticated = computed(() => authStore.isAuthenticated)

    // METODOS
    // Validacion general
    const validateProfileForm = () => {
        resetErrors()
        let valid = true

        if (!email.value) {
            fieldErrors.value.email = 'El correo electrónico es obligatorio.'
            valid = false
        } else if (!validateEmail(email.value)) {
            fieldErrors.value.email = 'Correo electrónico no válido.'
            valid = false
        }

        if (!full_name.value.trim()) {
            fieldErrors.value.full_name = 'El nombre es obligatorio.'
            valid = false
        } else if (!validateName(full_name.value)) {
            fieldErrors.value.full_name = 'El nombre no puede contener números ni caracteres especiales.'
            valid = false
        }

        if (new_password.value && !validatePassword(new_password.value)) {
            fieldErrors.value.new_password = 'La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.'
            valid = false
        }

        if (new_password.value && !old_password.value) {
            fieldErrors.value.old_password = 'Introduce tu contraseña actual para cambiarla.'
            valid = false
        }

        return valid
    }

    // Funcion que manejo imagen subida
    const handleFiles = (e) => {
        const file = e.target.files[0]
        if (file) {
            new_image.value = file
        }
    }

    // Funcion para obtener los datos del usuario
    onMounted( async () => {
        if (!isAuthenticated.value) return

        try {
            const { data } = await api.get(`users/${route.params.id}`)
            
            username.value = data.username
            email.value = data.email
            full_name.value = data.full_name
            bio.value = data.bio || ''
            profile_picture.value = data.profile_picture || ''
        } catch(err) {
            error.value = 'Error al cargar los datos del usuario'
        }
    })

    // Funcion para actualizar los datos del usuario
    const updateProfile = async () => {
        error.value = ''
        success.value = ''

        if (!isAuthenticated) return
        if (!validateProfileForm()) return

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
            const data = await updateUserServices(route.params.id, formData)

            if (data.logout) {
                authStore.logout()
                router.push({path: '/login', query: {message: 'Contraseña Cambiada Correctamente'}})
                return
            }

            success.value = 'Perfil actualizado correctamente.'
            authStore.fetchUser()
        }catch (err) {
            if (err.response?.status === 400 && err.response.data.detail) {
                error.value = err.response.data.detail
            } else {
                console.error(err)
                error.value = 'Error al actualizar el Usuario'
            }
        }
    }

    // Metodo para eliminar una cuenta
    const confirmDeleteUser = async () => {
        try {
            await deleteUserServices(route.params.id)
            successMessage.value = 'Tu cuenta ha sido eliminada correctamente.'
            showDeleteModal.value = false
            setTimeout(() => {
                authStore.logout()
                router.push({path: '/login', query: {message: 'Cuenta Eliminada Correctamente'}})
            }, 2000)
        } catch (error) {
            error.value = 'Error al eliminar la cuenta.'
        }
    }
</script>

<style lang="scss" scoped>
    .main-container {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0;
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity 0.3s ease;
    }
    .fade-enter-from, .fade-leave-to {
        opacity: 0;
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

            .success-deleted {
                color: var(--color-green);
                font-size: 1.5rem;
                font-weight: 900;
                text-align: center;
            }

            .buttons-container {
                width: 90%;
                display: flex;
                justify-content: space-between;
                margin: auto;
                gap: 2rem;
                
                button {
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

                .deleted {
                    background-color: var(--color-red-500);
                    border: 2px solid var(--color-red-700);

                    &:hover {
                        background-color: var(--color-red-300);
                        color: var(--color-black);
                    }
                }
            }
        }    
    }

    @media (max-width: 550px) {
        .route-form {
            width: 100%;
            padding: 1rem 0;
            border-top: 5px solid var(--color-green);
            border-bottom: 5px solid var(--color-green);
            border-radius: 0;
        }
    }

    @media (max-width: 350px) {
        .route-form {
            form {
                input[type="file"] {
                    padding: 0.5rem 0;
                }
            }
        }
    }
</style>