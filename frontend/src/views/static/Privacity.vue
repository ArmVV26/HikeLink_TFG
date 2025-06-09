<template>
    <section class="privacity">
        <h1>Política de Privacidad</h1>

        <h2>Última actualización: junio 2025</h2>

        <p>
            En <strong>HikeLink</strong>, nos comprometemos a proteger tu privacidad y a garantizar 
            el uso responsable de tus datos personales. Esta política explica qué información recopilamos,
            cómo la usamos y qué derechos tienes como usuario.
        </p>

        <h3>1. Información que recopilamos</h3>
            <ul>
                <li><strong>Email:</strong> utilizado para registro, inicio de sesión y contacto.</li>
                <li>
                    <strong>Nombre completo, nombre de usuario, biografía e imagen de perfil:</strong> 
                    mostrados en tu perfil público.
                </li>
                <li><strong>Contraseña:</strong> almacenada de forma cifrada y no accesible por terceros.</li>
                <li>
                    <strong>Actividad en la plataforma:</strong> como rutas subidas, valoraciones, 
                    comentarios y favoritos.
                </li>
            </ul>

        <h3>2. Uso de la información</h3>
        <p>
            Utilizamos tus datos personales únicamente para fines relacionados con el funcionamiento de
            <strong>HikeLink</strong>, tales como:
        </p>
        <ul>
            <li>Mostrar tu contenido en tu perfil y en las rutas.</li>
            <li>Gestionar tu cuenta de usuario.</li>
            <li>Mejorar la experiencia de usuario.</li>
        </ul>

        <h3>3. Almacenamiento de la sesión</h3>
        <p>
            Utilizamos un <strong>token almacenado en localStorage</strong> para mantener la sesión del 
            usuario iniciada. Este token no contiene tus datos personales completos, y se elimina 
            automáticamente al cerrar sesión o limpiar el navegador.
        </p>

        <h3>4. Servicios de terceros</h3>
        <p>
            <strong>HikeLink</strong> utiliza servicios externos como <strong>Leaflet</strong> para mostrar 
            mapas interactivos. Estos servicios pueden recopilar información técnica como tu dirección IP o 
            comportamiento de uso.
        </p>

        <h3>5. Cookies</h3>
        <p>
            No utilizamos cookies con fines de marketing ni seguimiento. Solo empleamos almacenamiento local
            para fines estrictamente funcionales (como el token de sesión).
        </p>

        <h3>6. Eliminación de datos</h3>
        <p>
            Puedes eliminar tu cuenta en cualquier momento desde tu perfil. Esto eliminará también todas 
            las rutas y publicaciones asociadas a tu cuenta de forma permanente.
        </p>

        <h3>7. Seguridad</h3>
        <p>
            Tomamos medidas técnicas razonables para proteger tu información. Aun así, ningún sistema es 
            100% seguro, por lo que recomendamos que utilices contraseñas seguras y no compartas tu cuenta 
            con terceros.
        </p>

        <h3>8. Cambios en esta política</h3>
        <p>
            Podemos modificar esta política para adaptarla a cambios legislativos o mejoras en la plataforma.
            Te avisaremos mediante esta misma página si realizamos cambios relevantes.
        </p>

        <h3>9. Contacto</h3>
        <p>
            Si tienes dudas sobre esta política o el tratamiento de tus datos, puedes escribirnos a
            <a href="mailto:hikelink.soporte@gmail.com">hikelink.soporte@gmail.com</a>.
        </p>
    </section>
</template>

<script setup>
</script>

<style lang="scss" scoped>
    .privacity {
        width: 50rem;
        margin: 2rem auto;
        padding: 2rem 4rem;
        box-shadow: 0px 0px 10px 0px var(--color-black);
        border-radius: 25px;

        h1 {
            font-family: "Montserrat-Bold";
            font-size: 2.5rem;
            color: var(--color-green);
            line-height: 1;
        }

        h2 {
            font-size: 1rem;
            font-style: italic;
            margin-bottom: 1rem;
        }

        p:first-of-type {
            text-align: center;
        }

        strong {
            font-weight: 900;
            color: var(--color-green);
        }
        
        p {
            text-align: justify;
            text-indent: 2rem;
        }

        h3 {
            font-family: "Montserrat-Bold";
            font-size: 1.5rem;
            color: var(--color-light-green);
            margin: 2rem 0 0.25rem;
        }

        li {
            list-style: disc;
            margin-left: 5rem;
        }

        a {
            font-weight: 900;
            color: var(--color-brown);
            transition: all 0.25s;

            &:hover {
                color: var(--color-vanille);
            }
        }
    }

    @media (max-width: 800px) {
        .privacity {
            width: 100%;
            padding: 1rem;
            border-top: 5px solid var(--color-green);
            border-bottom: 5px solid var(--color-green);
            border-radius: 0;

            h1 {
                font-size: 1.5rem;
            }

            p, li {
                font-size: 0.85rem;
            }

            h3 {
                font-size: 1.25rem;
            }

            li {
                margin-left: 1rem;
            }
        }
    }
</style>