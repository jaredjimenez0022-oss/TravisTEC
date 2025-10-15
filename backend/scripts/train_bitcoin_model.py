"""Train a Bitcoin price prediction model using time series data.

Uses historical Bitcoin price data to train a regression model.
"""
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import numpy as np

DATA = Path(__file__).parent.parent / 'datasets' / 'bitcoin.csv'
MODEL_OUT = Path(__file__).parent.parent / 'models' / 'bitcoin_model.joblib'

def main():
    if not DATA.exists():
        print(f"Dataset not found: {DATA}. Skipping training.")
        return

    df = pd.read_csv(DATA)
    print(f"Loaded {len(df)} Bitcoin price records")
    print(f"Columns: {df.columns.tolist()}")
    
    # Check if we have price data
    price_cols = [col for col in df.columns if 'price' in col.lower() or 'close' in col.lower()]
    if not price_cols:
        print("No price column found in dataset")
        return
    
    # Use first price column found
    price_col = price_cols[0]
    print(f"Using price column: {price_col}")
    
    # Create simple features: use rolling averages and lag features
    df = df.copy()
    df['price'] = pd.to_numeric(df[price_col], errors='coerce')
    df = df.dropna(subset=['price'])
    
    # Create lag features
    for lag in [1, 2, 3, 7]:
        df[f'price_lag_{lag}'] = df['price'].shift(lag)
    
    # Rolling averages
    df['rolling_mean_7'] = df['price'].rolling(window=7).mean()
    df['rolling_mean_30'] = df['price'].rolling(window=30).mean()
    
    # Drop rows with NaN
    df = df.dropna()
    
    if len(df) < 100:
        print("Not enough data after feature engineering")
        return
    
    feature_cols = [f'price_lag_{lag}' for lag in [1, 2, 3, 7]] + ['rolling_mean_7', 'rolling_mean_30']
    X = df[feature_cols]
    y = df['price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f'Test MAE: ${mae:.2f}')
    print(f'R2 Score: {r2:.4f}')
    print(f'Mean price: ${y_test.mean():.2f}')
    
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print(f'Saved model to {MODEL_OUT}')

if __name__ == '__main__':
    main()
