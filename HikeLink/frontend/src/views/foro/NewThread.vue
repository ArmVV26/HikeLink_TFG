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