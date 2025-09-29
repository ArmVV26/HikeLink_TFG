<template>
  <main
    class="mx-auto px-6 py-10 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:my-10 sm:w-150 sm:rounded-3xl"
  >
    <h1 class="font-montserrat-bold text-green text-center text-lg leading-6 sm:text-2xl">
      Centro de Ayuda
    </h1>

    <p class="font-montserrat text-center text-base">
      Encuentra respuestas a las preguntas más frecuentes sobre el uso de
      <strong class="text-green font-bold">HikeLink</strong>
    </p>

    <section v-for="(item, index) in faqs" :key="index" class="mt-6">
      <button @click="toggle(index)" class="flex items-center gap-4">
        <h3 class="font-montserrat-bold text-light-green text-base sm:text-lg">
          {{ item.pregunta }}
        </h3>
        <i
          class="fa-solid fa-caret-down text-brown text-2xl transition-all duration-300"
          :class="{ 'rotate-180': open[index] }"
        ></i>
      </button>
      <article v-show="open[index]">
        <p class="indent-6 text-sm sm:text-base">{{ item.respuesta }}</p>
      </article>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { ref } from "vue";

// VARIABLES
const faqs = ref([
  {
    pregunta: "¿Cómo puedo crear una cuenta en HikeLink?",
    respuesta:
      'Puedes crear una cuenta desde la página principal haciendo clic en "Registrarse". Solo necesitas proporcionar un nombre, correo electrónico, contraseña y aceptar los términos de uso.',
  },
  {
    pregunta: "¿Cómo subo una nueva ruta de senderismo?",
    respuesta:
      'Accede con tu cuenta y haz clic en "Subir ruta". Completa los campos requeridos: nombre de la ruta, descripción, dificultad, duración, imágenes y el arhivo GPX.',
  },
  {
    pregunta: "¿Puedo editar o eliminar una ruta que ya he subido?",
    respuesta:
      "Sí, desde tu perfil puedes editar o eliminar cualquiera de tus rutas en cualquier momento.",
  },
  {
    pregunta: "¿Qué significan las valoraciones de las rutas?",
    respuesta:
      "Cada ruta puede ser valorada de 0 a 5 por otros usuarios. Esto ayuda a destacar las rutas más recomendadas por la comunidad.",
  },
  {
    pregunta: "¿Cómo puedo eliminar mi cuenta?",
    respuesta:
      "Desde tu perfil, accede a editar perfil y encontrarás la opción de eliminar tu cuenta de forma permanente.",
  },
]);

const open = ref(Array(faqs.value.length).fill(false));

// METODOS
// Funcion para abrir la pregunta o no
const toggle = (index) => {
  open.value[index] = !open.value[index];
};
</script>

<style lang="scss" scoped>
.faq {
  width: 50rem;
  margin: 2rem auto;
  padding: 2rem 4rem;
  box-shadow: 0px 0px 10px 0px var(--color-black);
  border-radius: 25px;

  h1 {
    font-family: "Montserrat-Bold";
    font-size: 2.5rem;
    color: var(--color-green);
    line-height: 1;
  }

  h2 {
    font-size: 1rem;
    font-style: italic;
    margin-bottom: 1rem;
  }

  button {
    display: flex;
    align-items: center;
    margin: auto;
    gap: 1rem;

    h3 {
      font-family: "Montserrat-Bold";
      font-size: 1.5rem;
      color: var(--color-light-green);
    }

    i {
      font-size: 1.5rem;
      color: var(--color-brown);
      transition: all 0.25s;

      &.open {
        transform: rotate(180deg);
      }
    }
  }

  p {
    text-align: justify;
    text-indent: 2rem;
  }

  strong {
    font-weight: 900;
    color: var(--color-green);
  }
}

@media (max-width: 800px) {
  .faq {
    width: 100%;
    padding: 1rem;
    border-top: 5px solid var(--color-green);
    border-bottom: 5px solid var(--color-green);
    border-radius: 0;

    h1 {
      font-size: 1.5rem;
    }

    button {
      h3 {
        font-size: 1.25rem;
      }
    }

    p {
      font-size: 0.85rem;
    }
  }
}
</style>
