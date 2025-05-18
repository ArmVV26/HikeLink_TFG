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
    import { ref, computed, onMounted, toRefs, watch } from 'vue'
    import { useAuthStore } from '@/stores/authStore'
    import api from '@/api/api'

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

    const {routeId, routeUserId} = toRefs(props);

    const emit = defineEmits(['rating-updated'])

    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const currentUserId = computed(() => authStore.user?.id ?? null)
    const isOwner = computed(() => currentUserId.value === routeUserId.value)
    const accessToken = computed(() => authStore.accessToken)
    const userRatingId = ref(null)

    const rating = ref(0)
    const hoverRating = ref(null)
    const displayRating = computed(() => hoverRating.value ?? rating.value)

    onMounted(async () => {
        if (!isOwner.value) {
            watch([isAuthenticated, currentUserId], ([auth, userId]) => {
                if (auth && userId !== null) {
                    fetchUserRating()
                } 
            }, { immediate: true })
        }
    })

    const fetchUserRating = async () => {
        try {
            const response = await api.get(`/ratings/user/${routeId.value}/`, {
                headers: {
                    Authorization: `Bearer ${accessToken.value}`
                }
            })
            rating.value = response.data.rating
            userRatingId.value = response.data.id
        } catch (error) {
            if (error.response?.status === 404) {
                rating.value = 0
                userRatingId.value = null
            } else {
                console.error('Error obteniendo valoracion del usuario:', error)
            }
        }
    } 

    const handleMouseMove = (event) => {
        if (!isAuthenticated.value) return

        const { left, width } = event.currentTarget.getBoundingClientRect()
        const offsetX = event.clientX - left
        const percent = offsetX / width
        hoverRating.value = Math.round(percent * 10) / 2
    }

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
                await api.put(`/ratings/${userRatingId.value}/`, payload, {
                    headers: {
                        Authorization: `Bearer ${accessToken.value}`
                    }
                })
            } else {
                const response = await api.post(`/ratings/`, payload, {
                    headers: {
                        Authorization: `Bearer ${accessToken.value}`
                    }
                })
                userRatingId.value = response.data.id
            }
            emit('rating-updated')
        } catch (error) {
            console.error('Error guardando valoración: ', error)
        }
    }
    
    const resetHover = () => {
        hoverRating.value = null
    }

    const getStarClass = (index) => {
        const value = displayRating.value
        if (value >= index + 1) return 'fa-solid fa-star'
        if (value >= index + 0.5) return 'fa-solid fa-star-half-alt'
        return 'fa-regular fa-star'
    }
</script>

<style scoped>
    .rating-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        user-select: none;
    }

    .rating {
        display: inline-flex;
        font-size: 2rem;
        color: gold;
        cursor: pointer;
        transition: 0.3s;
    }

    .rating.disabled {
        pointer-events: none;
        opacity: 0.5;
    }

    .rating i {
        margin-right: 0.1rem;
        transition: color 0.2s;
    }

    .value {
        font-size: 1.2rem;
        color: var(--color-dark-grey);
    }
    .rating-disabled {
        font-size: 1.25rem;
        font-weight: 900;
        color: var(--color-light-green);
    }
</style>