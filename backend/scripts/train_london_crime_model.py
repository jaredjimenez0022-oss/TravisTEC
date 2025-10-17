"""Train a model to predict expected crimes per day in London boroughs.

Dataset: backend/datasets/london/london_crime_by_lsoa.csv
The dataset contains monthly counts per LSOA. We aggregate to borough-month,
convert monthly counts to average per day by dividing by days in month, and
train a regressor using Month, DayOfWeek (synthetic 1..7), and borough encoding.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
import calendar

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'datasets' / 'london' / 'london_crime_by_lsoa.csv'
OUT = ROOT / 'models' / 'london_crime_model.joblib'


def days_in_month(year, month):
    try:
        return calendar.monthrange(int(year), int(month))[1]
    except Exception:
        return 30


def train():
    if not CSV.exists():
        print(f"CSV not found: {CSV}")
        return
    print('Loading London crime dataset...')
    df = pd.read_csv(CSV)

    # Aggregate monthly counts to borough-month
    df_agg = df.groupby(['borough','year','month'])['value'].sum().reset_index()
    # Convert to daily average by dividing by days in month
    df_agg['days_in_month'] = df_agg.apply(lambda r: days_in_month(r['year'], r['month']), axis=1)
    df_agg['crimes_per_day'] = df_agg['value'] / df_agg['days_in_month']

    # We'll create synthetic day_of_week features by repeating each borough-month for 7 days
    rows = []
    for _, r in df_agg.iterrows():
        for dow in range(1,8):
            rows.append({
                'borough': r['borough'],
                'year': int(r['year']),
                'month': int(r['month']),
                'day_of_week': dow,
                'crimes_per_day': r['crimes_per_day']
            })
    df_days = pd.DataFrame(rows)

    # Encode borough
    le_borough = LabelEncoder()
    df_days['borough_le'] = le_borough.fit_transform(df_days['borough'])

    feature_cols = ['month','day_of_week','borough_le']
    X = df_days[feature_cols].astype(float)
    y = df_days['crimes_per_day'].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print('Training RandomForestRegressor...')
    rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1, max_depth=20)
    rf.fit(X_train, y_train)

    preds = rf.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f'Test MAE: {mae:.3f}, R2: {r2:.3f}')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pkg = {'model': rf, 'feature_cols': feature_cols, 'encoder': le_borough}
    joblib.dump(pkg, OUT)
    print(f'Saved london crime model to {OUT}')


if __name__ == '__main__':
    train()
