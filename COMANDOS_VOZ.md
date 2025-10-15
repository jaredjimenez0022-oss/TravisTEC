# 🎤 COMANDOS DE VOZ - TRAVISTEC

## Guía Completa de Comandos de Voz para el Asistente TravisTEC

Todos los comandos deben comenzar con la palabra clave **"TravisTEC"** seguida de la instrucción.

---

## 📋 LISTA DE 10 COMANDOS IMPLEMENTADOS

### 1️⃣ **Predicción de Bitcoin**
**Comando:** 
```
"TravisTEC bitcoin"
"TravisTEC predice el precio del bitcoin"
```

**Parámetros:** Ninguno (usa datos históricos recientes)

**Ejemplo de uso:**
- 🎤 "TravisTEC bitcoin"
- 🎤 "TravisTEC cuál es el precio del bitcoin"

**Respuesta esperada:**
```json
{
  "model": "bitcoin_model",
  "prediction": 45234.56,
  "message": "Predicción de Bitcoin: $45,234.56"
}
```

---

### 2️⃣ **Recomendación de Películas**
**Comando:** 
```
"TravisTEC recomienda una película"
"TravisTEC película [título]"
```

**Parámetros:** 
- `title` (opcional): Título de película para buscar similares

**Ejemplos de uso:**
- 🎤 "TravisTEC recomienda una película"
- 🎤 "TravisTEC película titanic"
- 🎤 "TravisTEC película matrix"

**Respuesta esperada:**
```json
{
  "model": "movie_recommender",
  "recommendations": [
    "The Matrix Reloaded",
    "The Matrix Revolutions",
    "Inception",
    "Interstellar",
    "Dark City"
  ]
}
```

---

### 3️⃣ **Predicción de Precio de Automóvil**
**Comando:** 
```
"TravisTEC automóvil [año] [kilometraje]"
"TravisTEC coche [año] [km]"
```

**Parámetros REQUERIDOS:**
- `year`: Año del vehículo (ej: 2015, 2020)
- `km`: Kilometraje del vehículo (ej: 50000, 120000)

**Ejemplos de uso:**
- 🎤 "TravisTEC automóvil 2015 80000"
- 🎤 "TravisTEC coche 2020 50000"
- 🎤 "TravisTEC predice el precio de un carro año 2018 con 100000 kilómetros"

**Respuesta esperada:**
```json
{
  "model": "car_model",
  "input": {"year": 2015, "km": 80000},
  "prediction": 12500.75,
  "message": "Precio estimado: $12,500.75"
}
```

---

### 4️⃣ **Predicción del S&P 500**
**Comando:** 
```
"TravisTEC sp500 [años]"
"TravisTEC predice el sp500 en [años] años"
```

**Parámetros:**
- `years` (opcional): Años hacia el futuro (default: 1)

**Ejemplos de uso:**
- 🎤 "TravisTEC sp500"
- 🎤 "TravisTEC sp500 en 2 años"
- 🎤 "TravisTEC predice el sp 500 para 5 años"

**Respuesta esperada:**
```json
{
  "model": "sp500_model",
  "input": {"years": 2},
  "prediction": 5234.67,
  "message": "Predicción S&P 500 (2 años): 5,234.67 puntos"
}
```

---

### 5️⃣ **Predicción de Masa Corporal (IMC/Grasa)**
**Comando:** 
```
"TravisTEC masa corporal [altura] [peso] [edad]"
"TravisTEC imc [altura] [peso]"
```

**Parámetros REQUERIDOS:**
- `height`: Altura en cm (ej: 175, 180)
- `weight`: Peso en kg (ej: 70, 85)
- `age` (opcional): Edad en años (default: 30)

**Ejemplos de uso:**
- 🎤 "TravisTEC masa corporal 180 75 28"
- 🎤 "TravisTEC imc 175 80"
- 🎤 "TravisTEC predice mi masa corporal, mido 182 y peso 90 kilos, tengo 35 años"

