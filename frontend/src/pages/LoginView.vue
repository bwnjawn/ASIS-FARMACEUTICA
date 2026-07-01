<template>
  <q-page class="flex flex-center q-pa-md bg-grey-1">
    <q-card class="q-pa-md shadow-3 bg-white" style="width: 380px; max-width: 92vw; border-radius: 20px;">
      
      <!-- ENCABEZADO MÁS COMPACTO Y ALTO -->
      <q-card-section class="text-center q-pb-sm q-pt-xs">
        <q-icon name="fa-solid fa-pills" color="primary" size="3rem" class="q-mb-xs" />
        <h1 class="text-h5 text-weight-bold q-ma-none text-dark">
          {{ esLogin ? '¡Hola!' : 'Crear Cuenta' }}
        </h1>
        <p class="text-body1 text-black-7 q-mt-xs q-mb-none">
          {{ esLogin ? 'Ingresa tus datos para acceder a tus remedios.' : 'Regístrate para guardar tus alarmas.' }}
        </p>
      </q-card-section>

      <!-- FORMULARIO OPTIMIZADO -->
      <q-card-section class="q-pt-md">
        <q-form @submit.prevent="procesarFormulario" class="q-gutter-y-sm">
          
          <!-- CAMPO: RUT -->
          <div>
            <div class="text-subtitle2 text-weight-medium q-mb-xs label-gris">Tu RUT (ej: 12345678-9)</div>
            <q-input
                v-model="rut"
                outlined
                placeholder="12345678-9"
                type="tel"
                mask="########-X"
                lazy-rules
                class="input-fino-gris custom-login-input"
                :disable="authStore.cargando"
                hide-bottom-space
                dense
                :rules="[
                  val => !!val || 'El RUT es obligatorio',
                  val => val.length >= 9 || 'RUT incompleto',
                  val => {
                    // Limpiar el RUT de guiones y dejarlo limpio
                    const limpio = val.replace(/[^0-9kK]/g, '');
                    if (limpio.length < 2) return 'RUT inválido';
                    
                    const cuerpo = limpio.slice(0, -1);
                    let dv = limpio.slice(-1).toLowerCase();
                    
                    // Calcular Dígito Verificador Chileno (Módulo 11)
                    let suma = 0;
                    let multiplicador = 2;
                    
                    for (let i = cuerpo.length - 1; i >= 0; i--) {
                      suma += parseInt(cuerpo.charAt(i)) * multiplicador;
                      multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
                    }
                    
                    let dvEsperado = 11 - (suma % 11);
                    if (dvEsperado === 11) dvEsperado = '0';
                    else if (dvEsperado === 10) dvEsperado = 'k';
                    else dvEsperado = String(dvEsperado);
                    
                    return dv === dvEsperado || 'El RUT no es real (DV incorrecto)';
                  }
                ]"
              />
          </div>

          <!-- CAMPO: NOMBRE COMPLETO (SOLO EN REGISTRO) -->
          <div v-if="!esLogin">
            <div class="text-subtitle2 text-weight-medium q-mb-xs label-gris">Tu Nombre Completo</div>
            <q-input
              v-model="nombreUsuario"
              outlined
              placeholder="Ej: Juan Pérez"
              type="text"
              lazy-rules
              class="input-fino-gris custom-login-input"
              :disable="authStore.cargando"
              :rules="[val => val && val.trim().length > 0 || 'El nombre es obligatorio']"
              hide-bottom-space
              dense
            />
          </div>

          <!-- CAMPO: CONTRASEÑA -->
          <div>
            <div class="text-subtitle2 text-weight-medium q-mb-xs label-gris">Tu Contraseña o PIN</div>
            <q-input
              v-model="password"
              outlined
              placeholder="••••••"
              type="password"
              lazy-rules
              class="input-fino-gris custom-login-input"
              :disable="authStore.cargando"
              :rules="[val => val && val.length >= 6 || 'Mínimo 6 caracteres']"
              hide-bottom-space
              dense
            />
          </div>

          <!-- REPORTE DE ERROR -->
          <q-banner v-if="authStore.error" class="bg-red-2 text-red-9 rounded-borders text-weight-bold text-body2 q-mt-sm">
            <q-icon name="error" size="xs" class="q-mr-xs" />
            {{ authStore.error }}
          </q-banner>

          <!-- BOTÓN PRINCIPAL -->
          <q-btn
            type="submit"
            color="primary"
            :label="esLogin ? 'Entrar a la Aplicación' : 'Registrar Cuenta'"
            class="full-width q-py-sm text-subtitle1 text-weight-bold q-mt-md"
            style="border-radius: 14px; min-height: 48px;"
            :loading="authStore.cargando"
          />

          <!-- BOTÓN SECUNDARIO CON FUENTE COMPENSADA -->
          <q-btn
            flat
            color="grey-8"
            :label="esLogin ? '¿No tienes cuenta? Regístrate aquí' : '¿Ya tienes cuenta? Inicia sesión'"
            class="full-width text-body2 text-weight-medium q-mt-sm text-capitalize"
            style="letter-spacing: 0px;"
            @click="conmutarModo"
          />
          
        </q-form>
      </q-card-section>

    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const esLogin = ref(true)
const rut = ref('')
const nombreUsuario = ref('')
const password = ref('')

const conmutarModo = () => {
  esLogin.value = !esLogin.value
  authStore.error = null
}

const procesarFormulario = async () => {
  try {
    if (esLogin.value) {
      await authStore.iniciarSesion(rut.value, password.value)
    } else {
      await authStore.registrarPaciente(rut.value, nombreUsuario.value, password.value)
    }
    
    $q.notify({
      type: 'positive',
      message: esLogin.value ? '¡Bienvenido de vuelta!' : 'Cuenta creada con éxito',
      position: 'top',
      icon: 'check'
    })
    
    router.push('/alarmas')
  } catch (err) {
    $q.notify({
      type: 'negative',
      message: err.message || 'Ocurrió un problema inesperado',
      position: 'top',
      icon: 'close'
    })
  }
}
</script>

<style scoped>
.label-gris {
  color: #334155; /* Gris slate moderno y legible */
}

/* Letra fina, limpia y grisácea-negra al escribir */
.input-fino-gris :deep(input) {
  font-size: 1rem !important;
  font-weight: 400 !important;
  color: #1e293b !important;
}

/* Estilo y radio refinado para las cajas */
:deep(.custom-login-input .q-field__control) {
  border-radius: 12px !important;
  background-color: #f8fafc !important;
  height: 46px !important;
}

:deep(.custom-login-input .q-field__outline) {
  border-radius: 12px !important;
}

:deep(.custom-login-input .q-field__outline__start),
:deep(.custom-login-input .q-field__outline__notch),
:deep(.custom-login-input .q-field__outline__end) {
  border-color: #cbd5e1 !important;
}
</style>