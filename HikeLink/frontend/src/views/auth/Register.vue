<template>
    <div class="main-container">
        <div class="register-form">
            <h1>Crear una cuenta</h1>
            <h2>HikeLink</h2>
            
            <form @submit.prevent="register">
                <input type="text" v-model="email" placeholder="Correo electrónico" />
                <input type="text" v-model="fullName" placeholder="Nombre y Apellidos" />
                <input type="text" v-model="username" placeholder="Nombre de usuario"  />
                <div class="password-wrapper">
                    <input :type="showPassword ? 'text' : 'password'"
                        v-model="password" 
                        placeholder="Contraseña" 
                    />
                    <span class="toggle-password" @click="togglePassword">
                        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                </div>
                <textarea v-model="bio" placeholder="Biografía (Opcional)"></textarea>
                <input type="file" @change="handleFile" accept="image/*" />
                
                <ul>
                    <li class="error" v-for="err in fieldErrors">{{ err }}</li>
                </ul>
                <p class="error" v-if="error">{{ error }}</p>
               
                <button type="submit">Registrarse</button>
            </form>

            <div class="divisor">o</div>
            <p>¿Ya tienes una cuenta?<router-link to="/login"> Inicia Sesión</router-link></p>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { registerUserServices } from '@/services/UserServices'
    import { useFormValidation } from '@/composables/useValidation'

    // VARIABLES
    const email = ref('')
    const fullName = ref('')
    const username = ref('')
    const password = ref('')
    const bio = ref('')
    const profileImage = ref(null)
    
    const error = ref('')
    const router = useRouter()

    const {
        fieldErrors,
        resetErrors,
        validateEmail,
        validatePassword,
        validateName,
        validateUsername,
    } = useFormValidation()

    // METODOS
    // Validacion general
    const validateRegisterForm = () => {
        resetErrors()
        let valid = true

        if (!email.value) {
            fieldErrors.value.email = 'El correo electrónico es obligatorio.'
            valid = false
        } else if (!validateEmail(email.value)) {
            fieldErrors.value.email = 'Correo electrónico no válido.'
            valid = false
        }

        if (!fullName.value.trim()) {
            fieldErrors.value.full_name = 'El nombre es obligatorio.'
            valid = false
        } else if (!validateName(fullName.value)) {
            fieldErrors.value.full_name = 'El nombre no puede contener números ni caracteres especiales.'
            valid = false
        }

        if (!username.value) {
            fieldErrors.value.username = 'El username es obligatorio.'
            valid = false
        } else if (!validateUsername(username.value)) {
            fieldErrors.value.username = 'El username no puede contener espacios ni caracteres muy raros y debe ser mayor a 5 caracteres.'
            valid = false
        }

        if (!password.value) {
            fieldErrors.value.password = 'La contraseña es obligatoria.'
            valid = false
        } else if (!validatePassword(password.value)) {
            fieldErrors.value.password = 'La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.'
            valid = false
        }

        return valid
    }

    // Para mostrar el contenido de la contraseña
    const showPassword = ref(false)
    const togglePassword = () => {
        showPassword.value = !showPassword.value
    }
    
    // Funcion que maneja la imagen de perfil del usuario
    const handleFile = (event) =>  {
        profileImage.value = event.target.files[0]
    }

    // Funcion que gestiona el registro de un usuario
    const register = async () => {
        error.value = ''

        if (!validateRegisterForm()) return

        const formData = new FormData()
        formData.append('email', email.value)
        formData.append('full_name', fullName.value)
        formData.append('username', username.value)
        formData.append('password', password.value)
        if (bio.value) formData.append('bio', bio.value)
        if (profileImage.value) formData.append('profile_picture', profileImage.value)

        try {
            await registerUserServices(formData)
            router.push({path: '/login', query: {message: 'Usuario Registrado Correctamente'}})
        } catch (err) {
            console.error(err)
            if (err.response?.data?.username) {
                error.value = 'El nombre de usuario ya está en uso.'
            } else if (err.response?.data?.email) {
                error.value = 'El correo electrónico ya está registrado.'
            } else {
                error.value = 'Error al registrar el usuario.'
            }
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

    .register-form {
        max-width: 25rem;
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

            input[type="email"], input[type="text"],
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
                min-height: 9rem;
            }

            input[type="file"] {
                width: 90%;
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
                text-align: center;
                color: var(--color-red-400);
                font-size: 1rem;
                font-weight: 900;
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

        .divisor {
            color: var(--color-dark-grey);
            text-align: center;
            margin: 0.5rem 0;
        }

        p {
            text-align: center;

            a {
                color: var(--color-green);
                font-weight: bold;
                cursor: pointer;
                transition: all 0.25s;

                &:hover {
                    color: var(--color-black);
                }
            }
        }
    }

    @media (max-width: 400px) {
        .register-form {
            width: 100%;
            padding: 1rem 0;
            border-top: 5px solid var(--color-green);
            border-bottom: 5px solid var(--color-green);
            border-radius: 0;
        }
    }
</style>