import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

api_key = os.getenv("NEWSAPI_KEY")


def fetch_news(api_key, query="finance"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url).json()
    articles = [
        {"title": a["title"], "desc": a["description"]}
        for a in response.get("articles", [])
    ]
    return pd.DataFrame(articles)

if __name__ == "__main__":
    df = fetch_news("YOUR_NEWS_API_KEY")
    df.to_csv("data/raw/unstructured_data.csv", index=False)
    print("✅ Unstructured news data saved")
