"""Train an Avocado price prediction model.

Uses historical avocado sales data to predict average prices.
"""
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib

DATA = Path(__file__).parent.parent / 'datasets' / 'avocado.csv'
MODEL_OUT = Path(__file__).parent.parent / 'models' / 'avocado_model.joblib'

def main():
    if not DATA.exists():
        print(f"Dataset not found: {DATA}. Skipping training.")
        return

    df = pd.read_csv(DATA)
    print(f"Loaded {len(df)} avocado sales records")
    
    # Prepare features
    df = df.copy()
    
    # Encode categorical variables
    le_type = LabelEncoder()
    le_region = LabelEncoder()
    
    df['type_encoded'] = le_type.fit_transform(df['type'])
    df['region_encoded'] = le_region.fit_transform(df['region'])
    
    # Select features
    feature_cols = ['Total Volume', '4046', '4225', '4770', 'Total Bags', 
                    'Small Bags', 'Large Bags', 'XLarge Bags', 
                    'type_encoded', 'region_encoded', 'year']
    
    X = df[feature_cols]
    y = df['AveragePrice']
    
    # Drop any NaN values
    mask = ~(X.isna().any(axis=1) | y.isna())
    X = X[mask]
    y = y[mask]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=15)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f'Test MAE: ${mae:.2f}')
    print(f'R2 Score: {r2:.4f}')
    print(f'Mean price: ${y_test.mean():.2f}')
    print(f'Trained on {len(X_train)} samples, tested on {len(X_test)} samples')
    
    # Save model with encoders
    model_data = {
        'model': model,
        'type_encoder': le_type,
        'region_encoder': le_region,
        'feature_cols': feature_cols
    }
    
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_data, MODEL_OUT)
    print(f'Saved model to {MODEL_OUT}')

if __name__ == '__main__':
    main()
