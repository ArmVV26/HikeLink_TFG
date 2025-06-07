<template>
  <HeroImage name="SobreNosotros">
    <h1>Sobre HikeLink</h1>
    <h2>Más que rutas, compartimos experiencias. Así nació HikeLink.</h2>
  </HeroImage>

  <div class="links-container">
    <div class="links">
      <h1>Sobre Nosotros</h1>
      <nav>
        <a href="#aboutus">Quiénes Somos</a>
        <a href="#values">Nuestros Valores</a>
        <a href="#living">Nuestros Forma de Vivir</a>
      </nav>
    </div>
  </div>

  <div id="aboutus" class="about-us">
    <h1>Quiénes Somos</h1>
    <p>
       HikeLink nació del amor por la montaña y el deseo de compartirla.
       Somos un equipo de senderistas, escaladores y aventureros que decidió 
       crear una plataforma donde cualquier persona pudiera descubrir rutas
       auténticas, compartir sus experiencias y conectar con otros amantes del outdoor.
    </p>
    
    <div class="collage">
      <img class="img1" src="/images/img-collage/img-collage-1.jpg" alt="Imagen Collage 1" >
      <img class="img2" src="/images/img-collage/img-collage-2.jpg" alt="Imagen Collage 2" >
      <img class="img3" src="/images/img-collage/img-collage-3.jpg" alt="Imagen Collage 3" >
      <img class="img4" src="/images/img-collage/img-collage-4.jpg" alt="Imagen Collage 4" >
    </div>
  </div>

  <div id="values" class="values">
    <h1>Nuestros Valores</h1>
    
    <div>
      <div class="value-card">
        <h1>Corresponsabilidad</h1>
        <p>Promovemos un senderismo consciente y sostenible, cuidando los entornos que amamos.</p>
      </div>

      <div class="value-card">
        <h1>Pasión</h1>
        <p>Cada paso que damos viene del amor por la montaña y la aventura al aire libre.</p>
      </div>

      <div class="value-card">
        <h1>Comunidad</h1>
        <p>Creemos en la fuerza de compartir y aprender juntos. Cada ruta es una historia que suma.</p>
      </div>

      <div class="value-card">
        <h1>Educación</h1>
        <p>Creemos que compartir conocimiento enriquece la experiencia de todos y nos hace mejores montañeros.</p>
      </div>
    </div>
  </div>

  <div id="living" class="living">
    <h1>Nuestra Forma de Vivir</h1>
    <h2>Conectar con la montaña es reconectar contigo</h2>
    <p>
      El deporte en la naturaleza fortalece cuerpo y mente, reduce el estrés y mejora la salud física mientras 
      te permite descubrir paisajes únicos y respirar aire puro.
    </p>
    <ResponsiveImage
      :info="['decorative-SobreNosotros', 'img-decorative']"
      :formats="['jpg', 'webp']"
      figureClass="about-us-img-container"
      imgClass="about-us-img"
      alt="Imagen Living HikeLink"
    />
  </div>
</template>

<script setup>
  // IMPORTS
  import HeroImage from '@/components/images/HeroImage.vue';
  import ResponsiveImage from '@/components/images/ResponsiveImage.vue';
</script>

