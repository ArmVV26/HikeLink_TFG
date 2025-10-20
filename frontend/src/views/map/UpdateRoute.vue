<template>
  <main class="flex h-full items-center justify-center py-10">
    <section
      class="w-full bg-white px-1 py-8 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] md:w-180 md:rounded-3xl md:px-4"
    >
      <h1 class="font-montserrat-bold text-green text-center text-3xl leading-6">Modificar Ruta</h1>
      <h2 class="font-montserrat-bold text-brown mb-4 text-center text-base sm:text-xl">
        {{ title }}
      </h2>

      <form
        @submit.prevent="updateRoute"
        class="font-lato flex flex-col gap-2 text-sm sm:text-base"
      >
        <input type="text" v-model="title" placeholder="Título" />

        <article>
          <label for="type">Tipo: </label>
          <select id="type" name="type" v-model="type">
            <option selected value="Para-Todos">Para Todos</option>
            <option value="Senderismo">Senderismo</option>
            <option value="Ciclismo">Ciclismo</option>
            <option value="Trail-Running">Trail-Running</option>
            <option value="Alpinismo">Alpinismo</option>
          </select>
        </article>

        <textarea
          v-model="description"
          class="min-h-90 resize-none"
          placeholder="Descripción de la ruta"
        ></textarea>

        <article>
          <label for="difficulty">Dificultad: </label>
          <select id="difficulty" name="difficulty" v-model="difficulty">
            <option selected value="Fácil">Fácil</option>
            <option value="Moderada">Moderada</option>
            <option value="Difícil">Difícil</option>
          </select>
        </article>

        <article>
          <label for="origin">Origen: </label>
          <select id="origin" name="origin" v-model="origin">
            <option selected value="Wikiloc">Wikiloc</option>
            <option value="Strava">Strava</option>
            <option value="OutdoorActive">OutdoorActive</option>
            <option value="AllTrails">AllTrails</option>
            <option value="Komoot">Komoot</option>
          </select>
        </article>

        <article v-if="images.length > 0" class="flex flex-col">
          <p class="text-xl font-bold">Imágenes Actuales</p>
          <div
            class="bg-vanille-50 flex flex-wrap items-center justify-center gap-2 rounded-3xl p-2"
          >
            <img
              v-for="(img, index) in images"
              :key="index"
              :src="getRouteAllImg(route, img)"
              @error="handleImgError"
              class="border-green h-22 w-22 rounded-3xl border-2 object-cover sm:h-32 sm:w-32"
              alt="Imagen de la Ruta"
            />
          </div>
        </article>

        <input type="file" @change="handleFiles" accept="image/*" multiple />

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
          <p class="text-center text-base font-bold text-red-100">
            <i class="fa-solid fa-circle-exclamation"></i>
            {{ err }}
          </p>
        </article>

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
            Modificar Ruta
          </button>
          <button
            type="button"
            class="w-[90%] bg-red-500 text-sm text-white hover:bg-red-300 hover:text-black sm:text-base"
            @click="showDeleteModal = true"
          >
            Borrar Ruta
          </button>
        </article>
      </form>
    </section>

    <transition name="fade">
      <DeleteModal
        v-if="showDeleteModal"
        :title="'¿Quieres eliminar esta Ruta?'"
        :message="'Si eliminas esta Ruta se borrará de la web. Piensatelo 2 veces.'"
        @confirm="confirmDeleteRoute"
        @cancel="showDeleteModal = false"
      />
    </transition>
  </main>
</template>

<script setup>
// IMPORTS
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/authStore";
import { useFormValidation } from "@/composables/useValidation";
import { useRouteImage } from "@/composables/useRouteImage";
import { updateRouteServices, deleteRouteServices } from "@/services/RouteServices";

import DeleteModal from "@/components/modal/DeleteModal.vue";
import api from "@/utils/api";

// PROPS
const props = defineProps({
  id: String,
  slug: String,
});

// VARIABLES
const showDeleteModal = ref(false);
const successMessage = ref("");

const title = ref("");
const type = ref("");
const description = ref("");
const difficulty = ref("");
const origin = ref("");
const images = ref([]);
const newImages = ref([]);

const error = ref("");
const route = ref(null);
const router = useRouter();

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);

const { getRouteAllImg, handleImgError } = useRouteImage();

const { fieldErrors, resetErrors, validateTitle } = useFormValidation();

// METODOS
// Validacion general
const validateUpdateRouteForm = () => {
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

  return valid;
};

// Funcion para obtener las nuevas imagenes que sean subido
function handleFiles(event) {
  newImages.value = Array.from(event.target.files);
}

// Llamada a la API para obtener los datos de la ruta a modificar
onMounted(async () => {
  if (!isAuthenticated.value) return;

  try {
    const response = await api.get(`/routes/${props.id}/`);
    route.value = response.data;

    title.value = route.value.title;
    type.value = route.value.type;
    description.value = route.value.description;
    difficulty.value = route.value.difficulty;
    origin.value = route.value.origin;
    images.value = route.value.img;
  } catch (error) {
    error.value = "Error recargando los datos de la ruta";
  }
});

// Funcion que modifica la ruta con los nuevos datos proporcionados
const updateRoute = async () => {
  if (!isAuthenticated.value) return;
  if (!validateUpdateRouteForm()) return;

  const formData = new FormData();
  formData.append("title", title.value);
  formData.append("type", type.value);
  formData.append("description", description.value);
  formData.append("difficulty", difficulty.value);
  formData.append("origin", origin.value);
  if (newImages.value.length > 0) {
    newImages.value.forEach((file) => {
      formData.append("images", file);
    });
  }

  try {
    await updateRouteServices(props.id, formData);
    router.push({
      name: "RouteDetail",
      params: { slug: route.value.slug, id: route.value.id },
    });
  } catch (err) {
    error.value = "Error actualizando la ruta";
    console.error(err);
  }
};

// Metodo para eliminar una ruta
const confirmDeleteRoute = async () => {
  try {
    await deleteRouteServices(props.id);
    successMessage.value = "Tu ruta ha sido eliminada correctamente.";
    showDeleteModal.value = false;
    setTimeout(() => {
      router.push(`/profile/${authStore.user.username}-${authStore.user.id}`);
    }, 2000);
  } catch (error) {
    error.value = "Error al eliminar la cuenta.";
  }
};
</script>

<style lang="scss" scoped>
form {
  input[type="text"],
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

  article {
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: center;

    select {
      margin-left: 1rem;
      padding: 0.5rem 0.75rem;
      color: var(--color-black);
      border: 2px solid var(--color-brown);
      border-radius: 25px;

      &:hover {
        border: 2px solid var(--color-green);
      }
    }
  }

  input[type="file"] {
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

  .buttons-container {
    button {
      padding: 0.5rem 0.75rem;
      margin: auto;
      font-weight: 900;
      border-radius: 25px;
      cursor: pointer;
      transition: all 0.25s;

      &:hover {
        background-color: var(--color-light-green);
        color: var(--color-green);
      }
    }
  }
}
</style>
