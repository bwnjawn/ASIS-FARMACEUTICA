<template>
  <q-page class="flex flex-center bg-grey-2">
    <q-card class="q-pa-md shadow-2" style="width: 400px; max-width: 90vw;">
      <q-card-section class="text-center">
        <div class="text-h4 text-primary text-weight-bold">ASIS Farmacéutica</div>
        <div class="text-subtitle1 text-grey-7">
          {{ isLogin ? 'Inicia sesión en tu cuenta' : 'Crea tu perfil de paciente' }}
        </div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          
          <q-input 
            v-if="!isLogin"
            outlined 
            v-model="form.nombre" 
            label="Nombre Completo" 
            lazy-rules
            :rules="[val => val && val.length > 0 || 'Por favor ingresa tu nombre']"
          />

          <q-input 
            outlined 
            v-model="form.rut" 
            label="RUT (Ej: 12345678-9)" 
            mask="########-X"
            lazy-rules
            :rules="[val => val && val.length >= 9 || 'RUT inválido']"
          />

          <q-input 
            outlined 
            type="password" 
            v-model="form.password" 
            label="Contraseña" 
            lazy-rules
            :rules="[val => val && val.length >= 6 || 'Mínimo 6 caracteres']"
          />

          <div class="q-mt-lg">
            <q-btn 
              :loading="loading"
              class="full-width" 
              color="primary" 
              size="lg" 
              :label="isLogin ? 'Ingresar' : 'Registrarse'" 
              type="submit" 
            />
          </div>
        </q-form>
      </q-card-section>

      <q-card-section class="text-center q-pt-none">
        <q-btn 
          flat 
          color="secondary" 
          :label="isLogin ? '¿No tienes cuenta? Regístrate aquí' : '¿Ya tienes cuenta? Inicia sesión'" 
          @click="isLogin = !isLogin" 
        />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useQuasar } from 'quasar'
import { supabase } from '../services/supabase'

const $q = useQuasar()
const isLogin = ref(true)
const loading = ref(false)

const form = reactive({
  nombre: '',
  rut: '',
  password: ''
})

// Función que aplica la Estrategia Técnica de conversión
const rutToEmail = (rut) => {
  return `${rut.toLowerCase()}@asis.cl`
}

const onSubmit = async () => {
  loading.value = true
  const correoGenerado = rutToEmail(form.rut)

  try {
    if (isLogin.value) {
      // LOGICA DE INICIO DE SESIÓN
      const { error } = await supabase.auth.signInWithPassword({
        email: correoGenerado,
        password: form.password,
      })

      if (error) throw error
      
      $q.notify({ type: 'positive', message: '¡Bienvenido de vuelta!' })
      // Aquí a futuro redirigiremos a la página principal de alarmas

    } else {
      // LOGICA DE REGISTRO
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: correoGenerado,
        password: form.password,
      })

      if (authError) throw authError

      // Generamos un código aleatorio de 6 caracteres para la vinculación
      const codigoAleatorio = Math.random().toString(36).substring(2, 8).toUpperCase()

      // Insertamos el perfil en nuestra tabla pública 'paciente'
      const { error: dbError } = await supabase.from('paciente').insert([
        {
          id_paciente: authData.user.id,
          nombre_usuario: form.nombre,
          rut: form.rut,
          codigo_vinculacion: codigoAleatorio
        }
      ])

      if (dbError) throw dbError

      $q.notify({ type: 'positive', message: '¡Cuenta creada con éxito!' })
      isLogin.value = true // Lo devolvemos al login para que entre
    }
  } catch (error) {
    $q.notify({ 
      type: 'negative', 
      message: error.message === 'Invalid login credentials' ? 'RUT o contraseña incorrectos' : error.message 
    })
  } finally {
    loading.value = false
  }
}
</script>