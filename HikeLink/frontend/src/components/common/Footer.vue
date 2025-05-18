<template>
    <footer class="flex flex-col">
        <div class="first-counter flex justify-center gap-10 py-5 px-10">
            <router-link to="/">
                <ResponsiveImage
                    :info="['LogoHikelink', 'logo']"
                    :formats="['svg', 'png']"
                    figureClass="logo"
                    alt="Logo Header"
                />
            </router-link>

            <div class="explore flex flex-col">
                <h2>Explora</h2>
                <router-link to="/map">Mapa</router-link>
                <router-link to="/searchroutes">Buscar Ruta</router-link>
                <router-link to="/foro">Foro</router-link>
            </div>
            
            <div class="about flex flex-col">
                <h2>Acerca de HikeLink</h2>
                <router-link to="/aboutus">Sobre Nosotros</router-link>
                <router-link to="/contact">Contacta con Nosotros</router-link>
                <router-link to="/help">Ayuda</router-link>
            </div>

            <div class="social grid grid-cols-2">
                <a href="https://www.instagram.com/">
                    <i class="fa-brands fa-instagram"></i>
                </a>
                <a href="https://www.youtube.com/">
                    <i class="fa-brands fa-youtube"></i>
                </a>
                <a href="https://es.pinterest.com/">
                    <i class="fa-brands fa-pinterest"></i>
                </a>
                <a href="https://www.facebook.com/">
                    <i class="fa-brands fa-facebook"></i>
                </a>
            </div>
        </div>

        <div class="second-counter flex justify-between px-5 py-2">
            <p><span>© HikeLink.</span> Todos los derechos reservados.</p>

            <div class="extra-links">
                <router-link to="/conditionuse">Condiciones de Uso</router-link>
                <router-link to="/privacity">Política de Privacidad</router-link>
            </div>
        </div>
    </footer>
</template>

<script setup>
    import ResponsiveImage from '../images/ResponsiveImage.vue';
</script>
  
<style scoped>
    /* First Counter  */
    .first-counter {
        background-color: var(--color-brown);
    }
    
    .logo {
        width: 13rem;
        height: auto;
    }

    .explore h2, .about h2 {
        color: var(--color-white);
        text-shadow: 2px 2px 8px var(--color-black);
        font-size: 2.5rem;
    }

    .explore a, .about a {
        color: var(--color-grey);
        text-decoration: none;
        font-size: 1.5rem;
        font-weight: bold;
        padding-left: 2rem;
        transition: all 0.25s;
    }

    .explore a:hover, .about a:hover {
        color: var(--color-white);
        text-shadow: 2px 2px 8px var(--color-black);
    }

    .fa-brands {
        color: var(--color-white);
        font-size: 5rem;
        transition: all 0.25s;
    }

    .fa-brands:hover {
        color: var(--color-light-green);
    }

    /* Second Counter */
    .second-counter {
        background-color: var(--color-vanille);
        color: var(--color-brown);
    }

    .second-counter span {
        font-weight: bold;
    }

    .extra-links a {
        text-decoration: none;
        padding: 0 0.5rem;
    }

    .extra-links a:hover {
        text-decoration: underline;
        font-weight: 600;
    }
</style>  