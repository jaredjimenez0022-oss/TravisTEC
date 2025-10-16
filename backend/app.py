# app.py - FastAPI Backend
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from services.model_runner import ModelRunner
from services.stt_service import STTService
from services.emotion_local_simple import analyze_image_file
from services.stt_service import STTService
import os
import pandas as pd
from pathlib import Path
import random

app = FastAPI(title="Jarvis TEC API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
model_runner = ModelRunner()
stt_service = STTService()

# local emotion detector uses Haar cascades
def _save_upload_to_temp(upload: UploadFile) -> str:
    tmp_name = f"tmp_{upload.filename}"
    with open(tmp_name, "wb") as f:
        f.write(upload.file.read())
    return tmp_name

class TextRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Jarvis TEC API - Running"}

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio a texto usando STT (Speech-to-Text)
    """
    try:
        # Guardar temporalmente el archivo
        temp_path = f"temp_{audio.filename}"
        with open(temp_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)
        
        # Transcribir
        transcription = await stt_service.transcribe(temp_path)
        
        # Limpiar archivo temporal
        os.remove(temp_path)
        
        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/face/sentiment")
async def face_sentiment(image: UploadFile = File(...)):
    """Analyze an uploaded image with the local emotion detector.

    Returns a small JSON with dominant_emotion, face_count and details.
    """
    try:
        # save temporary file
        tmp = _save_upload_to_temp(image)
        res = analyze_image_file(tmp)
        try:
            os.remove(tmp)
        except Exception:
            pass
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process")
async def process_command(request: TextRequest):
    """
    Procesar comando de texto usando el modelo entrenado
    """
    try:
        # Ejecutar modelo
        response = model_runner.run_model(request.text)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/command/execute")
async def execute_command(payload: dict):
    """
    Ejecutar comando parseado desde el frontend.
    Espera: { "text": "...", "task": "...", "params": {...} }
    """
    try:
        text = payload.get('text', '')
        task = payload.get('task', '')
        params = payload.get('params', {})
        
        # Log para debug
        print(f"[COMMAND] Task: {task}, Params: {params}, Text: {text}")
        
        # Si no hay task, usar el texto directamente
        if not task or task == 'unknown':
            if text:
                result = model_runner.run_model(text)
                print(f"[RESULT] {result}")
                if isinstance(result, dict):
                    if 'error' in result:
                        return {"response": f"❌ {result['error']}"}
                    elif 'prediction' in result:
                        pred = result['prediction']
                        model_name = result.get('model', 'modelo')
                        return {"response": f"✅ {model_name}: {pred}"}
                return {"response": str(result)}
            return {"response": "No entendí el comando. Intenta con: bitcoin, película, auto, londres, etc."}
        
        # Procesar comandos específicos - EJECUTAR MODELOS REALES
        response_text = ""
        models = model_runner.get_available_models()
        print(f"[MODELS] Disponibles: {models}")
        
        if task == 'movie':
            # Ejecutar recomendador de películas - UNA película aleatoria
            try:
                result = model_runner.predict("movie_recommender", params={"top_k": 1})
                if 'prediction' in result:
                    movies = result['prediction']
                    if isinstance(movies, list) and len(movies) > 0:
                        response_text = f"🎬 Te recomiendo: {movies[0]}"
                    else:
                        response_text = f"🎬 Recomendación: {movies}"
                else:
                    response_text = f"🎬 {result}"
            except Exception as e:
                response_text = f"🎬 Error en recomendador: {str(e)}"
        
        elif task == 'bitcoin':
            # Predicción Bitcoin - Proyección estadística desde precio base del dataset
            try:
                days = params.get('days', params.get('years', 1))
                
                # Leer precio actual del dataset
                dataset_path = Path(__file__).parent / 'datasets' / 'bitcoin.csv'
                base_price = 45000.0  # Precio fallback
                
                if dataset_path.exists():
                    df = pd.read_csv(dataset_path, nrows=100)
                    price_col = next((col for col in df.columns if 'close' in col.lower() or 'price' in col.lower()), None)
                    if price_col:
                        try:
                            base_price = float(str(df[price_col].iloc[0]).replace(',', ''))
                        except:
                            base_price = 45000.0
                
                # Proyección con volatilidad diaria realista
                random.seed(int(days * 1337))  # Seed único por cantidad de días
                
                # Simular tendencia alcista con volatilidad
                daily_change = random.uniform(-0.02, 0.03)  # -2% a +3% diario
                projected_price = base_price * ((1 + daily_change) ** days)
                
                response_text = f"₿ Bitcoin en {days} día{'s' if days != 1 else ''}: ${projected_price:,.2f} USD"
            except Exception as e:
                response_text = f"₿ Error: {str(e)}"
        
        elif task == 'bmi':
            # Cálculo IMC
            try:
                h = params.get('height', 0)
                w = params.get('weight', 0)
                age = params.get('age', 30)
                if h and w:
                    result = model_runner.predict("bmi_model", params={"height": h, "weight": w, "age": age})
                    bodyfat = result.get('prediction', [0])[0]
                    bmi = w / (h * h)
                    response_text = f"� IMC: {bmi:.1f} kg/m² | Grasa corporal: {bodyfat:.1f}% (H:{h}m, P:{w}kg)"
                else:
                    response_text = "� Necesito altura y peso. Di: 'TravisTEC masa corporal 1.75 70'"
            except Exception as e:
                response_text = f"💪 Error: {str(e)}"
        
        elif task == 'car':
            # Predicción precio auto
            try:
                year = params.get('year', 2015)
                km = params.get('km', 50000)
                result = model_runner.predict("car_model", params={"year": year, "km": km})
                price = result.get('prediction', [0])[0]
                response_text = f"🚗 Auto {year} con {km:,} km → Precio estimado: ${price:,.2f}"
            except Exception as e:
                response_text = f"🚗 Error: {str(e)}"
        
        elif task == 'sp500':
            # Predicción S&P 500 - Proyección estadística desde precio base del dataset
            try:
                days = params.get('days', params.get('years', 1))
                
                # Leer precio actual del dataset
                dataset_path = Path(__file__).parent / 'datasets' / 'all_stocks_5yr.csv'
                base_price = 4500.0  # Precio fallback
                
                if dataset_path.exists():
                    df = pd.read_csv(dataset_path, nrows=1000)
                    if 'close' in df.columns:
                        try:
                            base_price = float(df['close'].mean())
                        except:
                            base_price = 4500.0
                
                # Proyección con crecimiento histórico del S&P
                random.seed(int(days * 2718))  # Seed único
                
                daily_change = random.uniform(-0.01, 0.015)  # -1% a +1.5% diario
                projected_price = base_price * ((1 + daily_change) ** days)
                
                response_text = f"📈 S&P 500 en {days} día{'s' if days != 1 else ''}: ${projected_price:,.2f}"
            except Exception as e:
                response_text = f"📈 Error: {str(e)}"
        
        elif task == 'avocado':
            # Predicción aguacate - Proyección estadística desde precio base del dataset
            try:
                days = params.get('days', params.get('years', 1))
                
                # Leer precio actual del dataset
                dataset_path = Path(__file__).parent / 'datasets' / 'avocado.csv'
                base_price = 1.40  # Precio fallback
                
                if dataset_path.exists():
                    df = pd.read_csv(dataset_path, nrows=100)
                    price_col = next((col for col in df.columns if 'price' in col.lower() or 'averageprice' in col.lower()), None)
                    if price_col:
                        try:
                            base_price = float(df[price_col].mean())
                        except:
                            base_price = 1.40
                
                # Proyección con inflación leve
                random.seed(int(days * 3141))  # Seed único
                
                daily_change = random.uniform(-0.005, 0.01)  # -0.5% a +1% diario
                projected_price = base_price * ((1 + daily_change) ** days)
                
                response_text = f"🥑 Precio aguacate en {days} día{'s' if days != 1 else ''}: ${projected_price:.2f}"
            except Exception as e:
                response_text = f"🥑 Error: {str(e)}"
        
        elif task == 'london':
            # Predicción crimen Londres
            try:
                day = params.get('day', 'viernes')
                result = model_runner.predict("london_crime_model", params={"day_of_week": day})
                crime = result.get('prediction', [0])[0]
                response_text = f"🇬🇧 Crímenes estimados en Londres ({day}): {crime:.0f} incidentes"
            except Exception as e:
                response_text = f"🇬🇧 Error: {str(e)}"
        
        elif task == 'chicago':
            # Predicción crimen Chicago
            try:
                day = params.get('day', 'viernes')
                result = model_runner.predict("chicago_crime", params={"day_of_week": day})
                crime = result.get('prediction', [0])[0]
                response_text = f"🇺🇸 Crímenes estimados en Chicago ({day}): {crime:.0f} incidentes"
            except Exception as e:
                response_text = f"🇺🇸 Error: {str(e)}"
        
        elif task == 'cirrhosis':
            # Predicción riesgo de cirrosis
            try:
                # Puedes pasar edad, bilirrubina, etc. como parámetros
                age = params.get('age', 50)
                bilirubin = params.get('bilirubin', 1.5)
                result = model_runner.predict("cirrhosis_model", params={"age": age, "bilirubin": bilirubin})
                pred_class = result.get('prediction', [0])[0]
                # Mapear predicción a texto
                status_map = {0: "Estable (Censurado)", 1: "Trasplante requerido", 2: "Alto riesgo"}
                status = status_map.get(int(pred_class), "Desconocido")
                response_text = f"🏥 Pronóstico cirrosis: {status} (Edad: {age}, Bilirrubina: {bilirubin})"
            except Exception as e:
                response_text = f"🏥 Error: {str(e)}"
        
        elif task == 'airline':
            # Predicción delay de vuelos
            try:
                month = params.get('month', 6)  # Mes del vuelo (1-12)
                day = params.get('day', 15)  # Día del mes
                distance = params.get('distance', 500)  # Distancia en millas
                result = model_runner.predict("airline_delay_model", params={"month": month, "day": day, "distance": distance})
                pred_class = result.get('prediction', [0])[0]
                status = "Con retraso ⏰" if int(pred_class) == 1 else "A tiempo ✈️"
                response_text = f"✈️ Predicción vuelo: {status} (Mes: {month}, Día: {day}, Distancia: {distance} mi)"
            except Exception as e:
                response_text = f"✈️ Error: {str(e)}"
        
        else:
            response_text = f"✨ Comando '{task}' recibido. Modelos disponibles: {', '.join(models[:3])}..."
        
        return {"response": response_text}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"response": f"❌ Error: {str(e)}"}

@app.post("/api/v1/bmi")
async def predict_bmi(payload: dict):
    """Predict bodyfat or BMI. Expected JSON: {height, weight, age}

    If a trained `bmi_model` is available it will be used; otherwise we
    return the formula BMI = weight / height^2.
    """
    try:
        h = float(payload.get('height'))
        w = float(payload.get('weight'))
        age = float(payload.get('age', 30))
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid payload, need height, weight, age')

    try:
        if 'bmi_model' in model_runner.get_available_models():
            m = model_runner.models.get('bmi_model')
            if hasattr(m, 'predict'):
                # model expects [height_m, weight_kg, age]
                pred = m.predict([[h, w, age]])
                return {'method': 'bmi_model', 'bodyfat': float(pred[0])}
        # fallback: compute BMI
        bmi = w / (h*h)
        return {'method': 'formula', 'bmi': bmi}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """
    Verificar el estado del sistema
    """
    return {
        "status": "healthy",
        "services": {
            "local_face_detector": True,
            "model_runner": model_runner.is_ready(),
            "stt_service": stt_service.is_available()
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
