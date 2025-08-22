import shap
import joblib
import pandas as pd
import altair as alt
import plotly.express as px


model = joblib.load("models/saved_models/credit_model.pkl")

def explain(data: pd.DataFrame):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(data)
    return shap_values

if __name__ == "__main__":
    df = pd.read_csv("data/processed/structured_clean.csv")
    shap_vals = explain(df[["Open", "High", "Low", "Close", "Volume"]].fillna(0))
    print("✅ SHAP values generated")


def plot_feature_importance_shap(shap_values, X_test):
    df = pd.DataFrame({
        "Feature": X_test.columns,
        "SHAP Value": shap_values.values[0]
    })
    fig = px.bar(df, x="Feature", y="SHAP Value", title="Feature Attribution via SHAP")
    fig.show()

def plot_news_timeline(news_df):
    fig = px.timeline(news_df, x_start="publishedAt", x_end="publishedAt", y="source", hover_name="title")
    fig.update_yaxes(categoryorder="total ascending")
    fig.show()

def altair_feature_plot(shap_values, X_test):
    df = pd.DataFrame({
        "Feature": X_test.columns,
        "SHAP Value": shap_values.values[0]
    })
    chart = alt.Chart(df).mark_bar().encode(
        x="SHAP Value:Q",
        y=alt.Y("Feature:N", sort="-x"),
        color="SHAP Value:Q"
    ).properties(title="SHAP Feature Impact")
    chart.display()