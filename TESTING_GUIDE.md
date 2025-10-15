# 🧪 GUÍA DE PRUEBAS - Jarvis TEC

## ✅ Estado Actual de los Servidores

### Mock Server
```
✅ FUNCIONANDO en http://localhost:3001
```

### Frontend React
```
✅ FUNCIONANDO en http://localhost:5173
```

---

## 🎯 Pruebas Funcionales

### 1. Prueba de Navegación

**Pasos:**
1. Abrir navegador en http://localhost:5173
2. Verificar página Home carga correctamente
3. Click en "Iniciar Captura" → debe ir a /capture
4. Click en "Ver Resultados" → debe ir a /results
5. Click en "Volver al Inicio" → debe ir a /

**Resultado esperado:** ✅ Todas las rutas funcionan

---

### 2. Prueba de Captura de Cámara

**Pasos:**
1. Ir a /capture
2. Click "Iniciar Sistema"
3. Permitir acceso a cámara cuando el navegador lo solicite
4. Observar vista de cámara en vivo

**Resultado esperado:** 
- ✅ Video se muestra en pantalla
- ✅ Cada 2 segundos se captura un frame
- ✅ Logs muestran "Emoción detectada"

---

### 3. Prueba de Detección de Emociones

**Pasos:**
1. Con el sistema iniciado en /capture
2. Observar panel derecho "Emociones Detectadas"
3. Esperar 2-3 segundos

**Resultado esperado:**
- ✅ Se muestra una emoción dominante (feliz/neutral/triste/etc)
- ✅ Barras de progreso muestran porcentajes
- ✅ Emoji correspondiente aparece
- ✅ Logs muestran mensajes de éxito

---

### 4. Prueba de Snapshot Manual

**Pasos:**
1. Con el sistema iniciado
2. Click en botón "📸 Tomar Foto"
3. Observar sección "Última foto"

**Resultado esperado:**
- ✅ Imagen capturada aparece en preview
- ✅ Log muestra "Foto capturada"
- ✅ Emoción se detecta en la foto

---

### 5. Prueba de Grabación de Audio

**Pasos:**
1. Con el sistema iniciado
2. Permitir acceso al micrófono
3. Observar indicador de grabación

**Resultado esperado:**
- ✅ Indicador muestra "🎤 Grabando (Web Speech)" o "(MediaRecorder)"
- ✅ Punto rojo pulsa
- ✅ El navegador muestra que está usando el micrófono

---

### 6. Prueba de Reconocimiento de Voz

**Pasos:**
1. Con micrófono activo
2. Hablar claramente: "TravisTEC predice el precio de Bitcoin para 5 años"
3. Observar logs

**Resultado esperado:**
- ✅ Log muestra: "Reconocido: TravisTEC predice..."
- ✅ Log muestra: "Comando parseado: {task: 'bitcoin', params: {years: 5}}"
- ✅ Log muestra: "Respuesta: El precio de Bitcoin..."

---

### 7. Prueba de Visualización de Resultados

**Pasos:**
1. Después de usar /capture por 30 segundos
2. Click "📊 Ver Resultados"
3. Observar página /results

**Resultado esperado:**
- ✅ Estadísticas muestran total de eventos
- ✅ Cards muestran éxitos, errores, info
- ✅ Última emoción se visualiza
- ✅ Registro completo de logs aparece

---

### 8. Prueba de Mock Server

**Pasos:**
1. Abrir nueva terminal
2. Ejecutar:
```powershell
curl http://localhost:3001/api/health
```

**Resultado esperado:**
```json
{
  "status": "healthy",
  "timestamp": "...",
  "services": {...}
}
```

---

### 9. Prueba de API Client

**Pasos:**
1. Abrir DevTools del navegador (F12)
2. Ir a /capture
3. Iniciar sistema
4. Ir a pestaña "Network"
5. Observar requests

**Resultado esperado:**
- ✅ Requests a http://localhost:3001/api/v1/face/sentiment
- ✅ Status 200
- ✅ Response con emociones

---

### 10. Prueba de Modo Mock vs Real

**Pasos:**
1. Editar `frontend-react/.env`
2. Cambiar `VITE_USE_MOCK=true`
3. Reiniciar frontend
4. Observar logs de consola

**Resultado esperado:**
```
API Client initialized with base URL: http://localhost:3001
```

---

## 🔍 Pruebas de API con Postman

### Importar Colección

**Pasos:**
1. Abrir Postman
2. File → Import
3. Seleccionar `postman/Jarvis_TEC_API.postman_collection.json`
4. Configurar variables:
   - `base_url`: http://localhost:8000
   - `mock_url`: http://localhost:3001

### Ejecutar Requests

#### 1. Health Check
```
GET {{mock_url}}/api/health
```
**Esperado:** Status 200, JSON con "status": "healthy"

#### 2. Face Sentiment (con archivo)
```
POST {{mock_url}}/api/v1/face/sentiment
Body: form-data
  image: [seleccionar archivo .jpg]
```
**Esperado:** Status 200, JSON con emociones

#### 3. Command Execute
```
POST {{mock_url}}/api/v1/command/execute
Body: raw JSON
{
  "text": "predice bitcoin",
  "task": "bitcoin",
  "params": {"years": 5}
}
```
**Esperado:** Status 200, JSON con "response"

---

