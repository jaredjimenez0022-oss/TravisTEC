# Jarvis TEC 🤖# Jarvis TEC 🤖



Asistente inteligente con reconocimiento facial y procesamiento de voz para el TEC.Asistente inteligente con reconocimiento facial y procesamiento de voz para el TEC.



## ✅ Cumplimiento de Requisitos## 📁 Estructura del Proyecto



### Frontend & DevOps```

- ✅ **Scaffold React app con rutas**: `/`, `/capture`, `/results` implementado con React Router/jarvis-tec/

- ✅ **Componente de cámara (snapshot)**: `CameraCapture` con captura automática y manual  /frontend/                -> Persona B (Desarrollo Web)

- ✅ **Grabador de audio**: `AudioRecorder` con Web Speech API y MediaRecorder    /public/

- ✅ **Componentes UI**: `EmotionDisplay` para emociones y logs de transcripciones    /src/

- ✅ **api-client.js configurable**: Soporte .env con mock/backend real      index.html           # Interfaz principal

- ✅ **docker-compose.yml**: Frontend + Backend + Mock Server + DB stub      main.js              # Lógica: cámara + audio + parser + api-client

- ✅ **Colección Postman**: Endpoints documentados con ejemplos      api-client.js        # Cliente para comunicarse con backend

- ✅ **Página demo E2E**: Flujo completo con respuestas simuladas      styles.css           # Estilos

    package.json

### Objetivos del Proyecto    Dockerfile

    

#### OBJETIVO 1: Reconocimiento de Emociones  /backend/                 -> Persona A (ML & Backend)

- ✅ **Backend**: Azure Face API + fallback local para detectar emociones    app.py                  # FastAPI - API principal

- ✅ **Frontend**: Stream de imágenes cada 2s y visualización en tiempo real    /services/

      azure_face.py         # Servicio de Azure Face API

#### OBJETIVO 2: Procesamiento de Voz      model_runner.py       # Carga y ejecuta modelos entrenados

- ✅ **Backend**: Recibe comandos y devuelve respuestas procesadas con ML      stt_service.py        # Speech-to-Text (Azure/Google/Whisper)

- ✅ **Frontend**: Audio → Texto → Backend → Mostrar respuesta    /models/                # Modelos entrenados (.joblib, .pkl)

    requirements.txt

---    Dockerfile

    .env.example

## 📁 Estructura del Proyecto    

  /notebooks/               -> Persona A (Entrenamiento)

```    01_data_exploration.ipynb

/TravisTEC/    02_model_training.ipynb

  /frontend-react/          ⭐ Frontend React con Vite    

    /src/  docker-compose.yml

      /pages/  .gitignore

        Home.jsx            # Página principal (/)  README.md

        Capture.jsx         # Captura en tiempo real (/capture)```

        Results.jsx         # Visualización de resultados (/results)

      /components/## 🚀 Inicio Rápido

        CameraCapture.jsx   # Componente de cámara

        AudioRecorder.jsx   # Grabador de audio### Requisitos Previos

        EmotionDisplay.jsx  # Visualización de emociones

      /services/- Python 3.10+

        api-client.js       # Cliente API configurable- Node.js 18+ (para frontend)

      App.jsx               # Router principal- Docker y Docker Compose (opcional)

      main.jsx- Azure Cognitive Services (Face API y Speech Services)

    .env                    # Variables de entorno

    .env.example### Configuración Backend (Persona A)

    Dockerfile

    package.json1. **Navegar al directorio backend:**

       ```bash

  /backend/                 # FastAPI + ML + Azure   cd backend

    app.py   ```

    /services/

      azure_face.py2. **Crear entorno virtual:**

      model_runner.py   ```bash

      stt_service.py   python -m venv venv

      emotion_local.py   venv\Scripts\activate  # Windows

    /models/                # Modelos .joblib/.pkl   ```

    /datasets/

    /scripts/3. **Instalar dependencias:**

    requirements.txt   ```bash

    Dockerfile   pip install -r requirements.txt

       ```

  /mock-server/             ⭐ Mock API para desarrollo

    server.js               # Express server con endpoints mock4. **Configurar variables de entorno:**

    package.json   ```bash

    Dockerfile   cp .env.example .env

       # Editar .env con tus credenciales de Azure

  /postman/                 ⭐ Colección Postman   ```

    Jarvis_TEC_API.postman_collection.json

    5. **Ejecutar servidor:**

  /notebooks/   ```bash

    01_data_exploration.ipynb   python app.py

    02_model_training.ipynb   ```

    

  docker-compose.yml        ⭐ Orquestación completa   El backend estará disponible en: `http://localhost:8000`

  README.md

