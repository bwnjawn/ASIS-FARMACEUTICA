<template>
  <q-page class="q-pa-md bg-grey-1">
    
    <div class="q-mb-lg">
      <h1 class="text-h4 text-weight-bold q-ma-none text-dark q-mb-md">Cotizar Remedios</h1>
      <q-form @submit.prevent="ejecutarBusqueda">
        <q-input
          v-model="terminoBusqueda"
          outlined
          placeholder="Escriba el nombre del remedio..."
          type="search"
          bg-color="white"
          class="text-h6 shadow-1 rounded-borders"
          :disable="medicamentosStore.cargando"
        >
          <template v-slot:append>
            <q-btn round dense flat icon="search" color="primary" size="lg" @click="ejecutarBusqueda" />
          </template>
        </q-input>
      </q-form>
    </div>

    <q-banner v-if="medicamentosStore.error" class="bg-red-2 text-red-9 rounded-borders text-weight-bold text-subtitle1 q-mb-md">
      <q-icon name="error" size="sm" class="q-mr-xs" />
      {{ medicamentosStore.error }}
    </q-banner>

    <div v-if="medicamentosStore.cargando" class="text-center q-mt-xl">
      <q-spinner-dots color="primary" size="4em" />
      <div class="text-h6 text-grey-8 q-mt-md">Buscando información...</div>
    </div>

    <div v-else-if="medicamentosStore.farmaciasCotizadas.length === 0 && medicamentosStore.resultadosBusqueda.length > 0">
      <div class="text-h6 text-grey-8 q-mb-sm">Seleccione el correcto:</div>
      
      <q-list class="q-gutter-y-sm">
        <q-card 
          v-for="prod in medicamentosStore.resultadosBusqueda" 
          :key="prod.product_id" 
          class="shadow-2 bg-white cursor-pointer" 
          v-ripple 
          @click="seleccionarProducto(prod)"
        >
          <q-card-section class="row items-center">
            <q-icon name="medication" color="primary" size="xl" class="q-mr-md" />
            <div class="col">
              <div class="text-h5 text-weight-bold text-dark">{{ prod.name || prod.text }}</div>
              <div class="text-subtitle1 text-grey-7">{{ prod.active_principle || 'Presentación estándar' }}</div>
            </div>
            <q-icon name="chevron_right" color="grey-5" size="lg" />
          </q-card-section>
        </q-card>
      </q-list>
    </div>

    <div v-else-if="medicamentosStore.farmaciasCotizadas.length > 0">
      <div class="row items-center justify-between q-mb-md">
        <div class="text-h6 text-primary text-weight-bold">Mejores Precios:</div>
        <q-btn flat color="secondary" label="Volver a buscar" icon="arrow_back" @click="medicamentosStore.limpiarBusqueda" />
      </div>

      <q-list class="q-gutter-y-md">
        <q-card 
          v-for="(farmacia, index) in medicamentosStore.farmaciasCotizadas" 
          :key="index"
          class="shadow-2 cursor-pointer"
          v-ripple
          :class="index === 0 ? 'bg-green-1' : 'bg-white'"
          style="border-left: 8px solid var(--q-primary);"
          @click="abrirDetalles(farmacia)"
        >
          <q-card-section>
            <div class="row justify-between items-center">
              <div class="text-h5 text-weight-bold text-dark">
                {{ farmacia.pharmacy_name || farmacia.pharmacy?.name || 'Farmacia' }}
              </div>
              <div class="text-h4 text-weight-bold text-positive">
                ${{ farmacia.total || farmacia.price }}
              </div>
            </div>
            
            <div class="row items-center q-mt-sm text-subtitle1 text-grey-8">
              <q-icon name="place" size="sm" color="negative" class="q-mr-xs" />
              <span>A <strong>{{ farmacia.pharmacy_distance ? farmacia.pharmacy_distance + ' metros' : 'distancia no calculada' }}</strong></span>
            </div>
            <div class="text-subtitle1 text-grey-7 q-ml-md q-mt-xs ellipsis">
              {{ farmacia.pharmacy_address || farmacia.pharmacy?.address || farmacia.address || 'Toque para ver ubicación...' }}
            </div>
          </q-card-section>
        </q-card>
      </q-list>
    </div>

    <div v-else-if="!medicamentosStore.cargando && !medicamentosStore.error && terminoBusqueda === ''" class="text-center q-mt-xl">
      <q-icon name="fa-solid fa-magnifying-glass-dollar" size="4rem" color="grey-4" />
      <p class="text-h6 text-grey-6 q-mt-md">Escriba un medicamento arriba para comparar precios en las farmacias de Puerto Montt.</p>
    </div>

    <q-dialog v-model="modalAbierto">
      <q-card style="width: 100%; max-width: 400px; border-radius: 16px;">
        <q-card-section class="bg-primary text-white row items-center justify-between">
          <div class="text-h6 text-weight-bold">Detalle del Remedio</div>
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-md" v-if="farmaciaSeleccionada">
          
          <div class="text-center q-mb-md">
            <q-icon name="store" size="4rem" color="primary" />
            <div class="text-h5 text-weight-bold text-dark q-mt-sm">
              {{ farmaciaSeleccionada.pharmacy_name || farmaciaSeleccionada.pharmacy?.name || 'Farmacia' }}
            </div>
            <div class="text-h3 text-positive text-weight-bold q-mt-xs">
              ${{ farmaciaSeleccionada.total || farmaciaSeleccionada.price || 0 }}
            </div>
          </div>

          <q-list separator class="q-mt-md">
            
            <q-item>
              <q-item-section avatar>
                <q-icon name="place" color="negative" size="md" />
              </q-item-section>
              <q-item-section>
                <q-item-label caption class="text-subtitle1">Dirección</q-item-label>
                <q-item-label class="text-h6 text-weight-medium">
                  {{ farmaciaSeleccionada.pharmacy_address || farmaciaSeleccionada.pharmacy?.address || farmaciaSeleccionada.address || 'Dirección no especificada' }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item v-if="farmaciaSeleccionada.pharmacy_distance">
              <q-item-section avatar>
                <q-icon name="directions_walk" color="info" size="md" />
              </q-item-section>
              <q-item-section>
                <q-item-label caption class="text-subtitle1">Distancia aproximada</q-item-label>
                <q-item-label class="text-h6 text-weight-medium">{{ farmaciaSeleccionada.pharmacy_distance }} metros</q-item-label>
              </q-item-section>
            </q-item>

            <q-item v-if="farmaciaSeleccionada.format || farmaciaSeleccionada.quantity || farmaciaSeleccionada.description">
              <q-item-section avatar>
                <q-icon name="info" color="grey-7" size="md" />
              </q-item-section>
              <q-item-section>
                <q-item-label caption class="text-subtitle1">Detalles</q-item-label>
                <q-item-label class="text-h6 text-weight-medium">
                  {{ farmaciaSeleccionada.description || '' }} 
                  {{ farmaciaSeleccionada.format || '' }} 
                  {{ farmaciaSeleccionada.quantity || '' }}
                </q-item-label>
              </q-item-section>
            </q-item>

          </q-list>
        </q-card-section>

        <q-card-actions align="center" class="q-pb-md">
          <q-btn label="ENTENDIDO" color="primary" size="lg" style="border-radius: 8px; width: 90%;" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useMedicamentosStore } from '../stores/medicamentos'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const medicamentosStore = useMedicamentosStore()
