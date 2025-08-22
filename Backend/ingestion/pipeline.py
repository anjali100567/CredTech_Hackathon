# file: etl_flow_pg.py
import os 
import yfinance as yf
import requests
import pandas as pd
from textblob import TextBlob

from datetime import datetime
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(title="Credit Intelligence API")


load_dotenv()


# --- DB Connection Helper ---
def get_db():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "finance_db"),
        user=os.getenv("POSTGRES_USER", "anjli"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )

# --- Config ---
API_KEY = os.getenv("NEWSAPI_KEY")
if not API_KEY:
    raise ValueError("NEWSAPI_KEY not found in environment variables. Please set it in your .env file.")
TICKER = "AAPL"
COMPANY = "Apple Inc"

@app.get("/issuer/{ticker}")
def ensure_issuer(ticker=TICKER, name=COMPANY):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO issuers (ticker, name) VALUES (%s, %s) ON CONFLICT (ticker) DO NOTHING",
        (ticker, name),
    )
    conn.commit()
    cur.close()
    conn.close()

@app.get("/prices/{ticker}")
def fetch_prices(ticker=TICKER, period="1mo", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)

    conn = get_db()
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute(
            """INSERT INTO prices (issuer_id, ts, close, volume)
               SELECT id, %s, %s, %s FROM issuers WHERE ticker=%s
               ON CONFLICT DO NOTHING""",
            (row["Date"], row["Close"], row["Volume"], ticker),
        )
    conn.commit()
    cur.close()
    conn.close()
    return df

@app.get("/news/{ticker}")
def fetch_news(query=COMPANY):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    r = requests.get(url)
    articles = r.json().get("articles", [])
    df = pd.DataFrame(
        [
            {
                "time": a["publishedAt"],
                "source": a["source"]["name"],
                "title": a["title"],
                "description": a["description"],
            }
            for a in articles
        ]
    )
    if not df.empty:
        df["time"] = pd.to_datetime(df["time"])

    # Insert into DB
    conn = get_db()
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute(
            """INSERT INTO events (issuer_id, ts, source, headline, sentiment, impact)
               SELECT id, %s, %s, %s, %s, %s FROM issuers WHERE ticker=%s""",
            (
                row["time"],
                row["source"],
                row["title"],
                TextBlob(str(row["title"])).sentiment.polarity,
                0.5,  # placeholder impact
                TICKER,
            ),
        )
    conn.commit()
    cur.close()
    conn.close()
    return df

@app.get("/score/{ticker}")
def compute_score(prices: pd.DataFrame, news: pd.DataFrame):
    avg_sentiment = (
        news["title"].apply(lambda t: TextBlob(str(t)).sentiment.polarity).mean()
        if not news.empty
        else 0
    )
    price_change = (
        (prices["Close"].iloc[-1] - prices["Close"].iloc[0])
        / prices["Close"].iloc[0]
        * 100
    )

    score = 50 + price_change * 0.5 + avg_sentiment * 20

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO scores (issuer_id, ts, score, method)
           SELECT id, now(), %s, %s FROM issuers WHERE ticker=%s""",
        (round(score, 2), "toy-rule", TICKER),
    )
    conn.commit()
    cur.close()
    conn.close()

    return score


def credit_pipeline():
    ensure_issuer()
    prices = fetch_prices()
    news = fetch_news()
    score = compute_score(prices, news)
    print("Latest Credit Score:", score)

if __name__ == "__main__":
    credit_pipeline()
