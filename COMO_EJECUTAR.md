# 🚀 GUÍA DE EJECUCIÓN RÁPIDA - Jarvis TEC

## Cómo ejecutar y probar el proyecto

**Fecha:** Octubre 15, 2025  
**Tiempo estimado:** 5-10 minutos

---

## ⚡ OPCIÓN 1: EJECUCIÓN RÁPIDA (RECOMENDADA)

### Frontend + Mock Server (Sin backend)

Esta es la forma **MÁS RÁPIDA** de ver el proyecto funcionando.

#### Paso 1: Iniciar Mock Server

```powershell
# Terminal 1
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\mock-server
npm install
node server.js
```

**Resultado esperado:**
```
🚀 Mock Server running on http://localhost:3001
```

#### Paso 2: Iniciar Frontend

```powershell
# Terminal 2 (nueva ventana)
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\frontend-react
npm install
npm run dev
```

**Resultado esperado:**
```
VITE v7.1.10  ready in 445 ms

➜  Local:   http://localhost:5173/
```

#### Paso 3: Abrir en Navegador

1. Abre tu navegador en: **http://localhost:5173**
2. Verás la página de inicio (Home)
3. Click en **"Iniciar Captura"**
4. Permitir acceso a cámara y micrófono cuando lo pida

#### Paso 4: Probar Funcionalidades

**A. Captura de Emociones:**
1. Click en "Activar Captura"
2. Tu cámara se activará
3. Cada 2 segundos se captura automáticamente
4. Verás emociones detectadas en la barra lateral

**B. Comandos por Voz:**
1. Click en "Iniciar Grabación"
2. Di uno de estos comandos:
   - **"bitcoin"** → Predicción de Bitcoin
   - **"movie inception"** → Recomendación de películas
   - **"imc 180 75"** → Cálculo de IMC (altura cm, peso kg)
3. Verás la respuesta en la tabla de logs

**C. Ver Resultados:**
1. Click en "Ver Resultados"
2. Verás estadísticas de tu sesión
3. Logs categorizados por tipo

---

## 🐳 OPCIÓN 2: CON DOCKER (Proyecto Completo)

### Si tienes Docker instalado

```powershell
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC
docker-compose up -d
```

**Servicios disponibles:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Mock Server: http://localhost:3001
- PostgreSQL: localhost:5432

**Para detener:**
```powershell
docker-compose down
```

---

## 💻 OPCIÓN 3: BACKEND COMPLETO (Con Python)

### Solo si quieres probar con backend real

#### Paso 1: Configurar Python

```powershell
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\backend
```

#### Paso 2: Instalar Dependencias

```powershell
pip install -r requirements.txt
```

#### Paso 3: Configurar Variables de Entorno

Crear archivo `.env` en la carpeta `backend/`:

```env
# Azure (Opcional - funciona sin esto usando mock)
AZURE_FACE_KEY=your_key_here
AZURE_FACE_ENDPOINT=your_endpoint_here
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=your_region_here
```

#### Paso 4: Iniciar Backend

```powershell
# Desde backend/
uvicorn app:app --reload --port 8000
```

**Resultado esperado:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

#### Paso 5: Iniciar Frontend

```powershell
# Terminal nueva
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\frontend-react

# Configurar para usar backend real
# Editar .env:
# VITE_USE_MOCK=false
# VITE_API_URL=http://localhost:8000

npm run dev
```

---

## ✅ VERIFICACIÓN RÁPIDA

### Comprobar que todo funciona:

#### 1. Mock Server está corriendo:
```powershell
curl http://localhost:3001/health
```
**Esperado:** `{"status":"healthy","service":"mock-server"}`

#### 2. Frontend está corriendo:
- Abrir http://localhost:5173
- Debes ver la página de inicio

#### 3. Modelos ML están disponibles:
```powershell
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\backend\models
dir *.joblib
```
**Esperado:** Ver 9 archivos .joblib

---

## 🎬 DEMO COMPLETA - FLUJO E2E

### Escenario: Demostrar todas las funcionalidades

1. **Abrir aplicación**: http://localhost:5173

2. **Navegar a Captura**: Click "Iniciar Captura"

3. **Permitir permisos**:
   - Aceptar cámara
   - Aceptar micrófono

4. **Activar captura**: Click "Activar Captura"
   - Esperar 2-3 capturas automáticas
   - Ver emociones en panel derecho

5. **Probar comando voz - Bitcoin**:
   - Click "Iniciar Grabación"
   - Decir: **"bitcoin"**
   - Ver predicción en logs

6. **Probar comando voz - Película**:
   - Click "Iniciar Grabación"
   - Decir: **"movie titanic"**
   - Ver recomendaciones en logs

7. **Probar comando voz - IMC**:
   - Click "Iniciar Grabación"
   - Decir: **"imc 180 75"**
   - Ver cálculo en logs

8. **Ver snapshot manual**:
   - Click "Capturar Snapshot"
   - Ver foto capturada

9. **Ver estadísticas**:
   - Click "Ver Resultados"
   - Ver métricas de sesión
   - Ver todos los logs

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Problema: "Puerto ya en uso"

```powershell
# Verificar qué está usando el puerto 5173
netstat -ano | findstr :5173

# Matar proceso (usar PID del comando anterior)
taskkill /PID <PID> /F
```