```### Configuración Frontend (Persona B)



---1. **Navegar al directorio frontend:**

   ```bash

## 🚀 Inicio Rápido   cd frontend

   ```

### Opción 1: Docker Compose (Recomendado)

2. **Instalar dependencias:**

```powershell   ```bash

# Clonar el repositorio   npm install

git clone https://github.com/jaredjimenez0022-oss/TravisTEC.git   ```

cd TravisTEC

3. **Ejecutar servidor de desarrollo:**

# Configurar variables de entorno   ```bash

cp backend/.env.example backend/.env   npm run dev

# Editar backend/.env con tus credenciales de Azure   ```



# Levantar todos los servicios   El frontend estará disponible en: `http://localhost:3000`

docker-compose up --build

```### Usar Docker Compose (Ambos)



**Servicios disponibles:**```bash

- Frontend React: http://localhost:3000docker-compose up --build

- Backend (real): http://localhost:8000```

- Mock Server: http://localhost:3001

- PostgreSQL: localhost:5432## 📋 Tareas por Persona



### Opción 2: Desarrollo Local### Persona A - Backend & Machine Learning



#### Frontend React- ✅ Configurar Azure Face API y Speech Services

- ✅ Implementar endpoints FastAPI

```powershell- ✅ Entrenar modelos de ML en notebooks

cd frontend-react- ✅ Implementar `model_runner.py` para cargar modelos

- ✅ Configurar servicio STT (Speech-to-Text)

# Instalar dependencias- 📝 Crear y entrenar modelos personalizados

npm install- 📝 Optimizar rendimiento de reconocimiento



# Configurar .env### Persona B - Frontend

# VITE_API_URL=http://localhost:8000

# VITE_USE_MOCK=false  # Cambiar a true para usar mock- ✅ Diseñar interfaz HTML/CSS

- ✅ Implementar captura de cámara y audio

# Iniciar servidor de desarrollo- ✅ Crear cliente API (`api-client.js`)

npm run dev- ✅ Implementar visualización de resultados

```- 📝 Mejorar UX/UI

- 📝 Agregar notificaciones y feedback visual

Acceder a: http://localhost:3000

## 🔧 Configuración de Azure

#### Backend

### Azure Face API

```powershell

cd backend1. Crear recurso Face en Azure Portal

2. Obtener Key y Endpoint

# Crear entorno virtual3. Configurar en `.env`:

python -m venv venv   ```

.\venv\Scripts\Activate.ps1   AZURE_FACE_KEY=tu_key_aqui

   AZURE_FACE_ENDPOINT=https://tu-recurso.cognitiveservices.azure.com/

# Instalar dependencias   ```

pip install -r requirements.txt

### Azure Speech Services

# Configurar .env con credenciales Azure

copy .env.example .env1. Crear recurso Speech en Azure Portal

# Editar .env2. Obtener Key y Region

3. Configurar en `.env`:

# Ejecutar servidor   ```

python app.py   AZURE_SPEECH_KEY=tu_key_aqui

```   AZURE_SERVICE_REGION=tu_region_aqui

   ```

Acceder a: http://localhost:8000/docs

