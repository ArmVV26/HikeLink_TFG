<template>
    <div class="condition-use">
        <h1>Condiciones de Uso</h1>

        <h2>Última actualización: Junio 2025</h2>

        <p>
            Bienvenido/a a <strong>HikeLink</strong>, una plataforma donde los usuarios pueden compartir, 
            valorar y descubrir rutas de senderismo.Al registrarte y utilizar nuestros servicios, aceptas 
            las siguientes condiciones de uso. Por favor, léelas detenidamente.
        </p>

        <h3>1. Requisitos de registro</h3>
        <p>
            Para participar en la plataforma (subir rutas, comentar, valorar, etc.) es necesario registrarse 
            con una cuenta de usuario. Cada usuario debe proporcionar información veraz y mantener actualizados 
            sus datos personales.
        </p>

        <h3>2. Uso adecuado de la plataforma</h3>
        <p>
            El usuario se compromete a utilizar la plataforma de forma responsable y respetuosa. 
            Está prohibido:
        </p>
        <ul>
            <li>Publicar contenido ofensivo, falso o ilegal.</li>
            <li>
                Subir rutas peligrosas, inapropiadas o que violen leyes de propiedad privada o normas 
                medioambientales.
            </li>
            <li>Realizar acciones que puedan dañar la plataforma o a otros usuarios.</li>
        </ul>

        <h3>3. Contenido generado por los usuarios</h3>
        <p>
            Los usuarios son los únicos responsables del contenido que publican (rutas, imágenes, descripciones,
            comentarios). Dicho contenido sigue siendo propiedad del usuario, aunque <strong>HikeLink</strong> se reserva el
            derecho de eliminar contenido que incumpla estas condiciones.
        </p>

        <h3>4. Limitación de responsabilidad</h3>
        <p>
            <strong>HikeLink</strong> es una plataforma informativa. No garantizamos la seguridad, accesibilidad ni legalidad
            de las rutas publicadas. Cada usuario es responsable de planificar su actividad con la debida
            precaución. <strong>HikeLink</strong> no se hace responsable de accidentes, daños personales o materiales derivados 
            del uso de la información contenida en esta web.
        </p>

        <h3>5. Suspensión o eliminación de cuentas</h3>
        <p>
            El incumplimiento de estas condiciones puede conllevar la suspensión o eliminación de la cuenta del
            usuario. Cualquier usuario puede eliminar su cuenta y los datos asociados desde su perfil en cualquier 
            momento.
        </p>

        <h3>6. Modificaciones</h3>
        <p>
            Nos reservamos el derecho de modificar estas condiciones en cualquier momento. Los cambios serán
            notificados mediante esta misma página.
        </p>

        <h3>7. Contacto</h3>
        <p>
            Para cualquier duda relacionada con estas condiciones, puedes contactarnos en
            <a href="mailto:hikelink.soporte@gmail.com">hikelink.soporte@gmail.com</a>.
        </p>
    </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
    .condition-use {
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
        .condition-use {
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