<template>
  <q-page class="q-pa-md q-pb-xl">
    
    <!-- NUEVO ENCABEZADO ESTILO IMAGE_C76305.PNG -->
    <div class="row items-center no-wrap q-mb-lg q-pt-sm">
 
      
      <!-- Título y Fecha Central -->
      <div class="col q-px-md">
        <h1 class="text-h4 text-weight-bold text-dark q-my-none font-custom" style="line-height: 1.2;">
          Mis Alarmas<br>Diarias
        </h1>
        <div class="text-subtitle1 text-grey-7 text-weight-medium q-mt-xs">
          {{ fechaActual }}
        </div>
      </div>
    </div>

    <!-- TARJETA DE INSTRUCCIONES ESTILO BEIGE / NARANJA -->
    <q-card flat class="bg-orange-1 q-pa-md q-mb-lg" style="border: 1.5px solid #ffb74d; border-radius: 16px;">
      <div class="row items-center no-wrap">
        
        <div class="text-subtitle1 text-dark" style="line-height: 1.4;">
          <q-icon name="info" color="orange-9" size="md" class="q-mr-md" />
          Desliza la tarjeta a la <span class="text-weight-bold text-orange-9">DERECHA</span> para registrar tu toma.<br>
          
          <q-icon name="info" color="orange-9" size="md" class="q-mr-md" />
          Desliza a la <span class="text-weight-bold text-orange-9">IZQUIERDA</span> si necesitas borrarla.
        </div>
      </div>
    </q-card>

    <!-- LISTADO DE REMEDIOS -->
    <div v-if="alarmasStore.listaAlarmas.length === 0" class="text-center q-mt-xl">
      <q-icon name="fa-solid fa-notes-medical" size="4rem" color="grey-4" />
      <p class="text-h6 text-grey-6 q-mt-md">Aún no tienes remedios registrados.</p>
    </div>

    <q-list class="q-gutter-y-md q-mb-xl">
      <q-slide-item
        v-for="alarma in alarmasStore.listaAlarmas"
        :key="alarma.id_recordatorio"
        @right="onConfirmarToma(alarma, $event)"
        @left="onEliminarAlarmaCard(alarma, $event)"
        right-color="positive"
        left-color="negative"
        class="remedio-card bg-white"
        :class="{ 'border-tomado': alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) }"
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

        <!-- Contenido de la Tarjeta -->
        <q-item class="q-pa-md bg-transparent row items-center no-wrap">
          
          <!-- Icono Izquierdo de Estado -->
          <div class="col-auto q-pr-md">
            <q-icon 
              v-if="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio)" 
              name="check_circle" 
              color="positive" 
              size="42px" 
            />
            <q-icon 
              v-else 
              name="radio_button_unchecked" 
              color="primary" 
              size="42px" 
            />
          </div>

          <!-- Bloque de Información Principal -->
          <div class="col text-left">
            <!-- Nombre del Medicamento: Ocupa toda la parte superior libremente -->
            <div 
              class="text-h5 text-weight-bold text-dark q-mb-xs" 
              :class="{ 'text-strike text-grey-6': alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) }"
              style="word-break: break-word; line-height: 1.2;"
            >
              {{ alarma.nombre_medicamento }}
            </div>
            
            <!-- Etiqueta de Estado Tomado -->
            <div v-if="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio)" class="text-positive text-weight-bold q-mb-xs" style="font-size: 1rem;">
              Tomado <q-icon name="check" size="xs"/>
            </div>

            <!-- Fila Inferior: Hora, Dosis y el Botón de Editar alineados juntos -->
            <div class="row items-center justify-between no-wrap q-mt-xs full-width">
              <div class="row items-center q-gutter-x-md">
                <!-- Hora Destacada -->
                <div class="row items-center text-subtitle1 text-weight-bold text-dark bg-grey-2 q-px-sm q-py-xs" style="border-radius: 8px;">
                  <q-icon name="schedule" class="q-mr-xs" size="18px" />
                  {{ alarma.hora_programada.substring(0, 5) }}
                </div>
                
                <!-- Dosis -->
                <div class="text-subtitle1 text-grey-8">
                  {{ alarma.dosis }}
                </div>
              </div>

              <!-- Botón Editar: Movido abajo a la derecha de la hora y más pequeño -->
              <div class="col-auto">
                <q-btn 
                  flat 
                  round 
                  icon="edit" 
                  color="grey-7" 
                  class="bg-grey-2"
                  size="10px"
                  dense
                  @click.stop="abrirModalEdicion(alarma)" 
                />
              </div>
            </div>
          </div>

        </q-item>
      </q-slide-item>
    </q-list>

    <!-- Botón Inferior Ancho -->
    <q-page-sticky position="bottom" :offset="[0, 16]">
      <q-btn 
        color="primary" 
        text-color="white"
        icon="add" 
        label="AÑADIR NUEVA ALARMA" 
        class="text-h6 text-weight-bold shadow-4 q-py-sm"
        style="width: 90vw; max-width: 400px; border-radius: 30px;"
        @click="abrirModalNuevaAlarma" 
      />
    </q-page-sticky>

    <!-- Modal de Edición de Alarma -->
    <q-dialog v-model="mostrarModalEdicion" persistent transition-show="scale" transition-hide="scale">
      <q-card style="width: 85vw; max-width: 380px; border-radius: 20px;">
        <!-- Encabezado del modal alineado con tu paleta -->
        <q-card-section class="bg-primary text-white q-py-md">
          <div class="text-h5 text-weight-bold">Editar Medicamento</div>
        </q-card-section>

        <q-card-section class="q-pa-md q-gutter-y-sm">
          <!-- Campo Medicamento -->
          <div>
            <div class="text-subtitle2 text-weight-bold text-dark q-mb-xs">¿Qué remedio es?</div>
            <q-input 
              v-model="alarmaEditada.nombre_medicamento" 
              outlined 
              class="input-text-fino custom-modal-input" 
              dense
            />
          </div>

          <!-- Campo Dosis -->
          <div>
            <div class="text-subtitle2 text-weight-bold text-dark q-mb-xs">¿Cuánto debe tomar?</div>
            <q-input 
              v-model="alarmaEditada.dosis" 
              outlined 
              class="input-text-fino custom-modal-input" 
              dense
            />
          </div>

          <!-- Campo Hora -->
          <div>
            <div class="text-subtitle2 text-weight-bold text-dark q-mb-xs">Hora de la alarma</div>
            <q-input 
              v-model="alarmaEditada.hora_programada" 
              type="time" 
              outlined 
              class="input-text-fino custom-modal-input"
              dense
            />
          </div>
        </q-card-section>

        <!-- Botones de Acción Estilizados -->
        <q-card-actions align="center" class="q-pb-md q-px-md row no-wrap justify-center q-gutter-x-sm">
          <q-btn 
            label="CANCELAR" 
            color="negative" 
            flat 
            size="md" 
            v-close-popup 
            class="text-weight-bold text-uppercase" 
            style="min-width: 120px;"
          />
          <q-btn 
            label="GUARDAR" 
            color="primary" 
            @click="guardarEdicion" 
            size="md" 
            class="text-weight-bold text-uppercase" 
            style="border-radius: 12px; min-width: 120px; min-height: 40px;" 
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'
import { useAlarmasStore } from '../stores/alarmas'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()
const alarmasStore = useAlarmasStore()

