# ASIS Farmacéutica

**Sistema Integral de Asistencia Farmacéutica para Adultos Mayores**  
Puerto Montt, Región de Los Lagos, Chile

---

## Descripción

Plataforma digital (PWA) orientada a adultos mayores de Puerto Montt que permite:

- **Buscar y comparar precios** de medicamentos en farmacias cercanas (via API YAPP)
- **Programar recordatorios** de toma con confirmación explícita
- **Alertar al cuidador** si el paciente no confirma la toma en 15 minutos
- **Vincular cuidadores** mediante código de 6 caracteres
- **Funcionar sin internet** (alarmas via IndexedDB + Service Worker)

---

## Arquitectura

```
asis-farmaceutica/
├── frontend/          ← PWA (HTML + JS puro, sin framework externo)
│   ├── index.html     ← Aplicación completa
│   ├── sw.js          ← Service Worker (offline)
│   └── manifest.json  ← PWA manifest
│
├── backend/           ← FastAPI (Python 3.12)
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── medications.py   ← RF01, RF02
│   │   │   ├── alarms.py        ← RF03, RF04
│   │   │   ├── users.py         ← RF06
│   │   │   └── notifications.py ← Alertas cuidador
│   │   └── services/
│   │       └── yapp_service.py  ← Integración API YAPP
│   ├── tests/
│   │   └── test_api.py          ← 15 tests (100% pass)
│   └── requirements.txt
│
├── docker-compose.yml
└── nginx.conf
```

---

## Requerimientos Implementados

| Código | Requerimiento | Estado |
|--------|---------------|--------|
| RF01   | Búsqueda por nombre comercial o principio activo | ✅ Implementado |
| RF02   | Comparación de precios por geolocalización | ✅ Implementado |
| RF04   | Confirmación explícita de toma con botón grande | ✅ Implementado |
| RF06   | Vinculación de cuidador con código | ✅ Implementado |
| RNF01  | Tipografía ≥18pt, alto contraste, ≤3 clics | ✅ Implementado |
| RNF03  | Datos cifrados vía HTTPS (pendiente certificado en producción) | 🔄 Parcial |
| RNF04  | Módulo alarmas funciona sin internet (IndexedDB + SW) | ✅ Implementado |

---

## Puesta en Marcha


# Instalación y Configuración **Backend:**

## 🚀 Requisitos Previos
* **Python 3.12 o 3.13** instalado en tu sistema.
* Cuenta en [Supabase](https://supabase.com/) con el proyecto inicializado y las tablas creadas.

## ⚙️ Instrucciones de Instalación (Windows)

**1. Clonar el repositorio y entrar a la carpeta del backend**

```bash
git clone <url-de-tu-repo>
cd ASIS-FARMACEUTICA/backend
```

**2. Crear y activar el entorno virtual limpio**
Es estrictamente necesario crear el entorno forzando la versión estable de Python para evitar conflictos asíncronos con Playwright en Windows:
```bash
py -3.13 -m venv venv
venv\Scripts\activate
```

**3. Instalar las dependencias**
```bash
pip install -r requirements.txt
```

**4. Instalar los navegadores ocultos (Playwright)**
Este comando es obligatorio para que el bot extractor del Token de YAPP funcione:
```bash
playwright install chromium
```

**5. Configurar Variables de Entorno**
Crea un archivo llamado `.env` en la raíz de la carpeta `/backend` y añade tus credenciales:
```text
SUPABASE_URL="tu_url_de_supabase"
SUPABASE_KEY="tu_api_key_anon_de_supabase"
ENVIRONMENT="development"
```
*(Nota: Mantén `ENVIRONMENT="development"` mientras programas para usar el autómata de recarga. Cámbialo a `"production"` para ejecutar el bot de YAPP completo).*

## 🏃‍♂️ Levantar el Servidor

Para iniciar el servidor en modo desarrollo (recarga automática al guardar archivos):
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

La API interactiva (Swagger UI) estará disponible en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


# Instalación y Configuración (Frontend - Quasar PWA)

El cliente de **ASIS Farmacéutica** está construido utilizando **Quasar Framework (Vue 3 + Vite)**, optimizado para funcionar como una **Aplicación Web Progresiva (PWA)** de alta accesibilidad.

## Requisitos Previos

- **Node.js** (versión LTS recomendada, 18 o superior).
- **pnpm** instalado globalmente.

Si no tienes `pnpm`, instálalo ejecutando:

```bash
npm install -g pnpm
```

## Configuración del Entorno

### 1. Entrar a la carpeta del frontend e instalar dependencias

```bash
cd frontend
pnpm install
```

### 2. Configurar el módulo de entorno local

Para evitar conflictos con las variables de entorno de Vite en Windows y proteger las credenciales públicas de Supabase, el proyecto utiliza un archivo JavaScript local que no se sincroniza con el repositorio.

Crea un archivo llamado `env.js` dentro de `frontend/src/` y agrega las credenciales del proyecto:

```javascript
// frontend/src/env.js

export const ENV = {
  SUPABASE_URL: 'https://tu-proyecto.supabase.co',
  SUPABASE_ANON_KEY: 'tu-llave-anon-publica-aqui'
};
```

> **Nota:** El archivo `.gitignore` del proyecto ya está configurado para ignorar automáticamente `src/env.js`, por lo que tus credenciales locales no se subirán al repositorio.

## Ejecución en Desarrollo

Para iniciar el servidor de desarrollo con recarga automática (Hot Module Replacement):

```bash
pnpm dev
```

Una vez iniciado, la aplicación estará disponible en la URL mostrada por la consola (normalmente `http://localhost:9000` o similar).
---

## Configuración del Token YAPP

La API de precios requiere un token de sesión de YAPP:

1. Abre [web.yapp.cl](https://web.yapp.cl) en tu navegador
2. Presiona **F12** → pestaña **Red / Network**
3. Realiza una búsqueda
4. Busca cualquier request a `api-integration.yapp.cl`
5. Copia el valor del header **Authorization** (sin el prefijo "Bearer ")
6. En la app: ⚙️ Configuración → Token YAPP

> **Nota:** El token YAPP es de sesión anónima y expira periódicamente. La app funciona en modo demostración sin token.

---

## Tests

```bash
cd backend
pytest tests/test_api.py -v
```

**Resultado:** 15/15 tests pasando ✅

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend | HTML5 + CSS3 + JS (PWA) |
| Service Worker | Web APIs (Cache, IndexedDB, Notifications) |
| Backend | Python 3.12 + FastAPI |
| Base de Datos | PostgreSQL (Supabase) — producción |
| Infraestructura | Docker + Nginx |
| CI/CD | GitHub Actions → Render |
| Datos | API YAPP (precios en tiempo real) |

---

## Decisión de Ingeniería: API YAPP vs Web Scraping

Tras el PoC (`poc_api_yapp.py`), se eligió **integración via API YAPP** porque:

- Respuesta < 500ms (cumple RNF: < 2 segundos)
- Datos estructurados JSON (sin parsing frágil de HTML)
- Cobertura nacional de cadenas farmacéuticas
- Endpoint de geolocalización integrado

**Limitación:** El token de autenticación es de sesión y requiere renovación periódica. En producción se evaluará acuerdo con YAPP o fuente alternativa (API CENABAST, scraping como fallback).