## 📚 Endpoints de la API

#### Mock Server (para desarrollo sin Azure)

### `POST /api/transcribe`

```powershellTranscribe audio a texto.

cd mock-server- **Input:** Archivo de audio (webm)

- **Output:** `{ "transcription": "texto" }`

# Instalar dependencias

npm install### `POST /api/recognize-face`

Reconoce rostro en imagen.

# Iniciar servidor- **Input:** Imagen (jpg/png)

npm start- **Output:** `{ "identified": true/false, "name": "...", ... }`

```

### `POST /api/process`

Acceder a: http://localhost:3001Procesa comando de texto con modelo ML.

- **Input:** `{ "text": "comando" }`

---- **Output:** `{ "response": "respuesta" }`



## 🎯 Rutas del Frontend### `POST /api/v1/bmi` (nuevo)

Calcula IMC o estima BodyFat usando el modelo entrenado `bmi_model` si está disponible.

### `/` - Home- **Input:** JSON `{ "height": <meters>, "weight": <kg>, "age": <years> }`

Página principal con:- **Output (modelo):** `{ "bodyfat": <percent>, "units": "%", "method": "bmi_model" }`

- Hero section con descripción- **Output (fórmula):** `{ "bmi": <kg/m2>, "units": "kg/m2", "method": "formula" }`

- Cards de características principales

- CTAs a Capture y Results### `POST /api/v1/face/sentiment` (local fallback)

- Información del flujo de trabajoDevuelve la emoción detectada usando el detector local (heurístico Haar-cascade).

- **Input:** multipart/form-data con campo `image` (jpg/png/webp)

### `/capture` - Captura en Tiempo Real- **Output:** `{ "dominant_emotion": "happiness|neutral|no_face", "face_count": n, "details": {...} }`

- ✅ Control de inicio/detención del sistema

- ✅ Cámara con captura automática cada 2s## 🧪 Comandos rápidos (smoke tests)

- ✅ Botón de snapshot manualDesde `backend/` puedes ejecutar los scripts de prueba rápidos:

- ✅ Grabación de audio continua (Web Speech API + MediaRecorder)

- ✅ Visualización de emociones en tiempo real- Ejecutar detector de emoción simple:

- ✅ Logs de actividad codificados por colores```powershell

- ✅ Preview de última foto capturadapython scripts\run_smoke_emotion_simple.py

```

### `/results` - Resultados

- ✅ Estadísticas de la sesión (total, éxitos, errores)- Entrenar y guardar modelo BMI (usa `backend/datasets/bodyfat.csv`):

- ✅ Última emoción detectada con gráficos```powershell

- ✅ Registro completo de eventospython scripts\train_bmi_model.py

- ✅ Navegación rápida a nueva captura```



---- Probar el modelo BMI guardado:

```powershell

## 🔌 API Endpointspython scripts\run_smoke_bmi.py

```

### Health Check

```http- Listar modelos cargados en tiempo de ejecución (usa Python REPL en `backend/`):

GET /api/health```powershell

```python -c "import sys; sys.path.insert(0, 'backend'); from services import model_runner as mr; print(list(mr._runner.models.keys()))"

```

**Respuesta:**

```jsonEstas herramientas te permiten verificar rápidamente las funcionalidades sin iniciar el servidor.

{

  "status": "healthy",### `GET /api/health`

  "timestamp": "2025-10-15T12:00:00Z",Verifica estado del sistema.

  "services": {- **Output:** `{ "status": "healthy", "services": {...} }`

    "face_api": "available",

    "speech_api": "available",## 🧪 Notebooks de Entrenamiento

    "ml_models": "loaded"

  }Los notebooks en `/notebooks/` contienen:

}

```1. **01_data_exploration.ipynb**: Análisis exploratorio de datos

2. **02_model_training.ipynb**: Entrenamiento de modelos

### Reconocimiento Facial y Emociones

