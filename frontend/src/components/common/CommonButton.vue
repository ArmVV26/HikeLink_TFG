<template>
  <button
    v-if="asButton"
    type="button"
    @click="$emit('click')"
    :disabled="disabled"
    :class="[
      'font-lato cursor-pointer rounded-3xl border-2 font-bold transition-all duration-500 disabled:pointer-events-none',
      {
        'text-2xl sm:text-3xl': header,
        'text-base sm:text-xl': !header,
        'px-2 py-2': thin,
        'px-2 py-2 sm:px-4': !thin,
        'bg-grey border-black text-white': disabled,
        'bg-green border-light-green hover:bg-light-green hover:border-green hover:text-green text-white':
          !disabled,
      },
    ]"
  >
    <i v-if="icon !== ''" :class="icon" class="mr-2"></i>
    {{ text }}
  </button>

  <a
    v-else-if="samePage"
    @click.prevent="scrollToSection"
    :href="route"
    :class="[
      'font-lato border-light-green hover:bg-light-green hover:border-green hover:text-green bg-green cursor-pointer rounded-3xl border-2 px-2 py-2 font-bold text-white transition-all duration-500 disabled:pointer-events-none sm:px-4',
      { 'text-2xl sm:text-3xl': header, 'text-lg sm:text-xl': !header },
    ]"
  >
    {{ text }}
  </a>

  <router-link
    v-else
    :to="route"
    :class="[
      'font-lato cursor-pointer rounded-3xl border-2 font-bold transition-all duration-500 disabled:pointer-events-none',
      {
        'text-2xl sm:text-3xl': header,
        'text-base sm:text-xl': !header,
        'px-2 py-2': thin,
        'px-2 py-4 sm:px-4': !thin,
        'bg-grey pointer-events-none border-black text-white': disabled,
        'bg-green border-light-green hover:bg-light-green hover:border-green hover:text-green text-white':
          !disabled,
      },
    ]"
  >
    <i v-if="icon != ''" :class="icon" class="mr-2"></i>
    {{ text }}
  </router-link>
</template>

<script setup>
// PROPS
const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  route: {
    type: String,
    required: true,
  },
  samePage: {
    type: Boolean,
    default: false,
  },
  header: {
    type: Boolean,
    default: false,
  },
  icon: {
    type: String,
    default: "",
  },
  thin: {
    type: Boolean,
    default: false,
  },
  asButton: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

// VARIABLES
// Defino el emit
defineEmits(["click"]);

// METODOS
// Método para desplazarse a la sección
const scrollToSection = () => {
  const section = document.querySelector(props.route);
  if (section) {
    section.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }
};
</script>