### Problema: "Cannot find module 'prop-types'"

```powershell
cd frontend-react
npm install prop-types
```

### Problema: "Camera/Microphone not working"

1. Verificar permisos del navegador
2. Usar **Chrome** o **Edge** (mejor compatibilidad)
3. Abrir DevTools (F12) y ver errores en Console

### Problema: Mock server no responde

```powershell
# Verificar que está corriendo
curl http://localhost:3001/health

# Si no responde, reiniciar:
cd mock-server
node server.js
```

### Problema: Frontend muestra errores

1. Abrir DevTools (F12)
2. Ir a Console
3. Ver errores específicos
4. Verificar que `.env` existe con:
   ```
   VITE_USE_MOCK=true
   VITE_MOCK_API_URL=http://localhost:3001
   VITE_API_URL=http://localhost:8000
   ```

---

## 📸 CAPTURAS DE PANTALLA ESPERADAS

### 1. Home Page
- Hero section con título "Jarvis TEC"
- Botón "Iniciar Captura"
- Cards de features

### 2. Capture Page
- Video preview (tu cámara)
- Botón "Activar Captura"
- Botón "Iniciar Grabación"
- Panel derecho con emociones
- Tabla de logs abajo

### 3. Results Page
- Estadísticas de sesión
- Gráfico de emociones
- Lista de logs categorizados

---

## 🧪 TESTING CON POSTMAN

### Si quieres probar la API directamente:

1. Abrir Postman
2. Importar: `postman/Jarvis_TEC_API.postman_collection.json`
3. Configurar variables:
   - `base_url`: http://localhost:8000
   - `mock_url`: http://localhost:3001
4. Ejecutar requests:
   - Health Check
   - Face Sentiment
   - Transcribe Audio
   - Etc.

---

## ⚡ COMANDOS RÁPIDOS DE REFERENCIA

### Iniciar Todo (2 terminales)

**Terminal 1 - Mock Server:**
```powershell
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\mock-server; node server.js
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\frontend-react; npm run dev
```

### Detener Todo

Presionar `Ctrl+C` en ambas terminales.

---

## 🎯 COMANDOS DE VOZ SOPORTADOS

| Comando | Ejemplo | Resultado |
|---------|---------|-----------|
| **bitcoin** | "bitcoin" | Predicción de precio Bitcoin |
| **movie [título]** | "movie inception" | Recomendación de películas similares |
| **imc [altura] [peso]** | "imc 180 75" | Cálculo de IMC (altura en cm, peso en kg) |
| **stock [símbolo]** | "stock AAPL" | Predicción de precio de acción |

---

## 📊 VERIFICAR MODELOS ML

### Comprobar que los 9 modelos existen:

```powershell
cd c:\Users\34654\OneDrive\Documentos\GitHub\TravisTEC\backend\models
Get-ChildItem *.joblib | ForEach-Object { $_.Name }
```

**Debes ver:**
```
airline_delay_model.joblib
avocado_model.joblib
bitcoin_model.joblib
bmi_model.joblib
car_model.joblib
cirrhosis_model.joblib
london_crime_model.joblib
movie_recommender.joblib
sp500_model.joblib
```

---

## 🎓 PARA PRESENTACIÓN/DEMO

### Orden sugerido de demostración:

1. **Mostrar Home** (10 seg)
2. **Iniciar Captura** (20 seg)
3. **Detectar emociones** (30 seg) - dejar que capture 3-4 veces
4. **Comando "bitcoin"** (20 seg)
5. **Comando "movie titanic"** (20 seg)
6. **Ver Resultados** (20 seg)
7. **Mostrar código** (opcional)

**Tiempo total:** ~2 minutos

---

## 🔗 URLS IMPORTANTES

- **Frontend:** http://localhost:5173
- **Mock Server:** http://localhost:3001
- **Backend (si está corriendo):** http://localhost:8000
- **Health Check Mock:** http://localhost:3001/health
- **Health Check Backend:** http://localhost:8000/health

---

## 📝 NOTAS IMPORTANTES

1. ✅ **Mock Server es suficiente** para demostrar todas las funcionalidades
2. ✅ El backend completo es **opcional** (requiere Azure keys)
3. ✅ Usar **Chrome o Edge** para mejor compatibilidad
4. ✅ Permitir permisos de cámara/micrófono cuando lo pida
5. ✅ Los modelos ML funcionan con el mock server

---

## ✅ CHECKLIST PRE-DEMO

- [ ] Mock server corriendo en puerto 3001
- [ ] Frontend corriendo en puerto 5173
- [ ] Navegador abierto en http://localhost:5173
- [ ] Permisos de cámara/micrófono concedidos
- [ ] Audio funcionando (para comandos de voz)
- [ ] DevTools abierto (F12) para mostrar logs si es necesario

---

## 🎉 ¡LISTO!

Si seguiste la **OPCIÓN 1** (Frontend + Mock Server), deberías tener:

✅ Aplicación corriendo en http://localhost:5173  
✅ Mock server respondiendo en http://localhost:3001  
✅ Todas las funcionalidades demostrables  
✅ Sin necesidad de Azure o backend complejo  

**¡Disfruta la demo!** 🚀

---

**¿Problemas?** Revisa la sección de solución de problemas o abre DevTools (F12) para ver errores específicos.
