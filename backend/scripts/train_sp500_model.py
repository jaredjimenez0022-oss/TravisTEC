"""Train a S&P 500 stock price prediction model.

Uses historical stock market data to train a regression model.
"""
import pandas as pd
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

DATA = Path(__file__).parent.parent / 'datasets' / 'all_stocks_5yr.csv'
MODEL_OUT = Path(__file__).parent.parent / 'models' / 'sp500_model.joblib'

def main():
    if not DATA.exists():
        print(f"Dataset not found: {DATA}. Skipping training.")
        return

    df = pd.read_csv(DATA)
    print(f"Loaded {len(df)} stock price records")
    
    # Create features
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date', 'close', 'open', 'high', 'low', 'volume'])
    
    # Sort by date
    df = df.sort_values('date')
    
    # Create lag features
    for lag in [1, 5, 10]:
        df[f'close_lag_{lag}'] = df.groupby('Name')['close'].shift(lag)
    
    # Rolling averages per stock
    df['rolling_mean_5'] = df.groupby('Name')['close'].rolling(window=5).mean().reset_index(0, drop=True)
    df['rolling_mean_20'] = df.groupby('Name')['close'].rolling(window=20).mean().reset_index(0, drop=True)
    
    # Price change features
    df['price_change'] = df['close'] - df['open']
    df['high_low_diff'] = df['high'] - df['low']
    
    # Drop rows with NaN
    df = df.dropna()
    
    if len(df) < 1000:
        print("Not enough data after feature engineering")
        return
    
    feature_cols = ['open', 'high', 'low', 'volume', 'price_change', 'high_low_diff'] + \
                   [f'close_lag_{lag}' for lag in [1, 5, 10]] + ['rolling_mean_5', 'rolling_mean_20']
    
    X = df[feature_cols]
    y = df['close']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f'Test MAE: ${mae:.2f}')
    print(f'R2 Score: {r2:.4f}')
    print(f'Trained on {len(X_train)} samples, tested on {len(X_test)} samples')
    
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print(f'Saved model to {MODEL_OUT}')

if __name__ == '__main__':
    main()