```httpPara usar los notebooks:

POST /api/v1/face/sentiment```bash

Content-Type: multipart/form-datacd notebooks

jupyter notebook

image: <archivo de imagen>```

```

## 🐳 Docker

**Respuesta:**

```json### Construir imágenes:

{```bash

  "dominant_emotion": "happiness",docker-compose build

  "face_detected": true,```

  "face_count": 1,

  "attributes": {### Ejecutar servicios:

    "emotion": {```bash

      "happiness": 0.85,docker-compose up

      "sadness": 0.05,```

      "anger": 0.03,

      "surprise": 0.04,### Detener servicios:

      "neutral": 0.03```bash

    }docker-compose down

  }```

}

```## 🤝 Colaboración



### Transcripción de Audio- **Persona A**: Enfocado en backend, ML y servicios de Azure

```http- **Persona B**: Enfocado en frontend, UX/UI y integración de API

POST /api/v1/transcribe

Content-Type: multipart/form-data### Workflow sugerido:



audio: <archivo de audio .webm>1. Persona A desarrolla y prueba endpoints

```2. Persona B consume endpoints desde frontend

3. Ambos prueban integración completa

**Respuesta:**4. Iteración y mejoras continuas

```json

{## 📝 Notas

  "transcription": "TravisTEC predice el precio de Bitcoin",

  "confidence": 0.95,- Los modelos entrenados (`.joblib`, `.pkl`) no se suben a Git (ver `.gitignore`)

  "language": "es-ES",- Compartir modelos vía Google Drive o similar

  "duration_ms": 2500- Las credenciales de Azure deben mantenerse en `.env` (no subir a Git)

}

```## 🔗 Enlaces Útiles



### Procesamiento de Comandos- [FastAPI Docs](https://fastapi.tiangolo.com/)

```http- [Azure Face API Docs](https://docs.microsoft.com/en-us/azure/cognitive-services/face/)

POST /api/v1/command/execute- [Azure Speech Services Docs](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)

Content-Type: application/json- [MDN Web APIs](https://developer.mozilla.org/en-US/docs/Web/API)



{## 📄 Licencia

  "text": "predice bitcoin",

  "task": "bitcoin",MIT License - Ver archivo LICENSE para más detalles.

  "params": { "years": 5 }

}---

```

**Desarrollado por el equipo Jarvis TEC** 🚀
**Respuesta:**
```json
{
  "response": "El precio de Bitcoin en los próximos 5 años...",
  "task": "bitcoin",
  "params": { "years": 5 },
  "processed_at": "2025-10-15T12:00:00Z",
  "confidence": 0.92
}
```

### Calcular BMI
```http
POST /api/v1/bmi
Content-Type: application/json

{
  "height": 1.75,
  "weight": 70,
  "age": 30
}
```

**Respuesta:**
```json
{
  "bmi": 22.86,
  "bodyfat": 18.35,
  "units": "kg/m²",
  "method": "bmi_model",
  "height": 1.75,
  "weight": 70,
  "age": 30
}
```

**📮 Ver colección completa:** `/postman/Jarvis_TEC_API.postman_collection.json`

---

## 🧪 Modo Mock vs Real

### Usar Mock Server (desarrollo/testing sin Azure)

1. **Frontend React** - Editar `frontend-react/.env`:
```env
VITE_USE_MOCK=true
VITE_MOCK_API_URL=http://localhost:3001
```

2. **Iniciar mock server**:
```powershell
cd mock-server
npm start
```

3. **Iniciar frontend**:
```powershell
cd frontend-react
npm run dev
```

El mock devuelve respuestas simuladas sin necesitar Azure ni modelos ML.

### Usar Backend Real

1. **Frontend React** - Editar `frontend-react/.env`:
```env
VITE_USE_MOCK=false
VITE_API_URL=http://localhost:8000
```

