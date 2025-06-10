<template>
    <div class="not-found-container">
        <div class="not-found-content">
            <h1>404</h1>
            <h2>¡Ups! Página no encontrada</h2>
            <p>
               Lo sentimos, la página que estás buscando no existe o ha sido movida.
               Puedes volver a la página principal o intentar buscar lo que necesitas.
            </p>
            <router-link to="/" class="home-button">
                <i class="fa-solid fa-house"></i>
                Volver al inicio
            </router-link>
        </div>
    </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
    .not-found-container {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0;
    }
    .not-found-content {
        width: 35rem;
        padding: 2rem 0;
        background-color: white;
        border-radius: 25px;
        box-shadow: 0px 0px 10px 0px var(--color-black);
        text-align: center;
        
        h1 {
            font-size: 6rem;
            color: var(--color-green);
            margin: 0;
            line-height: 1;
        }
        
        h2 {
            color: var(--color-black);
            margin: 1rem 0;
            font-size: 2rem;
        }
        
        p {
            color: var(--color-gray);
            margin: 0.5rem 1rem;
            line-height: 1.6;
            text-indent: 2rem;
            text-align: justify;
        }
        
        .home-button {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background-color: var(--color-green);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            text-decoration: none;
            margin-top: 2rem;
            transition: all 0.3s ease;
        
            &:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
        
            i {
                font-size: 1.2rem;
            }
        }
    }

    @media (max-width: 550px) {
        .not-found-content {
            width: 100%;
            padding: 1rem 0;
            border-top: 5px solid var(--color-green);
            border-bottom: 5px solid var(--color-green);
            border-radius: 0;
        }
    }
</style> 