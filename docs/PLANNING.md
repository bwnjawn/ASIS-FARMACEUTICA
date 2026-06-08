# Planning del Proyecto

## Fase 1: Pruebas de Concepto (PoC) y Setup Arquitectónico

**Objetivo:** Despejar la mayor incógnita del proyecto (los datos) y preparar el entorno de trabajo.

### PoC 1: Extracción vía Web Scraping
- [ ] Crear un script rápido en Python utilizando BeautifulSoup o Playwright.
- [ ] Extraer precios y disponibilidad desde dos páginas de farmacias de Puerto Montt.
- [ ] Evaluar la estructura del DOM.
- [ ] Medir tiempos de respuesta.
- [ ] Analizar la presencia de bloqueos antibot.

### PoC 2: Extracción vía APIs Existentes
- [ ] Investigar e interceptar respuestas de red de portales gubernamentales o aplicaciones como YAPP.
- [ ] Identificar endpoints disponibles.
- [ ] Crear un script en Python para consumir los endpoints detectados.
- [ ] Evaluar la estructura de los datos JSON.
- [ ] Analizar la estabilidad de las conexiones.

### Decisión de Ingeniería
- [ ] Realizar reunión de análisis de resultados.
- [ ] Comparar ventajas y desventajas de cada enfoque.
- [ ] Definir la fuente de datos definitiva.

### Configuración del Repositorio
- [ ] Inicializar repositorio en GitHub.
- [ ] Configurar estructura monorepo.
  - [ ] Carpeta `frontend`.
  - [ ] Carpeta `backend`.

### Contenerización Local
- [ ] Crear `Dockerfile` para FastAPI.
- [ ] Crear archivo `docker-compose.yml`.
- [ ] Configurar backend local.
- [ ] Configurar base de datos PostgreSQL de prueba.

---

## Fase 2: Infraestructura Cloud y CI/CD

**Objetivo:** Automatizar despliegues y configurar la infraestructura en capas gratuitas.

### Setup de Base de Datos (Supabase)
- [ ] Crear cuenta en Supabase.
- [ ] Crear proyecto en plan Free.
- [ ] Obtener credenciales de conexión PostgreSQL.

### Setup del Servidor (Render)
- [ ] Crear servicio Web Service en Render.
- [ ] Vincular repositorio de GitHub.
- [ ] Configurar despliegue inicial.

### Pipelines de Integración Continua (GitHub Actions)
- [ ] Crear workflow YAML.
- [ ] Ejecutar validaciones automáticas en Push.
- [ ] Ejecutar validaciones automáticas en Pull Request.
- [ ] Configurar linting con Ruff.

### Pipelines de Despliegue Continuo (CI/CD)
- [ ] Configurar despliegue automático al hacer merge en `main`.
- [ ] Construir imagen Docker automáticamente.
- [ ] Desplegar aplicación automáticamente en Render.

---

## Fase 3: Desarrollo del Backend (API RESTful en FastAPI)

**Objetivo:** Construir el núcleo lógico de la aplicación y las integraciones de datos.

### Modelamiento de la Base de Datos
- [ ] Diseñar esquema de PostgreSQL.
- [ ] Crear tabla `Usuarios`.
- [ ] Crear tabla `Cuidadores`.
- [ ] Crear tabla `Medicamentos`.
- [ ] Crear tabla `HistorialMedico`.
- [ ] Implementar cifrado de datos conforme a la Ley 19.628.
- [ ] Ejecutar migraciones iniciales.

### Endpoint de Búsqueda y Cotización (UC1)
- [ ] Crear endpoint de búsqueda de medicamentos.
- [ ] Implementar búsqueda aproximada para corrección de errores tipográficos.
- [ ] Integrar fuente de datos seleccionada.
- [ ] Retornar lista de precios disponibles.

### Integración de Geolocalización
- [ ] Implementar cálculo de distancias utilizando la fórmula de Haversine.
- [ ] Ordenar resultados desde la farmacia más cercana a la más lejana.

