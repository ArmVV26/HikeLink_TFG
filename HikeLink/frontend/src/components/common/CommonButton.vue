<template>
    <button
        v-if="asButton"
        type="button"
        @click="$emit('click')"
        :disabled="disabled"
        :class="['common-button', { 'hero-button': header, 'thin-button': thin, 'disabled-button': disabled }]"
    >
        <i v-if="icon !== ''" :class="icon"></i>
        {{ text }}
    </button>
    
    <a 
        v-else-if="samePage"
        @click.prevent="scrollToSection"
        :href="route"
        :class="['common-button', {'hero-button': header}]"
    >
        {{ text }}
    </a>

    <router-link
        v-else 
        :to="route" 
        :class="['common-button', {'hero-button': header}, {'thin-button': thin}]"
    >
        <i v-if="icon != ''" :class="icon"></i>
        {{ text }}
    </router-link>
</template>

<script setup>
    // PROPS
    const props = defineProps({
        text: {
            type: String,
            required: true
        },
        route: {
            type: String,
            required: true
        },
        samePage: {
            type: Boolean,
            default: false
        },
        header: {
            type: Boolean,
            default: false
        },
        icon: {
            type: String,
            default: ''
        },
        thin: {
            type: Boolean,
            default: false
        },
        asButton: {
            type: Boolean,
            default: false
        },
        disabled: {
            type: Boolean,
            default: false
        }
    });

    // VARIABLES
    // Defino el emit
    defineEmits(['click'])

    // METODOS
    // Método para desplazarse a la sección
    const scrollToSection = () => {
        const section = document.querySelector(props.route);
        if (section) {
            section.scrollIntoView({
                behavior: 'smooth',
                block: 'start' 
            });
        }
    };
</script>

<style lang="scss" scoped>
    .common-button {
        font-size: 1.5rem;
        font-family: 'Lato';
        font-weight: bold;
        cursor: pointer;

        color: var(--color-white);

        padding: 1rem 2rem;
        background-color: var(--color-green);
        border: 2px solid var(--color-light-green);
        border-radius: 25px;

        transition: all 0.5s;
        
        &:hover {
            background-color: var(--color-light-green);
            border: 2px solid var(--color-green);
            color: var(--color-green);
        }

        &:disabled {
            pointer-events: none;
        }
        
    }
    
    .hero-button {
        font-size: 2rem;
    }

    .thin-button {
        padding: 0.25rem 1rem;
    }

    .disabled-button {
        background-color: var(--color-grey);
        border-color: var(--color-black);
        color: var(--color-white);
        cursor: not-allowed;
    }
    
    i {
        margin-right: 0.5rem;
    }
</style>