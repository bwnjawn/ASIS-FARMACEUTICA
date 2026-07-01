// frontend/src/router/routes.js

const routes = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      // Ruta por defecto: El Login
      { path: '', component: () => import('../pages/LoginView.vue') },
      
      // Módulo de Cotización de YAPP
      { path: 'buscar', component: () => import('../pages/BuscadorMedicamentos.vue') },
      
      // Módulo de Alarmas Offline
      { path: 'alarmas', component: () => import('../pages/MisRemediosView.vue') },
      
      // Formulario para nueva alarma
      { path: 'nueva-alarma', component: () => import('../pages/NuevaAlarmaView.vue') },
      
      // Ruta futura (puedes dejar IndexPage temporalmente o crear PerfilView)
      { path: 'perfil', component: () => import('../pages/MiPerfil.vue') }
    ]
  },

  // Captura de errores 404
  {
    path: '/:catchAll(.*)*',
    component: () => import('../pages/ErrorNotFound.vue')
  }
]

export default routes