import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAlarmasStore = defineStore('alarmas', () => {
  // RNF04: Inicializar desde el disco (localStorage) para que funcione sin internet
  const listaAlarmas = ref(JSON.parse(localStorage.getItem('lista_alarmas_offline')) || [])
  const registroTomas = ref(JSON.parse(localStorage.getItem('registro_tomas_offline')) || {})

  // Modificación: Uso de variable de entorno centralizada
  const API_URL = `https://asis-farmaceutica-backend.onrender.com/api/alarmas`

  const obtenerFechaHoy = () => {
    const hoy = new Date()
    return hoy.toLocaleDateString('en-CA') 
  }

  // 1. Marcar un remedio como tomado HOY
  const marcarComoTomado = async (alarma) => {
    const hoy = obtenerFechaHoy()
    
    registroTomas.value = { 
      ...registroTomas.value, 
      [alarma.id_recordatorio]: hoy 
    }
    
    // RNF04: Guardamos inmediatamente en el celular por si se corta el internet
    localStorage.setItem('registro_tomas_offline', JSON.stringify(registroTomas.value))
    
    try {
      await fetch(`${API_URL}/${alarma.id_recordatorio}/tomar`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
          estado: 'Tomado',
          fecha_hora_real: new Date().toISOString() 
          })
      })
      console.log("Historial guardado exitosamente en la base de datos")
    } catch (error) {
      console.warn("Modo Offline: El registro se guardó localmente. Se sincronizará luego.", error)
    }
  }

  // 2. Comprobar si ya se tomó hoy
  const yaSeTomoHoy = (id_recordatorio) => {
    return registroTomas.value[id_recordatorio] === obtenerFechaHoy()
  }

  // 3. Obtener alarmas de FastAPI
  const cargarAlarmasBackend = async (idPaciente) => {
    // Si no hay internet, no hacemos el fetch, confiamos en lo que cargó localStorage arriba
    if (!navigator.onLine) {
      console.log("Sin conexión: Mostrando alarmas desde memoria local.")
      return
    }

    try {
      const respuesta = await fetch(`${API_URL}/paciente/${idPaciente}`)
      if (respuesta.ok) {
        listaAlarmas.value = await respuesta.json()
        // RNF04: Actualizamos la copia de seguridad en el celular
        localStorage.setItem('lista_alarmas_offline', JSON.stringify(listaAlarmas.value))
      }
    } catch (error) {
      console.error("Error cargando alarmas, usando versión local.", error)
    }
  }

  // 4. Crear nueva alarma
  const crearAlarma = async (datosAlarma, idPaciente) => {
    try {
      const respuesta = await fetch(`${API_URL}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...datosAlarma,
          id_paciente: idPaciente,
          activo: true
        })
      })

      if (!respuesta.ok) {
        throw new Error('Error al guardar el recordatorio en el servidor')
      }

      const nuevaAlarmaDB = await respuesta.json()
      
      // Actualizamos la lista local inmediatamente para que se vea reflejada
      listaAlarmas.value.push(nuevaAlarmaDB)
      localStorage.setItem('lista_alarmas_offline', JSON.stringify(listaAlarmas.value))
      
      return true
    } catch (error) {
      console.error("Error creando alarma:", error)
      throw error
    }
  }

  // 5. Eliminar alarma
  const eliminarAlarma = async (id_recordatorio) => {
    // Eliminamos del estado local primero para asegurar la actualización de la interfaz
    listaAlarmas.value = listaAlarmas.value.filter(a => a.id_recordatorio !== id_recordatorio)
    localStorage.setItem('lista_alarmas_offline', JSON.stringify(listaAlarmas.value))

    try {
      const respuesta = await fetch(`${API_URL}/${id_recordatorio}`, {
        method: 'DELETE'
      })
      
      if (!respuesta.ok) {
        throw new Error('Error al eliminar en el servidor')
      }
      console.log(`Alarma ${id_recordatorio} eliminada del servidor con éxito.`)
    } catch (error) {
      console.warn("Modo Offline: Guardado localmente, el servidor se actualizará al recuperar red.", error)
    }
  }

  // 6. Actualizar alarma
  const actualizarAlarma = async (id_recordatorio, datosActualizados) => {
    try {
      const respuesta = await fetch(`${API_URL}/${id_recordatorio}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(datosActualizados)
      })

      if (!respuesta.ok) throw new Error('Error al actualizar en el servidor')
      
      const alarmaActualizada = await respuesta.json()
      
      const index = listaAlarmas.value.findIndex(a => a.id_recordatorio === id_recordatorio)
      if (index !== -1) {
        listaAlarmas.value[index] = { ...listaAlarmas.value[index], ...alarmaActualizada }
        localStorage.setItem('lista_alarmas_offline', JSON.stringify(listaAlarmas.value))
      }
    } catch (error) {
      console.warn("Modo Offline al actualizar la alarma:", error)
      // Respaldo local
      const index = listaAlarmas.value.findIndex(a => a.id_recordatorio === id_recordatorio)
      if (index !== -1) {
        listaAlarmas.value[index] = { ...listaAlarmas.value[index], ...datosActualizados }
        localStorage.setItem('lista_alarmas_offline', JSON.stringify(listaAlarmas.value))
      }
    }
  }

  return {
    listaAlarmas,
    registroTomas,
    marcarComoTomado,
    yaSeTomoHoy,
    cargarAlarmasBackend,
    crearAlarma,
    eliminarAlarma,
    actualizarAlarma
  }
})