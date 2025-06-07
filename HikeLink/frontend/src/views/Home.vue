<template>
  <HeroImage name="PaginaPrincipal">
    <h1>Explora. Comparte. Conecta.</h1>
    <h2>¿Quieres saber como funciona HikeLink?</h2>
    <CommonButton 
      :samePage="true"
      :header="true"  
      :text="'Saber Más'"
      :route="'#tutorial'"
    />
  </HeroImage>

  <RouteCarousel 
    :routes="topRoutes"
  />

  <div class="history">
    <ResponsiveImage
      :info="['decorative-PaginaPrincipal', 'img-decorative']"
      :formats="['jpg', 'webp']"
      figureClass="history-img-container"
      imgClass="history-img"
      alt="Imagen Historia HikeLink"
    />

    <div class="history-content">
      <h1>Nuestra Historia</h1>
      <p>
        HikiLink nació de la pasión por la montaña y la necesidad de tener
         un lugar donde compartir y descubrir rutas reales, contadas por quienes
         las han vivido.¿Quieres saber cómo empezó todo?
      </p>
      <div>
        <CommonButton 
          :text="'Conoce Nuestra Historia'"
          :route="'/about-us'"
        />
      </div>
    </div>
  </div>

  <div id="tutorial" class="tutorial">
    <div class="account">
      <i class="fa-solid fa-map-location-dot"></i>
      <h1>Crea tu cuenta</h1>
      <p>
        Regístrate gratis, crea tu perfil y únete a una comunidad de amantes de la
         montaña. Podrás explorar rutas subidas por otros usuarios y guardarlas en favoritos.
      </p>
    </div>

    <div class="upload">
      <i class="fa-solid fa-file-arrow-up"></i>
      <h1>Sube tus rutas</h1>
      <p>
        Guarda tus recorridos subiendo archivos GPX desde tu app favorita. Añade 
         descripciones, fotos y deja tu huella en el mapa.
      </p>
    </div>

    <div class="find-person">
      <i class="fa-solid fa-people-group"></i>
      <h1>Descubre y Conecta</h1>
      <p>
        Busca nuevas rutas, comenta en el foro, deja valoraciones y comparte experiencias. 
         HikiLink es una comunidad donde todos sumamos.
      </p>
    </div>
  </div>

</template>  

<script setup>
  // IMPORTS
  import { ref, onMounted, computed } from 'vue';
  import HeroImage from '@/components/images/HeroImage.vue';
  import CommonButton from '@/components/common/CommonButton.vue';
  import RouteCarousel from '@/components/images/RouteCarousel.vue';
  import ResponsiveImage from '@/components/images/ResponsiveImage.vue';
  import api from '@/utils/api';

  // VARIABLES
  const routes = ref(null)
  const topRoutes = computed(() => {
    return routes.value ? routes.value.slice(0, 5) : []
  })

  // METODOS
  // Funcion para obtener ordenadas por mayor rating
  onMounted(async () => {
    try {
      const response = await api.get('/routes/')
      const sortedRoutes = response.data.sort((a, b) => b.average_rating - a.average_rating)
      routes.value = sortedRoutes
    } catch (error) {
      console.error('Error cargando rutas:', error)
    }
  })
</script>

<style lang="scss" scoped>
  .history {
    display: flex;
    justify-content: space-around;
    align-items: stretch;
    background-color: var(--color-vanille);
    width: 100%;
    gap: 2rem;
    padding: 3rem 15%;
    margin-bottom: 2rem;
    
    .history-img-container,
    .history-content {
      flex: 1 1 0;
      max-width: 80rem;
      display: flex;
    }

    .history-img-container {
      align-items: stretch;
    }
    
    .history-content {
      width: 80rem;
      flex-direction: column;
      
      h1 {
        font-family: "Montserrat-Bold";
        font-size: 2rem;
        font-weight: bolder;
        font-style: italic;
        text-align: left;
        color: var(--color-green);
      }
      
      p {
        font-size: 1.25rem;
        font-weight: 900;
        text-align: justify;
        color: var(--color-brown);
      }
      
      div {
        margin-top: 2rem;
        margin-bottom: 0.75rem;
      }
    }
  }

  .tutorial {
    display: flex;
    flex-direction: row;
    gap: 2rem;
    padding: 0 15%;
    margin-bottom: 2rem;
    
    div {
      width: 45rem;
      height: 28rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background-color: var(--color-vanille-opacity);
      padding: 2rem 1rem;
      border-radius: 25px;
      box-shadow: 0px 0px 0px 2px var(--color-green),
                  0px 0px 5px 0px var(--color-black);
                  
      i {
        color: var(--color-light-green);
        font-size: 8rem;
      }
      
      h1 {
        color: var(--color-green);
        font-size: 1.75rem;
        padding: 1rem 0 0.25rem;
        font-family: "Montserrat-Bold";
      }
      
      p {
        text-align: center;
        color: var(--color-brown);
        font-weight: bolder;
      }
    }
    .account, .find-person {
      margin-top: 2rem;
    }
    .upload {
      margin-bottom: 2rem;
    }
  }

  @media (max-width: 1150px) {
    .history {
      flex-direction: column;
      padding: 3rem;
      
      .history-img-container {
        width: 100%;
      }

      .history-content {
        width: 100%;

        h1 {
          text-align: center;
        }

        p {
          text-align: center;
        }

        div {
          align-self: center;
          margin-top: 2rem;
        }
      }
    }

    .tutorial {
      padding: 0 1rem;
    }
  }
  
  @media (max-width: 750px) {
    .tutorial {
      flex-direction: column;
      align-items: center;

      div {
        width: 25rem;
      }

      .account, .find-person, .upload {
        margin-top: 0;
        margin-bottom: 0;
      }
    }
  }

  @media (max-width: 450px) {
    .tutorial {
      padding: 0;

      div {
        width: 100%;
        border-radius: 0;
        padding: 1rem;
      }
    }
  }  
</style>


<style>
  /* Estilo Global solamente para esto */
  .history-img {
    border-radius: 25px;
    box-shadow: 0px 0px 10px 0px var(--color-black);
  }
</style>