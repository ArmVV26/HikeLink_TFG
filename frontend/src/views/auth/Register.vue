<template>
  <main class="flex h-full items-center justify-center py-10 sm:px-6">
    <section
      class="flex w-full flex-col justify-center bg-white px-6 py-6 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:max-w-110 sm:rounded-3xl"
    >
      <h1 class="font-montserrat-bold text-green text-center text-3xl leading-6">
        Crear una cuenta
      </h1>
      <h2 class="font-montserrat-bold text-brown mb-6 text-center text-base sm:text-xl">
        HikeLink
      </h2>

      <form @submit.prevent="register" class="font-lato flex flex-col gap-2 text-sm sm:text-base">
        <input type="text" v-model="email" placeholder="Correo electrónico" />
        <input type="text" v-model="fullName" placeholder="Nombre y Apellidos" />
        <input type="text" v-model="username" placeholder="Nombre de usuario" />

        <article class="relative m-auto w-[90%]">
          <input
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            placeholder="Contraseña"
          />
          <span
            class="text-brown hover:text-green absolute top-[50%] right-0 -translate-y-1/2 cursor-pointer transition-all duration-250"
            @click="togglePassword"
          >
            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </span>
        </article>

        <textarea
          v-model="bio"
          class="min-h-40 resize-none"
          placeholder="Biografía (Opcional)"
        ></textarea>

        <input type="file" @change="handleFile" accept="image/*" />

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
          Registrarse
        </button>
      </form>

      <p class="text-dark-grey mx-2 text-center">o</p>
      <p class="text-center">
        ¿Ya tienes una cuenta?<router-link
          to="/login"
          class="text-green cursor-pointer font-bold transition-all duration-250 hover:text-black"
        >
          Inicia Sesión</router-link
        >
      </p>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { ref } from "vue";
import { useRouter } from "vue-router";
import { registerUserServices } from "@/services/UserServices";
import { useFormValidation } from "@/composables/useValidation";

// VARIABLES
const email = ref("");
const fullName = ref("");
const username = ref("");
const password = ref("");
const bio = ref("");
const profileImage = ref(null);

const error = ref("");
const router = useRouter();

const {
  fieldErrors,
  resetErrors,
  validateEmail,
  validatePassword,
  validateName,
  validateUsername,
} = useFormValidation();

// METODOS
// Validacion general
const validateRegisterForm = () => {
  resetErrors();
  let valid = true;

  if (!email.value) {
    fieldErrors.value.email = "El correo electrónico es obligatorio.";
    valid = false;
  } else if (!validateEmail(email.value)) {
    fieldErrors.value.email = "Correo electrónico no válido.";
    valid = false;
  }

  if (!fullName.value.trim()) {
    fieldErrors.value.full_name = "El nombre es obligatorio.";
    valid = false;
  } else if (!validateName(fullName.value)) {
    fieldErrors.value.full_name = "El nombre no puede contener números ni caracteres especiales.";
    valid = false;
  }

  if (!username.value) {
    fieldErrors.value.username = "El username es obligatorio.";
    valid = false;
  } else if (!validateUsername(username.value)) {
    fieldErrors.value.username =
      "El username no puede contener espacios ni caracteres muy raros y debe ser mayor a 5 caracteres.";
    valid = false;
  }

  if (!password.value) {
    fieldErrors.value.password = "La contraseña es obligatoria.";
    valid = false;
  } else if (!validatePassword(password.value)) {
    fieldErrors.value.password =
      "La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.";
    valid = false;
  }

  return valid;
};

// Para mostrar el contenido de la contraseña
const showPassword = ref(false);
const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

// Funcion que maneja la imagen de perfil del usuario
const handleFile = (event) => {
  profileImage.value = event.target.files[0];
};

// Funcion que gestiona el registro de un usuario
const register = async () => {
  error.value = "";

  if (!validateRegisterForm()) return;

  const formData = new FormData();
  formData.append("email", email.value);
  formData.append("full_name", fullName.value);
  formData.append("username", username.value);
  formData.append("password", password.value);
  if (bio.value) formData.append("bio", bio.value);
  if (profileImage.value) formData.append("profile_picture", profileImage.value);

  try {
    await registerUserServices(formData);
    router.push({ path: "/login", query: { message: "Usuario Registrado Correctamente" } });
  } catch (err) {
    console.error(err);
    if (err.response?.data?.username) {
      error.value = "El nombre de usuario ya está en uso.";
    } else if (err.response?.data?.email) {
      error.value = "El correo electrónico ya está registrado.";
    } else {
      error.value = "Error al registrar el usuario.";
    }
  }
};
</script>

<style lang="scss" scoped>
form {
  input[type="email"],
  input[type="text"],
  input[type="password"],
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

  input[type="file"] {
    width: 90%;
    padding: 0.5rem 0.75rem;
    margin: auto;
    font-size: 0.75rem;
    color: var(--color-black);

    &::file-selector-button {
      font-size: 1rem;
      padding: 0.5rem 0.5rem;
      border: 2px solid var(--color-brown);
      border-radius: 25px;
      cursor: pointer;
      transition: all 0.25s;

      &:hover {
        border: 2px solid var(--color-green);
      }
    }
  }
}
</style>
