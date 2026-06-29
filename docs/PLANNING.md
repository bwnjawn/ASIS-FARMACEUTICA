# PLANNING V2: Reestructuración Arquitectónica MVC

## Visión General de la Arquitectura

* [ ] **Modelo (Datos):** Supabase (PostgreSQL + Supabase Auth).
* [ ] **Vista (Frontend):** Quasar Framework (Vue.js 3) configurado como PWA.
* [ ] **Controlador (Backend):** FastAPI (Python) manejando la lógica de negocio y el scraping automático con Playwright.
* [ ] **Despliegue:** Vercel (Frontend) y Render (Backend) para acceso público mediante URL.

---

# FASE 0: Preparación del Entorno desde Cero

**Objetivo:** Inicializar las herramientas, repositorios y dependencias base para un desarrollo limpio.

## Limpieza y Nueva Rama

* [x] Crear la rama `refactor/mvc` en Git.
* [x] Crear dos carpetas principales en la raíz del proyecto: `/backend` y `/frontend`.

## Inicialización del Frontend (Quasar + Vue.js)

* [x] Instalar dependencias de Node.js:

```bash
npm install -g @quasar/cli pnpm
```

* [x] Ejecutar:

```bash
pnpm create quasar
```

* [x] Configurar:

  * [x] App with Quasar CLI
  * [x] Vue 3
  * [x] Vite
  * [x] Pinia
  * [x] PWA Mode

## Inicialización del Backend (FastAPI)

* [x] Navegar a `/backend`.
* [x] Crear entorno virtual:

```bash
python -m venv venv
```

* [x] Activar entorno virtual:

**Linux/Mac**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

* [x] Instalar dependencias:

```bash
pip install fastapi uvicorn supabase playwright apscheduler python-dotenv
```

* [x] Instalar Chromium para Playwright:

```bash
playwright install chromium
```

* [ ] Crear archivo `requirements.txt`.

## Configuración de Supabase

* [x] Crear un nuevo proyecto en Supabase.
* [x] Obtener URL y API Key.
* [x] Crear archivo `.env` en backend.
* [ ] Crear archivo `.env` en frontend.
* [ ] Guardar credenciales en ambos entornos.

---

# FASE 1: Base de Datos y Autenticación (El Modelo)

**Objetivo:** Diseñar la persistencia de datos y el sistema de Login con RUT.

## Modelado de Tablas en Supabase

* [ ] Crear tabla **Perfiles**.
* [ ] Crear tabla **Cuidadores**.
* [ ] Crear tabla **Vinculos**.
* [ ] Crear tabla **Recordatorios**.
* [ ] Crear tabla **Historial_Tomas**.

## Sistema de Login (RUT + Contraseña)

### Estrategia Técnica

* [ ] Implementar conversión automática:

```text
12345678-9 → 12345678-9@asis.cl
```

* [ ] Enviar correo generado y contraseña a Supabase Auth.

### Registro

* [ ] Crear formulario de registro.
* [ ] Solicitar Nombre Completo.
* [ ] Solicitar RUT.
* [ ] Solicitar Contraseña.

### Inicio de Sesión

* [ ] Crear formulario de login.
* [ ] Solicitar RUT.
* [ ] Solicitar Contraseña.

---

# FASE 2: Backend y Automatización (El Controlador)

**Objetivo:** Proveer las APIs de comunicación y automatizar el token de YAPP.

## Estructura MVC del Backend

* [ ] Crear carpeta `/models`.
* [ ] Crear carpeta `/controllers`.
* [ ] Crear carpeta `/services`.

### Models

* [ ] Crear esquemas Pydantic.

### Controllers

* [ ] Implementar Auth.
* [ ] Implementar Medicamentos.
* [ ] Implementar Alarmas.

### Services

* [ ] Integración Supabase.
* [ ] Integración YAPP.

## Bot Autómata del Token (Playwright)

* [ ] Crear archivo `/services/yapp_scraper.py`.
* [ ] Ejecutar Playwright en modo Headless.
* [ ] Abrir `web.yapp.cl`.
* [ ] Interceptar Network Requests.
* [ ] Extraer Header Authorization.
* [ ] Guardar token en memoria.

### Automatización

