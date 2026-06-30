// frontend/src/stores/auth.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

// OJO AL CAMBIO AL FINAL DEL ARCHIVO
export const useAuthStore = defineStore('auth', () => {
  const idPaciente = ref(null)
  const token = ref(null)
  
  const API_URL = 'http://127.0.0.1:8000/api'

  const iniciarSesion = async (rut, password) => {
    try {
      const respuesta = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rut, password })
      })

      if (!respuesta.ok) {
        throw new Error('RUT o contraseña incorrectos')
      }

      const datos = await respuesta.json()
      
      idPaciente.value = datos.id_usuario
      token.value = datos.access_token
      
      return true
    } catch (error) {
      console.error("Error en login:", error)
      throw error
    }
  }

  const registrarPaciente = async (rut, nombreUsuario, password) => {
    try {
      const respuesta = await fetch(`${API_URL}/auth/registro/paciente`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rut, nombre_usuario: nombreUsuario, password })
      })

      if (!respuesta.ok) throw new Error('Error al registrar el paciente')
      return true
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
}, {
  // 3. ESTA ES LA LÍNEA MÁGICA QUE GUARDA LA SESIÓN EN LOCALSTORAGE
  persist: true
})