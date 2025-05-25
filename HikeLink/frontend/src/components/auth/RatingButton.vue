<template>
    <div class="rating-container" v-if="!isOwner" @mouseleave="resetHover">
        <div 
            class="rating" 
            :class="{ 'disabled': !isAuthenticated }" 
            @mousemove="handleMouseMove" 
            @click="handleClick"
        >
            <i 
                v-for="(star, index) in 5" 
                :key="index"
                :class="getStarClass(index)"
            ></i>
        </div>
        <span class="value">{{ displayRating.toFixed(1) }}</span>
    </div>
    <div v-else class="rating-disabled">
        <p>No puedes valorar tu propia ruta</p>
    </div>
</template>

<script setup>
    // IMPORTS
    import { ref, computed, onMounted, toRefs, watch } from 'vue'
    import { useAuthStore } from '@/stores/authStore'
    import { ratingUserServices, createRatingServices, updateRatingServices } from '@/services/UserServices'

    // PROPS
    const props = defineProps({
        routeId: { 
            type: Number, 
            required: true 
        },
        routeUserId: { 
            type: Number,
            required: true
        },
    })

    // VARIABLES
    const {routeId, routeUserId} = toRefs(props);

    const emit = defineEmits(['rating-updated'])

    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const currentUserId = computed(() => authStore.user?.id ?? null)
    const isOwner = computed(() => currentUserId.value === routeUserId.value)
    const userRatingId = ref(null)

    const rating = ref(0)
    const hoverRating = ref(null)
    const displayRating = computed(() => hoverRating.value ?? rating.value)

    // METODOS
    // Metodo que hace una llamada despues de montar el componente
    onMounted(async () => {
        if (!isOwner.value) {
            watch([isAuthenticated, currentUserId], ([auth, userId]) => {
                if (auth && userId !== null) {
                    fetchUserRating()
                } 
            }, { immediate: true })
        }
    })

    // Metodo para obtener si un usuario tiene un rating puesto a la ruta o no
    const fetchUserRating = async () => {
        try {
            const data = await ratingUserServices(routeId.value);
            rating.value = data.rating
            userRatingId.value = data.id
        } catch (error) {
            console.error('Error obteniendo valoracion del usuario:', error)
        }
    } 

    // Metodo para añadir o cambiar el rating de un Usuario sobre la ruta indicada
    const handleClick = async () => {
        if (!isAuthenticated.value || isOwner.value || hoverRating.value == null) return

        rating.value = hoverRating.value
        const payload = {
            rating: rating.value,
            user: currentUserId.value,
            route: routeId.value
        }

        try {
            if (userRatingId.value) {
                await updateRatingServices(userRatingId.value, payload)
            } else {
                const data = await createRatingServices(payload)
                userRatingId.value = data.id
            }

            emit('rating-updated')
        } catch (error) {
            console.error('Error guardando valoración: ', error)
        }
    }
    
    // Funcion que detecta el hover del rating
    const handleMouseMove = (event) => {
        if (!isAuthenticated.value) return

        const { left, width } = event.currentTarget.getBoundingClientRect()
        const offsetX = event.clientX - left
        const percent = offsetX / width
        hoverRating.value = Math.round(percent * 10) / 2
    }

    // Funcion que elimina el efecto del hover
    const resetHover = () => {
        hoverRating.value = null
    }

    // Funcion que muetra las rutas en funciondel rating asignado
    const getStarClass = (index) => {
        const value = displayRating.value
        if (value >= index + 1) return 'fa-solid fa-star'
        if (value >= index + 0.5) return 'fa-solid fa-star-half-alt'
        return 'fa-regular fa-star'
    }
</script>

<style lang="scss" scoped>
    .rating-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        user-select: none;
        
        .rating {
            display: inline-flex;
            font-size: 2rem;
            color: gold;
            cursor: pointer;
            transition: 0.3s;
            
            &.disabled {
                pointer-events: none;
                color: var(--color-grey);
            }

            i {
                margin-right: 0.1rem;
                transition: color 0.2s;
            }

            .value {
                font-size: 1.2rem;
                color: var(--color-dark-grey);
            }
        }

    }
    
    .rating-disabled {
        font-size: 1.25rem;
        font-weight: 900;
        color: var(--color-light-green);
    }
</style>