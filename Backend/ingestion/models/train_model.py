import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

def train():
    data = pd.read_csv("data/processed/structured_clean.csv")
    data["target"] = (data["Close"].pct_change().shift(-1) > 0).astype(int)

    X = data[["Open", "High", "Low", "Close", "Volume"]].dropna()
    y = data["target"].dropna()

    model = DecisionTreeClassifier(max_depth=4)
    model.fit(X, y)

    joblib.dump(model, "models/saved_models/credit_model.pkl")
    print("✅ Model trained and saved")

if __name__ == "__main__":
    train()
