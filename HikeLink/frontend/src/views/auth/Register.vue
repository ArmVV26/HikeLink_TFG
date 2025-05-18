<template>
    <div class="main-container">
        <div class="register-form">
            <h1>Crear una cuenta</h1>
            <h2>HikeLink</h2>
            
            <form @submit.prevent="register">
                <input type="email" v-model="email" placeholder="Correo electrónico" required />
                <input type="text" v-model="fullName" placeholder="Nombre y Apellidos" required />
                <input type="text" v-model="username" placeholder="Nombre de usuario" @input="removeSpaces" required />
                <div class="password-wrapper">
                    <input :type="showPassword ? 'text' : 'password'"
                        v-model="password" 
                        placeholder="Contraseña" 
                        required 
                    />
                    <span class="toggle-password" @click="togglePassword">
                        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                </div>
                <textarea v-model="bio" placeholder="Biografía (Opcional)"></textarea>
                <input type="file" @change="handleFile" accept="image/*" />
                
                <p class="error" v-if="error">{{ error }}</p>
                <button type="submit">Registrarse</button>
            </form>

            <div class="divisor">o</div>
            <p>¿Ya tienes una cuenta?<router-link to="/login"> Inicia Sesión</router-link></p>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { useRoute } from 'vue-router'
    import api from '@/api/api'

    const email = ref('')
    const fullName = ref('')
    const username = ref('')
    const password = ref('')
    const bio = ref('')
    const profileImage = ref(null)
    const error = ref('')

    const showPassword = ref(false)
    const togglePassword = () => {
        showPassword.value = !showPassword.value
    }
    
    const removeSpaces = () => {
        username.value = username.value.replace(/\s+/g, '')
    }
    
    const handleFile = (event) =>  {
        profileImage.value = event.target.files[0]
    }

    const router = useRoute()
    
    const register = async () => {
        error.value = ''

        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/
        if (!passwordRegex.test(password.value)) {
            error.value =
            'La contraseña debe tener al menos 8 caracteres, incluyendo mayúscula, minúscula, número y símbolo.'
            return
        }

        const formData = new FormData()
        formData.append('email', email.value)
        formData.append('full_name', fullName.value)
        formData.append('username', username.value)
        formData.append('password', password.value)
        if (bio.value) formData.append('bio', bio.value)
        if (profileImage.value) formData.append('profile_picture', profileImage.value)

        try {
            await api.post('/register/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            })
            router.push('/login')
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
        padding: 2rem 0 2rem;
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