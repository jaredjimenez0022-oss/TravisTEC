# 🔧 TROUBLESHOOTING: Comandos sin respuesta

**Fecha:** Octubre 15, 2025  
**Problema:** Los comandos de voz se detectan pero no dan respuesta

---

## ✅ **VERIFICACIONES REALIZADAS**

### 1. Mock Server ✅
```bash
curl http://localhost:3001/api/health
```
**Resultado:** ✅ Servidor corriendo correctamente

### 2. Endpoint de Comandos ✅
```bash
POST http://localhost:3001/api/v1/command/execute
Body: {"task":"bitcoin","text":"bitcoin","params":{}}
```
**Resultado:** ✅ Responde correctamente:
```json
{
  "response": "📈 Predicción Bitcoin: $48835.15. Tendencia: LATERAL ➡️",
  "task": "bitcoin",
  "confidence": 0.92
}
```

### 3. Configuración .env ✅
```properties
VITE_USE_MOCK=true
VITE_MOCK_API_URL=http://localhost:3001
```
**Resultado:** ✅ Configurado correctamente

---

## 🐛 **POSIBLES CAUSAS**

### 1. Caché del Navegador
El navegador puede estar usando una versión antigua del código.

**Solución:**
1. Abre DevTools (F12)
2. Pestaña "Network"
3. Marca "Disable cache"
4. Recarga con Ctrl+Shift+R (hard reload)

### 2. Variables de Entorno no Cargadas
Vite necesita reiniciarse cuando cambias el `.env`

**Solución:**
1. Detén el servidor frontend (Ctrl+C)
2. Reinicia: `npm run dev`
3. Espera a que diga "ready"

### 3. CORS Bloqueado
El navegador puede estar bloqueando las peticiones.

**Verificar:**
1. Abre DevTools (F12)
2. Pestaña "Console"
3. Busca errores de CORS
4. Busca errores de red

### 4. AudioRecorder no Llama los Callbacks
El componente puede no estar llamando `onCommand` correctamente.

**Verificar:**
1. Abre DevTools (F12)
2. Pestaña "Console"
3. Di un comando
4. Busca: `"🎯 handleCommand llamado con:"`
5. Si no aparece, el problema está en AudioRecorder

---

## 🔍 **PASOS DE DEBUGGING**

### Paso 1: Verificar que el Audio se Activa
1. Click en "▶️ Activar Micrófono"
2. Deberías ver en logs: "🎤 Sistema de comandos de voz INICIADO"
3. Deberías ver: "🎤 Grabando (Web Speech)"

### Paso 2: Verificar que la Voz se Detecta
1. Di "TravisTEC bitcoin"
2. Deberías ver en logs: "🎤 Transcripción: travistec bitcoin"
3. Si no aparece, el problema es el micrófono

### Paso 3: Verificar que el Comando se Parsea
1. Después de la transcripción
2. Deberías ver en logs: "🎯 Comando parseado: {...}"
3. Si no aparece, el problema es el parseCommand

### Paso 4: Verificar la Llamada API
1. Abre DevTools → Network
2. Di un comando
3. Deberías ver petición POST a `/api/v1/command/execute`
4. Click en la petición
5. Revisa Response

### Paso 5: Verificar la Respuesta
1. Después de la petición
2. Deberías ver en logs: "✅ Respuesta: ..."
3. Si no aparece, hay error en el servidor

---

## 🎯 **SOLUCIONES RÁPIDAS**

### Solución 1: Hard Reload
```
1. Presiona Ctrl+Shift+R
2. O:
   - Abre DevTools (F12)
   - Click derecho en el botón recargar
   - "Empty Cache and Hard Reload"
```

### Solución 2: Reiniciar Todo
```bash
# Terminal 1 - Mock Server
cd mock-server
node server.js

# Terminal 2 - Frontend
cd frontend-react
npm run dev
```

### Solución 3: Verificar Console
```javascript
// Abrir DevTools (F12)
// Pegar en Console:
console.log('VITE_USE_MOCK:', import.meta.env.VITE_USE_MOCK);
console.log('API URL:', import.meta.env.VITE_MOCK_API_URL);
```

