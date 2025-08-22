import requests
import pandas as pd
from datetime import datetime

API_KEY = "NEWSAPI_KEY"
QUERY = "Apple Inc"

def fetch_news(query=QUERY):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    r = requests.get(url)
    articles = r.json().get("articles", [])
    df = pd.DataFrame([{
        "time": a["publishedAt"],
        "source": a["source"]["name"],
        "title": a["title"],
        "description": a["description"]
    } for a in articles])

    df.to_csv("data/raw/unstructured_data.csv", index=False)
    print(f"saved {len(df)} articles to data/raw/unstructured_data.csv")
    df["time"] = pd.to_datetime(df["time"])
    return df

if __name__ == "__main__":
    df=fetch_news()
    print(df.head())
    
