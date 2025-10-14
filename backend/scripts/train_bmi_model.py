"""Train a simple BMI/BodyFat model if dataset exists.

This script is safe to run even if the dataset isn't present; it will exit
with a friendly message.
"""
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

DATA = Path(__file__).parent.parent / 'datasets' / 'bodyfat.csv'
MODEL_OUT = Path(__file__).parent.parent / 'models' / 'bmi_model.joblib'

def main():
    if not DATA.exists():
        print(f"Dataset not found: {DATA}. Skipping training.")
        return

    df = pd.read_csv(DATA)
    # Expecting columns: Age, Weight_kg, Height_m, BodyFat
    if not {'Age','Weight_kg','Height_m','BodyFat'}.issubset(df.columns):
        print("Dataset doesn't contain required columns. Expected Age, Weight_kg, Height_m, BodyFat")
        return

    X = df[['Height_m','Weight_kg','Age']]
    y = df['BodyFat']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print('Test MAE:', mean_absolute_error(y_test, preds))
    print('R2:', r2_score(y_test, preds))

    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print('Saved model to', MODEL_OUT)

if __name__ == '__main__':
    main()
