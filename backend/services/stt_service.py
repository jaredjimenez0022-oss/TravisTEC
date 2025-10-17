# stt_service.py - Servicio de Speech-to-Text
import os
from dotenv import load_dotenv

load_dotenv()

class STTService:
    def __init__(self):
        self.service_type = os.getenv("STT_SERVICE", "azure")  # azure, google, whisper
        self.configure_service()
    
    def configure_service(self):
        """Configurar servicio STT según tipo"""
        if self.service_type == "azure":
            self.setup_azure()
        elif self.service_type == "google":
            self.setup_google()
        elif self.service_type == "whisper":
            self.setup_whisper()
        else:
            print(f"[WARN] Servicio STT no configurado: {self.service_type}")
    
    def setup_azure(self):
        """Configurar Azure Speech Services"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_key = os.getenv("AZURE_SPEECH_KEY", "")
            service_region = os.getenv("AZURE_SERVICE_REGION", "")
            
            if speech_key and service_region:
                self.speech_config = speechsdk.SpeechConfig(
                    subscription=speech_key,
                    region=service_region
                )
                self.speech_config.speech_recognition_language = "es-ES"
                self.configured = True
                print("[OK] Azure Speech configurado")
            else:
                self.configured = False
                print("[WARN] Azure Speech no configurado. Configure AZURE_SPEECH_KEY y AZURE_SERVICE_REGION")
        except ImportError:
            self.configured = False
            print("[WARN] Instale azure-cognitiveservices-speech")
    
    def setup_google(self):
        """Configurar Google Speech-to-Text"""
        try:
            from google.cloud import speech
            
            self.client = speech.SpeechClient()
            self.configured = True
            print("[OK] Google Speech configurado")
        except ImportError:
            self.configured = False
            print("[WARN] Instale google-cloud-speech")
        except Exception as e:
            self.configured = False
            print(f"[WARN] Error configurando Google Speech: {e}")
    
    def setup_whisper(self):
        """Configurar OpenAI Whisper (local)"""
        try:
            import importlib
            whisper = importlib.import_module('whisper')
            
            model_size = os.getenv("WHISPER_MODEL_SIZE", "base")
            self.model = whisper.load_model(model_size)
            self.configured = True
            print(f"[OK] Whisper configurado (modelo: {model_size})")
        except ImportError:
            self.configured = False
            print("[WARN] Instale openai-whisper")
        except Exception as e:
            self.configured = False
            print(f"[WARN] Error configurando Whisper: {e}")
    
    def is_available(self):
        """Verificar si el servicio está disponible"""
        return self.configured
    
    async def transcribe(self, audio_path: str):
        """
        Transcribir audio a texto
        
        Args:
            audio_path: Ruta al archivo de audio
            
        Returns:
            str: Texto transcrito
        """
        if not self.configured:
            return "Servicio STT no configurado"
        
        try:
            if self.service_type == "azure":
                return await self.transcribe_azure(audio_path)
            elif self.service_type == "google":
                return await self.transcribe_google(audio_path)
            elif self.service_type == "whisper":
                return await self.transcribe_whisper(audio_path)
        except Exception as e:
            return f"Error en transcripción: {str(e)}"
    
    async def transcribe_azure(self, audio_path: str):
        """Transcribir con Azure Speech"""
        import azure.cognitiveservices.speech as speechsdk
        
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        result = speech_recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No se pudo reconocer el audio"
        else:
            return f"Error: {result.reason}"
    
    async def transcribe_google(self, audio_path: str):
        """Transcribir con Google Speech-to-Text"""
        from google.cloud import speech
        
        with open(audio_path, 'rb') as audio_file:
            content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="es-ES"
        )
        
        response = self.client.recognize(config=config, audio=audio)
        
        if response.results:
            return response.results[0].alternatives[0].transcript
        return "No se pudo reconocer el audio"
    
    async def transcribe_whisper(self, audio_path: str):
        """Transcribir con Whisper (local)"""
        result = self.model.transcribe(audio_path, language="es")
        return result["text"]
