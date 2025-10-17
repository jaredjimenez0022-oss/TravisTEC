# backend/services/model_runner.py
import os
import joblib
import numpy as np
import traceback
import random
from typing import List, Dict, Any, Optional

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
# Compatibility aliases: map legacy model names to current saved artifacts
ALIASES = {
    'car_model': 'car_price',
}

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
        # include aliases as available names for convenience
        names = list(self.models.keys())
        # expose alias keys if their targets exist
        for alias, target in ALIASES.items():
            if target in self.models and alias not in names:
                names.append(alias)
        return names

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
                # Accept either 'days' or 'years' in params. Convert years -> days.
                years_val = params.get('years') if params and 'years' in params else None
                days_val = params.get('days') if params and 'days' in params else None
                if years_val is not None:
                    try:
                        horizon_days = int(float(years_val) * 365)
                    except Exception:
                        horizon_days = int(float(years_val))
                else:
                    try:
                        horizon_days = int(float(days_val)) if days_val is not None else 1
                    except Exception:
                        horizon_days = 1

                # Precio base más realista
                random.seed(int(max(1, horizon_days) * 137))  # Seed único por día
                base_price = 45000.0 + (horizon_days * random.uniform(50, 150))  # Variación diaria ~$50-150
                volatility = random.uniform(0.97, 1.03)  # ±3% volatilidad diaria
                # Return 7 features matching training: 6 price-derived features + horizon_days
                return [
                    base_price * volatility,
                    base_price * 0.998 * volatility,
                    base_price * 0.997 * volatility,
                    base_price * 0.995 * volatility,
                    base_price * 0.999 * volatility,
                    base_price * 1.001 * volatility,
                    float(horizon_days)
                ]
            if m in ("sp500_model",):
                # SP500 - Predicción a CORTO PLAZO (días)
                # Features: open, high, low, volume, price_change, high_low_diff, close_lag_1, close_lag_5, close_lag_10, rolling_mean_5, rolling_mean_20
                # Accept 'days' or 'years' and convert to days
                years_val = params.get('years') if params and 'years' in params else None
                days_val = params.get('days') if params and 'days' in params else None
                if years_val is not None:
                    try:
                        horizon_days = int(float(years_val) * 365)
                    except Exception:
                        horizon_days = int(float(years_val))
                else:
                    try:
                        horizon_days = int(float(days_val)) if days_val is not None else 1
                    except Exception:
                        horizon_days = 1

                random.seed(int(max(1, horizon_days) * 271))  # Seed único por día
                base = 4500.0 + (horizon_days * random.uniform(5, 20))  # Variación diaria ~$5-20
                vol_factor = random.uniform(0.98, 1.02)  # ±2% volatilidad
                # Return 12 features: the 11 price/volume features plus horizon_days
                return [
                    base * vol_factor,
                    base * 1.005 * vol_factor,
                    base * 0.995 * vol_factor,
                    5000000 + int(horizon_days * 50000),
                    random.uniform(-20, 20),
                    random.uniform(10, 30),
                    base * 0.999 * vol_factor,
                    base * 0.997 * vol_factor,
                    base * 0.995 * vol_factor,
                    base * vol_factor,
                    base * 1.002 * vol_factor,
                    float(horizon_days)
                ]
            if m in ("avocado_model", "avocado_price"):
                # Avocado - Predicción a CORTO PLAZO (months)
                # Features: Total Volume, 4046, 4225, 4770, Total Bags, Small Bags, Large Bags, XLarge Bags,
                # type_encoded, region_encoded, year, horizon_months
                # Accept 'months' or 'days' or 'years' in params; convert to months
                months_val = None
                if params:
                    if 'months' in params:
                        months_val = params.get('months')
                    elif 'days' in params:
                        try:
                            months_val = float(params.get('days')) / 30.0
                        except Exception:
                            months_val = None
                    elif 'years' in params:
                        try:
                            months_val = float(params.get('years')) * 12.0
                        except Exception:
                            months_val = None
                try:
                    horizon_months = int(float(months_val)) if months_val is not None else 1
                except Exception:
                    horizon_months = 1

                random.seed(int(max(1, horizon_months) * 181))  # Seed único por mes
                year_value = 2025  # Año actual
                # Small variations by months
                vol_factor = 1.0 + (horizon_months * 0.01 * random.uniform(0.95, 1.05))
                # Build realistic-looking features matching trainer feature_cols:
                # ['avg_price','total_volume','v_4046','v_4225','v_4770','total_bags','small_bags','large_bags','xlarge_bags','lag_1','lag_3','rolling_3','horizon_months']
                avg_price = 1.5 * vol_factor
                total_volume = 100000 * vol_factor
                v_4046 = 50000 * vol_factor
                v_4225 = 30000 * vol_factor
                v_4770 = 10000 * vol_factor
                total_bags = 5000 * vol_factor
                small_bags = 4000 * vol_factor
                large_bags = 800 * vol_factor
                xlarge_bags = 200 * vol_factor
                # lag features derived from avg_price
                lag_1 = avg_price * 0.99
                lag_3 = avg_price * 0.97
                rolling_3 = (avg_price * 0.99 + avg_price * 0.98 + avg_price * 1.0) / 3.0
                return [
                    avg_price,
                    total_volume,
                    v_4046,
                    v_4225,
                    v_4770,
                    total_bags,
                    small_bags,
                    large_bags,
                    xlarge_bags,
                    lag_1,
                    lag_3,
                    rolling_3,
                    float(horizon_months)
                ]
            if m in ("london_crime", "london_crime_model"):
                # London model expects ['month','day_of_week','borough_le']
                dow = params.get("day_of_week", params.get("day"))
                day_idx = 4
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
                    if dow > 6:
                        day_idx = (int(dow) - 1) % 7
                    else:
                        day_idx = int(dow)

                month = int(params.get('month', 10))
                # borough parameter - accept 'borough' or 'borough_le'
                borough = params.get('borough', params.get('borough_le', params.get('borough_name', None)))
                borough_le = 0
                try:
                    pkg = self.models.get('london_crime_model')
                    if isinstance(pkg, dict) and 'encoder' in pkg:
                        enc = pkg['encoder']
                        # encoder expected to be a LabelEncoder-like object
                        if borough is None:
                            borough_le = int(enc.transform([enc.classes_[0]])[0]) if hasattr(enc, 'classes_') else 0
                        else:
                            borough_le = int(enc.transform([str(borough)])[0])
                    else:
                        borough_le = int(params.get('borough_le', 0) or 0)
                except Exception:
                    borough_le = int(params.get('borough_le', 0) or 0)

                return [float(month), float(day_idx), float(borough_le)]

            if m in ("chicago_crime", "chicago_crime_model"):
                # For Chicago trainer we expect features: dow0 (0=Monday), month, community_area
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
                    # allow BigQuery style dayofweek (1=Sunday) or 0..6
                    if dow > 6:
                        # assume BigQuery 1..7 -> convert to 0..6
                        day_idx = (int(dow) - 1) % 7
                    else:
                        day_idx = int(dow)

                month = int(params.get('month', 10))
                community_area = int(params.get('community_area', params.get('district', -1) or -1))
                # Check if a pre-trained chicago model exists and what feature count it expects
                try:
                    loaded = self.models.get('chicago_crime') or self.models.get('chicago_crime_model')
                    model_obj = None
                    if isinstance(loaded, dict) and 'model' in loaded:
                        model_obj = loaded['model']
                    else:
                        model_obj = loaded
                    if model_obj is not None and hasattr(model_obj, 'n_features_in_'):
                        expected = int(getattr(model_obj, 'n_features_in_', 0))
                        if expected == 1:
                            return [float(day_idx)]
                except Exception:
                    # ignore and return full feature set
                    pass
                return [float(day_idx), float(month), float(community_area)]
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
                # Cirrosis feature order must match trainer:
                # cols_num (N_Days, Age, Bilirubin, Cholesterol, Albumin, Copper, Alk_Phos, SGOT, Tryglicerides, Platelets, Prothrombin)
                # + bools (Ascites_bin, Hepatomegaly_bin, Spiders_bin, Edema_bin)
                # + Sex_le, Drug_le  => total 17 features
                n_days = float(params.get("n_days", params.get('N_Days', 1000)))  # Días desde diagnóstico
                age = float(params.get("age", params.get('Age', 18250)))  # Age en días fallback
                bilirubin = float(params.get("bilirubin", params.get('Bilirubin', 1.5)))
                cholesterol = float(params.get("cholesterol", params.get('Cholesterol', 280)))
                albumin = float(params.get("albumin", params.get('Albumin', 3.5)))
                copper = float(params.get("copper", params.get('Copper', 70)))
                alk_phos = float(params.get("alk_phos", params.get('Alk_Phos', 1200)))
                sgot = float(params.get("sgot", params.get('SGOT', 100)))
                tryglicerides = float(params.get("tryglicerides", params.get('Tryglicerides', 100)))
                platelets = float(params.get("platelets", params.get('Platelets', 250)))
                prothrombin = float(params.get("prothrombin", params.get('Prothrombin', 11)))

                # Boolean flags: accept 'Y'/'N', True/False, 1/0, or numeric
                def _to_bin(v):
                    if v is None:
                        return 0
                    if isinstance(v, (int, float)):
                        return 1 if float(v) != 0 else 0
                    s = str(v).strip().upper()
                    if s in ('Y','YES','1','TRUE'):
                        return 1
                    return 0

                ascites = _to_bin(params.get('Ascites', params.get('ascites', 0)))
                hepatomegaly = _to_bin(params.get('Hepatomegaly', params.get('hepatomegaly', 0)))
                spiders = _to_bin(params.get('Spiders', params.get('spiders', 0)))
                # Edema in dataset had values like '0','S','Y' - map similarly
                edema = _to_bin(params.get('Edema', params.get('edema', 0)))

                # Sex and Drug - use saved encoders if available to ensure consistent mapping
                drug_val = params.get('Drug', params.get('drug', 'Unknown'))
                sex_val = params.get('Sex', params.get('sex', 'U'))
                drug_le = 0
                sex_le = 0
                # try to use encoders stored with model package
                try:
                    pkg = self.models.get(model_name)
                    encs = pkg.get('encoders', {}) if isinstance(pkg, dict) else {}
                    if 'sex' in encs:
                        sex_le = int(encs['sex'].transform([str(sex_val)])[0])
                    else:
                        sex_le = 1 if str(sex_val).strip().upper() in ('M','MALE') else 0
                    if 'drug' in encs:
                        drug_le = int(encs['drug'].transform([str(drug_val)])[0])
                    else:
                        drug_le = 0
                except Exception:
                    # graceful fallback
                    sex_le = 1 if str(sex_val).strip().upper() in ('M','MALE') else 0
                    drug_le = 0

                return [n_days, age, bilirubin, cholesterol, albumin, copper, alk_phos, sgot,
                        tryglicerides, platelets, prothrombin,
                        ascites, hepatomegaly, spiders, edema,
                        sex_le, drug_le]
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
        # resolve aliases
        if model_name not in self.models:
            if model_name in ALIASES:
                resolved = ALIASES[model_name]
                model_name = resolved
            else:
                raise ValueError(f"Modelo '{model_name}' no cargado. Modelos disponibles: {self.get_available_models()}")

        # Extraer el objeto modelo real (puede estar en dict['model'] o directamente)
        model_obj = self._get_model_object(model_name)
        if model_obj is None:
            raise ValueError(f"No se pudo extraer el modelo de '{model_name}'")
        
        # Caso especial: movie recommender
        if model_name == "movie_recommender":
            # The saved recommender is a dict with a DataFrame 'movies'
            loaded = self.models[model_name]
            if isinstance(loaded, dict):
                top_k = int(params.get("top_k", 1)) if params else 1  # Default 1 movie
                year = params.get('year') if params else None
                genre = params.get('genre') if params else None

                movies_df = loaded.get('movies')
                if movies_df is None:
                    return {"model": model_name, "input": params or {}, "prediction": []}

                # If movies_df is a DataFrame, filter by year/genre and return top_k by popularity
                try:
                    df = movies_df
                    # filter by year if provided
                    if year is not None:
                        try:
                            y = int(year)
                            df = df[df['year'] == y]
                        except Exception:
                            pass
                    # filter by genre if provided (case-insensitive substring in genres_str or in genres_list)
                    if genre:
                        g = str(genre).strip().lower()
                        df = df[df['genres_str'].str.lower().str.contains(g, na=False) | df['genres_list'].apply(lambda gl: any(g == gg.lower() for gg in gl))]

                    # If after filtering we have no matches, fallback to the full list
                    if df.shape[0] == 0:
                        df = movies_df

                    # Sort by popularity and take top_k
                    df_sorted = df.sort_values('popularity', ascending=False).head(top_k)
                    titles = df_sorted['title'].tolist()
                    return {"model": model_name, "input": params or {}, "prediction": titles}
                except Exception as e:
                    # fallback: if movies is a list
                    import random, time
                    random.seed(int(time.time() * 1000))
                    movies_list = loaded.get('movies', [])
                    if isinstance(movies_list, list) and len(movies_list) > 0:
                        recs = random.sample(movies_list, min(top_k, len(movies_list)))
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
