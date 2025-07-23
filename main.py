from fastapi import FastAPI, HTTPException
from models import LoginRequest, ScrapeRequest, ScrapeResult
from bs4 import BeautifulSoup
import httpx
from fastapi import FastAPI, HTTPException, Header
from fastapi import Depends
from urllib.parse import urljoin
import google.generativeai as genai
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import Optional


FAKE_TOKEN = "secret-token-123"  # demo token


app = FastAPI()


DUMMY_USER = {
    "email": "user@example.com",
    "password": "securepassword123"
}

genai.configure(api_key="AIzaSyAtmtH3GpauXi9PyaH_dnlj5pHyMZKuDxw")  
GEMINI_MODEL = genai.GenerativeModel("models/gemini-1.5-flash")

sentiment_analyzer = SentimentIntensityAnalyzer()


@app.post("/login")
async def login(request: LoginRequest):
    if request.email == DUMMY_USER["email"] and request.password == DUMMY_USER["password"]:
        return {"message": "Login successful", "token": FAKE_TOKEN}
    raise HTTPException(status_code=401, detail="Invalid email or password")



@app.post("/scrape", response_model=ScrapeResult)
async def scrape_page(
    request: ScrapeRequest,
    token: Optional[str] = Header(None)
):
    if token != FAKE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token. Please log in.")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(str(request.url))
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Title
            title = soup.title.string.strip() if soup.title else "No title found"

            # Headings
            headings = []
            for level in range(1, 7):
                for tag in soup.find_all(f'h{level}'):
                    headings.append(tag.get_text(strip=True))

            # Images
            images = []
            for img in soup.find_all("img"):
                src = img.get("src")
                if src:
                    if src.startswith("//"):
                        src = "https:" + src
                    elif src.startswith("/"):
                        from urllib.parse import urljoin
                        src = urljoin(str(request.url), src)
                    images.append(src)

            # Summary from Gemini
            text = soup.get_text(separator=" ", strip=True)
            prompt = f"Give a short summary of this page:\n{text[:4000]}"  # truncate for token limit
            gemini_response = GEMINI_MODEL.generate_content(prompt)
            summary = gemini_response.text.strip()

            scores = sentiment_analyzer.polarity_scores(summary)
            compound = scores['compound']
            if compound >= 0.5:
                sentiment = "positive"
            elif compound <= -0.5:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            return ScrapeResult(
                url=str(request.url),
                title=title,
                headings=headings,
                images=images,
                summary=summary,
                sentiment=sentiment
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")