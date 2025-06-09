<template>
  <div class="main-container">
    <div class="reset-form">
      <h1>Restablece tu contraseña</h1>
      <h2 v-if="userName">{{ userName }}</h2>

      <div v-if="validToken && userName">
        <form v-if="!success" @submit.prevent="submitPassword">
          <div class="password-wrapper">
            <input :type="showPassword? 'text' : 'password'"
              v-model="password" 
              placeholder="Nueva Contraseña" 
            />
            <span class="toggle-password" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
  
          <div class="password-wrapper">
            <input :type="showConfirm ? 'text' : 'password'"
              v-model="confirm"
              placeholder="Confirmar Contraseña" />
            <span class="toggle-password" @click="showConfirm = !showConfirm">
              <i :class="showConfirm ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
  
          <ul>
            <li class="error" v-for="err in fieldErrors">{{ err }}</li>
          </ul>
          <p class="error" v-if="error">{{ error }}</p>
  
          
          <button type="submit">Cambiar contraseña</button>
        </form>

        <h2 v-else-if="success" class="success">{{ success }}</h2>
      </div>
      
      <h2 v-else class="expired">Enlace expirado, vuelva a realizar el proceso.</h2>
    </div>
  </div>
</template>

<script setup>
  // IMPORTS
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { useResetPassword } from '@/composables/useResetPassword'
  import { useFormValidation } from '@/composables/useValidation'

  // VARIABLES
  const route = useRoute()
  const uidb64 = route.params.uidb64
  const token = route.params.token
  
  const password = ref('')
  const confirm = ref('')

  const {
    validToken,
    userName,
    error,
    success,
    validateToken,
    submit
  } = useResetPassword(uidb64, token)

  const { 
    fieldErrors,
    resetErrors,
    validatePassword,
  } = useFormValidation()

  const showPassword = ref(false)
  const showConfirm = ref(false)

  // METODOS
  // Validacion general
  const validatePasswordChange = () => {
    resetErrors()
    let valid = true

    if (!password.value) {
      fieldErrors.value.password = 'La contraseña es obligatoria.'
      valid = false
    } else if (password.value && !validatePassword(password.value)) {
      fieldErrors.value.password = 'La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.'
      valid = false
    }

    if (!confirm.value) {
      fieldErrors.value.confirm = 'Debes ecribir de nuevo la contraseña para confirmar.'
      valid = false
    } else if (confirm.value && password.value && confirm.value !== password.value) {
      fieldErrors.value.confirm = 'Debes escribir la misma contraseña válida.'
      valid = false
    }

    return valid
  }

  onMounted(async () => {
    validateToken()
  })
  
  const submitPassword = async () => {
    if (!validatePasswordChange()) return

    submit(password.value)
  }
</script>

<style lang="scss" scoped>
  .main-container {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem 0;
  }

  .reset-form {
    max-width: 31rem;
    padding: 2rem 1.5rem;
    background-color: var(--color-white);
    border-radius: 25px;
    box-shadow: 0px 0px 10px 0px var(--color-black);

    display: flex;
    flex-direction: column;
    justify-content: center;

    h1 {
      font-family: "Montserrat-Bold";
      font-size: 2rem;
      color: var(--color-green);
      text-shadow: none;
      line-height: 1;
    }

    h2 {
      font-family: "Montserrat-Bold";
      font-size: 1.5rem;
      color: var(--color-brown);
      text-shadow: none;
      margin-bottom: 1rem;
    }

    form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      font-family: "Lato";

      input[type="text"], input[type="password"] {
        width: 90%;
        padding: 0.5rem 0.75rem;
        margin: auto;
        font-size: 1rem;
        color: var(--color-black);
        border: 2px solid var(--color-brown);
        border-radius: 10px;
        
        &:hover {
          border: 2px solid var(--color-green);
        }
      }

      .password-wrapper {
        position: relative;
        width: 90%;
        margin: auto;

        input {
          width: 100%;
          padding-right: 2.5rem;
        }

        .toggle-password {
          position: absolute;
          top: 50%;
          right: 0.75rem;
          color: var(--color-brown);
          transform: translateY(-50%);
          transition: all 0.25s;
          cursor: pointer;
                    
          &:hover {
            color: var(--color-green);
          }
        }
      }  
      
      .error {
        text-align: center;
        color: var(--color-red-400);
        font-size: 1rem;
        font-weight: 900;
      }
            
      button[type="submit"] {
        width: 90%;
        padding: 0.5rem 0.75rem;
        margin: auto;
        font-size: 1rem;
        font-weight: 900;
        color: var(--color-white);
        background-color: var(--color-green);
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.25s;
                
        &:hover {
          background-color: var(--color-light-green);
          color: var(--color-green);
        }
      }
    }
    
    .success {
      color: var(--color-green);
      font-size: 1rem;
      font-weight: 900;
      text-align: center;
    }

    .expired {
      font-family: "Monteserrat-Bold";
      font-size: 1.5rem;
      color: var(--color-red-400);
      text-shadow: none;
    }
  }

  @media (max-width: 500px) {
    .reset-form {
      width: 100%;
      padding: 1rem 0;
      border-top: 5px solid var(--color-green);
      border-bottom: 5px solid var(--color-green);
      border-radius: 0;
    }
  }
</style>