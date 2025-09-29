<template>
  <main class="flex h-full items-center justify-center py-10">
    <section
      class="w-full bg-white px-1 py-8 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] sm:w-120 sm:rounded-3xl sm:px-4"
    >
      <h1 class="font-montserrat-bold text-green text-center text-3xl leading-6">
        Modificar Perfil
      </h1>
      <h2 class="font-montserrat-bold text-brown mb-4 text-center text-xl">{{ username }}</h2>

      <form
        @submit.prevent="updateProfile"
        class="font-lato flex flex-col gap-2 text-sm sm:text-base"
      >
        <input type="text" v-model="email" placeholder="Correo Electrónico" />
        <input type="text" v-model="full_name" placeholder="Nombre y Apellidos" />

        <article class="relative m-auto w-[90%]">
          <input
            :type="showOldPassword ? 'text' : 'password'"
            v-model="old_password"
            class="w-full pr-4"
            placeholder="Contraseña Actual"
          />
          <span
            class="text-brown hover:text-green absolute top-[50%] right-1 -translate-y-1/2 cursor-pointer transition-all duration-300"
            @click="showOldPassword = !showOldPassword"
          >
            <i :class="showOldPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </span>
        </article>

        <article class="relative m-auto w-[90%]">
          <input
            :type="showNewPassword ? 'text' : 'password'"
            v-model="new_password"
            class="w-full pr-4"
            placeholder="Nueva contraseña (opcional)"
          />
          <span
            class="text-brown hover:text-green absolute top-[50%] right-1 -translate-y-1/2 cursor-pointer transition-all duration-300"
            @click="showNewPassword = !showNewPassword"
          >
            <i :class="showNewPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </span>
        </article>

        <textarea
          v-model="bio"
          placeholder="Biografía (Opcional)"
          class="min-h-40 resize-none"
        ></textarea>

        <article class="flex flex-col items-center">
          <img
            :src="getIconUserImg(username, profile_picture)"
            @error="handleImgError"
            class="border-green w-30 rounded-3xl border-2"
            alt="Imagen de Perfil del Usuario"
          />
          <input
            type="file"
            @change="handleFiles"
            accept="image/*"
            class="pt-2 pb-4 text-[0.8rem] sm:text-base"
          />
        </article>

        <article
          v-if="error || Object.keys(fieldErrors).length > 0"
          class="my-1 rounded-lg bg-red-600 p-2"
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

        <p
          class="text-green bg-light-green-50 rounded-3xl px-1 py-2 text-center text-base font-bold"
          v-if="success"
        >
          {{ success }}
        </p>
        <p
          class="text-green bg-light-green-50 rounded-3xl px-1 py-2 text-center text-base font-bold"
          v-if="successMessage"
        >
          {{ successMessage }}
        </p>

        <article class="buttons-container m-auto flex w-[90%] justify-between gap-4">
          <button
            type="submit"
            class="bg-green hover:bg-light-green hover:text-green w-[90%] text-sm text-white sm:text-base"
          >
            Guardar Cambios
          </button>
          <button
            type="button"
            class="w-[90%] bg-red-500 text-sm text-white hover:bg-red-300 hover:text-black sm:text-base"
            @click="showDeleteModal = true"
          >
            Borrar Cuenta
          </button>
        </article>
      </form>
    </section>

    <transition name="fade">
      <DeleteModal
        v-if="showDeleteModal"
        :title="'¿Quieres eliminar el Usuario?'"
        :message="'Si eliminas el Usuario no podras acceder más a esta web con esta cuenta. Piensatelo 2 veces.'"
        @confirm="confirmDeleteUser"
        @cancel="showDeleteModal = false"
      />
    </transition>
  </main>
</template>

