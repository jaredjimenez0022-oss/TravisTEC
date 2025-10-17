# Backend API — Model endpoints

This file documents the lightweight model endpoints added to the FastAPI backend so the frontend can call models directly.

Base URL (when running locally): http://localhost:8000

Endpoints

- GET /api/v1/models
  - Returns: {"models": ["bitcoin_model","car_price","movie_recommender", ...]}

- POST /api/v1/models/{model_name}
  - Generic predict endpoint. Accepts JSON:
    - {"features": [..]}  OR
    - {"params": {...}}
  - Returns whatever ModelRunner.predict returns, typically: {"model":..., "input":..., "prediction": ...}

- Convenience endpoints (wrap common models):
  - POST /api/v1/predict/car  -> {"year":2015, "km":50000}
  - POST /api/v1/predict/bitcoin -> {"years":1}
  - POST /api/v1/predict/movie -> {"top_k":5, "genre":"Comedy", "year":1999}
  - POST /api/v1/predict/bmi -> {"height":1.78, "weight":78, "age":30}
  - POST /api/v1/predict/sp500 -> {"days":30}
  - POST /api/v1/predict/avocado -> {"days":7}
  - POST /api/v1/predict/london -> {"day":"viernes"}
  - POST /api/v1/predict/chicago -> {"day":"viernes"}
  - POST /api/v1/predict/cirrhosis -> pass medical params through
  - POST /api/v1/predict/airline -> {"month":6, "day":15, "distance":500}

Example JS (fetch) calls

```javascript
// Predict car price
fetch('/api/v1/predict/car', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({year:2015, km:50000})
}).then(r=>r.json()).then(console.log)

// Recommend movies
fetch('/api/v1/predict/movie', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({top_k:5, genre:'Drama', year:1994})
}).then(r=>r.json()).then(console.log)

// Generic model call
fetch('/api/v1/models/movie_recommender', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({params:{top_k:3, genre:'Comedy'}})
}).then(r=>r.json()).then(console.log)
```

Notes
- Some saved models include metadata packages (e.g., bitcoin_model.joblib contains {'model', 'feature_cols', 'last_date'}). ModelRunner attempts to handle those formats.
- If you update/retrain models, ensure they are saved in `backend/models/*.joblib` so the server loads them on start.

## Trained models (available)

The backend currently ships several trained models exposed via convenience endpoints. Use `GET /api/v1/models` to list them.

- `bitcoin_model` — POST `/api/v1/predict/bitcoin`
  - Params: `years` or `days` (horizon). Example: `{ "years": 1 }`
  - Response: model package with prediction and (if available) `last_date` used to compute the exact target date.

- `car_price` — POST `/api/v1/predict/car`
  - Params: `{ "year": 2015, "km": 50000 }`
  - Response: dataset-unit price and optional conversions (rupees / USD if env vars set).

- `movie_recommender` — POST `/api/v1/predict/movie`
  - Params: `{ "top_k": 5, "genre": "Drama", "year": 1994 }`
  - Response: list of recommended movie titles.

- `bmi_model` — POST `/api/v1/predict/bmi`
  - Params: `{ "height": 1.78, "weight": 78, "age": 30 }`
  - Response: predicted bodyfat (if model exists) or BMI formula fallback.

- `sp500_model` — POST `/api/v1/predict/sp500`
  - Params: `{ "days": 30 }` (or `years`)
  - Response: projected S&P 500 value.

- `avocado_model` — POST `/api/v1/predict/avocado`
  - Params: `{ "months": 3 }` (also accepts `days` or `years`, converted to months)
  - Response: predicted avocado price and (if saved) `target_date` computed from the model package `last_date`.

- `airline_delay_model` — POST `/api/v1/predict/airline`
  - Params (preferred): `{ "month": 6, "day": 15, "crs_dep_time": 900, "crs_arr_time": 1100, "crs_elapsed": 120, "distance": 500, "origin": "IAD", "dest": "TPA", "carrier": "WN" }`
  - Response: `{ "model": "airline_delay_model", "input": {...}, "prediction": { "delayed": true, "probability": 0.67 } }`
  - Metadata endpoint: `GET /api/v1/airline/metadata` returns lists of known `origins`, `dests`, and `carriers` (with best-effort full names for common codes).

- `london_crime_model` — POST `/api/v1/predict/london`
  - Params: `{ "month": 11, "day_of_week": 3, "borough": "Croydon" }` (day_of_week 1=Mon..7=Sun)
  - Response: a predicted expected crimes per day (numeric). Example: `{"model":"london_crime_model","input":{...},"prediction":[12.3]}`
  - Note: the training data is monthly by LSOA; the trainer converts to an average-per-day target so the model predicts expected crimes per day for a given borough/month/day_of_week.

If you add more models, please update this README and save the artifact under `backend/models/` so the server picks it up automatically.
