// frontend/src/router/routes.js

const routes = [
  {
    path: '/',
    // Usamos ../ para retroceder una carpeta desde /router y entrar a /layouts
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      // Ruta por defecto: El Login
      { path: '', component: () => import('../pages/LoginView.vue') },
      
      // Rutas futuras para las pestañas de la barra inferior
      { path: 'buscar', component: () => import('../pages/IndexPage.vue') },
      { path: 'alarmas', component: () => import('../pages/MisRemediosView.vue') },
      { path: 'nueva-alarma', component: () => import('../pages/NuevaAlarmaView.vue') },
      { path: 'perfil', component: () => import('../pages/IndexPage.vue') }
    ]
  },

  // Captura de errores 404
  {
    path: '/:catchAll(.*)*',
    component: () => import('../pages/ErrorNotFound.vue')
  }
]

export default routes