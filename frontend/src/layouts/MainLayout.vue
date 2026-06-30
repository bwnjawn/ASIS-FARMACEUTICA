<template>
  <q-layout view="hHh lpR fFf">
    
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title class="text-center text-weight-bold q-py-sm">
          ASIS Farmacéutica
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer bordered class="bg-white text-primary">
      <q-tabs
        no-caps
        active-color="primary"
        indicator-color="transparent"
        class="text-grey-8"
        align="justify"
      >
        <q-route-tab 
          to="/buscar" 
          exact
        >
          <q-icon name="fa-solid fa-magnifying-glass" size="md" />
          <span class="q-mt-xs text-weight-bold">Buscar Precios</span>
        </q-route-tab>

        <q-route-tab 
          to="/alarmas" 
          exact
        >
          <q-icon name="fa-solid fa-clock" size="md" />
          <span class="q-mt-xs text-weight-bold">Mis Remedios</span>
        </q-route-tab>

        <q-route-tab 
          to="/perfil" 
          exact
        >
          <q-icon name="fa-solid fa-user-check" size="md" />
          <span class="q-mt-xs text-weight-bold">Mi Perfil</span>
        </q-route-tab>

      </q-tabs>
    </q-footer>

  </q-layout>
</template>

<script setup>
// Layout base ultra simplificado. 
// No necesitamos estado reactivo aquí por ahora.
</script>

<style scoped>
/* Aumentamos un poco el tamaño de la barra inferior para que sea fácil de tocar */
.q-footer .q-tab {
  min-height: 80px;
}
</style>