### Solución 4: Test Manual
```bash
# Probar directamente el endpoint
curl -X POST http://localhost:3001/api/v1/command/execute \
  -H "Content-Type: application/json" \
  -d '{"task":"bitcoin","text":"bitcoin","params":{}}'
```

---

## 📊 **FLUJO ESPERADO**

```
1. Usuario dice "TravisTEC bitcoin"
   ↓
2. Web Speech API transcribe → "travistec bitcoin"
   ↓
3. parseCommand() detecta task="bitcoin"
   ↓
4. onCommand({task:"bitcoin", text:"bitcoin", params:{}})
   ↓
5. handleCommand() recibe el comando
   ↓
6. apiClient.processCommand() → POST /api/v1/command/execute
   ↓
7. Mock Server responde: "📈 Predicción Bitcoin: $48835.15..."
   ↓
8. handleCommand() añade a logs: "✅ Respuesta: ..."
   ↓
9. Usuario ve la respuesta en pantalla
```

---

## 🔧 **DEBUGGING EN VIVO**

### En DevTools Console:
```javascript
// Ver configuración actual
console.log({
  useMock: import.meta.env.VITE_USE_MOCK,
  mockUrl: import.meta.env.VITE_MOCK_API_URL,
  apiUrl: import.meta.env.VITE_API_URL
});

// Probar API directamente
fetch('http://localhost:3001/api/v1/command/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({task:'bitcoin',text:'bitcoin',params:{}})
})
.then(r => r.json())
.then(console.log);
```

---

## ✅ **CHECKLIST DE VERIFICACIÓN**

- [ ] Mock server corriendo (puerto 3001)
- [ ] Frontend corriendo (puerto 5173)
- [ ] .env tiene VITE_USE_MOCK=true
- [ ] Navegador sin caché (Ctrl+Shift+R)
- [ ] DevTools Console abierto
- [ ] Network tab mostrando peticiones
- [ ] Botón "Activar Micrófono" clickeado
- [ ] Permisos de micrófono aceptados
- [ ] Indicador de grabación visible
- [ ] Logs mostrando transcripciones
- [ ] Logs mostrando comandos parseados
- [ ] Logs mostrando respuestas

---

## 🚨 **ERRORES COMUNES**

### Error 1: "No se pudo acceder al micrófono"
**Causa:** Permisos no otorgados  
**Solución:** Permitir micrófono en el navegador

### Error 2: "CORS policy"
**Causa:** Mock server no configurado correctamente  
**Solución:** Verificar que mock-server/server.js tenga `app.use(cors())`

### Error 3: "Network Error"
**Causa:** Mock server no está corriendo  
**Solución:** Iniciar `node server.js` en mock-server/

### Error 4: "Cannot read property 'response'"
**Causa:** Mock server devuelve formato incorrecto  
**Solución:** Verificar que devuelve `{response: "..."}`

### Error 5: Transcribe pero no parsea
**Causa:** No dice "TravisTEC" al inicio  
**Solución:** Asegúrate de decir "TravisTEC" antes del comando

---

## 💡 **MEJORAS APLICADAS**

### 1. Logging Mejorado
```javascript
// Ahora todos los logs tienen emojis:
🎤 Transcripción: ...
🎯 Comando parseado: ...
✅ Respuesta: ...
❌ Error: ...
```

### 2. Console Debugging
```javascript
// Cada función ahora hace console.log:
console.log('📝 handleTranscription llamado con:', audioOrText);
console.log('🎯 handleCommand llamado con:', command);
console.log('✅ Respuesta del servidor:', response);
```

---

## 📞 **PRÓXIMOS PASOS**

1. Abre DevTools (F12)
2. Recarga la página (Ctrl+Shift+R)
3. Activa el micrófono
4. Di "TravisTEC bitcoin"
5. Observa la Console
6. Revisa qué paso del flujo falla
7. Reporta el error específico que ves

---

**Estado:** 🔍 DEBUGGING EN PROGRESO