const mostrarModalEdicion = ref(false)
const alarmaEditada = ref({ id_recordatorio: null, nombre_medicamento: '', dosis: '', hora_programada: '' })

// Fecha dinámica con formato en español: "Día de la semana, DD de Mes"
const fechaActual = computed(() => {
  const opciones = { weekday: 'long', day: 'numeric', month: 'long' }
  const fecha = new Date().toLocaleDateString('es-CL', opciones)
  // Capitalizar la primera letra
  return fecha.charAt(0).toUpperCase() + fecha.slice(1)
})

onMounted(() => {
  if (authStore.idPaciente && authStore.idPaciente !== 'undefined') {
    const rutaBackend = `https://tu-url-de-render.com/api/alarmas/${authStore.idPaciente}`
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

const onEliminarAlarmaCard = (alarma, details) => {
  $q.dialog({
    title: '<span class="text-weight-bold text-negative">¿Eliminar Remedio?</span>',
    message: `¿Estás seguro de que quieres quitar <b>${alarma.nombre_medicamento}</b> de tus recordatorios?`,
    html: true,
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
    await alarmasStore.eliminarAlarma(alarma.id_recordatorio)
    $q.notify({ 
      type: 'negative', 
      message: 'Alarma eliminada correctamente', 
      position: 'top' 
    })
  }).onCancel(() => {
    if (details && typeof details.reset === 'function') details.reset()
  }).onDismiss(() => {
    if (details && typeof details.reset === 'function') details.reset()
  })
}

const abrirModalEdicion = (alarma) => {
  alarmaEditada.value = { 
    id_recordatorio: alarma.id_recordatorio, 
    nombre_medicamento: alarma.nombre_medicamento, 
    dosis: alarma.dosis, 
    hora_programada: alarma.hora_programada.substring(0, 5)
  }
  mostrarModalEdicion.value = true
}

const guardarEdicion = async () => {
  const { id_recordatorio, nombre_medicamento, dosis, hora_programada } = alarmaEditada.value
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

<style scoped>
.font-custom {
  color: #1a2530; /* Color oscuro similar al de la imagen */
}

.remedio-card {
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.border-tomado {
  border-color: #4caf50;
  background-color: #f1f8e9 !important;
}
</style>