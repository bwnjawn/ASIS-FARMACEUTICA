// frontend/src/stores/index.js
import { store } from 'quasar/wrappers'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate' // 1. Importamos el plugin

export default store((/* { ssrContext } */) => {
  const pinia = createPinia()

  // 2. Le decimos a Pinia que use el plugin en toda la app
  pinia.use(piniaPluginPersistedstate)

  return pinia
})