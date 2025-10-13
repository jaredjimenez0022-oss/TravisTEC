# app.py - FastAPI Backend
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from services.azure_face import AzureFaceService
from services.model_runner import ModelRunner
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
azure_face = AzureFaceService()
model_runner = ModelRunner()
stt_service = STTService()

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

@app.post("/api/recognize-face")
async def recognize_face(image: UploadFile = File(...)):
    """
    Reconocer rostro usando Azure Face API
    """
    try:
        # Leer imagen
        image_data = await image.read()
        
        # Procesar con Azure Face
        result = await azure_face.identify_face(image_data)
        
        return result
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

@app.get("/api/health")
async def health_check():
    """
    Verificar el estado del sistema
    """
    return {
        "status": "healthy",
        "services": {
            "azure_face": azure_face.is_configured(),
            "model_runner": model_runner.is_ready(),
            "stt_service": stt_service.is_available()
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