2. **Configurar Azure** en `backend/.env`:
```env
AZURE_FACE_KEY=tu_key_aqui
AZURE_FACE_ENDPOINT=https://tu-recurso.cognitiveservices.azure.com/
AZURE_SPEECH_KEY=tu_key_aqui
AZURE_SERVICE_REGION=eastus
```

3. **Entrenar modelos ML** (opcional):
```powershell
cd backend
python scripts/train_bmi_model.py
```

---

## 🧠 Componentes React

### `<CameraCapture />`
Componente de captura de cámara con snapshot manual y automático.

```jsx
import CameraCapture from './components/CameraCapture';

<CameraCapture 
  isActive={true}
  onSnapshot={(imageBlob) => {
    // Manejar snapshot manual
  }}
  onEmotionDetected={(imageBlob) => {
    // Enviar al backend para análisis
  }}
/>
```

**Props:**
- `isActive` (boolean): Control de encendido/apagado
- `onSnapshot` (function): Callback para foto manual
- `onEmotionDetected` (function): Callback para captura automática

### `<AudioRecorder />`
Grabador de audio con Web Speech API y MediaRecorder fallback.

```jsx
import AudioRecorder from './components/AudioRecorder';

<AudioRecorder 
  isActive={true}
  onTranscription={(text) => {
    // Texto reconocido localmente
  }}
  onCommand={(parsedCommand) => {
    // Comando parseado con parámetros
  }}
/>
```

**Props:**
- `isActive` (boolean): Control de grabación
- `onTranscription` (function): Texto transcrito
- `onCommand` (function): Comando con palabra clave detectado

### `<EmotionDisplay />`
Visualización de emociones con barra de progreso y emoji dominante.

```jsx
import EmotionDisplay from './components/EmotionDisplay';

<EmotionDisplay 
  emotions={{
    happiness: 0.85,
    neutral: 0.10,
    sadness: 0.05
  }}
/>
```

**Props:**
- `emotions` (object): Diccionario de emociones y valores (0-1)

---

## 📦 Configuración de Azure

### Azure Face API

1. **Crear recurso:**
   - Ir a Azure Portal
   - Crear "Face" en Cognitive Services
   - Seleccionar región y pricing tier

2. **Obtener credenciales:**
   - Key 1 o Key 2
   - Endpoint URL

3. **Configurar en `backend/.env`:**
```env
AZURE_FACE_KEY=1234567890abcdef1234567890abcdef
AZURE_FACE_ENDPOINT=https://jarvis-tec-face.cognitiveservices.azure.com/
```

### Azure Speech Services

1. **Crear recurso Speech:**
   - Azure Portal → Speech Services
   - Seleccionar región

2. **Configurar:**
```env
AZURE_SPEECH_KEY=abcdef1234567890abcdef1234567890
AZURE_SERVICE_REGION=eastus
STT_SERVICE=azure
```

**Alternativas:** Google Cloud Speech, Whisper local

---

## 🐳 Docker Compose

### Servicios Incluidos

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **backend** | 8000 | FastAPI + ML + Azure |
| **frontend** | 3000 | React + Vite |
| **mock-server** | 3001 | Express mock API |
| **db-stub** | 5432 | PostgreSQL |

### Comandos Útiles

```powershell
# Levantar todos los servicios
docker-compose up

# Levantar en background
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f frontend

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Rebuild de un servicio específico
docker-compose up --build frontend

# Reiniciar un servicio
docker-compose restart backend
```

### Troubleshooting

**Puerto ya en uso:**
```powershell
# Ver procesos en puerto 3000
netstat -ano | findstr :3000

# Matar proceso (reemplazar PID)
taskkill /PID <PID> /F
```

**Permisos de volúmenes:**
```powershell
# Eliminar volúmenes y recrear
docker-compose down -v
docker-compose up --build
```

---

## 📮 Colección Postman

**Ubicación:** `/postman/Jarvis_TEC_API.postman_collection.json`

### Importar en Postman

