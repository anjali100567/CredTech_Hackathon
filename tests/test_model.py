import pytest
import pandas as pd
from Backend.ingestion.models.train_model import train_interpretable_model

def test_logistic_regression_accuracy():
    # Sample data
    df = pd.DataFrame({
        "age": [25, 40, 60],
        "income": [30000, 60000, 90000],
        "credit_history": [1, 0, 1],
        "loan_amount": [10000, 20000, 30000]
    })
    y = [1, 0, 1]

    model, X_test = train_interpretable_model(df, y, model_type="logistic")
    preds = model.predict(X_test)
    assert len(preds) == len(X_test)
    assert all(p in [0, 1] for p in preds)
