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

* [x] Crear archivo `requirements.txt`.

## Configuración de Supabase

* [x] Crear un nuevo proyecto en Supabase.
* [x] Obtener URL y API Key.
* [x] Crear archivo `.env` en backend.
* [x] Crear archivo `.env` en frontend.
* [x] Guardar credenciales en ambos entornos.

---

# FASE 1: Base de Datos y Autenticación (El Modelo)

**Objetivo:** Diseñar la persistencia de datos y el sistema de Login con RUT.

## Modelado de Tablas en Supabase

* [x] Crear tabla **paciente**.
* [x] Crear tabla **cuidador**.
* [x] Crear tabla **paciente_cuidador**.
* [x] Crear tabla **Recordatorio**.
* [x] Crear tabla **Historial_Toma**.

## Sistema de Login (RUT + Contraseña)

### Estrategia Técnica

* [x] Implementar conversión automática:

```text
12345678-9 → 12345678-9@asis.cl
```

* [x] Enviar correo generado y contraseña a Supabase Auth.

### Registro

* [x] Crear formulario de registro.
* [x] Solicitar Nombre Completo.
* [x] Solicitar RUT.
* [x] Solicitar Contraseña.

### Inicio de Sesión

* [x] Crear formulario de login.
* [x] Solicitar RUT.
* [x] Solicitar Contraseña.
* [ ] falta confirmacion de que el rut sea real chileno.
* [ ] quiza mas adelante poner correo real de confirmacion(postergar no es importante)

---

# FASE 2: Backend y Automatización (El Controlador)

**Objetivo:** Proveer las APIs de comunicación y automatizar el token de YAPP.

## Estructura MVC del Backend

* [x] Crear carpeta `/models`.
* [x] Crear carpeta `/controllers`.
* [x] Crear carpeta `/services`.

### Models

* [x] Crear esquemas Pydantic.

### Controllers

* [x] Implementar Auth.
* [x] Implementar Medicamentos.
* [x] Implementar Alarmas.

### Services

* [x] Integración Supabase.
* [x] Integración YAPP.

## Bot Autómata del Token (Playwright)

* [x] Crear archivo `/services/yapp_scraper.py`.
* [x] Ejecutar Playwright en modo Headless.
* [x] Abrir `web.yapp.cl`.
* [x] Interceptar Network Requests.
* [x] Extraer Header Authorization.
* [x] Guardar token en memoria.

### Automatización

* [x] Configurar APScheduler.
* [x] Ejecutar scraper cada 2 horas.
* [x] Renovar token automáticamente.
* [x] Validar funcionamiento sin intervención manual.

## Controladores (Endpoints REST)

* [x] Migrar buscador de medicamentos.
* [x] Migrar cotizador.
* [x] Inyectar token automáticamente en cada consulta.
* [x] Crear endpoint para guardar alarmas.
* [x] Crear endpoint para consultar alarmas.
* [ ] Integrar persistencia en Supabase.(esto postergar no es importante)

---

# FASE 3: Frontend PWA e Interfaz (La Vista)

**Objetivo:** Crear una interfaz accesible, modular y funcional offline usando Quasar.

## Diseño Inclusivo Global

* [x] Sobrescribir `quasar.variables.scss`.
* [x] Aplicar paleta de alto contraste.
* [x] Ajustar tipografía global a 18pt / 24px.
* [x] Verificar cumplimiento de RNF01.

## Desarrollo de Componentes

### LoginView.vue

* [x] Crear pantalla de autenticación.
+ [x] Falta el register.

### BuscadorMedicamentos.vue

* [x] Crear barra de búsqueda.
* [ ] Implementar autocompletado.
* [x] Conectar con API backend.

* [x] Mostrar farmacias en tarjetas.
* [x] Ordenar por precio.
* [ ] Ordenar por distancia.
* [x] Integrar geolocalización del navegador.
* [ ] Falta mas informacion que entregue de la farmacia o la cantidad que le quedan o cosas similares.

### GestorAlarmas.vue

* [x] Crear panel de alarmas.
* [x] Permitir agregar horarios.
* [x] Permitir agregar dosis.

## Persistencia Offline

### Pinia

* [x] Configurar Pinia.
* [x] Instalar plugin de persistencia local.
* [x] Persistir datos localmente.
* [ ] NO TENGO IDEA SI LO LOCAL ESTA FUNCIONANDO, hay que comprobarlo(no se como)


### Alarmas Offline

* [x] Guardar alarmas en almacenamiento local.
* [ ] Recuperar alarmas al reiniciar la aplicación.

### Notificaciones

* [x] Configurar Service Worker de Quasar.
* [x] Solicitar permisos de notificación.
* [x] Implementar notificaciones nativas.
* [x] Mostrar alerta:

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
