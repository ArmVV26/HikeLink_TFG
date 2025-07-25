<template>
    <figure :class="['hero-image', computedClass]">
        <div class="background-layer"></div>
        <div class="content-layer">
            <slot/>
        </div>
    </figure>
</template>

<script setup>
    // IMPORTS
    import { computed } from 'vue';

    // PROPS
    const props = defineProps ({
        name: {
            type: String,
            required: true
        }
    });

    // VARIABLES
    // Computar la clase CSS automaticamente
    const computedClass = computed(() => `hero-${props.name}`);
</script>

<style lang="scss">
    @use 'sass:list';

    /* Definimos formatos y resoluciones */
    $formats: ("avif", "webp", "jpg");
    $resolutions: (320px, 640px, 960px, 1600px, 2240px, 3200px);

    /* Mixin que genera todas las medias para una imagen */
    @mixin hero-background($name) {
        $res-count: list.length($resolutions);

        @for $i from 1 through $res-count - 2 {
            $min-width: list.nth($resolutions, $i);
            $target-image-resolution: list.nth($resolutions, $i + 2);

            @media (min-width: $min-width) {
                background-image:
                    url("/images/hero-image/avif/hero-#{$name}-#{$target-image-resolution}.avif"),
                    url("/images/hero-image/webp/hero-#{$name}-#{$target-image-resolution}.webp"),
                    url("/images/hero-image/jpg/hero-#{$name}-#{$target-image-resolution}.jpg");
            }
        }

        // Fallback para tamaños menores al primer valor
        @media (max-width: list.nth($resolutions, 1)) {
            background-image:
                url("/images/hero-image/avif/hero-#{$name}-#{list.nth($resolutions, 3)}.avif"),
                url("/images/hero-image/webp/hero-#{$name}-#{list.nth($resolutions, 3)}.webp"),
                url("/images/hero-image/jpg/hero-#{$name}-#{list.nth($resolutions, 3)}.jpg");
        }
    }

    /* Estilos generales de todas las hero images */
    .hero-image {
        width: 100%;
        height: 55rem;
        position: relative;
        overflow: hidden;
        margin-top: -10rem;
        padding-top: 10rem;
        box-shadow: 0px -2px 10px 10px var(--color-black);
        z-index: 0;
        
        .background-layer {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: brightness(0.75) contrast(100%) saturate(90%) sepia(10%);
            z-index: 0;
        }
        
        .content-layer {
            position: relative;
            z-index: 1;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            text-align: center;
            color: white;
            padding: 1rem;

            h1 {
                font-family: "Montserrat-Bold";
                font-style: italic;
                text-shadow: 4px 6px 2px var(--color-black);
            }

            h2 {
                font-size: 2rem;
                font-family: 'Lato';
                font-style: italic;
                font-weight: normal;
                line-height: 1;
                margin-bottom: 2rem;
                text-shadow: 2px 4px 2px var(--color-black);
            }
        }
    }

    /* Aquí automáticamente se generarán las imágenes */
    .hero-PaginaPrincipal .background-layer {
        @include hero-background('PaginaPrincipal');
    }

    .hero-SobreNosotros .background-layer {
        @include hero-background('SobreNosotros');
    }

    @media (max-width: 600px) {
        .hero-image {
            .content-layer {
                h1 {
                    font-size: 2.5rem;
                }

                h2 {
                    font-size: 1.5rem;
                }
            }
        }
    }
</style>