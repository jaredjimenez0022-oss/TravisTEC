# azure_face.py - Servicio de reconocimiento facial con Azure
import os
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv

load_dotenv()

class AzureFaceService:
    def __init__(self):
        self.key = os.getenv("AZURE_FACE_KEY", "")
        self.endpoint = os.getenv("AZURE_FACE_ENDPOINT", "")
        self.person_group_id = os.getenv("AZURE_PERSON_GROUP_ID", "jarvis-tec-group")
        
        if self.key and self.endpoint:
            self.client = FaceClient(
                self.endpoint,
                CognitiveServicesCredentials(self.key)
            )
        else:
            self.client = None
            print("⚠️ Azure Face API no configurado. Configure AZURE_FACE_KEY y AZURE_FACE_ENDPOINT")
    
    def is_configured(self):
        """Verificar si el servicio está configurado"""
        return self.client is not None
    
    async def identify_face(self, image_data: bytes):
        """
        Identificar rostro en una imagen
        
        Args:
            image_data: Datos binarios de la imagen
            
        Returns:
            dict: Información del rostro identificado
        """
        if not self.client:
            return {
                "identified": False,
                "message": "Azure Face API no configurado"
            }
        
        try:
            # Detectar rostros en la imagen
            detected_faces = self.client.face.detect_with_stream(
                image_data,
                detection_model='detection_03',
                recognition_model='recognition_04',
                return_face_attributes=['emotion', 'age', 'gender']
            )
            
            if not detected_faces:
                return {
                    "identified": False,
                    "message": "No se detectaron rostros"
                }
            
            # Extraer IDs de rostros detectados
            face_ids = [face.face_id for face in detected_faces]
            
            # Intentar identificar rostros
            try:
                results = self.client.face.identify(face_ids, self.person_group_id)
                
                if results and results[0].candidates:
                    candidate = results[0].candidates[0]
                    person = self.client.person_group_person.get(
                        self.person_group_id,
                        candidate.person_id
                    )
                    
                    face = detected_faces[0]
                    return {
                        "identified": True,
                        "name": person.name,
                        "confidence": candidate.confidence,
                        "attributes": {
                            "age": face.face_attributes.age if face.face_attributes else None,
                            "gender": face.face_attributes.gender if face.face_attributes else None,
                            "emotion": face.face_attributes.emotion.as_dict() if face.face_attributes else None
                        }
                    }
            except Exception as e:
                print(f"Error en identificación: {e}")
            
            # Si no se identificó pero hay rostro
            face = detected_faces[0]
            return {
                "identified": False,
                "message": "Rostro detectado pero no identificado",
                "face_detected": True,
                "attributes": {
                    "age": face.face_attributes.age if face.face_attributes else None,
                    "gender": face.face_attributes.gender if face.face_attributes else None,
                    "emotion": face.face_attributes.emotion.as_dict() if face.face_attributes else None
                }
            }
            
        except Exception as e:
            return {
                "identified": False,
                "error": str(e)
            }
    
    async def create_person_group(self):
        """Crear grupo de personas para reconocimiento"""
        if not self.client:
            return False
        
        try:
            self.client.person_group.create(
                person_group_id=self.person_group_id,
                name="Jarvis TEC Users",
                recognition_model='recognition_04'
            )
            return True
        except Exception as e:
            print(f"Error creando grupo: {e}")
            return False
    
    async def add_person(self, name: str, image_paths: list):
        """
        Agregar persona al grupo de reconocimiento
        
        Args:
            name: Nombre de la persona
            image_paths: Lista de rutas a imágenes de la persona
        """
        if not self.client:
            return None
        
        try:
            # Crear persona
            person = self.client.person_group_person.create(
                self.person_group_id,
                name=name
            )
            
            # Agregar imágenes
            for image_path in image_paths:
                with open(image_path, 'rb') as image:
                    self.client.person_group_person.add_face_from_stream(
                        self.person_group_id,
                        person.person_id,
                        image
                    )
            
            # Entrenar el grupo
            self.client.person_group.train(self.person_group_id)
            
            return person.person_id
        except Exception as e:
            print(f"Error agregando persona: {e}")
            return None