### Sistema de Notificaciones (UC2)
- [ ] Seleccionar proveedor de correo o SMS.
- [ ] Configurar SMTP (SendGrid o Mailgun) o proveedor SMS (Twilio).
- [ ] Crear endpoint para alertas de inactividad.
- [ ] Detectar ausencia de confirmación durante 15 minutos.
- [ ] Enviar alerta a familiar o cuidador vinculado.

### Pruebas de Backend
- [ ] Configurar Pytest.
- [ ] Crear pruebas unitarias para endpoints.
- [ ] Verificar tiempos de respuesta inferiores a 2 segundos (RNF02).
- [ ] Automatizar ejecución de pruebas.

---

## Fase 4: Desarrollo del Frontend (PWA con Vue.js)

**Objetivo:** Construir una interfaz accesible y funcional sin conexión.

### Setup de Vue PWA y Framework UI
- [ ] Inicializar proyecto Vue.js con soporte PWA.
- [ ] Instalar framework UI seleccionado.
  - [ ] Quasar.
  - [ ] O Vuetify.

### Sistema de Diseño Inclusivo (RNF01)
- [ ] Configurar tipografías con tamaño mínimo de 18pt.
- [ ] Ajustar contrastes según normativa W3C.
- [ ] Personalizar variables CSS del framework.

### Módulo de Cotización (UC1)
- [ ] Construir vista de búsqueda.
- [ ] Construir vista de resultados.
- [ ] Integrar API de cotización.
- [ ] Solicitar permisos de geolocalización mediante la API nativa del navegador.

### Motor Offline y Base de Datos Local
- [ ] Implementar IndexedDB mediante localforage o idb.
- [ ] Sincronizar catálogo básico de medicamentos.
- [ ] Almacenar alarmas localmente.
- [ ] Garantizar funcionamiento sin internet (RNF04).

### Módulo de Alarmas y Recordatorios (UC2)
- [ ] Implementar temporizadores con reloj interno del dispositivo.
- [ ] Diseñar botón de gran tamaño para "Confirmar Toma".
- [ ] Registrar confirmaciones en IndexedDB.
- [ ] Detectar ausencia de confirmación durante 15 minutos.
- [ ] Sincronizar eventos pendientes al recuperar conexión.
- [ ] Invocar API de notificaciones de FastAPI cuando corresponda.

---

## Fase 5: Validación, Piloto y Cierre

**Objetivo:** Validar el sistema en un entorno real y completar la entrega académica.

### Testing Interno
- [ ] Ejecutar pruebas en modo completamente offline.
- [ ] Simular paso del tiempo para verificar alarmas.
- [ ] Verificar persistencia de IndexedDB.
- [ ] Validar recuperación de sincronización al reconectar internet.

### Pruebas Piloto Presenciales
- [ ] Organizar sesiones de usabilidad con adultos mayores en Puerto Montt.
- [ ] Utilizar presupuesto estimado de $200.000.
- [ ] Observar interacción con flujos de menos de 3 clics.
- [ ] Registrar observaciones y dificultades detectadas.

### Evaluación de Métrica SUS
- [ ] Aplicar encuesta SUS.
- [ ] Analizar resultados obtenidos.
- [ ] Alcanzar puntaje objetivo superior a 70/100.

### Ajustes Finales
- [ ] Incorporar mejoras derivadas de las pruebas piloto.
- [ ] Corregir problemas de accesibilidad detectados.
- [ ] Optimizar experiencia visual y cognitiva.

### Despliegue de Producción (Hito Final)
- [ ] Compilar versión final de la PWA.
- [ ] Realizar despliegue de producción.
- [ ] Redactar manual de usuario.
- [ ] Redactar documentación técnica.
- [ ] Preparar informe de cierre.
- [ ] Preparar presentación final para finales de junio.