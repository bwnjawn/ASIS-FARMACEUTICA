import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMedicamentosStore = defineStore('medicamentos', () => {
  const resultadosBusqueda = ref([])
  const farmaciasCotizadas = ref([])
  const cargando = ref(false)
  const error = ref(null)

  const API_URL = 'http://127.0.0.1:8000/api/medicamentos'

  const buscarMedicamento = async (termino) => {
    if (!termino || termino.trim().length < 2) return

    cargando.value = true
    error.value = null
    resultadosBusqueda.value = []
    
    try {
      const respuesta = await fetch(`${API_URL}/buscar?q=${encodeURIComponent(termino)}`)
      
      if (!respuesta.ok) {
        const datosError = await respuesta.json()
        throw new Error(datosError.detail || 'Error al conectar con el buscador.')
      }

      const datos = await respuesta.json()
      // CORRECCIÓN AQUÍ: FastAPI devuelve {"data": [...]}. Debemos extraer el array.
      resultadosBusqueda.value = datos.data || [] 
      
      if (resultadosBusqueda.value.length === 0) {
        error.value = "No se encontraron remedios con ese nombre."
      }
    } catch (err) {
      error.value = err.message
    } finally {
      cargando.value = false
    }
  }

  const cotizarMedicamento = async (idProducto, lat, lng) => {
    cargando.value = true
    error.value = null
    farmaciasCotizadas.value = []
    
    try {
      const respuesta = await fetch(`${API_URL}/cotizar?id_producto=${idProducto}&lat=${lat}&lng=${lng}`)
      
      if (!respuesta.ok) throw new Error('Error al obtener los precios.')

      const datos = await respuesta.json()
      // CORRECCIÓN AQUÍ: Extraer el array 'data' de la respuesta
      farmaciasCotizadas.value = datos.data || []
    } catch (err) {
      error.value = err.message
    } finally {
      cargando.value = false
    }
  }

  const limpiarBusqueda = () => {
    resultadosBusqueda.value = []
    farmaciasCotizadas.value = []
    error.value = null
  }

  return {
    resultadosBusqueda,
    farmaciasCotizadas,
    cargando,
    error,
    buscarMedicamento,
    cotizarMedicamento,
    limpiarBusqueda
  }
})