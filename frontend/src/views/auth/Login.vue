<template>
  <main class="flex h-full items-center justify-center py-10 sm:px-6">
    <section
      class="flex w-full flex-col justify-center bg-white px-6 py-6 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:max-w-110 sm:rounded-3xl"
    >
      <h1 class="font-montserrat-bold text-green text-center text-3xl leading-6">Inicia sesión</h1>
      <h2 class="font-montserrat-bold text-brown mb-6 text-center text-lg sm:text-xl">
        Para comenzar la aventura
      </h2>

      <p
        class="text-green bg-light-green-50 rounded-3xl px-1 py-2 text-center text-base font-bold"
        v-if="success"
      >
        <i class="fa-solid fa-circle-check"></i>
        {{ success }}
      </p>

      <form @submit.prevent="login" class="font-lato flex flex-col gap-2">
        <input type="text" v-model="inputUserMail" placeholder="Usuario o Correo" />
        <article class="relative m-auto mb-4 w-[90%]">
          <input
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            placeholder="Contraseña"
          />
          <span
            class="text-brown hover:text-green absolute top-[35%] right-0 -translate-y-1/2 cursor-pointer transition-all duration-250"
            @click="togglePassword"
          >
            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </span>
          <p class="text-green m-0 p-0 text-left text-sm font-bold">
            <router-link to="/forgot-password" class="hover:text-brown"
              >¿Olvidaste tu contraseña?</router-link
            >
          </p>
        </article>

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
          class="bg-green hover:bg-light-green hover:text-green m-auto w-[90%] cursor-pointer rounded-3xl px-3 py-2 text-base font-bold text-white transition-all duration-250"
        >
          Iniciar Sesión
        </button>
      </form>

      <p class="text-dark-grey mx-2 text-center">o</p>
      <p class="text-center">
        ¿No tienes cuenta?<router-link
          to="/register"
          class="text-green cursor-pointer font-bold transition-all duration-250 hover:text-black"
        >
          Registrate Aquí</router-link
        >
      </p>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/authStore";
import { useFormValidation } from "@/composables/useValidation";

// VARIABLES
const inputUserMail = ref("");
const password = ref("");
const router = useRouter();
const route = useRoute();
const error = ref("");
const success = computed(() => route.query.message);
const authStore = useAuthStore();

const { fieldErrors, resetErrors, validateEmail, validateUsername } = useFormValidation();

// METODOS
// Validacion del email o username
const validateLoginIdentifier = (input) => {
  if (validateEmail(input)) return true;
  if (validateUsername(input)) return true;
  return false;
};

// Validacion general
const validateLoginForm = () => {
  resetErrors();
  let valid = true;

  if (!inputUserMail.value) {
    fieldErrors.value.email = "El correo electrónico o el username es obligatorio.";
    valid = false;
  } else if (!validateLoginIdentifier(inputUserMail.value)) {
    fieldErrors.value.identifier =
      "Debes introducir un correo válido o un nombre de usuario sin espacios.";
    valid = false;
  }

  if (!password.value) {
    fieldErrors.value.password = "La contraseña es obligatoria.";
    valid = false;
  }

  return valid;
};
// Para mostrar el contenido de la contraseña
const showPassword = ref(false);
const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

// Funcion para incicar sesion
const login = async () => {
  if (!validateLoginForm()) return;

  try {
    await authStore.login(inputUserMail.value, password.value);
    router.push("/");
  } catch (err) {
    error.value = "Usuario o contraseña incorrectos";
  }
};
</script>

<style lang="scss" scoped>
form {
  input[type="text"],
  input[type="password"] {
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