<script setup>
// IMPORTS
import { computed, onMounted, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/authStore";
import { useUserSpecificImage } from "@/composables/useUserImage";
import { updateUserServices, deleteUserServices } from "@/services/UserServices";
import { useFormValidation } from "@/composables/useValidation";
import { apiWithAuth } from "@/utils/api";

import DeleteModal from "@/components/modal/DeleteModal.vue";

// VARIABLES
const showDeleteModal = ref(false);
const successMessage = ref("");

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const username = ref("");
const email = ref("");
const full_name = ref("");
const bio = ref("");
const profile_picture = ref("");
const old_password = ref("");
const new_password = ref("");

const new_image = ref([]);
const success = ref("");
const error = ref("");

const showOldPassword = ref(false);
const showNewPassword = ref(false);

const { fieldErrors, resetErrors, validateEmail, validatePassword, validateName } =
  useFormValidation();

// Imagen de usuario
const { getIconUserImg, handleImgError } = useUserSpecificImage();

const isAuthenticated = computed(() => authStore.isAuthenticated);

// METODOS
// Validacion general
const validateProfileForm = () => {
  resetErrors();
  let valid = true;

  if (!email.value) {
    fieldErrors.value.email = "El correo electrónico es obligatorio.";
    valid = false;
  } else if (!validateEmail(email.value)) {
    fieldErrors.value.email = "Correo electrónico no válido.";
    valid = false;
  }

  if (!full_name.value.trim()) {
    fieldErrors.value.full_name = "El nombre es obligatorio.";
    valid = false;
  } else if (!validateName(full_name.value)) {
    fieldErrors.value.full_name = "El nombre no puede contener números ni caracteres especiales.";
    valid = false;
  }

  if (new_password.value && !validatePassword(new_password.value)) {
    fieldErrors.value.new_password =
      "La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.";
    valid = false;
  }

  if (new_password.value && !old_password.value) {
    fieldErrors.value.old_password = "Introduce tu contraseña actual para cambiarla.";
    valid = false;
  }

  return valid;
};

// Funcion que manejo imagen subida
const handleFiles = (e) => {
  const file = e.target.files[0];
  if (file) {
    new_image.value = file;
  }
};

// Funcion para obtener los datos del usuario
onMounted(async () => {
  if (!isAuthenticated.value) return;

  try {
    const { data } = await apiWithAuth().get(`users/${route.params.id}`);

    username.value = data.username;
    email.value = data.email;
    full_name.value = data.full_name;
    bio.value = data.bio || "";
    profile_picture.value = data.profile_picture || "";
  } catch (err) {
    error.value = "Error al cargar los datos del usuario";
  }
});

// Funcion para actualizar los datos del usuario
const updateProfile = async () => {
  error.value = "";
  success.value = "";

  if (!isAuthenticated) return;
  if (!validateProfileForm()) return;

  const formData = new FormData();
  formData.append("email", email.value);
  formData.append("full_name", full_name.value);
  formData.append("bio", bio.value);
  if (new_image.value) formData.append("profile_picture", new_image.value);

  if (new_password.value) {
    if (!old_password.value) {
      error.value = "Debes introducir tu contraseña actual para establecer una nueva.";
      return;
    }
    formData.append("old_password", old_password.value);
    formData.append("new_password", new_password.value);
  }

  try {
    const data = await updateUserServices(route.params.id, formData);

    if (data.logout) {
      authStore.logout();
      router.push({ path: "/login", query: { message: "Contraseña Cambiada Correctamente" } });
      return;
    }

    success.value = "Perfil actualizado correctamente.";
    authStore.fetchUser();
  } catch (err) {
    if (err.response?.status === 400 && err.response.data.detail) {
      error.value = err.response.data.detail;
    } else {
      console.error(err);
      error.value = "Error al actualizar el Usuario";
    }
  }
};

// Metodo para eliminar una cuenta
const confirmDeleteUser = async () => {
  try {
    await deleteUserServices(route.params.id);
    successMessage.value = "Tu cuenta ha sido eliminada correctamente.";
    showDeleteModal.value = false;
    setTimeout(() => {
      authStore.logout();
      router.push({ path: "/login", query: { message: "Cuenta Eliminada Correctamente" } });
    }, 2000);
  } catch (error) {
    error.value = "Error al eliminar la cuenta.";
  }
};
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

form {
  input[type="text"],
  input[type="email"],
  input[type="password"],
  textarea {
    width: 90%;
    padding: 0.5rem 0.75rem;
    margin: auto;
    color: var(--color-black);
    border: 2px solid var(--color-brown);
    border-radius: 12px;

    &:hover {
      border: 2px solid var(--color-green);
    }
  }

  input[type="file"] {
    margin: auto;
    color: var(--color-black);

    &::file-selector-button {
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

.buttons-container {
  button {
    padding: 0.5rem 0.75rem;
    margin: auto;
    font-weight: 900;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.25s;
  }
}
</style>
