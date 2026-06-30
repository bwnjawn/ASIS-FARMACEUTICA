<template>
  <q-page class="q-pa-md">
    
    <div class="text-center q-mb-xl">
      <h2 class="text-h4 text-weight-bold text-dark q-mt-none q-mb-sm">Mis Remedios</h2>
      <p class="text-grey-8 text-h6">Desliza la tarjeta hacia la derecha cuando te tomes tu medicina.</p>
    </div>

    <div v-if="alarmasStore.listaAlarmas.length === 0" class="text-center q-mt-xl">
      <q-icon name="fa-solid fa-notes-medical" size="4rem" color="grey-4" />
      <p class="text-h6 text-grey-6 q-mt-md">Aún no tienes remedios registrados.</p>
    </div>

    <q-list class="q-gutter-y-lg">
      <q-slide-item
        v-for="alarma in alarmasStore.listaAlarmas"
        :key="alarma.id_recordatorio"
        @right="onConfirmarToma(alarma, $event)"
        right-color="positive"
        class="rounded-borders shadow-2"
        :class="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) ? 'bg-green-1' : 'bg-white'"
      >
        <template v-slot:right>
          <div class="row items-center q-px-md text-h6">
            <q-icon name="check_circle" size="md" class="q-mr-sm" /> ¡Tomado!
          </div>
        </template>

        <q-item class="q-pa-md">
          <q-item-section avatar>
            <q-icon name="schedule" size="lg" color="primary" />
            <div class="text-weight-bold text-center q-mt-xs">{{ alarma.hora_programada.substring(0, 5) }}</div>
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-h5 text-weight-bold">{{ alarma.nombre_medicamento }}</q-item-label>
            <q-item-label caption class="text-subtitle1 text-grey-8">
              Tomar: <strong>{{ alarma.dosis }}</strong>
            </q-item-label>
          </q-item-section>

          <q-item-section side v-if="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio)">
            <q-icon name="task_alt" color="positive" size="xl" />
          </q-item-section>
        </q-item>
      </q-slide-item>
    </q-list>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn 
        fab 
        icon="fa-solid fa-plus" 
        color="primary" 
        size="xl" 
        @click="abrirModalNuevaAlarma" 
      />
    </q-page-sticky>

  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'
import { useAlarmasStore } from '../stores/alarmas'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()
const alarmasStore = useAlarmasStore()

onMounted(() => {
  // Validación de seguridad para evitar peticiones mal formadas
  if (authStore.idPaciente && authStore.idPaciente !== 'undefined') {
    const rutaBackend = `http://127.0.0.1:8000/api/alarmas/${authStore.idPaciente}`
    alarmasStore.cargarAlarmasBackend(authStore.idPaciente, rutaBackend)
  } else {
    console.warn("⚠️ No se detectó un ID de paciente válido. Redirigiendo al login.")
    router.push('/')
  }
})

const onConfirmarToma = async (alarma, details) => {
  if (!alarmasStore.yaSeTomoHoy(alarma.id_recordatorio)) {
    await alarmasStore.marcarComoTomado(alarma)
    
    $q.notify({
      type: 'positive',
      message: '¡Excelente! Has registrado tu toma.',
      position: 'top'
    })
  } else {
    $q.notify({
      type: 'warning',
      message: 'Ya registraste este medicamento hoy.',
      position: 'top'
    })
  }
  // Restablece visualmente el slide item después del deslizamiento
  if (details && typeof details.reset === 'function') {
    details.reset()
  }
}

const abrirModalNuevaAlarma = () => {
  router.push('/nueva-alarma') // O abre un modal si lo cambiaste a diálogo
}
</script>