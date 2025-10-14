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
