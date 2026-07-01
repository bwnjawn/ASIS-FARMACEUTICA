<template>
  <q-layout view="hHh lpR fFf">
    
    <!-- ENCABEZADO CORREGIDO CON COLOR ORIGINAL, NUEVO NOMBRE Y SÍMBOLO DE ESTRELLA -->
    <q-header class="bg-orange-5 text-white" v-if="rutaActual !== '/'">
      <q-toolbar class="q-px-md q-py-xs row items-center no-wrap">
        
        <!-- Símbolo de estrella y nuevo nombre a la izquierda -->
        <div class="col-auto row items-center no-wrap">
          <div class="simbolo-contenedor row items-center justify-center q-mr-sm shadow-1">
            <q-icon name="star" size="24px" color="white" />
          </div>
          
          <!-- Nuevo nombre corto y amigable para la app -->
          <div class="text-h5 text-weight-bold tracking-tight text-white font-app">
            TomApp
          </div>
        </div>

        <!-- Espaciador para mantener la alineación izquierda limpia -->
        <q-space />
        
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer bordered class="bg-white text-primary shadow-up-2" v-if="rutaActual !== '/'">
      <q-tabs
        no-caps
        active-color="primary"
        indicator-color="primary"
        class="text-grey-7 bg-white"
        align="justify"
        switch-indicator
      >
        <q-route-tab to="/buscar" exact icon="fa-solid fa-magnifying-glass" label="Buscar" />
        <q-route-tab to="/alarmas" exact icon="fa-solid fa-clock" label="Remedios" />
        <q-route-tab to="/perfil" exact icon="fa-solid fa-user-check" label="Perfil" />
      </q-tabs>
    </q-footer>

    <!-- Modal adaptado para móviles (sin maximized y con anchos relativos) -->
    <q-dialog v-model="mostrarAlarmaEnPantalla" persistent transition-show="scale" transition-hide="scale">
      <q-card class="bg-warning text-black text-center q-pa-md" style="width: 90vw; max-width: 400px; border-radius: 16px;">
        <q-card-section>
          <q-icon name="fa-solid fa-bell" size="4rem" color="negative" class="q-mb-sm" />
          <div class="text-h4 text-weight-bold">¡MEDICINA!</div>
          <div class="text-h6 q-mt-md">Te toca tomar:</div>
          <div class="text-h3 text-weight-bold q-mt-sm text-negative" style="word-wrap: break-word;">
            {{ alarmaEnCurso ? alarmaEnCurso.nombre_medicamento : '' }}
          </div>
        </q-card-section>

        <q-card-actions align="center" class="full-width q-mt-md">
          <q-btn 
            label="YA ME LO TOMÉ" 
            color="positive" 
            size="lg" 
            class="full-width text-weight-bold q-py-sm" 
            @click="confirmarToma" 
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router' // Removido useRouter de aquí
import { useAlarmasStore } from '../stores/alarmas'
import { useQuasar } from 'quasar'

const route = useRoute()
// Líneas de router y authStore eliminadas por completo
const alarmasStore = useAlarmasStore()
const $q = useQuasar()

const rutaActual = computed(() => route.path)

// Variables reactivas
const mostrarAlarmaEnPantalla = ref(false)
const alarmaEnCurso = ref(null)

async function solicitarPermisoNotificaciones() {
  if (!("Notification" in window)) {
    console.log("Este navegador no soporta notificaciones");
    return;
  }
  const permission = await Notification.requestPermission();
  if (permission === "granted") {
    console.log("¡Permiso concedido!");
  }
}

function reproducirSonido() {
  try {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    oscillator.type = 'square';
    oscillator.frequency.setValueAtTime(880, audioCtx.currentTime);
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 0.6); 
  } catch (error) {
    console.log("El navegador bloqueó el audio o no está soportado.", error);
  }
}

function enviarAlarma(alarmaObj) {
  reproducirSonido();

  if (Notification.permission === "granted") {
    new Notification("¡Hora de tomar tu medicamento!", {
      body: `Te toca tomar: ${alarmaObj.nombre_medicamento}`,
      icon: '/icons/favicon-128x128.png',
      vibrate: [200, 100, 200, 100, 200, 100, 200] 
    });
  }
  
  alarmaEnCurso.value = alarmaObj;
  mostrarAlarmaEnPantalla.value = true;
}

function revisarAlarmas() {
  const opcionesHora = { 
    timeZone: 'America/Santiago', 
    hour: '2-digit', 
    minute: '2-digit', 
    hour12: false 
  };
  const formatter = new Intl.DateTimeFormat('es-CL', opcionesHora);
  const horaFormateada = formatter.format(new Date()); 
  const horaActual = `${horaFormateada}:00`; 

  console.log(`⏱️ Buscando alarmas programadas para las: ${horaActual}`); 

  const alarmaActiva = alarmasStore.listaAlarmas.find(
    (alarma) => alarma.hora_programada === horaActual && alarma.activo
  );

  if (alarmaActiva) {
    enviarAlarma(alarmaActiva);
    alarmaActiva.activo = false; 
  }
}

const confirmarToma = async () => {
  if (alarmaEnCurso.value) {
    await alarmasStore.marcarComoTomado(alarmaEnCurso.value);
    $q.notify({
      type: 'positive',
      message: '¡Excelente! Has registrado tu toma.',
      position: 'top'
    });
  }
  mostrarAlarmaEnPantalla.value = false;
  alarmaEnCurso.value = null;
}

onMounted(() => {
  solicitarPermisoNotificaciones();
  setInterval(revisarAlarmas, 10000); 
})
</script>

<style scoped>
/* Contenedor del símbolo adaptado al color naranja con la estrella blanca */
.simbolo-contenedor {
  background-color: #f57c00; /* Naranja más intenso para resaltar la estrella */
  width: 40px;
  height: 40px;
  border-radius: 12px;
}

.tracking-tight {
  letter-spacing: -0.5px;
}

.font-app {
  font-family: system-ui, -apple-system, sans-serif;
  color: #ffffff !important;
}

:deep(.q-tab__icon) {
  font-size: 26px !important; 
  margin-bottom: 2px;
}

:deep(.q-tab__label) {
  font-size: 14px !important;
  font-weight: bold;
}

.q-footer .q-tab {
  min-height: 70px; 
  padding: 0 4px; 
}
</style>