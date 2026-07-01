<template>
  <q-page class="q-pa-md bg-grey-1">
    
    <!-- ENCABEZADO SUPERIOR OPTIMIZADO -->
    <div class="row items-center no-wrap q-mb-md q-pt-xs">
      <div class="col-auto">
        <q-btn 
          flat 
          round 
          icon="chevron_left" 
          color="dark" 
          class="bg-white shadow-1" 
          size="md"
          @click="router.push('/alarmas')" 
        />
      </div>
      <div class="col q-pl-sm row items-center no-wrap">
        <h1 class="text-h5 text-weight-bold text-dark q-my-none q-mr-sm">
          Nueva Alarma
        </h1>
        <!-- Icono de alarma naranja al costado derecho -->
        <q-icon name="notifications_active" color="orange-9" size="xl" />
      </div>
    </div>

    <!-- TARJETA FORMULARIO PRINCIPAL REESTRUCTURADA -->
    <q-card class="q-pa-md shadow-2 bg-white" style="border-radius: 20px;">
      <q-card-section class="q-pa-none">
        <q-form @submit.prevent="guardarAlarma" class="q-gutter-y-sm">
          
          <!-- CAMPO: NOMBRE DEL MEDICAMENTO -->
          <div>
            <div class="text-subtitle1 text-weight-bold q-mb-xs field-label">
              Nombre del medicamento
            </div>
            <q-input
              v-model="formulario.nombre_medicamento"
              outlined
              placeholder="Ej: Enalapril, Metformina"
              type="text"
              lazy-rules
              class="input-text-fino custom-input"
              :rules="[val => val && val.length > 0 || 'Debe ingresar un nombre']"
              hide-bottom-space
            />
          </div>

          <!-- CAMPO: DOSIS -->
          <div>
            <div class="text-subtitle1 text-weight-bold q-mb-xs field-label">
              Dosis
            </div>
            <q-input
              v-model="formulario.dosis"
              outlined
              placeholder="Ej: 10 mg — 1 comprimido"
              type="text"
              lazy-rules
              class="input-text-fino custom-input"
              :rules="[val => val && val.length > 0 || 'Debe especificar la dosis']"
              hide-bottom-space
            />
          </div>

          <!-- CAMPO: HORA DE LA ALARMA -->
          <div>
            <div class="text-subtitle1 text-weight-bold q-mb-xs field-label">
              Hora de la alarma
            </div>
            <q-input
              v-model="formulario.hora_programada"
              outlined
              type="time"
              lazy-rules
              class="input-text-fino custom-input"
              :rules="[val => !!val || 'Debe seleccionar una hora']"
              hide-bottom-space
            />
          </div>

          <!-- BOTÓN VERDE FINAL -->
          <q-btn
            type="submit"
            color="positive"
            text-color="white"
            icon="add"
            label="AÑADIR ALARMA"
            class="full-width q-py-sm text-subtitle1 text-weight-bold q-mt-md"
            style="border-radius: 16px; min-height: 48px;"
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
    if (!authStore.idPaciente) {
      throw new Error('Su sesión caducó. Por favor inicie sesión nuevamente.')
    }

    const payload = {
      ...formulario.value,
      hora_programada: `${formulario.value.hora_programada}:00`
    }

    await alarmasStore.crearAlarma(payload, authStore.idPaciente)

    $q.notify({
      type: 'positive',
      message: 'Remedio programado con éxito',
      position: 'top',
      icon: 'check'
    })

    router.push('/alarmas')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'No se pudo guardar la alarma. Intente nuevamente.',
      position: 'top',
      icon: 'close'
    })
  } finally {
    guardando.value = false
  }
}
</script>

<style scoped>
.field-label {
  color: #0b2240;
}

/* Letra más fina y tamaño adecuado para el texto que se escribe */
.input-text-fino :deep(input) {
  font-size: 1.1rem !important;
  font-weight: 400 !important;
  color: #2d3748 !important;
}

/* Redondear y suavizar las cajas de entrada de Quasar */
:deep(.custom-input .q-field__control) {
  border-radius: 14px !important;
  background-color: #f8fafc !important;
  height: 52px !important;
}

:deep(.custom-input .q-field__outline) {
  border-radius: 14px !important;
}

:deep(.custom-input .q-field__outline__start),
:deep(.custom-input .q-field__outline__notch),
:deep(.custom-input .q-field__outline__end) {
  border-color: #e2e8f0 !important;
}
</style>