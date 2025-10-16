# backend/services/model_runner.py
import os
import joblib
import numpy as np
import traceback
import random
from typing import List, Dict, Any, Optional

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

class ModelRunner:
    """
    Carga modelos .joblib desde backend/models/ al inicializarse.
    Provee:
      - get_available_models()
      - predict(model_name, features=None, params=None)
      - run_model(command_text)  # mapeo rápido de texto -> modelo
    """

    def __init__(self, model_dir: str = MODEL_DIR):
        self.model_dir = os.path.abspath(model_dir)
        self.models: Dict[str, Any] = {}
        self._load_all_models()

    def _load_all_models(self):
        if not os.path.isdir(self.model_dir):
            print(f"[ModelRunner] directorio de modelos no encontrado: {self.model_dir}")
            return
        for f in os.listdir(self.model_dir):
            if f.endswith(".joblib"):
                name = f.replace(".joblib", "")
                path = os.path.join(self.model_dir, f)
                try:
                    self.models[name] = joblib.load(path)
                    print(f"[ModelRunner] cargado modelo: {name}")
                except Exception as e:
                    print(f"[ModelRunner] ERROR cargando {f}: {e}")
                    traceback.print_exc()

    def get_available_models(self) -> List[str]:
        return list(self.models.keys())

    def is_ready(self) -> bool:
        return len(self.models) > 0

    def _get_model_object(self, model_name: str) -> Any:
        """
        Extrae el objeto modelo real desde el diccionario o devuelve directamente.
        Algunos modelos se guardan como dict con clave 'model', otros directamente.
        """
        loaded = self.models.get(model_name)
        if loaded is None:
            return None
        # Si es diccionario con 'model', extraer
        if isinstance(loaded, dict) and 'model' in loaded:
            return loaded['model']
        # Si no, asumir que ES el modelo
        return loaded

    # --------- helpers de conversión por modelo ----------
    def _to_features_for_model(self, model_name: str, params: Dict[str, Any]) -> Optional[List[float]]:
        """
        Convertir un dict de params en un vector de features para modelos
        con mapeos predefinidos.
        Si el modelo requiere un mapping no implementado, devuelve None.
        """
        m = model_name.lower()
        try:
            if m in ("car_price", "car_model"):
                # Car model necesita 7 features: Year, Present_Price, Kms_Driven, Fuel_Type_encoded, Seller_Type_encoded, Transmission_encoded, Owner
                year = float(params.get("year", 2015))
                km = float(params.get("km", 50000))
                # Estimamos el precio presente basado en el año (autos más nuevos valen más)
                present_price = max(1.0, 10.0 - (2025 - year) * 0.5)  # Depreciación aproximada
                fuel_type = 0  # 0=Petrol, 1=Diesel, 2=CNG
                seller_type = 0  # 0=Dealer, 1=Individual
                transmission = 0  # 0=Manual, 1=Automatic
                owner = min(3, int((2025 - year) / 5))  # Estimamos dueños previos basado en edad del carro
                return [year, present_price, km, fuel_type, seller_type, transmission, owner]
            if m == "bmi_model":
                # espera {'height': 1.78, 'weight': 78, 'age': 30}
                return [float(params.get("height")), float(params.get("weight")), float(params.get("age", 30))]
            if m in ("bitcoin_model",):
                # Bitcoin - Predicción a CORTO PLAZO (días, no años)
                # Features: price_lag_1, price_lag_2, price_lag_3, price_lag_7, rolling_mean_7, rolling_mean_30
                days = float(params.get("days", params.get("years", 1)))
                # Precio base más realista
                random.seed(int(days * 137))  # Seed único por día
                base_price = 45000.0 + (days * random.uniform(50, 150))  # Variación diaria ~$50-150
                volatility = random.uniform(0.97, 1.03)  # ±3% volatilidad diaria
                return [
                    base_price * volatility,
                    base_price * 0.998 * volatility,
                    base_price * 0.997 * volatility,
                    base_price * 0.995 * volatility,
                    base_price * 0.999 * volatility,
                    base_price * 1.001 * volatility
                ]
            if m in ("sp500_model",):
                # SP500 - Predicción a CORTO PLAZO (días)
                # Features: open, high, low, volume, price_change, high_low_diff, close_lag_1, close_lag_5, close_lag_10, rolling_mean_5, rolling_mean_20
                days = float(params.get("days", params.get("years", 1)))
                random.seed(int(days * 271))  # Seed único por día
                base = 4500.0 + (days * random.uniform(5, 20))  # Variación diaria ~$5-20
                vol_factor = random.uniform(0.98, 1.02)  # ±2% volatilidad
                return [
                    base * vol_factor,
                    base * 1.005 * vol_factor,
                    base * 0.995 * vol_factor,
                    5000000 + int(days * 50000),
                    random.uniform(-20, 20),
                    random.uniform(10, 30),
                    base * 0.999 * vol_factor,
                    base * 0.997 * vol_factor,
                    base * 0.995 * vol_factor,
                    base * vol_factor,
                    base * 1.002 * vol_factor
                ]
            if m in ("avocado_model", "avocado_price"):
                # Avocado - Predicción a CORTO PLAZO (días)
                # Features: Total Volume, 4046, 4225, 4770, Total Bags, Small Bags, Large Bags, XLarge Bags, type_encoded, region_encoded, year
                days = float(params.get("days", params.get("years", 1)))
                random.seed(int(days * 181))  # Seed único por día
                year_value = 2025  # Año actual
                # Variamos volúmenes ligeramente por día
                vol_factor = 1.0 + (days * 0.002 * random.uniform(0.95, 1.05))  # Variación muy pequeña diaria
                return [
                    100000 * vol_factor,
                    50000 * vol_factor,
                    30000 * vol_factor,
                    10000 * vol_factor,
                    5000 * vol_factor,
                    4000 * vol_factor,
                    800 * vol_factor,
                    200 * vol_factor,
                    random.choice([0, 1]),  # tipo: convencional u orgánico
                    random.randint(0, 5),  # región aleatoria
                    year_value
                ]
            if m in ("london_crime", "chicago_crime", "london_crime_model", "chicago_crime_model"):
                # espera {'day_of_week': 'monday'} -> map to int 0..6
                # London/Chicago necesitan: day_of_week, hour, district, month, population_density
                dow = params.get("day_of_week", params.get("day"))
                day_idx = 4  # Default viernes
                if isinstance(dow, str):
                    mapping = {
                        "monday":0,"mon":0,"lunes":0,
                        "tuesday":1,"tue":1,"martes":1,
                        "wednesday":2,"wed":2,"miercoles":2,"miércoles":2,
                        "thursday":3,"thu":3,"jueves":3,
                        "friday":4,"fri":4,"viernes":4,
                        "saturday":5,"sat":5,"sabado":5,"sábado":5,
                        "sunday":6,"sun":6,"domingo":6
                    }
                    key = dow.strip().lower()
                    day_idx = mapping.get(key, 4)
                elif isinstance(dow, int):
                    day_idx = dow
                # Retornar: day_of_week, hour (12pm), district (1), month (10), population_density (50.0)
                return [float(day_idx), 12.0, 1.0, 10.0, 50.0]
            if m in ("airline_delay", "airline_delay_model"):
                # Airline necesita: Month, DayofMonth, DayOfWeek, DepTime, CRSDepTime, CRSArrTime, Distance, + encoders
                # Aproximadamente 7-10 features según el modelo entrenado
                month = float(params.get("month", 6))  # Mes (1-12)
                day = float(params.get("day", 15))  # Día del mes (1-31)
                distance = float(params.get("distance", 500))  # Distancia en millas
                day_of_week = float(params.get("day_of_week", 3))  # Día de la semana (1-7)
                dep_time = float(params.get("dep_time", 1400))  # Hora de salida (formato 24h como 1400 = 2pm)
                crs_dep_time = float(params.get("crs_dep_time", 1400))  # Hora programada salida
                crs_arr_time = float(params.get("crs_arr_time", 1700))  # Hora programada llegada
                carrier = 0  # Código de aerolínea (0-N)
                origin = 0  # Código origen (0-N)
                dest = 0  # Código destino (0-N)
                return [month, day, day_of_week, dep_time, crs_dep_time, crs_arr_time, distance, carrier, origin, dest]
            if m in ("cirrhosis_classifier", "cirrhosis_model"):
                # Cirrosis necesita: N_Days, Age, Bilirubin, Cholesterol, Albumin, Copper, Alk_Phos, SGOT, 
                # Tryglicerides, Platelets, Prothrombin, Stage, + encoders (Drug, Sex, Ascites, Hepatomegaly, Spiders, Edema)
                # Total: 12 numeric + 6 categóricos = 18 features
                age = float(params.get("age", 18250))  # Age en días (50 años ≈ 18250 días)
                bilirubin = float(params.get("bilirubin", 1.5))
                n_days = float(params.get("n_days", 1000))  # Días desde diagnóstico
                cholesterol = float(params.get("cholesterol", 280))
                albumin = float(params.get("albumin", 3.5))
                copper = float(params.get("copper", 70))
                alk_phos = float(params.get("alk_phos", 1200))
                sgot = float(params.get("sgot", 100))
                tryglicerides = float(params.get("tryglicerides", 100))
                platelets = float(params.get("platelets", 250))
                prothrombin = float(params.get("prothrombin", 11))
                stage = float(params.get("stage", 3))  # Etapa de la enfermedad (1-4)
                # Encoders categóricos (valores por defecto)
                drug = 0  # 0=D-penicillamine, 1=Placebo
                sex = 0  # 0=F, 1=M
                ascites = 0  # 0=N, 1=Y
                hepatomegaly = 1  # 0=N, 1=Y
                spiders = 0  # 0=N, 1=Y
                edema = 0  # 0=N, 1=S, 2=Y
                return [n_days, age, bilirubin, cholesterol, albumin, copper, alk_phos, sgot, 
                       tryglicerides, platelets, prothrombin, stage, drug, sex, ascites, 
                       hepatomegaly, spiders, edema]
            if m == "movie_recommender":
                # recommender idealmente expone método recommend(user_id, k)
                # aquí no convertimos a features, se manejará aparte.
                return None
        except Exception as e:
            raise ValueError(f"Error al convertir params para {model_name}: {e}")
        return None

    # -------------- predict genérico --------------------
    def predict(self, model_name: str, features: Optional[List[float]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Predict:
          - Si features (lista) provista -> se usa tal cual.
          - Si params provista -> se intenta convertir con mapping por modelo.
          - Para recommenders: si el modelo tiene método 'recommend' se llama con user_id/k.
        Devuelve dict con keys: model, input, prediction.
        """
        if model_name not in self.models:
            raise ValueError(f"Modelo '{model_name}' no cargado. Modelos disponibles: {self.get_available_models()}")

        # Extraer el objeto modelo real (puede estar en dict['model'] o directamente)
        model_obj = self._get_model_object(model_name)
        if model_obj is None:
            raise ValueError(f"No se pudo extraer el modelo de '{model_name}'")
        
        # Caso especial: movie recommender
        if model_name == "movie_recommender":
            # El modelo está en un dict, necesitamos acceder a los datos
            loaded = self.models[model_name]
            if isinstance(loaded, dict):
                top_k = int(params.get("top_k", 1)) if params else 1  # Default 1 película
                # Recomendar películas aleatoriamente diferentes cada vez
                movies = loaded.get('movies', [])
                if len(movies) > 0:
                    import random
                    import time
                    # Usar timestamp para seed diferente en cada llamada
                    random.seed(int(time.time() * 1000))
                    if hasattr(movies, 'sample'):
                        # Si es DataFrame
                        recs = movies.sample(n=min(top_k, len(movies)))['title'].tolist()
                    else:
                        # Si es lista
                        recs = random.sample(movies, min(top_k, len(movies)))
                    return {"model": model_name, "input": params or {}, "prediction": recs}
                return {"model": model_name, "input": params or {}, "prediction": []}
        
        # si pasaron features explícitos
        if features is not None:
            X = np.array(features).reshape(1, -1)
            try:
                pred = model_obj.predict(X)
                out = pred.tolist() if hasattr(pred, "tolist") else pred
                # si clasificación y existe predict_proba
                if hasattr(model_obj, "predict_proba"):
                    proba = model_obj.predict_proba(X)
                    return {"model": model_name, "input": features, "prediction": out, "proba": proba.tolist()}
                return {"model": model_name, "input": features, "prediction": out}
            except Exception as e:
                raise RuntimeError(f"Error al predecir con {model_name}: {e}")
        # si pasaron params -> intentar mapping
        if params is not None:
            converted = self._to_features_for_model(model_name, params)
            if converted is None:
                # si no pudimos convertir, para algunos modelos intentamos llamar predict con dict/array
                try:
                    # intentar pasar DataFrame-like (algunos modelos sklearn aceptan arrays)
                    X = np.array(list(params.values())).reshape(1, -1)
                    pred = model_obj.predict(X)
                    return {"model": model_name, "input": params, "prediction": (pred.tolist() if hasattr(pred, "tolist") else pred)}
                except Exception:
                    raise ValueError(f"No se pudo convertir params a features para {model_name}. Pasa 'features' como lista.")
            # si conversion exitosa, predecir
            return self.predict(model_name, features=converted, params=None)

        # si no hay ni features ni params
        raise ValueError("Debe proveer 'features' (lista) o 'params' (dict) para predecir.")

    # -------------- run_model desde texto ----------------
    def run_model(self, command_text: str) -> Dict[str, Any]:
        """
        Mapeo básico de texto -> llamadas predict.
        Ajusta las reglas a tu gramática esperada.
        """
        text = command_text.lower()
        # bitcoin: buscar número (años)
        import re
        n = re.search(r'(\d+)', text)
        num = int(n.group(1)) if n else 1

        try:
            if "bitcoin" in text:
                return self.predict("bitcoin_model", params={"years": num})
            if "sp500" in text or "sp 500" in text or "sp50" in text:
                return self.predict("sp500_model", params={"years": num})
            if "aguacate" in text or "avocado" in text:
                return self.predict("avocado_model", params={"years": num})
            if "automovil" in text or "automóvil" in text or "car" in text or "auto" in text:
                # intentar extraer año y km
                y = re.search(r'año\s*(\d{4})', text) or re.search(r'year\s*(\d{4})', text)
                km = re.search(r'kilometraje\s*(\d+)', text) or re.search(r'km\s*(\d+)', text)
                params = {}
                if y: params["year"] = int(y.group(1))
                if km: params["km"] = int(km.group(1))
                return self.predict("car_model", params=params if params else {"year": 2015, "km": 50000})
            if "masa corporal" in text or "bmi" in text:
                # extraer numbers
                nums = re.findall(r'(\d+(\.\d+)?)', text)
                if len(nums) >= 2:
                    h = float(nums[0][0])
                    w = float(nums[1][0])
                    age = float(nums[2][0]) if len(nums) >= 3 else 30
                    return self.predict("bmi_model", params={"height": h, "weight": w, "age": age})
                return {"error": "Proveer altura y peso (ej. 'altura 1.78 peso 78')"}
            if "londres" in text or "london" in text:
                # intentar día
                dow = re.search(r'(lunes|martes|miercoles|miércoles|jueves|viernes|sabado|sábado|domingo)', text)
                day = dow.group(1) if dow else "viernes"
                return self.predict("london_crime_model", params={"day_of_week": day}) 
            if "chicago" in text:
                dow = re.search(r'(lunes|martes|miercoles|miércoles|jueves|viernes|sabado|sábado|domingo)', text)
                day = dow.group(1) if dow else "viernes"
                return self.predict("chicago_crime", params={"day_of_week": day})
            if "cirrosis" in text:
                return self.predict("cirrhosis_model", params={})  # preferir pasar features explícitas
            if "avion" in text or "vuelo" in text or "airline" in text:
                # buscar lugar y mes
                month = re.search(r'(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|\d{1,2})', text)
                loc = re.search(r'desde\s+([A-Za-zÁÉÍÓÚáéíóúñÑ ]+)', text)
                params = {}
                if month:
                    params["month"] = month.group(1)
                if loc:
                    params["location"] = loc.group(1).strip()
                return self.predict("airline_delay_model", params=params)
            if "pelicula" in text or "recomienda" in text or "movie" in text:
                # recommender
                return self.predict("movie_recommender", params={"top_k":5})
        except Exception as e:
            return {"error": str(e)}

        return {"error": "No se reconoció el comando. Debes usar palabras claves como 'bitcoin', 'automovil', 'londres', etc."}
