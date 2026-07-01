<template>
  <q-page class="q-pa-md bg-grey-1">
    
    <!-- Pestañas para simular ambos roles rápidamente en la presentación -->
    <q-tabs
      v-model="tab"
      dense
      class="text-grey-7 bg-white shadow-1 rounded-borders q-mb-md"
      active-color="primary"
      indicator-color="primary"
      align="justify"
      narrow-indicator
    >
      <q-tab name="paciente" icon="person" label="Mi Perfil" />
      <q-tab name="cuidador" icon="health_and_safety" label="Portal Cuidador" />
    </q-tabs>

    <q-tab-panels v-model="tab" animated class="bg-transparent">
      
      <!-- ================================ -->
      <!-- FLUJO DEL PACIENTE (MI PERFIL)   -->
      <!-- ================================ -->
      <q-tab-panel name="paciente" class="q-pa-none">
        <q-card class="shadow-2 bg-white text-center q-pa-lg" style="border-radius: 20px;">
          
          <div class="row justify-end q-mb-none">
            <q-btn 
              flat 
              round 
              icon="edit" 
              color="grey-7" 
              class="bg-grey-2" 
              size="sm" 
              @click="abrirModalPerfil"
            />
          </div>

          <q-icon name="account_circle" size="90px" color="primary" class="q-mb-sm" />
          
          <!-- Datos Dinámicos enlazados a AuthStore / Editables localmente -->
          <div class="text-h4 text-weight-bold text-dark q-mb-xs">{{ nombreVisual }}</div>
          <div class="text-h6 text-grey-8 q-mb-lg">RUT: {{ rutVisual }}</div>

          <q-separator class="q-my-md" />

          <div class="text-h6 text-weight-bold text-dark q-mb-md" style="line-height: 1.2;">
            ¿Un familiar te ayuda con tus remedios?
          </div>

          <!-- Botón Generar Código -->
          <q-btn 
            v-if="!codigoGenerado"
            color="positive" 
            label="Vincular Cuidador" 
            icon="link"
            size="lg"
            class="full-width text-weight-bold q-py-sm"
            style="border-radius: 14px;"
            @click="generarCodigo"
          />

          <!-- Caja del Código -->
          <div v-else class="q-mt-md">
            <div class="text-subtitle1 text-grey-8 q-mb-sm">Dicta este código a tu cuidador:</div>
            <div class="bg-orange-1 q-py-md q-px-sm shadow-1 contenedor-codigo">
              <div class="text-h3 text-weight-bolder text-orange-9 texto-codigo">
                {{ codigoGenerado }}
              </div>
            </div>
          </div>

          <!-- Botón de Salir -->
          <q-btn 
            flat
            color="negative" 
            label="Salir de la cuenta" 
            icon="logout"
            class="full-width text-weight-bold q-mt-xl"
            @click="salirCuenta"
          />

        </q-card>
      </q-tab-panel>

      <!-- ================================ -->
      <!-- FLUJO DEL CUIDADOR (SIMULACIÓN)  -->
      <!-- ================================ -->
      <q-tab-panel name="cuidador" class="q-pa-none">
        <q-card class="shadow-2 bg-white q-pa-lg" style="border-radius: 20px;">
          
          <div class="text-center q-mb-lg">
            <q-icon name="supervisor_account" size="80px" color="orange-5" class="q-mb-sm" />
            <h2 class="text-h4 text-weight-bold text-dark q-ma-none">Portal Cuidador</h2>
            <p class="text-subtitle1 text-grey-7 q-mt-sm">Supervisa las tomas de tu familiar a distancia.</p>
          </div>

          <!-- Input Código -->
          <div class="q-mb-lg">
            <div class="text-subtitle1 text-weight-bold text-dark q-mb-xs">
              Código de Vinculación
            </div>
            <q-input 
              v-model="codigoIngreso" 
              outlined 
              placeholder="Ej: 123456" 
              mask="######" 
              class="text-h5 bg-grey-2" 
              input-class="text-center text-weight-bold tracking-widest"
              style="border-radius: 14px;"
            />
          </div>

          <!-- Botón Vincular -->
          <q-btn 
            color="primary" 
            label="Vincular Paciente" 
            size="lg"
            class="full-width text-weight-bold q-py-sm"
            style="border-radius: 14px;"
            :disable="codigoIngreso.length !== 6"
            @click="simularVinculacion"
          />
        </q-card>
      </q-tab-panel>

    </q-tab-panels>

    <!-- MODAL PARA EDICIÓN VISUAL TEMPORAL -->
    <q-dialog v-model="modalPerfilOpen" persistent>
      <q-card style="width: 85vw; max-width: 380px; border-radius: 16px;">
        <q-card-section class="bg-primary text-white q-py-md">
          <div class="text-h6 text-weight-bold">Editar Datos de Pantalla</div>
        </q-card-section>

        <q-card-section class="q-pa-md q-gutter-y-sm">
          <div>
            <div class="text-subtitle2 text-weight-bold text-dark q-mb-xs">Nombre Completo</div>
            <q-input v-model="editNombre" outlined dense class="input-text-fino" />
          </div>
          <div>
            <div class="text-subtitle2 text-weight-bold text-dark q-mb-xs">RUT</div>
            <q-input v-model="editRut" outlined dense mask="########-X" class="input-text-fino" />
          </div>
        </q-card-section>

        <q-card-actions align="center" class="q-pb-md">
          <q-btn label="CANCELAR" color="negative" flat v-close-popup />
          <q-btn label="ACEPTAR" color="primary" @click="guardarCambiosVisuales" class="text-weight-bold" style="border-radius: 8px;" />
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

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const tab = ref('paciente')

