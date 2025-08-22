import pytest
from Backend import fetch_financial_news
import os
from dotenv import load_dotenv

load_dotenv()

def test_newsapi_response():
    api_key = os.getenv("NEWSAPI_KEY")
    assert api_key is not None, "Missing NEWSAPI_KEY"

    df = fetch_financial_news(api_key, query="credit")
    assert not df.empty
    assert "title" in df.columns
    assert "publishedAt" in df.columns

if __name__ == "__main__":
    pytest.main()