## 🐛 Troubleshooting - Problemas Comunes

### ❌ Cámara no funciona

**Síntomas:**
- Video negro
- Mensaje "Cámara inactiva"

**Soluciones:**
1. Verificar permisos del navegador
2. Cerrar otras apps que usen la cámara (Zoom, Teams, etc.)
3. Probar en Chrome/Edge (mejor soporte)
4. Verificar que estás usando `localhost` (no IP)

### ❌ Micrófono no funciona

**Síntomas:**
- Indicador muestra "inactivo"
- No se reconoce voz

**Soluciones:**
1. Permitir permisos en el navegador
2. Verificar que Web Speech API esté disponible (Chrome/Edge)
3. Hablar más fuerte y claro
4. Usar palabra clave "TravisTEC" antes del comando

### ❌ Emociones no aparecen

**Síntomas:**
- Panel de emociones vacío
- Log muestra "Error procesando rostro"

**Soluciones:**
1. Verificar que mock server está corriendo (puerto 3001)
2. Abrir DevTools → Network para ver errores
3. Verificar `.env` tiene `VITE_USE_MOCK=true`
4. Reiniciar mock server

### ❌ Frontend no carga

**Síntomas:**
- Página en blanco
- Error en consola

**Soluciones:**
```powershell
cd frontend-react
npm install
npm run dev
```

### ❌ Mock server error

**Síntomas:**
- "Cannot GET /api/health"
- "EADDRINUSE: address already in use"

**Soluciones:**
```powershell
# Verificar puerto 3001
netstat -ano | findstr :3001

# Matar proceso
taskkill /PID <PID> /F

# Reiniciar
cd mock-server
npm start
```

---

## 📊 Métricas de Éxito

### Funcionalidad Mínima Viable
- [x] Frontend carga en http://localhost:5173
- [x] 3 rutas funcionan (/, /capture, /results)
- [x] Cámara captura video
- [x] Micrófono graba audio
- [x] Mock server responde en puerto 3001
- [x] Emociones se visualizan
- [x] Logs se actualizan

### Funcionalidad Completa
- [x] Captura automática cada 2s
- [x] Snapshot manual
- [x] Web Speech API funciona
- [x] Parser de comandos funciona
- [x] Navegación entre páginas
- [x] Estadísticas en /results
- [x] Cliente API configurable
- [x] Docker compose configurado
- [x] Colección Postman
- [x] Documentación completa

---

## 🎬 Demo Script Completo

### Preparación (5 minutos)
```powershell
# Terminal 1
cd mock-server
npm start

# Terminal 2
cd frontend-react
npm run dev

# Navegador
http://localhost:5173
```

### Demo (10 minutos)

**Minuto 1-2: Home**
- Mostrar hero section
- Explicar características
- Click "Iniciar Captura"

**Minuto 3-5: Capture**
- Click "Iniciar Sistema"
- Permitir cámara/micrófono
- Mostrar video en vivo
- Explicar captura automática cada 2s

**Minuto 6-7: Emociones**
- Mostrar panel de emociones
- Hacer diferentes expresiones faciales
- Observar cambios en emociones
- Mostrar logs actualizándose

**Minuto 8-9: Comandos de Voz**
- Decir: "TravisTEC predice Bitcoin para 5 años"
- Mostrar comando parseado
- Mostrar respuesta del mock
- Decir: "TravisTEC recomienda una película"

**Minuto 10: Results**
- Click "Ver Resultados"
- Mostrar estadísticas
- Mostrar última emoción
- Revisar logs completos
- Click "Nueva Captura" para cerrar el círculo

---

## 📝 Checklist Pre-Demo

- [ ] Mock server corriendo en 3001
- [ ] Frontend corriendo en 5173
- [ ] Permisos de cámara/mic otorgados
- [ ] Postman collection importada
- [ ] README.md abierto para referencia
- [ ] DevTools listos para mostrar Network
- [ ] Comandos de voz preparados
- [ ] Lighting adecuado para reconocimiento facial

---

## 🎓 Testing Avanzado (Opcional)

### Performance Testing
```javascript
// En DevTools Console
console.time('capture');
// Esperar captura
console.timeEnd('capture');
// Debe ser < 100ms
```

### Memory Leaks
```javascript
// Iniciar sistema
// Esperar 5 minutos
// Detener sistema
// Verificar en DevTools → Memory que se liberó
```

### Browser Compatibility
- [ ] Chrome (primario)
- [ ] Edge (primario)
- [ ] Firefox (secundario)
- [ ] Safari (básico)

---

## 📞 Recursos para Testing

### URLs de Prueba
- Frontend: http://localhost:5173
- Mock API: http://localhost:3001
- Health: http://localhost:3001/api/health

### Archivos de Prueba
- Imagen: Cualquier .jpg con un rostro
- Audio: Grabar voz con comando

### Comandos de Voz
```
"TravisTEC predice el precio de Bitcoin para 5 años"
"TravisTEC calcula el índice de masa corporal con altura 175 y peso 70"
"TravisTEC recomienda una película de ciencia ficción"
"TravisTEC analiza el precio del aguacate"
"TravisTEC predice el SP 500"
```

---

**¡Listo para probar! ✅**

**Nota:** Si encuentras algún problema, consulta la sección de Troubleshooting o revisa los logs en la consola del navegador.
