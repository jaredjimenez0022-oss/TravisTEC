# 📝 Contrato de API - Jarvis TEC

## Base URLs

- **Producción:** `http://localhost:8000`
- **Mock Server:** `http://localhost:3001`

---

## Endpoints

### 1. Health Check

**GET** `/api/health`

**Descripción:** Verifica el estado del sistema y servicios disponibles.

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-15T12:00:00Z",
  "services": {
    "face_api": "available",
    "speech_api": "available",
    "ml_models": "loaded"
  }
}
```

---

### 2. Reconocimiento Facial y Emociones

**POST** `/api/v1/face/sentiment`

**Descripción:** Detecta rostros y analiza emociones en una imagen.

**Content-Type:** `multipart/form-data`

**Request Body:**
```
image: <file> (jpg/png/webp)
```

**Response 200:**
```json
{
  "face_detected": true,
  "face_count": 1,
  "dominant_emotion": "happiness",
  "attributes": {
    "emotion": {
      "happiness": 0.85,
      "sadness": 0.05,
      "anger": 0.03,
      "surprise": 0.04,
      "neutral": 0.03,
      "fear": 0.00,
      "disgust": 0.00,
      "contempt": 0.00
    }
  },
  "details": {
    "happiness": 0.85,
    "sadness": 0.05,
    "anger": 0.03
  }
}
```

**Response 200 (No face):**
```json
{
  "face_detected": false,
  "face_count": 0,
  "message": "No face detected in image"
}
```

**Emociones posibles:**
- `happiness` - Felicidad
- `sadness` - Tristeza
- `anger` - Enojo
- `surprise` - Sorpresa
- `neutral` - Neutral
- `fear` - Miedo
- `disgust` - Disgusto
- `contempt` - Desprecio

---

### 3. Transcripción de Audio

**POST** `/api/v1/transcribe`

**Descripción:** Transcribe audio a texto usando Azure Speech Services.

**Content-Type:** `multipart/form-data`

**Request Body:**
```
audio: <file> (webm/wav/mp3)
```

**Response 200:**
```json
{
  "transcription": "TravisTEC predice el precio de Bitcoin para los próximos 5 años",
  "confidence": 0.95,
  "language": "es-ES",
  "duration_ms": 2500
}
```

**Response 400:**
```json
{
  "error": "Invalid audio format",
  "detail": "Only webm, wav, and mp3 are supported"
}
```

---

### 4. Procesamiento de Comandos

**POST** `/api/v1/command/execute`

**Descripción:** Procesa un comando y ejecuta el modelo ML correspondiente.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "text": "predice el precio de bitcoin",
  "task": "bitcoin",
  "params": {
    "years": 5
  }
}
```

**Campos:**
- `text` (string, required): Texto del comando
- `task` (string, optional): Tipo de tarea (bitcoin, movie, bmi, etc.)
- `params` (object, optional): Parámetros específicos del modelo

**Response 200:**
```json
{
  "response": "El precio de Bitcoin en los próximos 5 años se estima en $85,000 con tendencia alcista.",
  "task": "bitcoin",
  "params": {
    "years": 5
  },
  "processed_at": "2025-10-15T12:00:00Z",
  "confidence": 0.92
}
```

**Tareas soportadas:**
- `bitcoin` - Predicción de precio Bitcoin
- `sp500` - Predicción S&P 500
- `aguacate` / `avocado` - Precio de aguacate
- `pelicula` / `movie` - Recomendación de películas
- `automovil` / `coche` / `car` - Precio de automóvil
- `imc` / `bmi` - Cálculo de masa corporal
- `londres` / `london` - Análisis de crimen
- `chicago` - Análisis de crimen
- `cirrosis` - Predicción médica
- `avion` / `vuelo` / `flight` - Retraso de vuelos

---

### 5. Cálculo de BMI / Body Fat

**POST** `/api/v1/bmi`

**Descripción:** Calcula el BMI y estima el porcentaje de grasa corporal.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "height": 1.75,
  "weight": 70,
  "age": 30
}
```

**Campos:**
- `height` (float, required): Altura en metros
- `weight` (float, required): Peso en kilogramos
- `age` (integer, optional): Edad en años

**Response 200:**
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

**Response 400:**
```json
{
  "error": "Missing required parameters",
  "detail": "height and weight are required"
}
```

---

### 6. Predicción de Precio de Acciones

**POST** `/api/v1/predict/stock`

**Descripción:** Predice el precio futuro de acciones o criptomonedas.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "symbol": "BTC",
  "years": 5
}
```

