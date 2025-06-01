<template>
    <div class="main-container">
        <div class="login-form">
            <h1>Inicia sesión</h1>
            <h2>Para comenzar la aventura</h2>
            <p class="success" v-if="success">{{ success }}</p>

            <form @submit.prevent="login">
                <input type="text" v-model="inputUserMail" placeholder="Usuario o Correo" />
                <div class="password-wrapper">
                    <input :type="showPassword ? 'text' : 'password'"
                        v-model="password" 
                        placeholder="Contraseña"  
                    />
                    <span class="toggle-password" @click="togglePassword">
                        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                    <p class="forgot-password">
                        <router-link to="/forgot-password">¿Olvidaste tu contraseña?</router-link>
                    </p>
                </div>

                <ul>
                    <li class="error" v-for="err in fieldErrors">{{ err }}</li>
                </ul>
                <p class="error" v-if="error">{{ error }}</p>
                
                <button type="submit">Iniciar Sesión</button>
            </form>

            <div class="divisor">o</div>
            <p>¿No tienes cuenta?<router-link to="/register"> Registrate Aquí</router-link></p>
        </div>
    </div>
</template>
  
<script setup>
    // IMPORTS
    import { ref, computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { useAuthStore } from '@/stores/authStore'
    import { useFormValidation } from '@/composables/useValidation'
    
    // VARIABLES
    const inputUserMail = ref('')
    const password = ref('')
    const router = useRouter()
    const route = useRoute()
    const error = ref('')
    const success = computed(() => route.query.message)
    const authStore = useAuthStore()

    const { 
        fieldErrors,
        resetErrors,
        validateEmail,
        validateUsername
    } = useFormValidation();
    
    // METODOS
    // Validacion del email o username
    const validateLoginIdentifier = (input) => {
        if (validateEmail(input)) return true
        if (validateUsername(input)) return true
        return false
    }
    
    // Validacion general
    const validateLoginForm = () => {
        resetErrors()
        let valid = true

        if (!inputUserMail.value) {
            fieldErrors.value.email = 'El correo electrónico o el username es obligatorio.'
            valid = false
        } else if (!validateLoginIdentifier(inputUserMail.value)) {
            fieldErrors.value.identifier = 'Debes introducir un correo válido o un nombre de usuario sin espacios.'
            valid = false
        }

        if (!password.value) {
            fieldErrors.value.password = 'La contraseña es obligatoria.'
            valid = false
        }

        return valid
    }
    // Para mostrar el contenido de la contraseña
    const showPassword = ref(false)
    const togglePassword = () => {
        showPassword.value = !showPassword.value
    }

    // Funcion para incicar sesion
    const login = async () => {
        if (!validateLoginForm()) return

        try {
            await authStore.login(inputUserMail.value, password.value)
            router.push('/')
        } catch (err) {
            error.value = 'Usuario o contraseña incorrectos'
        }
    }
</script>
  
<style lang="scss" scoped>
    .main-container {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .login-form {
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
        
        .success {
            color: var(--color-green);
            font-size: 1rem;
            font-weight: 900;
            text-align: center;
            margin-top: -1rem;
            margin-bottom: 2rem;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            font-family: "Lato";

            input[type="text"], input[type="password"] {
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
                    top: 35%;
                    right: 0.75rem;
                    color: var(--color-brown);
                    transform: translateY(-50%);
                    transition: all 0.25s;
                    cursor: pointer;
                    
                    &:hover {
                        color: var(--color-green);
                    }
                }

                .forgot-password {
                    padding: 0;
                    margin: 0;
                    text-align: left;
                    font-size: 0.85rem;
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
</style>  