**Respuesta esperada:**
```json
{
  "model": "bmi_model",
  "input": {"height": 180, "weight": 75, "age": 28},
  "prediction": 18.5,
  "message": "Porcentaje de grasa corporal estimado: 18.5%"
}
```

---

### 6️⃣ **Predicción de Precio de Aguacate**
**Comando:** 
```
"TravisTEC aguacate [años]"
"TravisTEC predice el precio del aguacate en [años] años"
```

**Parámetros:**
- `years` (opcional): Años hacia el futuro (default: 1)

**Ejemplos de uso:**
- 🎤 "TravisTEC aguacate"
- 🎤 "TravisTEC aguacate en 3 años"
- 🎤 "TravisTEC predice el precio del aguacate"

**Respuesta esperada:**
```json
{
  "model": "avocado_model",
  "input": {"years": 3},
  "prediction": 1.45,
  "message": "Precio estimado del aguacate (3 años): $1.45"
}
```

---

### 7️⃣ **Predicción de Crímenes en Londres**
**Comando:** 
```
"TravisTEC Londres [día de la semana]"
"TravisTEC crímenes en Londres el [día]"
```

**Parámetros:**
- `day`: Día de la semana (lunes, martes, miércoles, jueves, viernes, sábado, domingo)

**Ejemplos de uso:**
- 🎤 "TravisTEC Londres lunes"
- 🎤 "TravisTEC crímenes en Londres el viernes"
- 🎤 "TravisTEC predice crímenes Londres sábado"

**Respuesta esperada:**
```json
{
  "model": "london_crime",
  "input": {"day": "lunes"},
  "prediction": 342,
  "message": "Crímenes estimados en Londres (lunes): 342"
}
```

---

### 8️⃣ **Predicción de Crímenes en Chicago**
**Comando:** 
```
"TravisTEC Chicago [día de la semana]"
"TravisTEC crímenes en Chicago el [día]"
```

**Parámetros:**
- `day`: Día de la semana (lunes, martes, miércoles, jueves, viernes, sábado, domingo)

**Ejemplos de uso:**
- 🎤 "TravisTEC Chicago martes"
- 🎤 "TravisTEC crímenes en Chicago el domingo"
- 🎤 "TravisTEC predice Chicago miércoles"

**Respuesta esperada:**
```json
{
  "model": "chicago_crime",
  "input": {"day": "martes"},
  "prediction": 487,
  "message": "Crímenes estimados en Chicago (martes): 487"
}
```

---

### 9️⃣ **Clasificación de Cirrosis**
**Comando:** 
```
"TravisTEC cirrosis"
"TravisTEC clasifica cirrosis"
```

**Parámetros:** 
- `features` (opcional): Valores numéricos de características médicas

**Ejemplos de uso:**
- 🎤 "TravisTEC cirrosis"
- 🎤 "TravisTEC clasifica el tipo de cirrosis"

**Respuesta esperada:**
```json
{
  "model": "cirrhosis_classifier",
  "prediction": "C",
  "probability": {
    "C": 0.65,
    "CL": 0.25,
    "D": 0.10
  },
  "message": "Clasificación: C (Cirrosis - 65% confianza)"
}
```

---

### 🔟 **Predicción de Precio de Vuelo**
**Comando:** 
```
"TravisTEC avión [lugar] [mes]"
"TravisTEC vuelo desde [lugar] en [mes]"
```

**Parámetros:**
- `location`: Lugar de origen/destino
- `month`: Mes del vuelo (enero-diciembre o 1-12)

**Ejemplos de uso:**
- 🎤 "TravisTEC avión desde San José en marzo"
- 🎤 "TravisTEC vuelo a Miami en julio"
- 🎤 "TravisTEC predice precio de vuelo para Nueva York en diciembre"