* [ ] Configurar APScheduler.
* [ ] Ejecutar scraper cada 2 horas.
* [ ] Renovar token automáticamente.
* [ ] Validar funcionamiento sin intervención manual.

## Controladores (Endpoints REST)

* [ ] Migrar buscador de medicamentos.
* [ ] Migrar cotizador.
* [ ] Inyectar token automáticamente en cada consulta.
* [ ] Crear endpoint para guardar alarmas.
* [ ] Crear endpoint para consultar alarmas.
* [ ] Integrar persistencia en Supabase.

---

# FASE 3: Frontend PWA e Interfaz (La Vista)

**Objetivo:** Crear una interfaz accesible, modular y funcional offline usando Quasar.

## Diseño Inclusivo Global

* [ ] Sobrescribir `quasar.variables.scss`.
* [ ] Aplicar paleta de alto contraste.
* [ ] Ajustar tipografía global a 18pt / 24px.
* [ ] Verificar cumplimiento de RNF01.

## Desarrollo de Componentes

### LoginView.vue

* [ ] Crear pantalla de autenticación.

### BuscadorMedicamentos.vue

* [ ] Crear barra de búsqueda.
* [ ] Implementar autocompletado.
* [ ] Conectar con API backend.

### CotizadorView.vue

* [ ] Mostrar farmacias en tarjetas.
* [ ] Ordenar por precio.
* [ ] Ordenar por distancia.
* [ ] Integrar geolocalización del navegador.

### GestorAlarmas.vue

* [ ] Crear panel de alarmas.
* [ ] Permitir agregar horarios.
* [ ] Permitir agregar dosis.

## Persistencia Offline

### Pinia

* [ ] Configurar Pinia.
* [ ] Instalar plugin de persistencia local.
* [ ] Persistir datos localmente.

### Alarmas Offline

* [ ] Guardar alarmas en almacenamiento local.
* [ ] Recuperar alarmas al reiniciar la aplicación.

### Notificaciones

* [ ] Configurar Service Worker de Quasar.
* [ ] Solicitar permisos de notificación.
* [ ] Implementar notificaciones nativas.
* [ ] Mostrar alerta:

```text
¡Hora de tomar tu medicamento!
```

* [ ] Verificar funcionamiento sin internet.

---

# FASE 4: Despliegue Público (Exposición y Testing Real)

**Objetivo:** Hacer accesible la aplicación mediante un enlace web desde cualquier dispositivo.

## Backend (Render)

* [ ] Crear Web Service en Render.
* [ ] Conectar carpeta `/backend`.
* [ ] Configurar variables de entorno.
* [ ] Instalar dependencias.
* [ ] Ejecutar:

```bash
playwright install-deps
```

* [ ] Validar funcionamiento del scraper.

## Frontend (Vercel o Netlify)

* [ ] Conectar carpeta `/frontend`.
* [ ] Configurar variables de entorno.
* [ ] Apuntar a URL productiva del backend.
* [ ] Verificar despliegue correcto.

## Validación Final

* [ ] Obtener URL pública.
* [ ] Probar login.
* [ ] Probar búsqueda.
* [ ] Probar cotización.
* [ ] Probar alarmas.
* [ ] Probar modo PWA.
* [ ] Probar instalación en Android.
* [ ] Probar instalación en iPhone.

### Resultado Esperado

* [ ] Aplicación accesible mediante:

```text
https://asis-farmaceutica.vercel.app
```

* [ ] Permitir agregar a pantalla de inicio.
* [ ] Comportamiento similar a aplicación nativa.

---

# FASE 5: Validaciones y Funciones Post-MVP

**Objetivo:** Implementar funcionalidades secundarias una vez que el flujo principal esté completamente estable.

## Vínculo Cuidador–Paciente

* [ ] Diseñar lógica de código de 6 dígitos.
* [ ] Crear generación de códigos.
* [ ] Crear validación de códigos.
* [ ] Crear relación cuidador-paciente en Supabase.

## Notificaciones Reales (Postergado)

* [ ] Evaluar Twilio.
* [ ] Evaluar SendGrid.
* [ ] Integrar proveedor seleccionado.
* [ ] Detectar 15 minutos sin respuesta.
* [ ] Disparar alerta a terceros.
* [ ] Registrar eventos en backend.
* [ ] Realizar pruebas de funcionamiento.
