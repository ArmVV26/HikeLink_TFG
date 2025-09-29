<template>
  <main class="flex h-full items-center justify-center py-10 sm:px-6">
    <section
      class="flex w-full flex-col justify-center bg-white px-6 py-6 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:max-w-110 sm:rounded-3xl"
    >
      <h1 class="font-montserrat-bold text-green text-center text-3xl leading-6">
        Restablece tu contraseña
      </h1>
      <h2
        v-if="userName"
        class="font-montserrat-bold text-brown mb-4 text-center text-base sm:text-xl"
      >
        {{ userName }}
      </h2>

      <article v-if="validToken && userName">
        <form
          v-if="!success"
          @submit.prevent="submitPassword"
          class="font-lato flex flex-col gap-2 text-sm sm:text-base"
        >
          <article class="relative m-auto mb-4 w-[90%]">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Nueva Contraseña"
            />
            <span
              class="text-brown hover:text-green absolute top-[35%] right-0 -translate-y-1/2 cursor-pointer transition-all duration-250"
              @click="showPassword = !showPassword"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </article>

          <article class="relative m-auto mb-4 w-[90%]">
            <input
              :type="showConfirm ? 'text' : 'password'"
              v-model="confirm"
              placeholder="Confirmar Contraseña"
            />
            <span
              class="text-brown hover:text-green absolute top-[35%] right-0 -translate-y-1/2 cursor-pointer transition-all duration-250"
              @click="showConfirm = !showConfirm"
            >
              <i :class="showConfirm ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
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
            Cambiar contraseña
          </button>
        </form>

        <h2
          v-else-if="success"
          class="text-green bg-light-green-50 mb-6 rounded-3xl px-1 py-2 text-center text-base font-bold"
        >
          {{ success }}
        </h2>
      </article>

      <h2 v-else class="font-montserrat-bold my-2 text-center text-red-400">
        Enlace expirado, vuelva a realizar el proceso.
      </h2>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useResetPassword } from "@/composables/useResetPassword";
import { useFormValidation } from "@/composables/useValidation";

// VARIABLES
const route = useRoute();
const uidb64 = route.params.uidb64;
const token = route.params.token;

const password = ref("");
const confirm = ref("");

const { validToken, userName, error, success, validateToken, submit } = useResetPassword(
  uidb64,
  token,
);

const { fieldErrors, resetErrors, validatePassword } = useFormValidation();

const showPassword = ref(false);
const showConfirm = ref(false);

// METODOS
// Validacion general
const validatePasswordChange = () => {
  resetErrors();
  let valid = true;

  if (!password.value) {
    fieldErrors.value.password = "La contraseña es obligatoria.";
    valid = false;
  } else if (password.value && !validatePassword(password.value)) {
    fieldErrors.value.password =
      "La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.";
    valid = false;
  }

  if (!confirm.value) {
    fieldErrors.value.confirm = "Debes ecribir de nuevo la contraseña para confirmar.";
    valid = false;
  } else if (confirm.value && password.value && confirm.value !== password.value) {
    fieldErrors.value.confirm = "Debes escribir la misma contraseña válida.";
    valid = false;
  }

  return valid;
};

onMounted(async () => {
  validateToken();
});

const submitPassword = async () => {
  if (!validatePasswordChange()) return;

  submit(password.value);
};
</script>

<style lang="scss" scoped>
form {
  input[type="text"],
  input[type="password"] {
    border: 2px solid var(--color-brown);
    border-radius: 10px;
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
