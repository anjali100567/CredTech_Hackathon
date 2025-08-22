import joblib
import pandas as pd

model = joblib.load("models/saved_models/credit_model.pkl")

def score(data: pd.DataFrame):
    preds = model.predict_proba(data)[:, 1]
    return preds

if __name__ == "__main__":
    df = pd.read_csv("data/processed/structured_clean.csv")
    scores = score(df[["Open", "High", "Low", "Close", "Volume"]].fillna(0))
    print("✅ Scores:", scores[:5])
