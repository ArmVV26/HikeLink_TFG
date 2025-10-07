<template>
  <figure ref="counter" class="counter-img" :class="figureClass" role="img" :aria-label="alt">
    <div v-if="isSvg && svgRaw" class="inline-svg" :class="imgClass" v-html="processedSvg" />

    <picture v-else>
      <source v-for="(src, key) in currentSources" :key="key" :type="mimeType(key)" :srcset="src" />
      <img :class="imgClass" :src="currentImg" :alt="alt" loading="lazy" />
    </picture>
  </figure>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";

// Defino las propiedades del componente
const props = defineProps({
  info: Array,
  alt: String,
  imgClass: String,
  figureClass: String,
  formats: Array,
});

// Elemento DOM que me da el tamaño
const counter = ref(null);
let resizeObserver = null;

const mimeType = (ext) => {
  switch (ext) {
    case "webp":
      return "image/webp";
    case "jpg":
      return "image/jpeg";
    case "png":
      return "image/png";
    case "svg":
      return "image/svg+xml";
    default:
      return "";
  }
};

// Contiene las imagenes generadas
const imgs = ref([]);
// Guarda los srcset que debe tener picture
const currentSources = ref({});
// Guarda el src actual que debe tener el img
const currentImg = ref("");
// Para almacenar cuando se trata de una imagen SVG
const svgRaw = ref("");
const processedSvg = computed(() => {
  if (!svgRaw.value) return "";
  // Agrega las clases directamente al SVG si no las tiene
  return svgRaw.value.replace(/<svg([^>]+)>/, `<svg$1 class="${props.imgClass || ""}">`);
});
const svgContent = ref("div");

const isSvg = computed(() => props.formats.includes("svg"));

// Genera las lista de imagenes con sus rutas correctas
const generateImages = () => {
  const [name, type] = props.info;
  const base = "/images";
  const sizes = type === "logo" ? [512, 256, 128] : [3200, 2240, 1600, 960, 640, 320];

  return sizes.map((width) => {
    const obj = { width };
    props.formats.forEach((ext) => {
      if (ext === "svg") {
        obj[ext] = `${base}/${type}/${ext}/${name}.${ext}`;
      } else {
        obj[ext] = `${base}/${type}/${ext}/${name}-${width}px.${ext}`;
      }
    });
    return obj;
  });
};

// Cuando cambia de tamaño el contenedor, busca la imagen basando en el ancho
// Actualiza currentSources y currentImg
const changeImg = (widthCounter) => {
  // Ordena de menor a mayor
  const sortedImgs = [...imgs.value].sort((a, b) => a.width - b.width);

  // Busca la primera imagen que sea mas ancha que el contenedor
  const select = sortedImgs.find((i) => widthCounter <= i.width);

  const newSources = {};
  props.formats.forEach((ext) => {
    if (select[ext]) newSources[ext] = select[ext];
  });

  currentSources.value = newSources;
  currentImg.value = newSources.svg || newSources.png || newSources.jpg || newSources.webp || "";
};

// Genera las rutas, crea un ResizeObserver para ver el tamaño del contenedor
onMounted(async () => {
  imgs.value = generateImages();

  resizeObserver = new ResizeObserver((entries) => {
    for (let entry of entries) {
      changeImg(entry.contentRect.width);
    }
  });

  resizeObserver.observe(counter.value);

  // Si el formato principal es SVG
  if (isSvg.value && imgs.value[0]?.svg) {
    try {
      const res = await fetch(imgs.value[0].svg);
      svgRaw.value = await res.text();
      svgContent.value = "div";
    } catch (err) {
      console.warn("No se pudo cargar el SVG:", err);
    }
  }
});

// Detiene el ResizeObserver para evitar fugas de memoria
onBeforeUnmount(() => {
  resizeObserver?.disconnect();
});
</script>
