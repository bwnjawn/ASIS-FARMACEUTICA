<template>
  <q-page class="q-pa-md bg-grey-1">
    
    <q-btn 
      flat 
      icon="arrow_back" 
      color="primary" 
      label="Volver" 
      class="text-h6 q-mb-md" 
      @click="router.push('/alarmas')" 
    />

    <q-card class="q-pa-lg shadow-2 bg-white" style="border-radius: 16px;">
      <q-card-section class="text-center q-pb-md">
        <q-icon name="fa-solid fa-bell" color="primary" size="3.5rem" class="q-mb-sm" />
        <h1 class="text-h4 text-weight-bold q-ma-none text-dark">Nuevo Remedio</h1>
        <p class="text-subtitle1 text-grey-7 q-mt-sm">Configure a qué hora debe tomar su medicamento.</p>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="guardarAlarma" class="q-gutter-y-lg">
          
          <q-input
            v-model="formulario.nombre_medicamento"
            outlined
            label="¿Qué remedio es? (Ej: Paracetamol)"
            type="text"
            lazy-rules
            bg-color="white"
            label-color="primary"
            class="text-h6"
            :rules="[val => val && val.length > 0 || 'Debe ingresar un nombre']"
          />

          <q-input
            v-model="formulario.dosis"
            outlined
            label="¿Cuánto debe tomar? (Ej: 1 pastilla)"
            type="text"
            lazy-rules
            bg-color="white"
            label-color="primary"
            class="text-h6"
            :rules="[val => val && val.length > 0 || 'Debe especificar la dosis']"
          />

          <q-input
            v-model="formulario.hora_programada"
            outlined
            label="Hora de la toma"
            type="time"
            lazy-rules
            bg-color="white"
            label-color="primary"
            class="text-h6"
            :rules="[val => !!val || 'Debe seleccionar una hora']"
          />

          <q-btn
            type="submit"
            color="primary"
            label="Guardar Alarma"
            icon="save"
            class="full-width q-py-sm text-h6 text-weight-bold q-mt-xl"
            style="border-radius: 12px;"
            :loading="guardando"
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
import { useAlarmasStore } from '../stores/alarmas'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()
const alarmasStore = useAlarmasStore()

const guardando = ref(false)

const formulario = ref({
  nombre_medicamento: '',
  dosis: '',
  hora_programada: ''
})

const guardarAlarma = async () => {
  guardando.value = true
  try {
    // Validamos seguridad para no enviar undefined al backend
    if (!authStore.idPaciente) {
      throw new Error('Su sesión caducó. Por favor inicie sesión nuevamente.')
    }

    // Le agregamos los segundos a la hora porque tu BD PostgreSQL (tipo time) lo requiere
    const payload = {
      ...formulario.value,
      hora_programada: `${formulario.value.hora_programada}:00`
    }

    await alarmasStore.crearAlarma(payload, authStore.idPaciente)

    $q.notify({
      type: 'positive',
      message: 'Remedio programado con éxito',
      position: 'top',
      icon: 'fa-solid fa-check'
    })

    // Devolvemos al usuario a su lista de remedios
    router.push('/alarmas')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'No se pudo guardar la alarma. Intente nuevamente.',
      position: 'top',
      icon: 'fa-solid fa-xmark'
    })
  } finally {
    guardando.value = false
  }
}
</script>