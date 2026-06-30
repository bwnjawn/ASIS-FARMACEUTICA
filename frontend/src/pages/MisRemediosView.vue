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
          <div class="row items-center q-px-md">
            <q-icon name="fa-solid fa-check-circle" size="2.5rem" class="q-mr-md" />
            <span class="text-h5 text-weight-bold">¡Dosis Registrada!</span>
          </div>
        </template>

        <q-item class="q-py-lg q-px-md rounded-borders">
          <q-item-section avatar>
            <q-icon 
              :name="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) ? 'fa-solid fa-check-circle' : 'fa-solid fa-pills'" 
              :color="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) ? 'positive' : 'primary'" 
              size="3.5rem" 
            />
          </q-item-section>

          <q-item-section>
            <q-item-label 
              class="text-h5 text-weight-bold"
              :class="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) ? 'text-positive' : 'text-dark'"
            >
              {{ alarma.nombre_medicamento }}
            </q-item-label>
            <q-item-label caption class="text-h6 text-grey-8">{{ alarma.dosis }}</q-item-label>
          </q-item-section>

          <q-item-section side>
            <div class="text-h4 text-weight-bolder" :class="alarmasStore.yaSeTomoHoy(alarma.id_recordatorio) ? 'text-positive' : 'text-primary'">
              {{ alarma.hora_programada ? alarma.hora_programada.substring(0, 5) : '--:--' }}
            </div>
          </q-item-section>
        </q-item>
      </q-slide-item>

    </q-list>

    <q-page-sticky position="bottom-right" :offset="[20, 20]">
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
  // Aquí mantén la ruta que arreglaste y te funcionó en el paso anterior.
  const rutaBackend = `http://127.0.0.1:8000/api/alarmas/${authStore.idPaciente}`
  alarmasStore.cargarAlarmasBackend(authStore.idPaciente, rutaBackend)
})

const onConfirmarToma = async (alarma, eventDetails) => {
  // Comprobamos usando el ID correcto
  if (!alarmasStore.yaSeTomoHoy(alarma.id_recordatorio)) {
    await alarmasStore.marcarComoTomado(alarma)
    
    $q.notify({
      type: 'positive',
      message: '¡Excelente! Remedio marcado como tomado.',
      position: 'top',
      icon: 'fa-solid fa-check'
    })
  }

  // Esto hace que la tarjeta se cierre sola tras 800 milisegundos para que 
  // el usuario alcance a leer "¡Dosis Registrada!" y luego vea el fondo verde.
  setTimeout(() => {
    eventDetails.reset()
  }, 800)
}

const abrirModalNuevaAlarma = () => {
  router.push('/nueva-alarma')
}
</script>