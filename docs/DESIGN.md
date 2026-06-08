# DESIGN.md: Sistema Integral de Asistencia Farmacéutica para Adultos Mayores

## 1. Visión General del Proyecto

El proyecto consiste en el desarrollo de una plataforma digital (Aplicación Móvil) orientada a adultos mayores en la comuna de Puerto Montt.

El objetivo principal es optimizar la adherencia terapéutica y reducir en un 20% el gasto de bolsillo mensual en salud mediante la mitigación de la asimetría de información.

El sistema soluciona dos problemas críticos derivados de las condiciones climáticas y topográficas de la zona:

- La dificultad de cotizar presencialmente de farmacia en farmacia.
- La falta de plataformas digitales con accesibilidad adecuada para la tercera edad.

---

## 2. Arquitectura del Sistema

El proyecto se estructura bajo una arquitectura cliente-servidor de tres capas:

### Capa de Presentación (Frontend)

Construida como una Aplicación Web Progresiva (PWA). Se prioriza la accesibilidad extrema y la capacidad de operar módulos críticos sin conexión a internet.

### Capa de Lógica de Negocio (Backend)

Una API RESTful que centraliza el procesamiento, los algoritmos de búsqueda aproximada para mitigar errores tipográficos y el cálculo de distancias geográficas.

### Capa de Datos (Base de Datos)

Un motor relacional encargado de almacenar perfiles de usuarios, historiales médicos y catálogos de precios de forma segura y cifrada.

---

## 3. Stack Tecnológico Definido

### Frontend
- Vue.js configurado como PWA.
- Framework UI (Vuetify o Quasar) con variables CSS sobrescritas para garantizar alto contraste y fuentes a gran escala.

### Almacenamiento Local (Offline)
- `IndexedDB` gestionado mediante librerías como `localforage` o `idb` para garantizar persistencia de datos y alarmas sin conexión a internet.

### Backend
- Python utilizando el framework FastAPI.

### Base de Datos Relacional
- PostgreSQL.

### Notificaciones Externas
- Integración de un servicio SMTP (correo electrónico) o proveedor SMS directamente en FastAPI para alertar a cuidadores.

### Infraestructura y DevOps
- Contenedores Docker para estandarizar el entorno.
- GitHub Actions para pipelines de Integración Continua y Despliegue Continuo (CI/CD).
- Render (capa gratuita) para el alojamiento del backend.
- Supabase (plan Free) para el alojamiento de la base de datos PostgreSQL.

---

## 4. Casos de Uso Principales (Core)

### UC1: Cotizar Medicamento

#### Flujo
1. El usuario ingresa un fármaco con tolerancia a errores tipográficos.
2. El sistema obtiene la ubicación GPS del dispositivo y consulta la base de datos.
3. Se despliega una lista de farmacias ordenada por cercanía y precio.

#### Restricción
- El tiempo de respuesta de la búsqueda debe ser inferior a 2 segundos.

### UC2: Configurar y Confirmar Alarma

#### Flujo
1. El usuario programa un recordatorio de toma.
2. A la hora indicada, se emite una alerta visual o sonora persistente que requiere confirmación explícita mediante un botón de gran tamaño.

#### Lógica Offline y Cuidador
1. La alarma se ejecuta localmente utilizando el reloj interno del dispositivo.
2. Si después de 15 minutos no existe confirmación de la toma, se notifica al cuidador o familiar vinculado.

---

## 5. Requerimientos Clave Innegociables

### Requerimientos Funcionales (RF)

- **RF01:** Búsqueda por nombre comercial o principio activo.
- **RF02:** Comparación de precios ordenada por geolocalización.
- **RF04:** Confirmación explícita mediante un botón en pantalla para registrar la ingesta.
- **RF06:** Vinculación de cuenta mediante un código para la supervisión remota de un cuidador.

### Requerimientos No Funcionales (RNF)

- **RNF01 (Accesibilidad):** Interfaces con tipografías mínimas de 18pt, alto contraste y flujos de navegación que no superen los 3 clics.
- **RNF03 (Seguridad):** Cifrado de datos personales e historial médico conforme a la Ley 19.628 de Protección de la Vida Privada.
- **RNF04 (Disponibilidad Offline):** El módulo de alarmas debe funcionar estrictamente sin conexión a internet.

---

## 6. Limitaciones y Supuestos Estructurales

- **Naturaleza no transaccional:** El sistema no procesará compras, pagos en línea ni administrará carritos de compra.
- **Sin logística:** No se gestionará el despacho ni reparto de medicamentos a domicilio.
- **Autonomía de Hardware:** El sistema está diseñado para ejecutarse en dispositivos móviles de gama baja o antiguos, minimizando el consumo de recursos.

---

## 7. Directrices de Desarrollo (AI Context)

### Frontend (Vue)

- Priorizar etiquetas semánticas HTML5.
- Utilizar atributos ARIA para accesibilidad.
- Implementar estilos responsivos basados en `rem` y `em`.
- Respetar el escalado de fuentes configurado por el sistema operativo del usuario.

### Backend (FastAPI)

- Mantener endpoints modulares.
- Aprovechar la documentación automática mediante OpenAPI (Swagger).
- Delegar operaciones intensivas a funciones asíncronas utilizando `async def`.

### Pruebas (Testing)

- Mantener una cobertura mínima del 80% en el backend.
- Utilizar `pytest` para pruebas unitarias e integración.