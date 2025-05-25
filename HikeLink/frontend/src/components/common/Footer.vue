<template>
    <footer>
        <div class="first-counter">
            <router-link to="/">
                <ResponsiveImage
                    :info="['LogoHikelink', 'logo']"
                    :formats="['svg', 'png']"
                    figureClass="logo"
                    alt="Logo Header"
                />
            </router-link>

            <div class="links">
                <h2>Explora</h2>
                <router-link to="/map">Mapa</router-link>
                <router-link to="/search-routes">Buscar Ruta</router-link>
                <router-link to="/foro">Foro</router-link>
            </div>
            
            <div class="links">
                <h2>Acerca de HikeLink</h2>
                <router-link to="/about-us">Sobre Nosotros</router-link>
                <router-link to="/contact">Contacta con Nosotros</router-link>
                <router-link to="/help">Ayuda</router-link>
            </div>

            <div class="social">
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

        <div class="second-counter">
            <p><span>© HikeLink.</span> Todos los derechos reservados.</p>

            <div class="extra-links">
                <router-link to="/condition-use">Condiciones de Uso</router-link>
                <router-link to="/privacity">Política de Privacidad</router-link>
            </div>
        </div>
    </footer>
</template>

<script setup>
    // IMPORTS
    import ResponsiveImage from '../images/ResponsiveImage.vue';
</script>
  
<style lang="scss" scoped>
    footer {
        display: flex;
        flex-direction: column;
        
        .first-counter {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 3.5rem;
            padding: 1rem 0;
            background-color: var(--color-brown);
            
            .logo {
                width: 13rem;
                height: auto;
            }

            .links {
                display: flex;
                flex-direction: column;

                h2 {
                    color: var(--color-white);
                    text-shadow: 2px 2px 8px var(--color-black);
                    font-size: 2.5rem;
                }

                a {
                    color: var(--color-grey);
                    text-decoration: none;
                    font-size: 1.5rem;
                    font-weight: bold;
                    padding-left: 2rem;
                    transition: all 0.25s;

                    &:hover {
                        color: var(--color-white);
                        text-shadow: 2px 2px 8px var(--color-black);
                    }
                }
            }

            .social {
                display: grid;
                grid-template-columns: 1fr 1fr;
                
                .fa-brands {
                    color: var(--color-white);
                    font-size: 5rem;
                    transition: all 0.25s;
                    
                    &:hover {
                        color: var(--color-light-green);
                    }
                }
            }
        }

        .second-counter {
            display: flex;
            justify-content: space-between;
            padding: 0.25rem 1rem;
            background-color: var(--color-vanille);
            color: var(--color-brown);
            
            span {
                font-weight: bold;
            }
   
            .extra-links {
                a {
                    text-decoration: none;
                    padding: 0 0.5rem;
                    
                    &:hover {
                        text-decoration: underline;
                        font-weight: 600;
                    }
                }    
            } 
        }
    }
</style>  