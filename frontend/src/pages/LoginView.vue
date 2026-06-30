<template>
  <q-page class="flex flex-center q-pa-md">
    <q-card class="q-pa-lg shadow-2 bg-white" style="width: 400px; max-width: 90vw; border-radius: 16px;">
      
      <q-card-section class="text-center q-pb-md">
        <q-icon name="fa-solid fa-pills" color="primary" size="3.5rem" class="q-mb-sm" />
        <h1 class="text-h4 text-weight-bold q-ma-none text-dark">¡Hola!</h1>
        <p class="text-subtitle1 text-grey-7 q-mt-sm">Ingresa tus datos para acceder a tus remedios.</p>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-form @submit.prevent="procesarLogin" class="q-gutter-y-md">
          
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
            :disable="cargando"
            :rules="[val => val && val.length >= 9 || 'RUT inválido']"
          >
            <template v-slot:prepend>
              <q-icon name="fa-solid fa-id-card" color="primary" />
            </template>
          </q-input>

          <q-input
            v-model="password"
            outlined
            label="Tu Contraseña o PIN"
            type="password"
            bg-color="white"
            label-color="primary"
            class="text-h6"
            :disable="cargando"
            :rules="[val => !!val || 'La contraseña es obligatoria']"
          >
            <template v-slot:prepend>
              <q-icon name="fa-solid fa-lock" color="primary" />
            </template>
          </q-input>

          <div class="q-mt-xl">
            <q-btn
              label="Ingresar"
              type="submit"
              color="primary"
              size="lg"
              class="full-width text-weight-bold"
              rounded
              unelevated
              :loading="cargando"
            />
          </div>
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

const rut = ref('')
const password = ref('')
const cargando = ref(false)

const procesarLogin = async () => {
  cargando.value = true
  console.log("1. Botón presionado. Iniciando petición de login...")
  
  try {
    const authStore = useAuthStore()
    
    console.log("2. Enviando datos a FastAPI:", rut.value)
    await authStore.iniciarSesion(rut.value, password.value)
    
    console.log("3. ¡Login exitoso! ID guardado en Pinia:", authStore.idPaciente)
    
    $q.notify({
      type: 'positive',
      message: '¡Bienvenido!',
      position: 'top',
      icon: 'fa-solid fa-check'
    })
    
    console.log("4. Ejecutando redirección a /alarmas...")
    router.push('/alarmas')

  } catch (err) {
    console.error("❌ ERROR DETECTADO EN EL LOGIN:", err)
    
    $q.notify({
      type: 'negative',
      message: 'Revisa tu RUT o Contraseña e intenta de nuevo.',
      position: 'top',
      icon: 'fa-solid fa-triangle-exclamation'
    })
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
:deep(.q-field__native) {
  font-size: 1.2rem !important;
  font-weight: bold;
}
:deep(.q-field__label) {
  font-size: 1.1rem !important;
}
</style>