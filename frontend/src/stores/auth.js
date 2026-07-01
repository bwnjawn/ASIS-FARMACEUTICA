import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const idPaciente = ref(localStorage.getItem('id_paciente') || null)
  const token = ref(localStorage.getItem('access_token') || null)
  
  // Rescatamos los datos o ponemos un default seguro
  const nombreUsuario = ref(localStorage.getItem('nombre_usuario') || 'Paciente Activo')
  const rut = ref(localStorage.getItem('rut') || '')
  
  const API_URL = `https://asis-farmaceutica-backend.onrender.com/api/auth`

  const iniciarSesion = async (rutInput, password) => {
    try {
      const respuesta = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rut: rutInput, password })
      })

      if (!respuesta.ok) throw new Error('RUT o contraseña incorrectos')

      const datos = await respuesta.json()
      
      idPaciente.value = datos.id_paciente || datos.id_usuario
      token.value = datos.access_token
      
      // PARCHE PRESENTACIÓN: Si Render no envía el RUT, usamos el que tipeó el usuario
      rut.value = datos.rut || rutInput
      
      // Si Render enviara el nombre, lo usamos. Si no, conservamos el local.
      if (datos.nombre_usuario && datos.nombre_usuario !== 'undefined') {
        nombreUsuario.value = datos.nombre_usuario
      }
      
      if (idPaciente.value) {
        localStorage.setItem('id_paciente', idPaciente.value)
        localStorage.setItem('access_token', token.value)
        localStorage.setItem('rut', rut.value)
        localStorage.setItem('nombre_usuario', nombreUsuario.value)
      }
      
      return true
    } catch (error) {
      console.error("Error en login:", error)
      throw error
    }
  }

  const registrarPaciente = async (rutInput, nombreInput, password) => {
    try {
      // TRUCO: Guardamos el nombre en el frontend INMEDIATAMENTE al registrar
      // Así no dependemos de si Render se actualizó o no
      nombreUsuario.value = nombreInput
      localStorage.setItem('nombre_usuario', nombreInput)

      const respuesta = await fetch(`${API_URL}/registro/paciente`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rut: rutInput, nombre_usuario: nombreInput, password })
      })

      if (!respuesta.ok) throw new Error('Error en el registro')

      return await iniciarSesion(rutInput, password)
    } catch (error) {
      console.error("Error en registro:", error)
      throw error
    }
  }

  return { idPaciente, token, nombreUsuario, rut, iniciarSesion, registrarPaciente }
})