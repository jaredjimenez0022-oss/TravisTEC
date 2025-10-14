# model_runner.py - Carga y ejecuta modelos de ML
import os
import joblib
import pickle
from pathlib import Path

class ModelRunner:
    def __init__(self):
        self.models_dir = Path(__file__).parent.parent / "models"
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Cargar todos los modelos disponibles"""
        if not self.models_dir.exists():
            print(f"⚠️ Directorio de modelos no encontrado: {self.models_dir}")
            return
        
        # Buscar archivos .joblib y .pkl
        for model_file in self.models_dir.glob("*.joblib"):
            try:
                model_name = model_file.stem
                self.models[model_name] = joblib.load(model_file)
                print(f"✓ Modelo cargado: {model_name}")
            except Exception as e:
                print(f"✗ Error cargando {model_file}: {e}")
        
        for model_file in self.models_dir.glob("*.pkl"):
            try:
                model_name = model_file.stem
                with open(model_file, 'rb') as f:
                    self.models[model_name] = pickle.load(f)
                print(f"✓ Modelo cargado: {model_name}")
            except Exception as e:
                print(f"✗ Error cargando {model_file}: {e}")
    
    def is_ready(self):
        """Verificar si hay modelos cargados"""
        return len(self.models) > 0
    
    def run_model(self, text: str, model_name: str = None):
        """
        Ejecutar modelo con el texto de entrada
        
        Args:
            text: Texto de entrada
            model_name: Nombre del modelo a usar (opcional)
            
        Returns:
            str: Respuesta del modelo
        """
        if not self.models:
            return "No hay modelos disponibles. Por favor entrena un modelo primero."
        
        # Si no se especifica modelo, usar el primero disponible
        if model_name is None:
            model_name = list(self.models.keys())[0]
        
        if model_name not in self.models:
            return f"Modelo '{model_name}' no encontrado. Modelos disponibles: {list(self.models.keys())}"
        
        try:
            model = self.models[model_name]
            
            # Aquí iría la lógica específica según el tipo de modelo
            # Este es un ejemplo básico
            if hasattr(model, 'predict'):
                # Modelo de clasificación/regresión
                prediction = model.predict([text])
                return f"Predicción: {prediction[0]}"
            elif hasattr(model, 'transform'):
                # Transformador (vectorizador, etc.)
                transformed = model.transform([text])
                return f"Transformación aplicada: {transformed.shape}"
            else:
                return f"Modelo cargado pero tipo no soportado: {type(model)}"
                
        except Exception as e:
            return f"Error ejecutando modelo: {str(e)}"
    
    def get_available_models(self):
        """Obtener lista de modelos disponibles"""
        return list(self.models.keys())

    def get_model(self, name):
        return self.models.get(name)
    
    def reload_models(self):
        """Recargar todos los modelos"""
        self.models = {}
        self.load_models()
