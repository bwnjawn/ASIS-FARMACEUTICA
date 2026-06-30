<template>
  <q-page class="q-pa-md">
    
    <div class="text-center q-mb-xl">
      <h2 class="text-h4 text-weight-bold text-dark q-mt-none q-mb-sm">Mis Remedios</h2>
      <p class="text-grey-8 text-h6">Desliza a la <b>derecha</b> para tomar. Desliza a la <b>izquierda</b> para borrar.</p>
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
        @left="onEliminarAlarma(alarma, $event)"
        right-color="positive"
        left-color="negative"
        class="rounded-borders shadow-2"
        :class="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) ? 'bg-green-1' : 'bg-white'"
      >
        <!-- Acción de Tomar (Derecha) -->
        <template v-slot:right>
          <div class="row items-center q-px-md text-h6">
            <q-icon name="check_circle" size="md" class="q-mr-sm" /> ¡Tomado!
          </div>
        </template>

        <!-- Acción de Eliminar (Izquierda) -->
        <template v-slot:left>
          <div class="row items-center q-px-md text-h6">
            <q-icon name="delete" size="md" class="q-mr-sm" /> Borrar
          </div>
        </template>

        <q-item class="q-pa-md bg-transparent">
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

          <!-- Botón de Edición -->
          <q-item-section side>
            <q-btn 
              v-if="!alarmasStore.yaSeTomoHoy(alarma.id_recordatorio)"
              flat 
              round 
              icon="edit" 
              color="primary" 
              size="lg"
              @click.stop="abrirModalEdicion(alarma)" 
            />
            <q-icon v-else name="task_alt" color="positive" size="xl" />
          </q-item-section>
        </q-item>
      </q-slide-item>
    </q-list>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="fa-solid fa-plus" color="primary" size="xl" @click="abrirModalNuevaAlarma" />
    </q-page-sticky>

    <!-- Modal de Edición de Alarma -->
    <q-dialog v-model="mostrarModalEdicion" persistent transition-show="scale" transition-hide="scale">
      <q-card style="width: 90vw; max-width: 400px; border-radius: 12px;">
        <q-card-section class="bg-primary text-white">
          <div class="text-h5 text-weight-bold">Editar Medicamento</div>
        </q-card-section>

        <q-card-section class="q-pt-lg">
          <q-input 
            v-model="alarmaEditada.nombre_medicamento" 
            label="¿Qué remedio es?" 
            outlined 
            class="q-mb-md text-h6" 
          />
          <q-input 
            v-model="alarmaEditada.dosis" 
            label="¿Cuánto debe tomar?" 
            outlined 
            class="q-mb-md text-h6" 
          />
          <q-input 
            v-model="alarmaEditada.hora_programada" 
            label="Hora de la alarma" 
            type="time" 
            outlined 
            class="text-h6"
          />
        </q-card-section>

        <q-card-actions align="center" class="q-pa-md">
          <q-btn label="Cancelar" color="negative" flat size="lg" v-close-popup class="q-mr-sm text-weight-bold" />
          <q-btn label="Guardar" color="primary" @click="guardarEdicion" size="lg" class="text-weight-bold" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'
import { useAlarmasStore } from '../stores/alarmas'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()
const alarmasStore = useAlarmasStore()

// Variables para el modal de edición
const mostrarModalEdicion = ref(false)
const alarmaEditada = ref({ id_recordatorio: null, nombre_medicamento: '', dosis: '', hora_programada: '' })

onMounted(() => {
  if (authStore.idPaciente && authStore.idPaciente !== 'undefined') {
    const rutaBackend = `http://127.0.0.1:8000/api/alarmas/${authStore.idPaciente}`
    alarmasStore.cargarAlarmasBackend(authStore.idPaciente, rutaBackend)
  } else {
    router.push('/')
  }
})

const onConfirmarToma = async (alarma, details) => {
  if (!alarmasStore.yaSeTomoHoy(alarma.id_recordatorio)) {
    await alarmasStore.marcarComoTomado(alarma)
    $q.notify({ type: 'positive', message: '¡Excelente! Has registrado tu toma.', position: 'top' })
  } else {
    $q.notify({ type: 'warning', message: 'Ya registraste este medicamento hoy.', position: 'top' })
  }
  if (details && typeof details.reset === 'function') details.reset()
}

// Nueva función de eliminación
const onEliminarAlarma = (alarma, details) => {
  $q.dialog({
    title: '<span class="text-weight-bold text-negative">¿Eliminar Remedio?</span>',
    message: `¿Estás seguro de que quieres quitar <b>${alarma.nombre_medicamento}</b> de tus recordatorios?`,
    html: true, // Permite usar etiquetas HTML para mejorar la legibilidad para adultos mayores
    cancel: {
      label: 'Cancelar',
      color: 'dark',
      flat: true
    },
    ok: {
      label: 'Sí, Borrar',
      color: 'negative',
      unelevated: true
    },
    persistent: true
  }).onOk(async () => {
    // Si presiona confirmar, ejecuta la acción
    await alarmasStore.eliminarAlarma(alarma.id_recordatorio)
    $q.notify({ 
      type: 'negative', 
      message: 'Alarma eliminada correctamente', 
      position: 'top' 
    })
  }).onCancel(() => {
    // Si cancela, regresamos el slide a su posición original
    if (details && typeof details.reset === 'function') {
      details.reset()
    }
  }).onDismiss(() => {
    // Asegurar el reset del componente en cualquier cierre del diálogo
    if (details && typeof details.reset === 'function') {
      details.reset()
    }
  })
}

// Funciones de Edición
const abrirModalEdicion = (alarma) => {
  alarmaEditada.value = { 
    id_recordatorio: alarma.id_recordatorio, 
    nombre_medicamento: alarma.nombre_medicamento, 
    dosis: alarma.dosis, 
    hora_programada: alarma.hora_programada.substring(0, 5) // Convertir "08:00:00" a "08:00" para el input
  }
  mostrarModalEdicion.value = true
}

const guardarEdicion = async () => {
  const { id_recordatorio, nombre_medicamento, dosis, hora_programada } = alarmaEditada.value
  
  // Agregar los segundos para cumplir con el formato de base de datos de PostgreSQL
  const horaConSegundos = `${hora_programada}:00`

  await alarmasStore.actualizarAlarma(id_recordatorio, {
    nombre_medicamento,
    dosis,
    hora_programada: horaConSegundos
  })
  
  mostrarModalEdicion.value = false
  $q.notify({ type: 'positive', message: 'Alarma actualizada', position: 'top' })
}

const abrirModalNuevaAlarma = () => {
  router.push('/nueva-alarma') 
}
</script>