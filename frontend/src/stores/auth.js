import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // Leemos de localStorage para mantener la sesión si el usuario refresca la página
  const idPaciente = ref(localStorage.getItem('id_paciente') || null)
  const token = ref(localStorage.getItem('access_token') || null)
  
  // Modificación: Uso de variable de entorno apuntando a las rutas de auth
  const API_URL = `${import.meta.env.VITE_API_URL}/auth`

  const iniciarSesion = async (rut, password) => {
    try {
      const respuesta = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rut, password })
      })

      if (!respuesta.ok) {
        throw new Error('RUT o contraseña incorrectos')
      }

      const datos = await respuesta.json()
      
      // Ajuste de seguridad: detecta id_paciente o id_usuario según lo que devuelva FastAPI
      idPaciente.value = datos.id_paciente || datos.id_usuario
      token.value = datos.access_token
      
      // Guardamos en el disco para resiliencia offline y recargas
      if (idPaciente.value) {
        localStorage.setItem('id_paciente', idPaciente.value)
        localStorage.setItem('access_token', datos.access_token)
      }
      
      return true
    } catch (error) {
      console.error("Error en login:", error)
      throw error
    }
  }

  const registrarPaciente = async (rut, nombreUsuario, password) => {
    try {
      const respuesta = await fetch(`${API_URL}/registro/paciente`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rut, nombre_usuario: nombreUsuario, password })
      })

      if (!respuesta.ok) {
        throw new Error('Error en el registro')
      }

      return await iniciarSesion(rut, password)
    } catch (error) {
      console.error("Error en registro:", error)
      throw error
    }
  }

  return {
    idPaciente,
    token,
    iniciarSesion,
    registrarPaciente
  }
})