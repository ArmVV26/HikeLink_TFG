<template>
    <div class="modal-overlay" @keydown.esc="$emit('cancel')" tabindex="0">
        <div class="modal-box">
            <i class="fa-solid fa-xmark close-btn" @click="$emit('cancel')"></i>
            <h1>{{ title }}</h1>
            <p>{{ message }}</p>
            <div class="modal-actions">
                <button @click="$emit('cancel')">Cancelar</button>
                <button class="danger" @click="$emit('confirm')">Eliminar</button>
            </div>
        </div>
  </div>
</template>

<script setup>
    defineProps({
        title: { 
            type: String,
            default: '¿Eliminar?' 
        },
        message: { 
            type: String,
            default: 'Esta acción no se puede deshacer.' 
        },
    })
</script>

<style lang="scss" scoped>
    .modal-overlay {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: var(--color-vanille-opacity);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;

        .modal-box {
            position: relative;
            background: var(--color-white);
            padding: 3rem 1rem 1rem;
            border-radius: 25px;
            width: 100%;
            max-width: 40rem;
            text-align: center;

            .close-btn {
                color: var(--color-black);
                position: absolute;
                top: 1rem; 
                right: 1rem;
                font-size: 1.5rem;
                cursor: pointer;
                transition: all 0.25s;

                &:hover {
                    color: var(--color-green);
                    transform: rotate(90deg) scale(0.90);
                }
            }

            h1 {
                font-family: "Montserrat-Bold";
                font-size: 2.25rem;
                color: var(--color-green);
            }

            .modal-actions {
                margin-top: 1.5rem;
                display: flex;
                justify-content: space-between;

                button {
                    background-color: var(--color-green);
                    color: var(--color-white);
                    border: 2px solid var(--color-light-green);
                    border-radius: 25px;
                    padding: 0.5rem 1.5rem;
                    font-weight: 900;
                    cursor: pointer;
                    transition: all 0.25s;

                    &:hover {
                        background-color: var(--color-light-green);
                        color: var(--color-green);
                        border: 2px solid var(--color-green);
                    }
                }

                .danger {
                    background-color: var(--color-red-500);
                    border: 2px solid var(--color-red-700);

                    &:hover {
                        background-color: var(--color-red-300);
                        color: var(--color-black);
                        border: 2px solid var(--color-red-700);
                    }
                }
            }
        }
    }
</style>