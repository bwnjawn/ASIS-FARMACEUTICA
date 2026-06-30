<template>
  <q-layout view="hHh lpR fFf">
    
    <q-header elevated class="bg-primary text-white" v-if="rutaActual !== '/'">
      <q-toolbar>
        <q-toolbar-title class="text-center text-weight-bold q-py-sm">
          <q-icon name="fa-solid fa-notes-medical" class="q-mr-sm" />
          ASIS Farmacéutica
        </q-toolbar-title>
        
        <q-btn flat round dense icon="logout" @click="cerrarSesion" />
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
        <q-route-tab 
          to="/buscar" 
          exact
          icon="fa-solid fa-magnifying-glass"
          label="Buscar"
        />

        <q-route-tab 
          to="/alarmas" 
          exact
          icon="fa-solid fa-clock"
          label="Remedios"
        />

        <q-route-tab 
          to="/perfil" 
          exact
          icon="fa-solid fa-user-check"
          label="Perfil"
        />

      </q-tabs>
    </q-footer>

  </q-layout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Computed seguro para ocultar el menú sin depender de si Pinia ya cargó en memoria
const rutaActual = computed(() => route.path)

const cerrarSesion = () => {
  authStore.cerrarSesion()
  router.push('/')
}
</script>

<style scoped>
/* Ajustes CSS para garantizar accesibilidad visual sin generar scroll lateral */
:deep(.q-tab__icon) {
  font-size: 26px !important; /* Íconos grandes para adultos mayores */
  margin-bottom: 2px;
}

:deep(.q-tab__label) {
  font-size: 14px !important;
  font-weight: bold;
}

.q-footer .q-tab {
  min-height: 70px; /* Área táctil suficientemente grande */
  padding: 0 4px; /* Reducimos el margen interno para que los 3 botones encajen siempre */
}
</style>