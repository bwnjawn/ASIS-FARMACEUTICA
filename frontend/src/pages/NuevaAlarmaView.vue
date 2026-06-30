<template>
  <q-page class="q-pa-md">
    
    <div class="row items-center q-mb-xl">
      <q-btn 
        flat 
        round 
        icon="fa-solid fa-arrow-left" 
        color="primary" 
        size="lg" 
        @click="$router.back()" 
      />
      <h2 class="text-h4 text-weight-bold text-dark q-ml-sm q-my-none">Nuevo Remedio</h2>
    </div>

    <q-form @submit.prevent="guardarAlarma" class="q-gutter-y-lg">
      
      <q-input
        v-model="formulario.nombre_medicamento"
        outlined
        label="¿Qué remedio es?"
        placeholder="Ej: Paracetamol"
        bg-color="white"
        label-color="primary"
        class="text-h6"
        :disable="cargando"
        :rules="[val => !!val || 'Debes escribir un nombre']"
      >
        <template v-slot:prepend>
          <q-icon name="fa-solid fa-pills" color="primary" />
        </template>
      </q-input>

      <q-input
        v-model="formulario.dosis"
        outlined
        label="¿Cuánto debes tomar?"
        placeholder="Ej: 1 pastilla"
        bg-color="white"
        label-color="primary"
        class="text-h6"
        :disable="cargando"
        :rules="[val => !!val || 'Debes escribir la cantidad']"
      >
        <template v-slot:prepend>
          <q-icon name="fa-solid fa-spoon" color="primary" />
        </template>
      </q-input>

      <q-input
        v-model="formulario.hora_programada"
        outlined
        type="time"
        label="¿A qué hora?"
        bg-color="white"
        label-color="primary"
        class="text-h6"
        :disable="cargando"
        :rules="[val => !!val || 'Debes elegir una hora']"
      >
        <template v-slot:prepend>
          <q-icon name="fa-solid fa-clock" color="primary" />
        </template>
      </q-input>

      <q-btn
        label="Guardar Remedio"
        type="submit"
        color="positive" 
        size="xl"
        class="full-width text-weight-bold q-py-sm q-mt-xl"
        rounded
        unelevated
        :loading="cargando"
      />
      
    </q-form>

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

const cargando = ref(false)

const formulario = ref({
  nombre_medicamento: '',
  dosis: '',
  hora_programada: ''
})

const guardarAlarma = async () => {
  cargando.value = true

  try {
    // 1. Armamos los datos tal como los pide tu modelo en FastAPI
    const payload = {
      nombre_medicamento: formulario.value.nombre_medicamento,
      dosis: formulario.value.dosis,
      // FastAPI espera formato de tiempo completo. El input type="time" da "HH:MM", le sumamos los segundos.
      hora_programada: formulario.value.hora_programada + ":00", 
      activo: true,
      // 2. Extraemos el ID del paciente que Pinia guardó al hacer Login
      id_paciente: authStore.idPaciente
    }
    console.log("Datos a enviar a FastAPI:", payload)

    // 3. Enviamos la petición a tu Backend
    const respuesta = await fetch('http://127.0.0.1:8000/api/alarmas/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!respuesta.ok) {
      throw new Error('Fallo en el servidor al guardar la alarma')
    }

    $q.notify({
      type: 'positive',
      message: '¡Remedio guardado con éxito!',
      position: 'top',
      icon: 'fa-solid fa-check'
    })

    // 4. Lo devolvemos a la lista de remedios
    router.back()

  } catch (err) {
    console.error("Error guardando alarma:", err)
    $q.notify({
      type: 'negative',
      message: 'Hubo un problema al guardar. Intenta de nuevo.',
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