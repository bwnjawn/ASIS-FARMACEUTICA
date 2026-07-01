<template>
  <q-page class="q-pa-md bg-grey-1">
    
    <div class="q-mb-lg">
      <h1 class="text-h4 text-weight-bold q-ma-none text-dark q-mb-md">Cotizar Remedios</h1>
      <p class="text-subtitle1 text-grey-8 q-mb-sm">Escriba el remedio y selecciónelo de la lista:</p>
      
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
        bg-color="white"
        class="text-h6 shadow-1 rounded-borders"
        @filter="filtrarMedicamentos"
        @update:model-value="alSeleccionarMedicamento"
      >
        <template v-slot:append>
          <q-icon name="search" color="primary" />
        </template>
        
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey text-h6 text-center q-pa-md">
              No se encontraron resultados para esa búsqueda.
            </q-item-section>
          </q-item>
        </template>
        
        <!-- CORRECCIÓN: Adaptado al nuevo formato del JSON de autocomplete -->
        <template v-slot:option="scope">
          <q-item v-bind="scope.itemProps" class="q-pa-md" style="border-bottom: 1px solid #eee;">
            <q-item-section avatar>
              <q-avatar square size="60px" style="border-radius: 8px;">
                <img :src="scope.opt.product_logo || 'https://via.placeholder.com/60?text=Rx'">
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <!-- El product_name ahora trae todo: nombre + dosis + laboratorio -->
              <q-item-label class="text-h6 text-weight-bold text-dark" style="line-height: 1.1;">
                {{ scope.opt.product_name }}
              </q-item-label>
              <!-- Si viene la fórmula activa, la mostramos como subtítulo de apoyo -->
              <q-item-label caption class="text-subtitle1 text-grey-9 q-mt-xs" v-if="scope.opt.formula_name">
                <q-icon name="medication" size="sm" color="primary" class="q-mr-xs"/> 
                Componente: {{ scope.opt.formula_name }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </template>
      </q-select>
    </div>

    <q-banner v-if="medicamentosStore.error" class="bg-red-2 text-red-10 rounded-borders text-weight-bold text-h6 q-mb-md">
      <q-icon name="error_outline" size="md" class="q-mr-sm" />
      {{ medicamentosStore.error }}
    </q-banner>

    <div v-if="medicamentosStore.cargando" class="text-center q-mt-xl">
      <q-spinner-dots color="primary" size="4em" />
      <div class="text-h6 text-grey-8 q-mt-md">Buscando las farmacias más cercanas...</div>
    </div>

    <div v-else-if="medicamentosStore.farmaciasCotizadas.length > 0">
      <div class="row items-center justify-between q-mb-md">
        <div class="text-h5 text-primary text-weight-bold">Farmacias Cercanas:</div>
        <q-btn flat color="secondary" label="Limpiar" icon="delete_outline" size="md" @click="limpiarTodo" />
      </div>
      <q-list class="q-gutter-y-md">
        <q-card 
          v-for="(farmacia, index) in medicamentosStore.farmaciasCotizadas" 
          :key="index"
          class="shadow-2 cursor-pointer"
          v-ripple
          style="border-radius: 12px; border-left: 8px solid var(--q-primary);"
          @click="abrirDetalles(farmacia)"
        >
          <q-card-section>
            <div class="row no-wrap items-center">
              <q-avatar size="60px" square class="q-mr-md bg-white">
                <img :src="farmacia.pharmacy_chain_logo || farmacia.pharmacy?.logo" alt="Logo Farmacia">
              </q-avatar>
              
              <div class="col">
                <div class="text-h6 text-weight-bold text-dark" style="line-height: 1.1;">
                  {{ farmacia.pharmacy_chain_name || farmacia.pharmacy?.name || 'Farmacia' }}
                </div>
                <div class="text-subtitle1 text-grey-8 q-mt-xs" v-if="farmacia.pharmacy_address">
                  <q-icon name="storefront" size="sm" color="grey-7"/> {{ farmacia.pharmacy_address }}
                </div>
                <div class="text-subtitle1 text-grey-9 q-mt-xs">
                  <q-icon name="directions_walk" size="sm" color="primary" class="q-mr-xs" />
                  <strong>A {{ (farmacia.pharmacy_distance / 1000).toFixed(1) }} km</strong>
                </div>
              </div>

              <div class="text-h4 text-weight-bold text-positive q-ml-sm">
                ${{ farmacia.total || farmacia.price }}
              </div>
            </div>
          </q-card-section>
        </q-card>
      </q-list>
    </div>

    <q-dialog v-model="modalAbierto">
      <q-card style="width: 100%; max-width: 400px; border-radius: 16px;">
        <q-card-section class="bg-primary text-white row items-center justify-between">
          <div class="text-h6 text-weight-bold">Detalles de Compra</div>
          <q-btn icon="close" flat round dense size="lg" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-md" v-if="farmaciaSeleccionada">
          <div class="text-center q-mb-md">
            <q-avatar size="100px" class="q-mb-sm">
              <img :src="farmaciaSeleccionada.pharmacy_chain_logo || farmaciaSeleccionada.pharmacy?.logo" alt="Logo">
            </q-avatar>
            <div class="text-h5 text-weight-bold text-dark">
              {{ farmaciaSeleccionada.pharmacy_chain_name || farmaciaSeleccionada.pharmacy?.name }}
            </div>
            <div class="text-h2 text-positive text-weight-bold q-my-md">
              ${{ farmaciaSeleccionada.total || farmaciaSeleccionada.price }}
            </div>
          </div>
          
          <q-list separator class="text-h6">
            <q-item v-if="farmaciaSeleccionada.pharmacy_address">
              <q-item-section avatar>
                <q-icon name="place" color="negative" size="md" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">Dirección</q-item-label>
                <q-item-label caption class="text-subtitle1 text-dark">{{ farmaciaSeleccionada.pharmacy_address }}</q-item-label>
              </q-item-section>
            </q-item>
            
            <q-item>
              <q-item-section avatar>
                <q-icon name="directions_walk" color="primary" size="md" />
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

// Variables reactivas
const medicamentoSeleccionado = ref(null)
const opcionesBusqueda = ref([])
const modalAbierto = ref(false)
const farmaciaSeleccionada = ref(null)

// Coordenadas por defecto (Centro de Puerto Montt)
const LAT_PUERTO_MONTT = -41.4693
const LNG_PUERTO_MONTT = -72.9424

// Lógica de Autocompletado
const filtrarMedicamentos = async (val, update, abort) => {
  if (!val || val.trim().length < 4) {
    abort()
    return
  }

  try {
    await medicamentosStore.buscarMedicamento(val)

    update(() => {
      // Nos aseguramos de leer correctamente el array desde la store
      opcionesBusqueda.value = medicamentosStore.resultadosBusqueda
    })
  } catch {
    abort()
  }
}

// Al elegir una pastilla de la lista, buscamos GPS y cotizamos inmediatamente
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
        medicamentosStore.cotizarMedicamento(
          producto.product_id, 
          pos.coords.latitude, 
          pos.coords.longitude
        )
      },
      (err) => {
        console.warn("Sin GPS. Usando ubicación por defecto.", err)
        medicamentosStore.cotizarMedicamento(
          producto.product_id, 
          LAT_PUERTO_MONTT, 
          LNG_PUERTO_MONTT
        )
      },
      { timeout: 5000, maximumAge: 60000 }
    )
  } else {
    medicamentosStore.cotizarMedicamento(
      producto.product_id, 
      LAT_PUERTO_MONTT, 
      LNG_PUERTO_MONTT
    )
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