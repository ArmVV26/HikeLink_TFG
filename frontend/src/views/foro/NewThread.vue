<template>
  <main class="flex h-full items-center justify-center py-10 sm:px-6">
    <section
      class="w-full bg-white px-6 py-6 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:w-100 sm:rounded-3xl"
    >
      <h1 class="font-montserrat-bold text-green text-center text-3xl leading-6">Nuevo Hilo</h1>
      <h2 class="font-montserrat-bold text-brown mb-2 text-center text-lg sm:text-xl">HikeLink</h2>

      <form @submit.prevent="uploadThread" class="font-lato flex flex-col gap-2">
        <input type="text" v-model="title" placeholder="Título" class />

        <textarea
          v-model="content"
          class="min-h-12 resize-none"
          placeholder="Descripción del hilo"
        ></textarea>

        <article
          v-if="error || Object.keys(fieldErrors).length > 0"
          class="mb-5 rounded-lg bg-red-600 p-2"
        >
          <ul>
            <li class="text-center text-base font-bold text-red-100" v-for="err in fieldErrors">
              <i class="fa-solid fa-circle-exclamation"></i>
              {{ err }}
            </li>
          </ul>
          <p v-if="error" class="text-center text-base font-bold text-red-100">
            <i class="fa-solid fa-circle-exclamation"></i>
            {{ error }}
          </p>
        </article>

        <button
          type="submit"
          class="bg-green hover:bg-light-green hover:text-green m-auto w-[50%] cursor-pointer rounded-3xl px-3 py-2 text-base font-bold text-white transition-all duration-250"
        >
          Subir Hilo
        </button>
      </form>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useFormValidation } from "@/composables/useValidation";
import { uploadThreadServices } from "@/services/ThreadServices";

// VARIABLES
const title = ref("");
const content = ref("");

const error = ref("");
const router = useRouter();

const { fieldErrors, resetErrors, validateTitle } = useFormValidation();

// METODOS
// Validacion general
const validateThreadForm = () => {
  resetErrors();
  let valid = true;

  if (!title.value) {
    fieldErrors.value.title = "El título es obligatorio.";
    valid = false;
  } else if (!validateTitle(title.value)) {
    fieldErrors.value.title =
      "El título solo puede contener todas las letras, espacios, numeros, comas y guiones (-).";
    valid = false;
  }

  if (!content.value) {
    fieldErrors.value.content = "El contenido es obligatorio.";
    valid = false;
  }

  return valid;
};

// Funcion para subir el Hilo
const uploadThread = async () => {
  error.value = "";

  if (!validateThreadForm()) return;

  const formData = new FormData();
  formData.append("title", title.value);
  formData.append("content", content.value);

  try {
    const data = await uploadThreadServices(formData);
    router.push({ name: "ThreadDetail", params: { slug: data.slug, id: data.id } });
  } catch (err) {
    if (err.response && err.response.data && err.response.data.error) {
      error.value = err.response.data.error;
    } else {
      error.value = "Error al guardar la ruta.";
    }
    console.error(err);
  }
};
</script>

<style lang="scss" scoped>
form {
  input[type="text"],
  textarea {
    border: 2px solid var(--color-brown);
    border-radius: 12px;
    margin: auto;
    width: 90%;
    padding: 0.5rem 0.75rem;
    font-size: 1rem;
    color: var(--color-black);

    &:hover {
      border: 2px solid var(--color-green);
    }
  }
}
</style>
