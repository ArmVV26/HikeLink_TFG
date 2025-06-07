<template>
    <div class="main-container">
        <div class="route-form">
            <h1>Modificar Ruta</h1>
            <h2>{{ title }}</h2>
            
            <form @submit.prevent="updateRoute">
                <input type="text" v-model="title" placeholder="Título" />
                
                <div>
                    <label for="type">Tipo: </label>
                    <select id="type" name="type" v-model="type">
                        <option selected value="Para-Todos">Para Todos</option>
                        <option value="Senderismo">Senderismo</option>
                        <option value="Ciclismo">Ciclismo</option>
                        <option value="Trail-Running">Trail-Running</option>
                        <option value="Alpinismo">Alpinismo</option>
                    </select>
                </div>

                <textarea v-model="description" placeholder="Descripción de la ruta"></textarea>
                
                <div>
                    <label for="difficulty">Dificultad: </label>
                    <select id="difficulty" name="difficulty" v-model="difficulty">
                        <option selected value="Fácil">Fácil</option>
                        <option value="Moderada">Moderada</option>
                        <option value="Difícil">Difícil</option>
                    </select>
                </div>

                <div>
                    <label for="origin">Origen: </label>
                    <select id="origin" name="origin" v-model="origin">
                        <option selected value="Wikiloc">Wikiloc</option>
                        <option value="Strava">Strava</option>
                        <option value="OutdoorActive">OutdoorActive</option>
                        <option value="AllTrails">AllTrails</option>
                        <option value="Komoot">Komoot</option>
                    </select>
                </div>

                <div v-if="images.length > 0" class="image-preview">
                    <p>Imágenes Actuales</p>
                    <div class="image-list">
                        <img v-for="(img, index) in images" :key="index"
                            :src="getRouteAllImg(route, img)" 
                            @error="handleImgError"
                            alt="Imagen de la Ruta"
                        />
                    </div>
                </div>

                <input type="file" @change="handleFiles" accept="image/*" multiple/>

                <ul>
                    <li class="error" v-for="err in fieldErrors">{{ err }}</li>
                </ul>
                <p class="error" v-if="error">{{ error }}</p>
                <p class="success-deleted" v-if="successMessage">{{ successMessage }}</p>

                <div class="buttons-container">
                    <button type="submit">Modificar Ruta</button>
                    <button type="button" class="deleted" @click="showDeleteModal = true">Borrar Ruta</button> 
                </div>
            </form>
        </div>

        <transition name="fade">
            <DeleteModal
                v-if="showDeleteModal"
                :title="'¿Quieres eliminar esta Ruta?'"
                :message="'Si eliminas esta Ruta se borrará de la web. Piensatelo 2 veces.'"
                @confirm="confirmDeleteRoute"
                @cancel="showDeleteModal = false"
            />
        </transition>
    </div>
</template>

<script setup>
    // IMPORTS
    import { computed, onMounted, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { useAuthStore } from '@/stores/authStore';
    import { useFormValidation } from '@/composables/useValidation';
    import { useRouteImage } from '@/composables/useRouteImage';
    import { updateRouteServices, deleteRouteServices } from '@/services/RouteServices';
    
    import DeleteModal from '@/components/modal/DeleteModal.vue';
    import api from '@/utils/api';
    
    // PROPS
    const props = defineProps({
        id: String,
        slug: String
    })
    
    // VARIABLES
    const showDeleteModal = ref(false)
    const successMessage = ref('')

    const title = ref('')
    const type = ref('')
    const description = ref('')
    const difficulty = ref('')
    const origin = ref('')
    const images = ref([])
    const newImages = ref([])
    
    const error = ref('')
    const route = ref(null)
    const router = useRouter()

    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)

    const { getRouteAllImg, handleImgError } = useRouteImage()

    const {
        fieldErrors,
        resetErrors,
        validateTitle
    } = useFormValidation()

    // METODOS
    // Validacion general
    const validateUpdateRouteForm = () => {
        resetErrors()
        let valid = true

        if (!title.value) {
            fieldErrors.value.title = 'El título es obligatorio.'
            valid = false
        } else if (!validateTitle(title.value)) {
            fieldErrors.value.title = 'El título solo puede contener todas las letras, espacios, numeros, comas y guiones (-).'
            valid = false
        }

        return valid
    }
    
    // Funcion para obtener las nuevas imagenes que sean subido
    function handleFiles(event) {
        newImages.value = Array.from(event.target.files)
    }

    // Llamada a la API para obtener los datos de la ruta a modificar
    onMounted(async () => {
        if (!isAuthenticated.value) return

        try {
            const response = await api.get(`/routes/${props.id}/`)  
            route.value = response.data

            title.value = route.value.title
            type.value = route.value.type
            description.value = route.value.description
            difficulty.value = route.value.difficulty
            origin.value = route.value.origin
            images.value = route.value.img
        } catch(error) {
            error.value = 'Error recargando los datos de la ruta'
        }
    })


    // Funcion que modifica la ruta con los nuevos datos proporcionados
    const updateRoute = async () => {
        if (!isAuthenticated.value) return
        if (!validateUpdateRouteForm()) return

        const formData = new FormData()
        formData.append('title', title.value)
        formData.append('type', type.value)
        formData.append('description', description.value)
        formData.append('difficulty', difficulty.value)
        formData.append('origin', origin.value)
        if (newImages.value.length > 0) {
            newImages.value.forEach((file) => {
               formData.append('images', file)
            })
        }

        try {
            await updateRouteServices(props.id, formData)
            router.push({
                name: 'RouteDetail',
                params: { slug: route.value.slug, id: route.value.id }
            })
        } catch (err) {
            error.value = 'Error actualizando la ruta'
            console.error(err)
        }
    }

    // Metodo para eliminar una ruta
    const confirmDeleteRoute = async () => {
        try {
            await deleteRouteServices(props.id)
            successMessage.value = 'Tu ruta ha sido eliminada correctamente.'
            showDeleteModal.value = false
            setTimeout(() => {
                router.push(`/profile/${authStore.user.username}-${authStore.user.id}`)
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
        padding: 2rem 0 2rem;
    }

    .route-form {
        width: 50rem;
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

            input[type="text"], textarea{
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

            div {
                margin: auto;
                display: flex;
                align-items: center;
                justify-content: center;

                select {
                    margin-left: 1rem;
                    padding: 0.5rem 0.75rem;
                    color: var(--color-black);
                    border: 2px solid var(--color-brown);
                    border-radius: 25px;
                    
                    &:hover {
                        border: 2px solid var(--color-green);
                    }
                }
            }

            textarea {
                resize: none;
                min-height: 20rem;
            }

            .image-preview {
                display: flex;
                flex-direction: column;

                p {
                    font-size: 1.25rem;
                    font-weight: 900;                    
                }

                .image-list {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.25rem;
                    background-color: var(--color-vanille-opacity);
                    border-radius: 25px;
                    padding: 0.25rem;

                    img {
                        width: 9rem;
                        height: 9rem;
                        border-radius: 25px;
                        border: 2px solid var(--color-green);
                        object-fit: cover;
                    }
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

    @media (max-width: 800px) {
        .route-form {
            width: 100%;
            padding: 1rem 0;
            border-top: 5px solid var(--color-green);
            border-bottom: 5px solid var(--color-green);
            border-radius: 0;
        }

        .route-form {
            form {
                .buttons-container {
                    button {
                        padding: 0.25rem 0.5rem;
                    }
                }
            }
        }
    }
</style>