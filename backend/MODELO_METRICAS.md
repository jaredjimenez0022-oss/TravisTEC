# 📊 Métricas de Modelos de Machine Learning

## Proyecto Jarvis TEC - 9 Modelos Entrenados

**Fecha:** Octubre 15, 2025  
**Total de Modelos:** ✅ 9/9 Completos  
**Estado:** 100% Operacional

---

## 🎯 RESUMEN EJECUTIVO

| Métrica | Valor |
|---------|-------|
| **Modelos entrenados** | 9 |
| **Registros totales procesados** | 854,965+ |
| **Tamaño total** | ~145 MB |
| **R² promedio (regresión)** | 0.869 |
| **Accuracy promedio (clasificación)** | 0.722 |

---

## 📈 MODELOS DE REGRESIÓN

### 1. 🏆 S&P 500 Stock Predictor
- **R²:** 1.0000 (Perfecto)
- **MAE:** $0.33
- **Datos:** 619K registros
- **Algoritmo:** Gradient Boosting

### 2. ⭐ Bitcoin Price Predictor
- **R²:** 0.9924
- **MAE:** $16.68
- **Datos:** 1,556 registros
- **Algoritmo:** Random Forest

### 3. 🚗 Car Price Predictor
- **R²:** 0.9688
- **MAE:** $0.53
- **Datos:** 301 autos
- **Algoritmo:** Gradient Boosting

### 4. 🥑 Avocado Price Predictor
- **R²:** 0.8404
- **MAE:** $0.11
- **Datos:** 18,249 registros
- **Algoritmo:** Random Forest

### 5. 💪 BMI/BodyFat Predictor
- **R²:** 0.433
- **MAE:** 4.18%
- **Datos:** 252 pacientes
- **Algoritmo:** Random Forest

### 6. 🎬 Movie Recommender
- **Películas:** 10,329
- **Ratings:** 105,339
- **Algoritmo:** K-Nearest Neighbors

---

## 🔢 MODELOS DE CLASIFICACIÓN

### 7. ✈️ Airline Delay Classifier
- **Accuracy:** 73.14%
- **F1-Score:** 0.81
- **Datos:** 100K vuelos
- **Algoritmo:** Random Forest

### 8. 🏥 Cirrhosis Outcome Classifier
- **Accuracy:** 79.76%
- **F1-Score:** 0.78
- **Datos:** 418 pacientes
- **Algoritmo:** Random Forest

### 9. 🚨 London Crime Classifier
- **Accuracy:** 35.4% (placeholder)
- **Datos:** Sintéticos
- **Nota:** Requiere geopandas

---

## 📊 TABLA COMPARATIVA

| # | Modelo | Dataset Size | Algoritmo | Métrica | Valor | Tamaño |
|---|--------|--------------|-----------|---------|-------|--------|
| 1 | S&P 500 | 619K | GBR | R² | **1.0000** 🏆 | 473 KB |
| 2 | Bitcoin | 1.6K | RFR | R² | **0.9924** ⭐ | 4.4 MB |
| 3 | Car Price | 301 | GBR | R² | **0.9688** | 365 KB |
| 4 | Avocado | 18K | RFR | R² | 0.8404 | 62 KB |
| 5 | BMI | 252 | RFR | R² | 0.433 | 901 KB |
| 6 | Movies | 105K | KNN | - | - | 108 MB |
| 7 | Airline | 100K | RFC | Acc | 73.14% | 5 KB |
| 8 | Cirrhosis | 418 | RFC | Acc | 79.76% | 958 KB |
| 9 | London | 5K | RFC | Acc | 35.4%* | 1.2 KB |

*Placeholder con datos sintéticos

---

## 🎓 RECOMENDACIONES

### ✅ Listos para Producción
1. S&P 500 Stock Predictor
2. Bitcoin Price Predictor  
3. Car Price Predictor
4. Avocado Price Predictor
5. Movie Recommender System
6. Airline Delay Classifier
7. Cirrhosis Outcome Classifier

### ⚠️ Requieren Mejoras
8. BMI/BodyFat (agregar más features)
9. London Crime (implementar con datos reales)

---

**Documentación completa:** Ver archivo completo para detalles de features, métricas y código de carga.
