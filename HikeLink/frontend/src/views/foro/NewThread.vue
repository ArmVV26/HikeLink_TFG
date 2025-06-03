<template>
    <div class="main-container">
        <div class="thread-form">
            <h1>Nuevo Hilo</h1>
            <h2>HikeLink</h2>

            <form @submit.prevent="uploadThread">
                <input type="text" v-model="title" placeholder="Título"/>

                <textarea v-model="content" placeholder="Descripción del hilo"></textarea>

                <ul>
                    <li class="error" v-for="err in fieldErrors">{{ err }}</li>
                </ul>
                <p class="error" v-if="error">{{ error }}</p>

                <button type="submit">Subir Hilo</button>
            </form>
        </div>
    </div>
</template>

<script setup>
    // IMPORTS
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useFormValidation } from '@/composables/useValidation'
    import { uploadThreadServices } from '@/services/ThreadServices'

    // VARIABLES
    const title = ref('')
    const content = ref('')

    const error = ref('')
    const router = useRouter()

    const {
        fieldErrors,
        resetErrors,
        validateTitle,
    } = useFormValidation()

    // METODOS
    // Validacion general
    const validateThreadForm = () => {
        resetErrors()
        let valid = true

        if (!title.value) {
            fieldErrors.value.title = 'El título es obligatorio.'
            valid = false
        } else if (!validateTitle(title.value)) {
            fieldErrors.value.title = 'El título solo puede contener todas las letras, espacios, numeros, comas y guiones (-).'
            valid = false
        }

        if (!content.value) {
            fieldErrors.value.content = 'El contenido es obligatorio.'
            valid = false
        }

        return valid
    }

    // Funcion para subir el Hilo
    const uploadThread = async () => {
        error.value = ''

        if (!validateThreadForm()) return

        const formData = new FormData()
        formData.append('title', title.value)
        formData.append('content', content.value)

        try {
            const data = await uploadThreadServices(formData)
            router.push({ name: 'ThreadDetail', params: { slug: data.slug, id: data.id }})
        } catch (err) {
            if (err.response && err.response.data && err.response.data.error) {
                error.value = err.response.data.error
            } else {
                error.value = 'Error al guardar la ruta.'
            }
            console.error(err)
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

        .thread-form {
            width: 25rem;
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

                input[type="text"], textarea {
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

                textarea {
                    resize: none;
                    min-height: 9rem;
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
        }
    }
</style>