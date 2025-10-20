<template>
  <main class="flex h-full items-center justify-center py-10">
    <section
      class="w-full bg-white px-1 py-8 shadow-[0px_0px_10px_0px_rgb(0,_0,_0)] md:w-150 md:rounded-3xl md:px-4"
    >
      <h1 class="font-montserrat-bold text-green text-center text-3xl leading-6">Subir ruta</h1>
      <h2 class="font-montserrat-bold text-brown mb-4 text-center text-base sm:text-xl">
        HikeLink
      </h2>

      <form
        @submit.prevent="uploadRoute"
        class="font-lato flex flex-col gap-2 text-sm sm:text-base"
      >
        <input type="text" v-model="title" placeholder="Título" />

        <article class="input-select">
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

        <article class="input-select">
          <label for="difficulty">Dificultad: </label>
          <select id="difficulty" name="difficulty" v-model="difficulty">
            <option selected value="Fácil">Fácil</option>
            <option value="Moderada">Moderada</option>
            <option value="Difícil">Difícil</option>
          </select>
        </article>

        <article class="input-select">
          <label for="origin">Origen: </label>
          <select id="origin" name="origin" v-model="origin">
            <option selected value="Wikiloc">Wikiloc</option>
            <option value="Strava">Strava</option>
            <option value="OutdoorActive">OutdoorActive</option>
            <option value="AllTrails">AllTrails</option>
            <option value="Komoot">Komoot</option>
          </select>
        </article>

        <article class="input-file">
          <label for="images">Imágenes: </label>
          <input type="file" @change="handleFiles" accept="image/*" multiple />
        </article>

        <article class="input-file">
          <label for="gpxFile">Archivo GPX: </label>
          <input type="file" @change="handleGPX" accept=".gpx" />
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
          <p class="text-center text-base font-bold text-red-100">
            <i class="fa-solid fa-circle-exclamation"></i>
            {{ err }}
          </p>
        </article>

        <button
          type="submit"
          class="bg-green hover:bg-light-green hover:text-green m-auto w-[40%] cursor-pointer rounded-3xl px-3 py-2 text-base font-bold text-white transition-all duration-250"
        >
          Subir Ruta
        </button>
      </form>
    </section>
  </main>
</template>

<script setup>
// IMPORTS
import { computed, ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";
import { useFormValidation } from "@/composables/useValidation";
import { uploadRouteServices } from "@/services/RouteServices";

// VARIABLES
const title = ref("");
const type = ref("Para-Todos");
const description = ref("");
const difficulty = ref("Fácil");
const origin = ref("Wikiloc");
const images = ref([]);
const gpxFile = ref(null);

const router = useRouter();

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);

const error = ref("");
const routeData = ref({});

const { fieldErrors, resetErrors, validateTitle } = useFormValidation();

// METODOS
// Validacion general
const validateUploadRouteForm = () => {
  resetErrors();
  let valid = true;
  const maxSize = 100 * 1024 * 1024;

  if (!title.value) {
    fieldErrors.value.title = "El título es obligatorio.";
    valid = false;
  } else if (!validateTitle(title.value)) {
    fieldErrors.value.title =
      "El título solo puede contener todas las letras, espacios, numeros, comas y guiones (-).";
    valid = false;
  }

  if (!gpxFile.value) {
    fieldErrors.value.gpxFile = "El archivo GPX es obligatorio.";
    valid = false;
  } else if (gpxFile.value.size > maxSize) {
    fieldErrors.value.gpxFile = "El archivo GPX es demasiado grande.";
    valid = false;
  }

  return valid;
};

// Convierte las imagenes en un array normal
const handleFiles = (event) => {
  images.value = Array.from(event.target.files);
};

// Funcion para obtener los datos necesarios del archivo GPX
const handleGPX = async (event) => {
  // Campruebo que es un archivo GPX
  const file = event.target.files[0];
  if (!file || !file.name.endsWith(".gpx")) {
    error.value = "Por favor, sube un archivo GPX válido.";
    return;
  }

  // Leo el contenido de dentro del archivo
  gpxFile.value = file;

  const text = await file.text();
  const parser = new DOMParser();
  const xml = parser.parseFromString(text, "application/xml");

  // Saco todos los puntos de ruta y si no hay muestra un error
  const trkpts = xml.querySelectorAll("trkpt");
  if (trkpts.length === 0) {
    error.value = "Archivo GPX no contiene puntos de ruta.";
    return;
  }

  // Saco las coordenadas del primer punto
  const firstPoint = trkpts[0];
  const latInicial = parseFloat(firstPoint.getAttribute("lat"));
  const lonInicial = parseFloat(firstPoint.getAttribute("lon"));

  // Calculo la duracion
  const times = Array.from(trkpts)
    .map((pt) => {
      const time = pt.querySelector("time");
      return time ? new Date(time.textContent) : null;
    })
    .filter(Boolean);

  const duration = times.length >= 2 ? (times[times.length - 1] - times[0]) / 1000 : 0;

  //  Formula de Haversine que sirve para calcular la distancia de entre dos coordenadas geograficas
  const toRad = (deg) => (deg * Math.PI) / 180;
  const haversine = (lat1, lon1, lat2, lon2) => {
    const R = 6371e3;
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  };

  // Calculo de la distancia total
  let distance = 0;
  for (let i = 1; i < trkpts.length; i++) {
    const prev = trkpts[i - 1];
    const curr = trkpts[i];
    const lat1 = parseFloat(prev.getAttribute("lat"));
    const lon1 = parseFloat(prev.getAttribute("lon"));
    const lat2 = parseFloat(curr.getAttribute("lat"));
    const lon2 = parseFloat(curr.getAttribute("lon"));
    distance += haversine(lat1, lon1, lat2, lon2);
  }
  // Guardo los datos
  routeData.value = {
    latInicial,
    lonInicial,
    duration,
    distance,
  };
};

const uploadRoute = async () => {
  if (!isAuthenticated.value) return;
  if (!validateUploadRouteForm()) return;

  const formData = new FormData();
  formData.append("title", title.value);
  formData.append("type", type.value);
  formData.append("description", description.value);
  formData.append("difficulty", difficulty.value);
  formData.append("origin", origin.value);
  images.value.forEach((img, i) => formData.append(`images[${i}]`, img));
  formData.append("gpxFile", gpxFile.value);

  formData.append("start_latitude", routeData.value.latInicial);
  formData.append("start_longitude", routeData.value.lonInicial);
  formData.append("duration", routeData.value.duration);
  formData.append("distance", routeData.value.distance);

  try {
    const data = await uploadRouteServices(formData);
    const routeId = data.id;
    const routeSlug = data.slug;
    router.push({
      name: "RouteDetail",
      params: { slug: routeSlug, id: routeId },
    });
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
    width: 90%;
    padding: 0.5rem 0.75rem;
    margin: auto;
    font-size: 1rem;
    color: var(--color-black);
    border: 2px solid var(--color-brown);
    border-radius: 10px;

    &:hover {
      border: 2px solid var(--color-green);
    }
  }

  .input-select {
    width: 90%;
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

  .input-file {
    width: 90%;
    margin: auto;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    label {
      font-size: 1rem;
      font-weight: 900;
      color: var(--color-black);
      line-height: 0;
      margin-top: 1rem;
      text-align: center;
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
}
</style>
