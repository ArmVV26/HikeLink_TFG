<template>
    <div class="main-container">
        <div class="email-form">
            <h1>Recupera tu contraseña</h1>
            <p>Inserta el correo para mandarte un correo con un enlace para que recuperes tu contraseña.</p>

            <form v-if="!success && !error" @submit.prevent="submitEmail">
                <input type="text" v-model="email" placeholder="Tu correo" />
                <button type="submit">Enviar enlace</button>
            </form>
            
            <p class="success" v-if="success">
                <i class="fa-solid fa-circle-check"></i>
                {{ success }}
            </p>
            <div v-if="error || Object.keys(fieldErrors).length > 0" class="errors-container">
                <ul>
                    <li class="error" v-for="err in fieldErrors">{{ err }}</li>
                </ul>
                <p class="error">{{ error }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { ref } from 'vue'
    import { forgotPasswordServices } from '@/services/UserServices'
    import { useFormValidation } from '@/composables/useValidation'

    // VARIABLES
    const email = ref('')
    const success = ref('')
    const error = ref('')

    const {
        fieldErrors,
        resetErrors,
        validateEmail,
    } = useFormValidation()

    // METODOS
    // Validacion general
    const validateEmailForm = () => {
        resetErrors()
        let valid = true

        if (!email.value) {
            fieldErrors.value.email = 'El correo electrónico es obligatorio.'
            valid = false
        } else if (!validateEmail(email.value)) {
            fieldErrors.value.email = 'Correo electrónico no válido.'
            valid = false
        }

        return valid
    }

    // Funcion para mandar el correo para que el usuario recupere su contraseña
    const submitEmail = async () => {
        success.value = ''
        error.value = ''

        if (!validateEmailForm()) return

        try {
            await forgotPasswordServices(email.value)
            success.value = 'Si el correo está registrado, te enviamos un enlace para restablecer tu contraseña.'
        } catch (err) {
            error.value = 'Hubo un problema al enviar el correo.'
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

    .email-form {
        max-width: 30rem;
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
            line-height: 1.5;
        }

        p {
            font-size: 1rem;
            color: var(--color-black);
            text-align: center;
            margin-bottom: 1.5rem;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            font-family: "Lato";

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
        .success {
            color: var(--color-green);
            background-color: var(--color-light-green-opacity);
            border-radius: 25px;
            padding: 0.25rem 0.5rem;
            font-size: 1rem;
            font-weight: 900;
            text-align: center;
        }

        .errors-container {
            background-color: rgba(255, 103, 103, 0.3);
            border-radius: 25px;
            padding: 0.25rem 0 0;
            margin: 1rem;

            .error {
                text-align: center;
                color: var(--color-red-400);
                font-size: 1rem;
                font-weight: 900;
                margin: auto;
                padding: 0.5rem 0;
            }
        }
    }

    @media (max-width: 500px) {
        .email-form {
            width: 100%;
            max-width: 100%;
            padding: 1rem 0.25rem;
            border-top: 5px solid var(--color-green);
            border-bottom: 5px solid var(--color-green);
            border-radius: 0;
        }
    }
</style>