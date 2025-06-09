// JS que contiene los componentes reutilizables necesarios para validar formularios
import { ref } from "vue";

// Validaciones de Formularios
export function useFormValidation() {
    const fieldErrors = ref({})

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/
    const nameRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/
    const usernameRegex = /^[a-zA-Z0-9._-]{5,}$/
    const titleRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s-,.]+$/

    const validateEmail = (email) => emailRegex.test(email)
    const validatePassword = (password) => passwordRegex.test(password)
    const validateName = (name) => nameRegex.test(name)
    const validateUsername = (username) => usernameRegex.test(username)
    const validateTitle = (title) => titleRegex.test(title)

    const resetErrors = () => {
        fieldErrors.value = {}
    }

    return {
        fieldErrors,
        resetErrors,
        validateEmail,
        validatePassword,
        validateName,
        validateUsername,
        validateTitle
    }
}