**Campos:**
- `symbol` (string, required): Símbolo de la acción (BTC, AAPL, etc.)
- `years` (integer, optional): Años a predecir (default: 5)

**Response 200:**
```json
{
  "symbol": "BTC",
  "predictions": [
    {
      "year": 2026,
      "predicted_price": "65432.50",
      "confidence": "0.85"
    },
    {
      "year": 2027,
      "predicted_price": "72100.30",
      "confidence": "0.80"
    },
    {
      "year": 2028,
      "predicted_price": "79850.75",
      "confidence": "0.75"
    },
    {
      "year": 2029,
      "predicted_price": "85200.60",
      "confidence": "0.72"
    },
    {
      "year": 2030,
      "predicted_price": "91500.25",
      "confidence": "0.70"
    }
  ],
  "model": "lstm_model"
}
```

---

### 7. Recomendación de Películas

**POST** `/api/v1/recommend/movie`

**Descripción:** Recomienda películas basadas en preferencias del usuario.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "user_id": 123,
  "genre": "Sci-Fi"
}
```

**Campos:**
- `user_id` (integer, optional): ID del usuario
- `genre` (string, optional): Género preferido

**Response 200:**
```json
{
  "recommendation": {
    "title": "Inception",
    "rating": 8.8,
    "genre": "Sci-Fi",
    "year": 2010
  },
  "confidence": 0.88,
  "model": "collaborative_filtering"
}
```

---

## Códigos de Estado HTTP

### Success
- **200 OK** - Solicitud exitosa
- **201 Created** - Recurso creado

### Client Errors
- **400 Bad Request** - Datos inválidos
- **401 Unauthorized** - No autenticado
- **404 Not Found** - Recurso no encontrado
- **422 Unprocessable Entity** - Validación fallida

### Server Errors
- **500 Internal Server Error** - Error del servidor
- **503 Service Unavailable** - Servicio no disponible

---

## Headers Comunes

### Request Headers
```
Content-Type: application/json
Content-Type: multipart/form-data
Accept: application/json
```

### Response Headers
```
Content-Type: application/json
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## Ejemplos de Uso con cURL

### Health Check
```bash
curl http://localhost:3001/api/health
```

### Face Sentiment
```bash
curl -X POST http://localhost:3001/api/v1/face/sentiment \
  -F "image=@path/to/image.jpg"
```

### Transcribe Audio
```bash
curl -X POST http://localhost:3001/api/v1/transcribe \
  -F "audio=@path/to/audio.webm"
```

### Execute Command
```bash
curl -X POST http://localhost:3001/api/v1/command/execute \
  -H "Content-Type: application/json" \
  -d '{
    "text": "predice bitcoin",
    "task": "bitcoin",
    "params": {"years": 5}
  }'
```

### Calculate BMI
```bash
curl -X POST http://localhost:3001/api/v1/bmi \
  -H "Content-Type: application/json" \
  -d '{
    "height": 1.75,
    "weight": 70,
    "age": 30
  }'
```

---

## Ejemplos de Uso con JavaScript (Axios)

### Health Check
```javascript
import axios from 'axios';

const response = await axios.get('http://localhost:3001/api/health');
console.log(response.data);
```

### Face Sentiment
```javascript
const formData = new FormData();
formData.append('image', imageBlob, 'photo.jpg');

const response = await axios.post(
  'http://localhost:3001/api/v1/face/sentiment',
  formData,
  {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }
);

console.log(response.data.dominant_emotion);
```

### Transcribe Audio
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.webm');

const response = await axios.post(
  'http://localhost:3001/api/v1/transcribe',
  formData
);

console.log(response.data.transcription);
```

### Execute Command
```javascript
const response = await axios.post(
  'http://localhost:3001/api/v1/command/execute',
  {
    text: 'predice bitcoin',
    task: 'bitcoin',
    params: { years: 5 }
  }
);

console.log(response.data.response);
```

---

## Rate Limiting

**Mock Server:** Sin límites  
**Production Backend:** 
- 100 requests/minuto por IP
- 1000 requests/hora por usuario

---

## Versionado

- **Versión actual:** v1
- **Endpoint base:** `/api/v1/`
- **Deprecation policy:** 6 meses de aviso

---

## Soporte

- **Documentación:** README.md
- **Postman Collection:** `/postman/Jarvis_TEC_API.postman_collection.json`
- **Issues:** GitHub Issues

---

**Última actualización:** Octubre 15, 2025
