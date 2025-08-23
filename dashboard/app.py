from flask import Flask, render_template, jsonify
import pandas as pd
from Backend.ingestion.models.scoring_engine import score
import requests

app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_csv("data/processed/structured_clean.csv")
    scores = score(df[["Open", "High", "Low", "Close", "Volume"]].fillna(0))
    return jsonify({"scores": scores[:10].tolist()})

response = requests.post("https://credtech-hackathon-fk1l.onrender.com")


if __name__ == "__main__":
    app.run(debug=True)
