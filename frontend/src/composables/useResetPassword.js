// JS para gestionar el reseteo de la contraseña del usuraio
import { ref } from 'vue'
import { validateResetToken } from '@/utils/api'
import { resetPasswordServices } from '@/services/UserServices'
import { useRouter } from 'vue-router'

export function useResetPassword(uidb64, token) {
    const validToken = ref(false)
    const userName = ref('')
    const error = ref('')
    const success = ref('')
    const router = useRouter()

    const validateToken = async () => {
        try {
        const res = await validateResetToken(uidb64, token)
        if (res.data.valid) {
            validToken.value = true
            userName.value = res.data.username
        }
        } catch {
            validToken.value = false
        }
    }

    const submit = async (password) => {
        error.value = ''
        success.value = ''

        try {
            await resetPasswordServices( uidb64, token, password)
            success.value = 'Contraseña restablecida correctamente. Redirigiendo a iniciar sesión.'
            setTimeout(() => {
                router.push({path: '/login', query: {message: 'Contraseña Cambiada'}})
            }, 2000)
        } catch (err) {
            console.log(err.response.data)
            error.value = err.response?.data?.new_password?.[0] || 'Error al cambiar la contraseña.'
        }
    }

    return {
        validToken,
        userName,
        error,
        success,
        validateToken,
        submit
    }
}
