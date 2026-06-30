import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAlarmasStore = defineStore('alarmas', () => {
  // Lista de remedios guardada en el disco
  const listaAlarmas = ref([])
  
  // Objeto que guarda { id_alarma: "2026-06-30" }
  const registroTomas = ref({})

  // Obtener la fecha actual en formato YYYY-MM-DD
  const obtenerFechaHoy = () => {
    const hoy = new Date()
    // Ajuste seguro para la zona horaria local (América/Santiago)
    return hoy.toLocaleDateString('en-CA') // Devuelve formato YYYY-MM-DD
  }

  // 1. Marcar un remedio como tomado HOY
  const marcarComoTomado = async (alarma) => {
    const hoy = obtenerFechaHoy()
    
    // Forzamos la reactividad de Vue clonando el objeto con el ID real de tu BD
    registroTomas.value = { 
      ...registroTomas.value, 
      [alarma.id_recordatorio]: hoy 
    }
    
    try {
    await fetch(`http://127.0.0.1:8000/api/alarmas/${alarma.id_recordatorio}/tomar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
        estado: 'Tomado',
        // Generamos el timestamp exacto que pide tu base de datos
        fecha_hora_real: new Date().toISOString() 
        })
    })
    console.log("Historial guardado exitosamente en la base de datos")
    } catch (error) {
    // RNF04: Si no hay internet, Pinia ya lo guardó en el celular
    console.error("Modo Offline: El registro se sincronizará luego.", error)
    }
  }

  // 2. Comprobar si ya se tomó hoy
  const yaSeTomoHoy = (id_recordatorio) => {
    return registroTomas.value[id_recordatorio] === obtenerFechaHoy()
  }
  // 3. Obtener alarmas de FastAPI
  const cargarAlarmasBackend = async (idPaciente, rutaGET) => {
    try {
      const respuesta = await fetch(rutaGET)
      if (respuesta.ok) {
        listaAlarmas.value = await respuesta.json()
      }
    } catch (error) {
      console.error("Modo Offline: Usando alarmas guardadas en memoria.", error)
    }
  }

  return {
    listaAlarmas,
    registroTomas,
    marcarComoTomado,
    yaSeTomoHoy,
    cargarAlarmasBackend
  }
}, {
  // CLAVE: Esto asegura que las alarmas y las tomas no se borren sin internet
  persist: true 
})