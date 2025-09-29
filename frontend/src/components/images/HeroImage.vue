<template>
  <figure
    :class="[
      'relative z-0 mt-[-10rem] h-200 w-full overflow-hidden pt-[10rem] shadow-[0px_-2px_10px_10px_rgb(0,_0,_0)] md:h-240',
      'hero-image',
      computedClass,
    ]"
  >
    <div
      class="background-layer sature-90 absolute inset-0 z-0 bg-cover bg-center bg-no-repeat brightness-75 contrast-100 sepia-10"
    ></div>
    <article
      class="content-layer relative z-1 flex h-full w-full flex-col items-center justify-center p-4 text-center text-white"
    >
      <slot />
    </article>
  </figure>
</template>

<script setup>
// IMPORTS
import { computed } from "vue";

// PROPS
const props = defineProps({
  name: {
    type: String,
    required: true,
  },
});

// VARIABLES
// Computar la clase CSS automaticamente
const computedClass = computed(() => `hero-${props.name}`);
</script>

<style lang="scss">
@use "sass:list";

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
.content-layer {
  h1 {
    font-size: 3rem;
    font-family: "Montserrat-Bold";
    font-style: italic;
    text-shadow: 4px 6px 2px var(--color-black);
  }

  h2 {
    font-size: 1.5rem;
    font-family: "Lato";
    text-shadow: 2px 4px 2px var(--color-black);
    line-height: 1;
    margin-bottom: 3rem;
  }
}

/* Aquí automáticamente se generarán las imágenes */
.hero-PaginaPrincipal .background-layer {
  @include hero-background("PaginaPrincipal");
}

.hero-SobreNosotros .background-layer {
  @include hero-background("SobreNosotros");
}

@media (max-width: 1024px) {
  .content-layer {
    h1 {
      font-size: 2.5rem;
    }
  }
}

@media (max-width: 768px) {
  .content-layer {
    h1 {
      font-size: 2.25rem;
    }

    h2 {
      font-size: 1.25rem;
    }
  }
}
</style>
