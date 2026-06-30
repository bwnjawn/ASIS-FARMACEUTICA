<template>
  <q-page class="flex flex-center q-pa-md bg-grey-1">
    <q-card class="q-pa-lg shadow-2 bg-white" style="width: 400px; max-width: 90vw; border-radius: 16px;">
      
      <q-card-section class="text-center q-pb-md">
        <q-icon name="fa-solid fa-pills" color="primary" size="3.5rem" class="q-mb-sm" />
        <h1 class="text-h4 text-weight-bold q-ma-none text-dark">
          {{ esLogin ? '¡Hola!' : 'Crear Cuenta' }}
        </h1>
        <p class="text-subtitle1 text-grey-7 q-mt-sm">
          {{ esLogin ? 'Ingresa tus datos para acceder a tus remedios.' : 'Regístrate para guardar tus alarmas.' }}
        </p>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-form @submit.prevent="procesarFormulario" class="q-gutter-y-md">
          
          <q-input
            v-model="rut"
            outlined
            label="Tu RUT (ej: 12345678-9)"
            type="tel"
            mask="########-X"
            lazy-rules
            bg-color="white"
            label-color="primary"
            class="text-h6"
            :disable="authStore.cargando"
            :rules="[val => val && val.length >= 9 || 'RUT inválido']"
          />

          <q-input
            v-if="!esLogin"
            v-model="nombreUsuario"
            outlined
            label="Tu Nombre Completo"
            type="text"
            lazy-rules
            bg-color="white"
            label-color="primary"
            class="text-h6"
            :disable="authStore.cargando"
            :rules="[val => val && val.trim().length > 0 || 'El nombre es obligatorio']"
          />

          <q-input
            v-model="password"
            outlined
            label="Tu Contraseña o PIN"
            type="password"
            lazy-rules
            bg-color="white"
            label-color="primary"
            class="text-h6"
            :disable="authStore.cargando"
            :rules="[val => val && val.length >= 6 || 'Mínimo 6 caracteres']"
          />

          <q-banner v-if="authStore.error" class="bg-red-2 text-red-9 rounded-borders text-weight-bold text-subtitle1 q-mt-md">
            <q-icon name="error" size="sm" class="q-mr-xs" />
            {{ authStore.error }}
          </q-banner>

          <q-btn
            type="submit"
            color="primary"
            :label="esLogin ? 'Entrar a la Aplicación' : 'Registrar Cuenta'"
            class="full-width q-py-sm text-h6 text-weight-bold"
            style="border-radius: 12px;"
            :loading="authStore.cargando"
          />

          <q-btn
            flat
            color="secondary"
            :label="esLogin ? '¿No tienes cuenta? Regístrate aquí' : '¿Ya tienes cuenta? Inicia sesión'"
            class="full-width text-subtitle1 q-mt-sm"
            @click="conmutarModo"
          />
          
        </q-form>
      </q-card-section>

    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

// Estados del formulario
const esLogin = ref(true)
const rut = ref('')
const nombreUsuario = ref('')
const password = ref('')

const conmutarModo = () => {
  esLogin.value = !esLogin.value
  authStore.error = null // Limpia errores previos al cambiar de vista
}

const procesarFormulario = async () => {
  console.log(`1. Botón presionado. Modo: ${esLogin.value ? 'Login' : 'Registro'}`)
  
  try {
    if (esLogin.value) {
      console.log("2. Enviando credenciales de acceso a FastAPI...")
      await authStore.iniciarSesion(rut.value, password.value)
    } else {
      console.log("2. Enviando datos de nueva cuenta a FastAPI...")
      await authStore.registrarPaciente(rut.value, nombreUsuario.value, password.value)
    }
    
    console.log("3. Operación exitosa. ID registrado en Pinia:", authStore.idPaciente)
    
    $q.notify({
      type: 'positive',
      message: esLogin.value ? '¡Bienvenido de vuelta!' : 'Cuenta creada con éxito',
      position: 'top',
      icon: 'fa-solid fa-check'
    })
    
    console.log("4. Redirigiendo a panel de alarmas...")
    router.push('/alarmas')

  } catch (err) {
    console.error("❌ ERROR DETECTADO EN EL FLUJO DE ACCESO:", err)
    $q.notify({
      type: 'negative',
      message: err.message || 'Ocurrió un problema inesperado',
      position: 'top',
      icon: 'fa-solid fa-xmark'
    })
  }
}
</script>