1. Abrir Postman
2. **File** → **Import**
3. Seleccionar `Jarvis_TEC_API.postman_collection.json`
4. Configurar variables de entorno:
   - `base_url`: http://localhost:8000
   - `mock_url`: http://localhost:3001

### Endpoints Incluidos

✅ Health Check  
✅ Face Recognition & Emotions  
✅ Audio Transcription  
✅ Command Execution  
✅ BMI Calculation  
✅ Stock Price Prediction  
✅ Movie Recommendation  

Cada endpoint incluye:
- Descripción completa
- Ejemplos de request
- Ejemplos de response
- Status codes

---

## 🎬 Demo E2E - Flujo Completo

### Con Mock Server (sin Azure)

1. **Configurar modo mock:**
```env
# frontend-react/.env
VITE_USE_MOCK=true
VITE_MOCK_API_URL=http://localhost:3001
```

2. **Levantar servicios:**
```powershell
# Terminal 1: Mock server
cd mock-server
npm start

# Terminal 2: Frontend
cd frontend-react
npm run dev
```

3. **Ejecutar demo:**
   - Ir a http://localhost:3000
   - Click en "Iniciar Captura"
   - Click en "Iniciar Sistema"
   - **Observar:**
     - ✅ Cámara captura frames cada 2s
     - ✅ Emociones simuladas aparecen
     - ✅ Audio se transcribe automáticamente
     - ✅ Comandos se procesan

4. **Comandos de prueba:**
   - *"TravisTEC predice el precio de Bitcoin para 5 años"*
   - *"TravisTEC calcula el índice de masa corporal con altura 175 y peso 70"*
   - *"TravisTEC recomienda una película"*

5. **Ver resultados:**
   - Click en "Ver Resultados"
   - Revisar estadísticas y logs

### Con Backend Real (Azure + ML)

1. **Configurar:**
```env
# frontend-react/.env
VITE_USE_MOCK=false
VITE_API_URL=http://localhost:8000
```

2. **Configurar Azure** (ver sección anterior)

3. **Levantar con Docker:**
```powershell
docker-compose up
```

4. **O manualmente:**
```powershell
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend-react
npm run dev
```

---

## 🧪 Scripts de Testing

### Backend - Smoke Tests

```powershell
cd backend

# Test detector de emociones local
python scripts\run_smoke_emotion_simple.py

# Entrenar modelo BMI
python scripts\train_bmi_model.py

# Test modelo BMI
python scripts\run_smoke_bmi.py

# Ejecutar todas las predicciones
python scripts\run_all_predictions.py
```

### Frontend - Linting y Build

```powershell
cd frontend-react

# Ejecutar linter
npm run lint

# Build de producción
npm run build

# Preview de build
npm run preview
```

---

## 📊 Notebooks de Machine Learning

### `/notebooks/01_data_exploration.ipynb`
- Análisis exploratorio de datasets
- Visualizaciones con matplotlib/seaborn
- Limpieza y preprocesamiento de datos
- Estadísticas descriptivas

### `/notebooks/02_model_training.ipynb`
- Entrenamiento de modelos supervisados
- Validación cruzada
- Optimización de hiperparámetros
- Evaluación de métricas (accuracy, F1, RMSE)
- Exportación a `.joblib`

**Iniciar Jupyter:**
```powershell
cd notebooks
jupyter notebook
```

**Modelos disponibles:**
- Bitcoin price prediction (LSTM)
- Avocado price prediction
- BMI/BodyFat estimation
- Movie recommender (collaborative filtering)
- S&P 500 prediction
- London crime classification
- Airline delay prediction

---

## 🤝 Colaboración - División de Tareas

### Persona A - Backend & Machine Learning

**Responsabilidades:**
- ✅ Configuración de Azure Face API y Speech Services
- ✅ Implementación de endpoints FastAPI
- ✅ Entrenamiento de modelos ML en notebooks
- ✅ Sistema de carga de modelos (`model_runner.py`)
- ✅ Servicio STT con múltiples backends
- ✅ Fallback local para detección de emociones
- ✅ Optimización de rendimiento

