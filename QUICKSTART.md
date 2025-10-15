# 🚀 Guía de Inicio Rápido - Jarvis TEC

## Inicio Rápido en 3 Pasos

### 1️⃣ Desarrollo con Mock (Sin Azure)

```powershell
# Terminal 1: Mock Server
cd mock-server
npm install
npm start

# Terminal 2: Frontend React
cd frontend-react
npm install
# Editar .env: VITE_USE_MOCK=true
npm run dev
```

Acceder a: **http://localhost:3000**

### 2️⃣ Desarrollo con Backend Real

```powershell
# Configurar Azure credentials en backend/.env
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py

# En otra terminal
cd frontend-react
# Editar .env: VITE_USE_MOCK=false
npm run dev
```

### 3️⃣ Docker Compose (Todo en uno)

```powershell
docker-compose up --build
```

Servicios:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Mock: http://localhost:3001

---

## 🎯 Flujo de Uso

1. **Ir a** http://localhost:3000
2. **Click** "Iniciar Captura"
3. **Click** "Iniciar Sistema"
4. **Permitir** cámara y micrófono
5. **Observar** emociones detectadas en tiempo real
6. **Hablar** comandos: "TravisTEC predice Bitcoin para 5 años"
7. **Ver** resultados procesados

---

## 📋 Checklist de Implementación

### Frontend & DevOps ✅
- [x] Scaffold React app con Vite
- [x] Rutas: /, /capture, /results
- [x] Componente de cámara con snapshot
- [x] Grabador de audio (Web Speech + MediaRecorder)
- [x] Componentes UI para emociones y transcripciones
- [x] api-client.js configurable con .env
- [x] docker-compose.yml completo
- [x] Mock server funcional
- [x] Colección Postman
- [x] Página demo E2E

### Objetivos del Proyecto ✅
- [x] **Objetivo 1**: Stream de imágenes → Azure → Emociones → Frontend
- [x] **Objetivo 2**: Audio → Texto → Backend → Respuesta → Frontend

---

## 🔧 Configuración Rápida

### .env Frontend
```env
VITE_USE_MOCK=true          # Cambiar a false para backend real
VITE_API_URL=http://localhost:8000
VITE_MOCK_API_URL=http://localhost:3001
```

### .env Backend
```env
AZURE_FACE_KEY=tu_key
AZURE_FACE_ENDPOINT=https://tu-recurso.cognitiveservices.azure.com/
AZURE_SPEECH_KEY=tu_key
AZURE_SERVICE_REGION=eastus
```

---

## 📦 Importar Postman

1. Abrir Postman
2. File → Import
3. Seleccionar: `postman/Jarvis_TEC_API.postman_collection.json`
4. Configurar variables:
   - base_url: http://localhost:8000
   - mock_url: http://localhost:3001

---

## 🆘 Problemas Comunes

### Puerto ocupado
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Permisos cámara/mic
- Ir a configuración del navegador
- Permitir acceso a localhost

### Docker no inicia
```powershell
docker-compose down -v
docker system prune -a
docker-compose up --build
```

---

## 📞 Soporte

- **Documentación completa**: README.md
- **Issues**: GitHub Issues
- **Colección API**: postman/Jarvis_TEC_API.postman_collection.json

---

**¡Listo para desarrollar! 🎉**