<style lang="scss" scoped>
  .links-container {
    text-align: center;

    .links {
      display: inline-flex;   
      align-items: center;
      gap: 2rem;
      margin: 2rem auto 0;
      border-bottom: 3px solid var(--color-black);
  
      h1 {
        font-family: "Montserrat-Bold";
        font-size: 2rem;
        font-style: italic;
        color: var(--color-green);
        margin: 0;
        padding-bottom: 1rem;
        line-height: 0;
        white-space: nowrap;
      }
      
      nav {
        display: flex;
        gap: 2rem;
        
        a {
          padding-bottom: 0.5rem;
          border-bottom: 3px solid transparent;
          white-space: nowrap;
          transition: all 0.25s;
    
          &:hover {
            font-weight: 900;
            border-bottom-color: var(--color-green);
          }
        }
      }
    }
  }

  .about-us {
    display: flex;
    flex-direction: column;
    margin: 1rem 0;

    h1 {
      font-family: "Montserrat-Bold";
      font-size: 2.5rem;
      color: var(--color-green);
    } 

    p {
      width: 40%;
      margin: auto;
      text-align: center;
    }

    .collage {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      grid-template-rows: 20rem 20rem;
      gap: 1rem;
      margin: 1rem auto;
      width: 50%;

      img {
        border-radius: 25px;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .img1 {
        grid-column: 1 / 3;
        grid-row: 1 / 2;
      }

      .img2 {
        grid-column: 3 / 4;
        grid-row: 1 / 3;
      }

      .img3 {
        grid-column: 1 / 2;
        grid-row: 2 / 3;
      }

      .img4 {
        grid-column: 2 / 3;
        grid-row: 2 / 3;
      }
    }
  }

  .values {
    margin-top: 5rem;
    padding: 1rem 2rem 2rem;
    background-color: var(--color-vanille-opacity);

    h1 {
      font-family: "Montserrat-Bold";
      font-size: 2.5rem;
      color: var(--color-green);
    }

    div {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 2rem;

      .value-card {
        display: flex;
        flex-direction: column;
        gap: 0rem;
        background-color: var(--color-white);
        border-radius: 25px;
        box-shadow: 3px 3px 8px 0px var(--color-black);
        padding: 2rem 1rem;
        width: 20rem;

        h1 {
          font-size: 1.5rem;
          font-style: italic;
          color: var(--color-light-green);
        }

        p {
          text-align: center;
        }
      }
    }
  }

  .living {
    display: flex;
    flex-direction: column;
    margin: 5rem 0;

    h1 {
      font-family: "Montserrat-Bold";
      font-size: 2.5rem;
      color: var(--color-green);
      line-height: 1;
    }

    h2 {
      font-family: "Montserrat-Bold";
      font-size: 1.5rem;
      color: var(--color-light-green);
    }

    p {
      text-align: center;
      width: 40%;
      margin: auto;
    }

    .about-us-img-container {
      margin: 2rem auto;
    }
  }

  @media (max-width: 1440px) {
    .about-us {
      p {
        width: 70%;
      }

      .collage {
        width: 80%;
      }
    }

    .living {
      p {
        width: 70%;
      }

      .about-us-img-container {
        margin: 2rem 5rem;
      }
    }
  }

  @media (max-width: 768px) {
    .links-container {
      .links {
        flex-direction: column;
        gap: 1rem;

        h1 {
          padding-bottom: 0;
        }

        nav {
          justify-content: center;
          align-items: center;
        }
      }
    }

    .about-us {
      .collage {
        display: flex;
        flex-direction: column;

        img {
          width: 100%;
          height: 20rem;
        }

        .img1, .img2, .img3 {
          display: none;
        }
      }
    }
  }

  @media (max-width: 470px) {
    .links-container {
        .links {
          h1 {
            font-size: 1.5rem;
          }

          nav {
            gap: 1rem;

            a {
              font-size: 0.85rem;
            }
          }
        }
    }

    .about-us {
      h1 {
        font-size: 1.5rem;
      }

      p {
        width: 90%;
        font-size: 0.85rem;
      }

      .collage {
        width: 90%;
      }
    }

    .values {
      margin-top: 0.5rem;

      h1 {
        font-size: 1.5rem;
      }

      div {
        .value-card {
          h1 {
            font-size: 1.25rem;
          }

          p {
            font-size: 0.85rem;
          }
        }
      }
    }

    .living {
      margin-top: 2rem;
      margin-bottom: 2rem;

      h1 {
        font-size: 1.5rem;
      }

      h2 {
        font-size: 1rem;
      }

      p {
        font-size: 0.85rem;
      }

      .about-us-img-container {
        margin: 2rem 1rem;
      }
    }
  }

  @media (max-width: 370px) {
    .links-container {
      .links {
        width: 100%;
        margin: 2rem 0;

        nav {
          gap: 0;
          flex-direction: column;

          a {
            padding-bottom: 0;
          }
        }
      }
    }
  }
</style>

<style>
  .about-us-img {
    width: 70rem;
    height: 40rem;
    border-radius: 25px;
    box-shadow: 0px 0px 10px 0px var(--color-black);
    object-fit: cover;
  }
</style>