const terminoBusqueda = ref('')

// Estados para el Modal de detalles
const modalAbierto = ref(false)
const farmaciaSeleccionada = ref(null)

const LAT_PUERTO_MONTT = -41.4693
const LNG_PUERTO_MONTT = -72.9424

const ejecutarBusqueda = async () => {
  if (terminoBusqueda.value.length < 2) return
  await medicamentosStore.buscarMedicamento(terminoBusqueda.value)
}

const seleccionarProducto = (producto) => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      async (posicion) => {
        await medicamentosStore.cotizarMedicamento(
          producto.product_id, 
          posicion.coords.latitude, 
          posicion.coords.longitude
        )
      },
      async (error) => {
        console.warn("No se pudo obtener GPS, usando Puerto Montt central.", error)
        $q.notify({
          message: 'Mostrando farmacias referenciales en Puerto Montt',
          color: 'info',
          icon: 'info',
          position: 'top'
        })
        await medicamentosStore.cotizarMedicamento(producto.product_id, LAT_PUERTO_MONTT, LNG_PUERTO_MONTT)
      },
      { timeout: 5000 }
    )
  } else {
    medicamentosStore.cotizarMedicamento(producto.product_id, LAT_PUERTO_MONTT, LNG_PUERTO_MONTT)
  }
}

// Función para abrir el modal inyectando los datos de la farmacia clickeada
const abrirDetalles = (farmacia) => {
  farmaciaSeleccionada.value = farmacia
  modalAbierto.value = true
}
</script>