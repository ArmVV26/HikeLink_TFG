<template>
  <HeroImage name="SobreNosotros">
    <h1>Sobre HikeLink</h1>
    <h2>Más que rutas, compartimos experiencias. Así nació HikeLink.</h2>
  </HeroImage>

  <section class="text-center">
    <article
      class="mx-auto mt-6 inline-flex w-[70%] flex-col items-center justify-center gap-6 border-b-4 border-black md:flex-row"
    >
      <h1
        class="font-montserrat-bold text-green text-2xl leading-0 whitespace-nowrap italic md:pb-4"
      >
        Sobre Nosotros
      </h1>
      <nav class="flex flex-col md:flex-row md:gap-6">
        <a
          href="#aboutus"
          class="hover:border-b-green border-b-4 border-transparent pb-2 whitespace-nowrap transition-all duration-300 hover:font-bold"
          >Quiénes Somos</a
        >
        <a
          href="#values"
          class="hover:border-b-green border-b-4 border-transparent pb-2 whitespace-nowrap transition-all duration-300 hover:font-bold"
          >Nuestros Valores</a
        >
        <a
          href="#living"
          class="hover:border-b-green border-b-4 border-transparent pb-2 whitespace-nowrap transition-all duration-300 hover:font-bold"
          >Nuestros Forma de Vivir</a
        >
      </nav>
    </article>
  </section>

  <section id="aboutus" class="my-10 flex flex-col text-center">
    <h1 class="font-montserrat-bold text-green text-3xl md:text-5xl">Quiénes Somos</h1>
    <p class="m-auto w-[90%] text-sm sm:w-[60%] sm:text-base xl:w-[40%]">
      HikeLink nació del amor por la montaña y el deseo de compartirla. Somos un equipo de
      senderistas, escaladores y aventureros que decidió crear una plataforma donde cualquier
      persona pudiera descubrir rutas auténticas, compartir sus experiencias y conectar con otros
      amantes del outdoor.
    </p>

    <article
      class="mx-auto my-4 w-[90%] sm:w-[70%] md:grid md:grid-cols-3 md:grid-rows-[20rem_20rem] md:gap-4 xl:w-[50%]"
    >
      <img
        class="col-span-2 row-span-1 hidden h-full w-full rounded-3xl object-cover md:block"
        src="/images/img-collage/img-collage-1.jpg"
        alt="Imagen Collage 1"
      />
      <img
        class="col-span-1 row-span-2 hidden h-full w-full rounded-3xl object-cover md:block"
        src="/images/img-collage/img-collage-2.jpg"
        alt="Imagen Collage 2"
      />
      <img
        class="col-span-1 row-span-1 h-full w-full rounded-3xl object-cover"
        src="/images/img-collage/img-collage-3.jpg"
        alt="Imagen Collage 3"
      />
      <img
        class="col-span-1 row-span-1 hidden h-full w-full rounded-3xl object-cover md:block"
        src="/images/img-collage/img-collage-4.jpg"
        alt="Imagen Collage 4"
      />
    </article>
  </section>

  <main id="values" class="bg-vanille-50 mb-10 px-4 py-6 text-center">
    <h1 class="font-montserrat-bold text-green text-3xl md:text-5xl">Nuestros Valores</h1>

    <section class="mt-4 flex flex-wrap justify-center gap-6">
      <article
        class="flex w-80 flex-col rounded-3xl bg-white px-4 py-6 shadow-[3px_3px_8px_0px_rgb(0,_0,_0)]"
      >
        <h1 class="font-montserrat-bold text-light-green text-lg italic sm:text-2xl">
          Corresponsabilidad
        </h1>
        <p class="text-sm sm:text-base">
          Promovemos un senderismo consciente y sostenible, cuidando los entornos que amamos.
        </p>
      </article>

      <article
        class="flex w-80 flex-col rounded-3xl bg-white px-4 py-6 shadow-[3px_3px_8px_0px_rgb(0,_0,_0)]"
      >
        <h1 class="font-montserrat-bold text-light-green text-lg italic sm:text-2xl">Pasión</h1>
        <p class="text-sm sm:text-base">
          Cada paso que damos viene del amor por la montaña y la aventura al aire libre.
        </p>
      </article>

      <article
        class="flex w-80 flex-col rounded-3xl bg-white px-4 py-6 shadow-[3px_3px_8px_0px_rgb(0,_0,_0)]"
      >
        <h1 class="font-montserrat-bold text-light-green text-lg italic sm:text-2xl">Comunidad</h1>
        <p class="text-sm sm:text-base">
          Creemos en la fuerza de compartir y aprender juntos. Cada ruta es una historia que suma.
        </p>
      </article>

      <article
        class="flex w-80 flex-col rounded-3xl bg-white px-4 py-6 shadow-[3px_3px_8px_0px_rgb(0,_0,_0)]"
      >
        <h1 class="font-montserrat-bold text-light-green text-lg italic sm:text-2xl">Educación</h1>
        <p class="text-sm sm:text-base">
          Creemos que compartir conocimiento enriquece la experiencia de todos y nos hace mejores
          montañeros.
        </p>
      </article>
    </section>
  </main>

  <section id="living" class="mb-10 flex flex-col text-center">
    <h1 class="font-montserrat-bold text-green text-3xl md:text-5xl">Nuestra Forma de Vivir</h1>
    <h2 class="font-montserrat-bold text-light-green text-lg md:text-2xl">
      Conectar con la montaña es reconectar contigo
    </h2>
    <p class="m-auto w-[90%] text-sm sm:w-[60%] sm:text-base xl:w-[40%]">
      El deporte en la naturaleza fortalece cuerpo y mente, reduce el estrés y mejora la salud
      física mientras te permite descubrir paisajes únicos y respirar aire puro.
    </p>
    <ResponsiveImage
      :info="['decorative-SobreNosotros', 'img-decorative']"
      :formats="['jpg', 'webp']"
      figureClass="about-us-img-container"
      imgClass="about-us-img"
      class="mx-6 my-6 sm:mx-20 xl:mx-auto"
      alt="Imagen Living HikeLink"
    />
  </section>
</template>

<script setup>
// IMPORTS
import HeroImage from "@/components/images/HeroImage.vue";
import ResponsiveImage from "@/components/images/ResponsiveImage.vue";
</script>

<style>
.about-us-img {
  width: 70rem;
  height: 100%;
  border-radius: 25px;
  box-shadow: 0px 0px 10px 0px var(--color-black);
  object-fit: cover;
}
</style>
