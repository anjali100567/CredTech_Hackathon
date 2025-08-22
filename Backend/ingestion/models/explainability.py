import shap
import joblib
import pandas as pd

model = joblib.load("models/saved_models/credit_model.pkl")

def explain(data: pd.DataFrame):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(data)
    return shap_values

if __name__ == "__main__":
    df = pd.read_csv("data/processed/structured_clean.csv")
    shap_vals = explain(df[["Open", "High", "Low", "Close", "Volume"]].fillna(0))
    print("✅ SHAP values generated")
