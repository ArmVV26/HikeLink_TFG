<template>
  <main
    class="bg-vanille-50 fixed top-0 right-0 bottom-0 left-0 z-1000 flex items-center justify-center"
    @keydown.esc="$emit('cancel')"
    tabindex="0"
  >
    <section class="relative w-full max-w-120 rounded-3xl bg-white px-4 pt-8 pb-4 text-center">
      <i
        class="fa-solid fa-xmark hover:text-green absolute top-2 right-2 cursor-pointer text-2xl transition-all duration-250 hover:scale-90 hover:rotate-90"
        @click="$emit('cancel')"
      ></i>
      <h1 class="font-montserrat-bold text-green text-3xl">{{ title }}</h1>
      <p class="text-base">{{ message }}</p>
      <article class="mt-4 flex justify-between">
        <button
          @click="$emit('cancel')"
          class="bg-green border-light-green hover:bg-light-green hover:text-green hover:border-green cursor-pointer rounded-3xl border-2 px-4 py-2 font-bold text-white transition-all duration-250"
        >
          Cancelar
        </button>
        <button
          @click="$emit('confirm')"
          class="cursor-pointer rounded-3xl border-2 border-red-700 bg-red-500 px-4 py-2 font-bold text-white transition-all duration-250 hover:bg-red-300 hover:text-black"
        >
          Eliminar
        </button>
      </article>
    </section>
  </main>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: "¿Eliminar?",
  },
  message: {
    type: String,
    default: "Esta acción no se puede deshacer.",
  },
});
</script>