**Archivos clave:**
- `backend/app.py`
- `backend/services/*.py`
- `notebooks/*.ipynb`
- `backend/scripts/train_*.py`

### Persona B - Frontend & DevOps

**Responsabilidades:**
- ✅ Desarrollo de React app con Vite
- ✅ Implementación de rutas con React Router
- ✅ Componentes reutilizables (Camera, Audio, Emotions)
- ✅ Cliente API configurable con .env
- ✅ Docker y docker-compose
- ✅ Mock server para desarrollo
- ✅ Colección Postman
- ✅ Documentación y README

**Archivos clave:**
- `frontend-react/src/**/*`
- `mock-server/server.js`
- `docker-compose.yml`
- `postman/*.json`

---

## 📝 Variables de Entorno - Referencia Completa

### Frontend (`frontend-react/.env`)

```env
# URL del backend real
VITE_API_URL=http://localhost:8000

# Activar modo mock (true/false)
VITE_USE_MOCK=false

# URL del mock server
VITE_MOCK_API_URL=http://localhost:3001
```

### Backend (`backend/.env`)

```env
# Azure Face API
AZURE_FACE_KEY=tu_face_api_key_aqui
AZURE_FACE_ENDPOINT=https://tu-recurso.cognitiveservices.azure.com/

# Azure Speech Services
AZURE_SPEECH_KEY=tu_speech_api_key_aqui
AZURE_SERVICE_REGION=eastus

# Speech-to-Text Service (azure|google|whisper)
STT_SERVICE=azure

# Opcional: Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Opcional: Configuración de modelos
MODEL_PATH=./models
```

---

## 🔗 Enlaces Útiles

### Frameworks y Librerías
- [React](https://react.dev/) - Framework frontend
- [React Router](https://reactrouter.com/) - Navegación
- [Vite](https://vitejs.dev/) - Build tool
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Axios](https://axios-http.com/) - HTTP client

### Azure Services
- [Azure Face API](https://docs.microsoft.com/azure/cognitive-services/face/)
- [Azure Speech Services](https://docs.microsoft.com/azure/cognitive-services/speech-service/)
- [Azure Portal](https://portal.azure.com/)

### ML & Data Science
- [Scikit-learn](https://scikit-learn.org/)
- [Pandas](https://pandas.pydata.org/)
- [Jupyter](https://jupyter.org/)

### DevOps
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Postman](https://www.postman.com/)

---

## 🐛 Troubleshooting

### Frontend no conecta con backend

**Verificar:**
1. Backend está corriendo en puerto 8000
2. `.env` tiene la URL correcta
3. CORS está habilitado en FastAPI
4. Firewall/antivirus no bloquea puerto

**Solución:**
```powershell
# Verificar que backend responde
curl http://localhost:8000/api/health

# Verificar variables de entorno
cd frontend-react
cat .env
```

### Cámara/micrófono no funciona

**Causas comunes:**
1. Permisos del navegador denegados
2. HTTPS requerido (Chrome/Firefox)
3. Dispositivo ya en uso

**Solución:**
- Permitir permisos en configuración del navegador
- Usar `localhost` (permitido sin HTTPS)
- Cerrar otras apps que usen cámara/mic

### Mock server no responde

**Verificar:**
```powershell
cd mock-server
npm install
npm start

# En otra terminal
curl http://localhost:3001/api/health
```

### Docker build falla

**Limpiar caché:**
```powershell
docker-compose down -v
docker system prune -a
docker-compose up --build
```

---

## 📄 Licencia

MIT License

Copyright (c) 2025 Jarvis TEC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**Desarrollado con ❤️ por el equipo Jarvis TEC** 🚀

**Repositorio:** https://github.com/jaredjimenez0022-oss/TravisTEC