**Respuesta esperada:**
```json
{
  "model": "airline_delay",
  "input": {"location": "San José", "month": 3},
  "prediction": 0.23,
  "message": "Probabilidad de retraso: 23%"
}
```

---

## 🎯 GUÍA DE USO RÁPIDO

### Estructura General:
```
"TravisTEC" + [comando] + [parámetros]
```

### Ejemplos Prácticos:

| # | Comando Completo | Descripción |
|---|------------------|-------------|
| 1 | `TravisTEC bitcoin` | Precio de Bitcoin |
| 2 | `TravisTEC película matrix` | Recomienda películas similares |
| 3 | `TravisTEC coche 2020 50000` | Precio de auto (año 2020, 50K km) |
| 4 | `TravisTEC sp500 en 3 años` | S&P 500 en 3 años |
| 5 | `TravisTEC imc 180 75 30` | Masa corporal (180cm, 75kg, 30 años) |
| 6 | `TravisTEC aguacate en 2 años` | Precio aguacate en 2 años |
| 7 | `TravisTEC Londres viernes` | Crímenes en Londres el viernes |
| 8 | `TravisTEC Chicago lunes` | Crímenes en Chicago el lunes |
| 9 | `TravisTEC cirrosis` | Clasifica tipo de cirrosis |
| 10 | `TravisTEC vuelo a Miami en julio` | Precio vuelo a Miami en julio |

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Frontend (AudioRecorder.jsx)
El componente `AudioRecorder` utiliza:
1. **Web Speech API** para reconocimiento de voz en tiempo real
2. **MediaRecorder API** como fallback
3. Función `parseCommand()` que extrae:
   - Palabra clave: `travistec`
   - Tipo de tarea: `bitcoin`, `movie`, `car`, etc.
   - Parámetros: números, días, lugares, etc.

### Backend (app.py + model_runner.py)
El backend procesa comandos mediante:
1. Endpoint `/api/process` recibe el comando parseado
2. `ModelRunner.run_model()` ejecuta el modelo correspondiente
3. Métodos de conversión `_to_features_for_model()` preparan los datos
4. Retorna predicción en formato JSON

---

## 📊 MODELOS ML ASOCIADOS

| Comando | Modelo | Archivo |
|---------|--------|---------|
| Bitcoin | Random Forest Regressor | `bitcoin_model.joblib` |
| Películas | K-Nearest Neighbors | `movie_recommender.joblib` |
| Automóvil | Gradient Boosting | `car_model.joblib` |
| S&P 500 | Gradient Boosting | `sp500_model.joblib` |
| Masa Corporal | Random Forest | `bmi_model.joblib` |
| Aguacate | Random Forest | `avocado_model.joblib` |
| Londres | Random Forest | `london_crime.joblib` |
| Chicago | Random Forest | `chicago_crime.joblib` |
| Cirrosis | Random Forest Classifier | `cirrhosis_model.joblib` |
| Avión | Random Forest Classifier | `airline_delay_model.joblib` |

---

## ✅ CHECKLIST DE VALIDACIÓN

- [x] 1. Bitcoin - Sin parámetros
- [x] 2. Películas - Título opcional
- [x] 3. Automóvil - Año + Kilometraje
- [x] 4. S&P 500 - Años (opcional)
- [x] 5. Masa Corporal - Altura + Peso + Edad
- [x] 6. Aguacate - Años (opcional)
- [x] 7. Londres - Día de la semana
- [x] 8. Chicago - Día de la semana
- [x] 9. Cirrosis - Features opcionales
- [x] 10. Avión - Lugar + Mes

---

## 🎉 ESTADO: TODOS LOS COMANDOS IMPLEMENTADOS

**Total:** 10/10 comandos ✅  
**Frontend:** Parsing completo ✅  
**Backend:** Modelos cargados ✅  
**Documentación:** Completa ✅  

---

**Última actualización:** Octubre 15, 2025  
**Proyecto:** TravisTEC - Asistente Inteligente con IA
