<template>
  <main class="flex h-full items-center justify-center px-6">
    <section
      class="flex max-w-110 flex-col justify-center rounded-3xl bg-white px-6 py-6 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)]"
    >
      <h1 class="font-montserrat-bold text-green text-center text-2xl leading-6">
        Recupera tu contraseña
      </h1>
      <p class="mb-2 text-center text-base text-black">
        Inserta el correo para mandarte un correo con un enlace para que recuperes tu contraseña.
      </p>

      <form
        v-if="!success && !error"
        @submit.prevent="submitEmail"
        class="font-lato flex flex-col gap-2"
      >
        <input
          type="text"
          v-model="email"
          placeholder="Tu correo"
          class="border-brown hover:border-green m-auto w-[90%] rounded-3xl border-2 px-3 py-2 text-base text-black"
        />
        <button
          type="submit"
          class="bg-green hover:bg-light-green hover:text-green m-auto w-[90%] cursor-pointer rounded-3xl px-1 py-2 text-base font-bold text-white transition-all duration-250"
        >
          Enviar enlace
        </button>
      </form>

      <p
        class="text-green bg-light-green-50 rounded-3xl px-1 py-2 text-center text-base font-bold"
        v-if="success"
      >
        <i class="fa-solid fa-circle-check"></i>
        {{ success }}
      </p>

      <article
        v-if="error || Object.keys(fieldErrors).length > 0"
        class="my-1 rounded-lg bg-red-500 p-2"
      >
        <ul>
          <li class="text-center text-base font-bold text-white" v-for="err in fieldErrors">
            <i class="fa-solid fa-circle-exclamation"></i>
            {{ err }}
          </li>
        </ul>
        <p class="text-center text-base font-bold text-white">{{ error }}</p>
      </article>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { ref } from "vue";
import { forgotPasswordServices } from "@/services/UserServices";
import { useFormValidation } from "@/composables/useValidation";

// VARIABLES
const email = ref("");
const success = ref("");
const error = ref("");

const { fieldErrors, resetErrors, validateEmail } = useFormValidation();

// METODOS
// Validacion general
const validateEmailForm = () => {
  resetErrors();
  let valid = true;

  if (!email.value) {
    fieldErrors.value.email = "El correo electrónico es obligatorio";
    valid = false;
  } else if (!validateEmail(email.value)) {
    fieldErrors.value.email = "Correo electrónico no válido";
    valid = false;
  }

  return valid;
};

// Funcion para mandar el correo para que el usuario recupere su contraseña
const submitEmail = async () => {
  success.value = "";
  error.value = "";

  if (!validateEmailForm()) return;

  try {
    await forgotPasswordServices(email.value);
    success.value =
      "Si el correo está registrado, te enviamos un enlace para restablecer tu contraseña";
  } catch (err) {
    error.value = "Hubo un problema al enviar el correo";
  }
};
</script>