// Variables que alimentan el HTML
const nombreVisual = ref('')
const rutVisual = ref('')

// Al montar la pantalla, sacamos los datos limpios de la store
onMounted(() => {
  let nombreReal = authStore.nombreUsuario
  let rutReal = authStore.rut

  // Filtro de seguridad por si queda caché basura ("undefined")
  if (!nombreReal || nombreReal === 'undefined') nombreReal = 'Benjamín Ojeda'
  if (!rutReal || rutReal === 'undefined') rutReal = '21526999-K'

  nombreVisual.value = nombreReal
  rutVisual.value = rutReal
})

// Variables para el modal
const modalPerfilOpen = ref(false)
const editNombre = ref('')
const editRut = ref('')

const abrirModalPerfil = () => {
  editNombre.value = nombreVisual.value
  editRut.value = rutVisual.value
  modalPerfilOpen.value = true
}

const guardarCambiosVisuales = () => {
  nombreVisual.value = editNombre.value
  rutVisual.value = editRut.value
  
  // También los guardamos en memoria local por si navegas a otra vista
  authStore.nombreUsuario = editNombre.value
  authStore.rut = editRut.value
  localStorage.setItem('nombre_usuario', editNombre.value)
  localStorage.setItem('rut', editRut.value)
  
  modalPerfilOpen.value = false
  $q.notify({ type: 'positive', message: 'Datos actualizados visualmente', position: 'top', timeout: 1000 })
}

const salirCuenta = () => {
  localStorage.clear()
  authStore.idPaciente = null
  authStore.token = null
  authStore.nombreUsuario = ''
  authStore.rut = ''
  router.push('/')
}

const codigoGenerado = ref(null)
const generarCodigo = () => {
  codigoGenerado.value = Math.floor(100000 + Math.random() * 900000)
}

const codigoIngreso = ref('')
const simularVinculacion = () => {
  $q.loading.show({ message: 'Validando código en la base de datos...', boxClass: 'bg-grey-2 text-grey-9', spinnerColor: 'primary' })
  setTimeout(() => {
    $q.loading.hide()
    $q.notify({ type: 'positive', message: 'Paciente vinculado con éxito.', position: 'top', icon: 'check_circle', color: 'positive' })
    codigoIngreso.value = ''
    codigoGenerado.value = null
    tab.value = 'paciente'
  }, 1500)
}
</script>

<style scoped>
.contenedor-codigo {
  border: 2px dashed #f57c00; 
  border-radius: 16px;
  max-width: 100%;
  box-sizing: border-box;
}

.texto-codigo {
  letter-spacing: 4px !important;
  font-size: 2.25rem !important;
  line-height: 1 !important;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tracking-widest {
  letter-spacing: 6px !important;
}

.input-text-fino :deep(input) {
  font-size: 1rem !important;
  font-weight: 400 !important;
}

:deep(.q-field__control) {
  border-radius: 12px !important;
}
</style>