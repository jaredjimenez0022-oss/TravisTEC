# backend/services/model_runner.py
import os
import joblib
import numpy as np
import traceback
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

    # --------- helpers de conversión por modelo ----------
    def _to_features_for_model(self, model_name: str, params: Dict[str, Any]) -> Optional[List[float]]:
        """
        Convertir un dict de params en un vector de features para modelos
        con mapeos predefinidos.
        Si el modelo requiere un mapping no implementado, devuelve None.
        """
        m = model_name.lower()
        try:
            if m == "car_price":
                # espera {'year': 2015, 'km': 80000}
                year = float(params.get("year"))
                km = float(params.get("km"))
                return [year, km]
            if m == "bmi_model":
                # espera {'height': 1.78, 'weight': 78, 'age': 30}
                return [float(params.get("height")), float(params.get("weight")), float(params.get("age", 30))]
            if m in ("bitcoin_model", "sp500_model", "avocado_price"):
                # espera {'years': 1} (horizon)
                years = float(params.get("years", params.get("horizon", 1)))
                return [years]
            if m in ("london_crime", "chicago_crime"):
                # espera {'day_of_week': 'monday'} -> map to int 0..6
                dow = params.get("day_of_week", params.get("day"))
                if isinstance(dow, str):
                    mapping = {
                        "monday":0,"mon":0,"martes":1,"tuesday":1,"tue":1,
                        "wednesday":2,"wed":2,"miercoles":2,"miernes":2,
                        "thursday":3,"thu":3,"jueves":3,
                        "friday":4,"fri":4,"viernes":4,
                        "saturday":5,"sat":5,"sabado":5,
                        "sunday":6,"sun":6,"domingo":6
                    }
                    key = dow.strip().lower()
                    idx = mapping.get(key)
                    if idx is None:
                        # try parse number
                        try:
                            idx = int(dow)
                        except:
                            raise ValueError(f"day_of_week desconocido: {dow}")
                    return [idx]
                else:
                    # si viene numérico
                    return [int(dow)]
            if m == "airline_delay":
                # espera {'location': 'SanJose', 'month': 3} -> fallback: require 'features' or numeric month
                month = params.get("month")
                loc = params.get("location")
                if month is not None and loc is not None:
                    # Simple fallback: encode month as number and try using hash of location
                    month_n = int(month)
                    loc_code = float(abs(hash(str(loc))) % 1000)  # crude encoding
                    return [loc_code, month_n]
            if m == "cirrhosis_classifier":
                # mejor pasar 'features' explicitos; si pasan params, tomarlos en orden alfabético
                keys = sorted(params.keys())
                if keys:
                    return [float(params[k]) for k in keys]
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

        model = self.models[model_name]
        # caso recommender con método recommend
        if params and model_name == "movie_recommender":
            user_id = params.get("user_id")
            top_k = int(params.get("top_k", 5))
            if hasattr(model, "recommend"):
                recs = model.recommend(user_id, k=top_k)
                return {"model": model_name, "input": params, "prediction": recs}
            # fallback: si tiene method predict and expects features, require features
            if features is None:
                raise ValueError("movie_recommender requiere 'user_id' en params o 'features' explicitas.")
        # si pasaron features explícitos
        if features is not None:
            X = np.array(features).reshape(1, -1)
            try:
                pred = model.predict(X)
                out = pred.tolist() if hasattr(pred, "tolist") else pred
                # si clasificación y existe predict_proba
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(X)
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
                    pred = model.predict(X)
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
                return self.predict("avocado_price", params={"years": num})
            if "automovil" in text or "automóvil" in text or "car" in text:
                # intentar extraer año y km
                y = re.search(r'año\s*(\d{4})', text) or re.search(r'year\s*(\d{4})', text)
                km = re.search(r'kilometraje\s*(\d+)', text) or re.search(r'km\s*(\d+)', text)
                params = {}
                if y: params["year"] = int(y.group(1))
                if km: params["km"] = int(km.group(1))
                return self.predict("car_price", params=params if params else {"year": 2015, "km": 50000})
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
                day = dow.group(1) if dow else None
                return self.predict("london_crime", params={"day_of_week": day}) 
            if "chicago" in text:
                dow = re.search(r'(lunes|martes|miercoles|miércoles|jueves|viernes|sabado|sábado|domingo)', text)
                day = dow.group(1) if dow else None
                return self.predict("chicago_crime", params={"day_of_week": day})
            if "cirrosis" in text:
                return self.predict("cirrhosis_classifier", params={})  # preferir pasar features explícitas
            if "avion" in text or "vuelo" in text:
                # buscar lugar y mes
                month = re.search(r'(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|\d{1,2})', text)
                loc = re.search(r'desde\s+([A-Za-zÁÉÍÓÚáéíóúñÑ ]+)', text)
                params = {}
                if month:
                    params["month"] = month.group(1)
                if loc:
                    params["location"] = loc.group(1).strip()
                return self.predict("airline_delay", params=params)
            if "pelicula" in text or "recomienda" in text:
                # recommender
                return self.predict("movie_recommender", params={"top_k":5})
        except Exception as e:
            return {"error": str(e)}

        return {"error": "No se reconoció el comando. Debes usar palabras claves como 'bitcoin', 'automovil', 'londres', etc."}
