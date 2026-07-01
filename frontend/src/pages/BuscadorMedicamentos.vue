<template>
  <q-page class="q-pa-md bg-grey-1">
    
    <!-- TITULO DE LA VISTA -->
    <div class="q-mb-md q-pt-xs">
      <h1 class="text-h4 text-weight-bold q-ma-none text-dark q-mb-xs">Cotizar Remedios</h1>
      
      <!-- BUSCADOR -->
      <q-select
        v-model="medicamentoSeleccionado"
        use-input
        hide-selected
        fill-input
        input-debounce="600"
        :options="opcionesBusqueda"
        option-value="product_id"
        option-label="product_name" 
        placeholder="Ej: Paracetamol..."
        outlined
        menu-anchor="bottom left"
        menu-self="top left"
        class="input-text-fino custom-search shadow-1"
        @filter="filtrarMedicamentos"
        @update:model-value="alSeleccionarMedicamento"
      >
        <template v-slot:append>
          <q-icon name="search" color="primary" />
        </template>
        
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey text-subtitle1 text-center q-pa-md">
              No se encontraron resultados para esa búsqueda.
            </q-item-section>
          </q-item>
        </template>
        
        <template v-slot:option="scope">
          <q-item v-bind="scope.itemProps" class="q-pa-md" style="border-bottom: 1px solid #f1f5f9;">
            <q-item-section avatar>
              <q-avatar square size="50px" style="border-radius: 8px;">
                <img :src="scope.opt.product_logo || 'https://via.placeholder.com/50?text=Rx'">
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-subtitle1 text-weight-bold text-dark" style="line-height: 1.2;">
                {{ scope.opt.product_name }}
              </q-item-label>
              <q-item-label caption class="text-body2 text-grey-7 q-mt-xs" v-if="scope.opt.formula_name">
                Componente: {{ scope.opt.formula_name }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </template>
      </q-select>
    </div>

    <!-- BANNER DE ERROR -->
    <q-banner v-if="medicamentosStore.error" class="bg-red-2 text-red-10 rounded-borders text-weight-bold text-subtitle1 q-mb-md">
      <q-icon name="error_outline" size="sm" class="q-mr-sm" />
      {{ medicamentosStore.error }}
    </q-banner>

    <!-- CARGANDO -->
    <div v-if="medicamentosStore.cargando" class="text-center q-mt-xl">
      <q-spinner-dots color="primary" size="3.5em" />
      <div class="text-subtitle1 text-grey-8 q-mt-md">Buscando las farmacias más cercanas...</div>
    </div>

    <!-- LISTADO DE FARMACIAS DISPONIBLES REESTRUCTURADO -->
    <div v-else-if="medicamentosStore.farmaciasCotizadas.length > 0">
      <div class="row items-center justify-between q-mb-md q-mt-lg">
        <div class="text-h6 text-primary text-weight-bold">Farmacias Cercanas:</div>
        <q-btn flat color="secondary" label="Limpiar" icon="delete_outline" size="sm" @click="limpiarTodo" />
      </div>

      <q-list class="q-gutter-y-md">
        <q-card 
          v-for="(farmacia, index) in medicamentosStore.farmaciasCotizadas" 
          :key="index"
          class="farmacia-card bg-white cursor-pointer"
          v-ripple
          @click="abrirDetalles(farmacia)"
        >
          <q-card-section class="q-pa-md">
            
            <!-- PARTE SUPERIOR: LOGO + DATOS COMPLETOS DE LA FARMACIA (CON ANCHO LIBRE) -->
            <div class="row no-wrap items-start">
              <q-avatar size="56px" square class="q-mr-md bg-white border-logo shrink-0">
                <img :src="farmacia.pharmacy_chain_logo || farmacia.pharmacy?.logo" alt="Logo">
              </q-avatar>
              
              <div class="col text-left">
                <!-- Nombre completo con salto de línea natural si es largo -->
                <div class="text-h6 text-weight-bold text-dark q-mb-xs" style="line-height: 1.2; word-break: break-word;">
                  {{ farmacia.pharmacy_chain_name || farmacia.pharmacy?.name || 'Farmacia' }}
                </div>
                <!-- Dirección completa sin recortes -->
                <div class="text-subtitle2 text-grey-8 q-mb-xs" v-if="farmacia.pharmacy_address" style="line-height: 1.3; word-break: break-word;">
                  {{ farmacia.pharmacy_address }}
                </div>
                <!-- Distancia -->
                <div class="text-body2 text-orange-9 text-weight-bold row items-center q-mt-xs">
                  <q-icon name="directions_walk" size="16px" class="q-mr-xs" />
                  A {{ (farmacia.pharmacy_distance / 1000).toFixed(1) }} km
                </div>
              </div>
            </div>

            <!-- PARTE INFERIOR: PRECIO GRANDE, SEPARADO Y TOTALMENTE AISLADO -->
            <div class="row items-center justify-between q-mt-md q-pt-sm" style="border-top: 1px dashed #e2e8f0;">
              <div class="text-subtitle2 text-grey-6 text-weight-medium">Precio del medicamento:</div>
              <div class="text-h4 text-weight-bolder text-positive">
                ${{ farmacia.total || farmacia.price }}
              </div>
            </div>

          </q-card-section>
        </q-card>
      </q-list>
    </div>

    <!-- MODAL DETALLES -->
    <q-dialog v-model="modalAbierto">
      <q-card style="width: 85vw; max-width: 380px; border-radius: 20px;">
        <q-card-section class="bg-primary text-white row items-center justify-between q-py-md">
          <div class="text-h6 text-weight-bold">Detalles de Compra</div>
          <q-btn icon="close" flat round dense size="md" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-md" v-if="farmaciaSeleccionada">
          <div class="text-center q-mb-md">
            <q-avatar size="80px" class="q-mb-sm shadow-1">
              <img :src="farmaciaSeleccionada.pharmacy_chain_logo || farmaciaSeleccionada.pharmacy?.logo" alt="Logo">
            </q-avatar>
            <div class="text-h6 text-weight-bold text-dark">
              {{ farmaciaSeleccionada.pharmacy_chain_name || farmaciaSeleccionada.pharmacy?.name }}
            </div>
            <div class="text-h3 text-positive text-weight-bold q-my-sm">
              ${{ farmaciaSeleccionada.total || farmaciaSeleccionada.price }}
            </div>
          </div>
          
          <q-list separator class="text-subtitle1">
            <q-item v-if="farmaciaSeleccionada.pharmacy_address" class="q-px-none">
              <q-item-section avatar>
                <q-icon name="place" color="negative" size="sm" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">Dirección</q-item-label>
                <q-item-label caption class="text-subtitle1 text-dark">{{ farmaciaSeleccionada.pharmacy_address }}</q-item-label>
              </q-item-section>
            </q-item>
            
            <q-item class="q-px-none">
              <q-item-section avatar>
                <q-icon name="directions_walk" color="primary" size="sm" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">Distancia</q-item-label>
                <q-item-label caption class="text-subtitle1 text-dark">A {{ (farmaciaSeleccionada.pharmacy_distance / 1000).toFixed(1) }} kilómetros</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
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

const medicamentoSeleccionado = ref(null)
const opcionesBusqueda = ref([])
const modalAbierto = ref(false)
const farmaciaSeleccionada = ref(null)

const LAT_PUERTO_MONTT = -41.4693
const LNG_PUERTO_MONTT = -72.9424

const filtrarMedicamentos = async (val, update, abort) => {
  if (!val || val.trim().length < 4) {
    abort()
    return
  }
  try {
    await medicamentosStore.buscarMedicamento(val)
    update(() => {
      opcionesBusqueda.value = medicamentosStore.resultadosBusqueda
    })
  } catch {
    abort()
  }
}

const alSeleccionarMedicamento = (producto) => {
  if (!producto) return
  $q.notify({
    message: 'Buscando sucursales cercanas...',
    color: 'primary',
    icon: 'location_on',
    timeout: 2000
  })
  
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        medicamentosStore.cotizarMedicamento(producto.product_id, pos.coords.latitude, pos.coords.longitude)
      },
      (err) => {
        console.warn("Sin GPS. Usando ubicación por defecto.", err)
        medicamentosStore.cotizarMedicamento(producto.product_id, LAT_PUERTO_MONTT, LNG_PUERTO_MONTT)
      },
      { timeout: 5000, maximumAge: 60000 }
    )
  } else {
    medicamentosStore.cotizarMedicamento(producto.product_id, LAT_PUERTO_MONTT, LNG_PUERTO_MONTT)
  }
}

const abrirDetalles = (farmacia) => {
  farmaciaSeleccionada.value = farmacia
  modalAbierto.value = true
}

const limpiarTodo = () => {
  medicamentoSeleccionado.value = null
  medicamentosStore.limpiarBusqueda()
}
</script>

<style scoped>
.input-text-fino :deep(input) {
  font-size: 1.1rem !important;
  font-weight: 400 !important;
}

:deep(.custom-search .q-field__control) {
  border-radius: 14px !important;
  background-color: #ffffff !important;
  height: 52px !important;
}
:deep(.custom-search .q-field__outline) {
  border-radius: 14px !important;
}

.farmacia-card {
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  border-left: 6px solid #f57c00 !important;
  overflow: hidden;
}

.border-logo {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 2px;
}

.shrink-0 {
  flex-shrink: 0;
}
</style>