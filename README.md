# Jarvis TEC 🤖

Asistente inteligente con reconocimiento facial y procesamiento de voz para el TEC.

## 📁 Estructura del Proyecto

```
/jarvis-tec/
  /frontend/                -> Persona B (Desarrollo Web)
    /public/
    /src/
      index.html           # Interfaz principal
      main.js              # Lógica: cámara + audio + parser + api-client
      api-client.js        # Cliente para comunicarse con backend
      styles.css           # Estilos
    package.json
    Dockerfile
    
  /backend/                 -> Persona A (ML & Backend)
    app.py                  # FastAPI - API principal
    /services/
      azure_face.py         # Servicio de Azure Face API
      model_runner.py       # Carga y ejecuta modelos entrenados
      stt_service.py        # Speech-to-Text (Azure/Google/Whisper)
    /models/                # Modelos entrenados (.joblib, .pkl)
    requirements.txt
    Dockerfile
    .env.example
    
  /notebooks/               -> Persona A (Entrenamiento)
    01_data_exploration.ipynb
    02_model_training.ipynb
    
  docker-compose.yml
  .gitignore
  README.md
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.10+
- Node.js 18+ (para frontend)
- Docker y Docker Compose (opcional)
- Azure Cognitive Services (Face API y Speech Services)

### Configuración Backend (Persona A)

1. **Navegar al directorio backend:**
   ```bash
   cd backend
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales de Azure
   ```

5. **Ejecutar servidor:**
   ```bash
   python app.py
   ```

   El backend estará disponible en: `http://localhost:8000`

### Configuración Frontend (Persona B)

1. **Navegar al directorio frontend:**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Ejecutar servidor de desarrollo:**
   ```bash
   npm run dev
   ```

   El frontend estará disponible en: `http://localhost:3000`

### Usar Docker Compose (Ambos)

```bash
docker-compose up --build
```

## 📋 Tareas por Persona

### Persona A - Backend & Machine Learning

- ✅ Configurar Azure Face API y Speech Services
- ✅ Implementar endpoints FastAPI
- ✅ Entrenar modelos de ML en notebooks
- ✅ Implementar `model_runner.py` para cargar modelos
- ✅ Configurar servicio STT (Speech-to-Text)
- 📝 Crear y entrenar modelos personalizados
- 📝 Optimizar rendimiento de reconocimiento

### Persona B - Frontend

- ✅ Diseñar interfaz HTML/CSS
- ✅ Implementar captura de cámara y audio
- ✅ Crear cliente API (`api-client.js`)
- ✅ Implementar visualización de resultados
- 📝 Mejorar UX/UI
- 📝 Agregar notificaciones y feedback visual

## 🔧 Configuración de Azure

### Azure Face API

1. Crear recurso Face en Azure Portal
2. Obtener Key y Endpoint
3. Configurar en `.env`:
   ```
   AZURE_FACE_KEY=tu_key_aqui
   AZURE_FACE_ENDPOINT=https://tu-recurso.cognitiveservices.azure.com/
   ```

### Azure Speech Services

1. Crear recurso Speech en Azure Portal
2. Obtener Key y Region
3. Configurar en `.env`:
   ```
   AZURE_SPEECH_KEY=tu_key_aqui
   AZURE_SERVICE_REGION=tu_region_aqui
   ```

## 📚 Endpoints de la API

### `POST /api/transcribe`
Transcribe audio a texto.
- **Input:** Archivo de audio (webm)
- **Output:** `{ "transcription": "texto" }`

### `POST /api/recognize-face`
Reconoce rostro en imagen.
- **Input:** Imagen (jpg/png)
- **Output:** `{ "identified": true/false, "name": "...", ... }`

### `POST /api/process`
Procesa comando de texto con modelo ML.
- **Input:** `{ "text": "comando" }`
- **Output:** `{ "response": "respuesta" }`

### `POST /api/v1/bmi` (nuevo)
Calcula IMC o estima BodyFat usando el modelo entrenado `bmi_model` si está disponible.
- **Input:** JSON `{ "height": <meters>, "weight": <kg>, "age": <years> }`
- **Output (modelo):** `{ "bodyfat": <percent>, "units": "%", "method": "bmi_model" }`
- **Output (fórmula):** `{ "bmi": <kg/m2>, "units": "kg/m2", "method": "formula" }`

### `POST /api/v1/face/sentiment` (local fallback)
Devuelve la emoción detectada usando el detector local (heurístico Haar-cascade).
- **Input:** multipart/form-data con campo `image` (jpg/png/webp)
- **Output:** `{ "dominant_emotion": "happiness|neutral|no_face", "face_count": n, "details": {...} }`

## 🧪 Comandos rápidos (smoke tests)
Desde `backend/` puedes ejecutar los scripts de prueba rápidos:

- Ejecutar detector de emoción simple:
```powershell
python scripts\run_smoke_emotion_simple.py
```

- Entrenar y guardar modelo BMI (usa `backend/datasets/bodyfat.csv`):
```powershell
python scripts\train_bmi_model.py
```

- Probar el modelo BMI guardado:
```powershell
python scripts\run_smoke_bmi.py
```

- Listar modelos cargados en tiempo de ejecución (usa Python REPL en `backend/`):
```powershell
python -c "import sys; sys.path.insert(0, 'backend'); from services import model_runner as mr; print(list(mr._runner.models.keys()))"
```

Estas herramientas te permiten verificar rápidamente las funcionalidades sin iniciar el servidor.

### `GET /api/health`
Verifica estado del sistema.
- **Output:** `{ "status": "healthy", "services": {...} }`

## 🧪 Notebooks de Entrenamiento

Los notebooks en `/notebooks/` contienen:

1. **01_data_exploration.ipynb**: Análisis exploratorio de datos
2. **02_model_training.ipynb**: Entrenamiento de modelos

Para usar los notebooks:
```bash
cd notebooks
jupyter notebook
```

## 🐳 Docker

### Construir imágenes:
```bash
docker-compose build
```

### Ejecutar servicios:
```bash
docker-compose up
```

### Detener servicios:
```bash
docker-compose down
```

## 🤝 Colaboración

- **Persona A**: Enfocado en backend, ML y servicios de Azure
- **Persona B**: Enfocado en frontend, UX/UI y integración de API

### Workflow sugerido:

1. Persona A desarrolla y prueba endpoints
2. Persona B consume endpoints desde frontend
3. Ambos prueban integración completa
4. Iteración y mejoras continuas

## 📝 Notas

- Los modelos entrenados (`.joblib`, `.pkl`) no se suben a Git (ver `.gitignore`)
- Compartir modelos vía Google Drive o similar
- Las credenciales de Azure deben mantenerse en `.env` (no subir a Git)

## 🔗 Enlaces Útiles

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Azure Face API Docs](https://docs.microsoft.com/en-us/azure/cognitive-services/face/)
- [Azure Speech Services Docs](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [MDN Web APIs](https://developer.mozilla.org/en-US/docs/Web/API)

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles.

---

**Desarrollado por el equipo Jarvis TEC** 🚀