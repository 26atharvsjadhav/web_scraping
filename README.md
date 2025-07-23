 # Web Scraper API
 
This project is a FastAPI-based web scraper that extracts information from web pages, summarizes the content using Google Gemini, and performs sentiment analysis using NLTK.

## Features
- **User Authentication**: Simple login endpoint with a demo user.
- **Web Scraping**: Extracts title, headings, and images from a given URL.
- **Content Summarization**: Uses Google Gemini API to generate a summary of the scraped page.
- **Sentiment Analysis**: Analyzes the summary's sentiment (positive, negative, neutral) using NLTK VADER.

## Endpoints
- `POST /login`: Authenticate and receive a token.
- `POST /scrape`: Scrape a web page (requires token).

## Setup Instructions

1. **Clone the repository**
   ```
   git clone <your-repo-url>
   cd tata-neu
   ```

2. **Install dependencies**
   ```
   pip install fastapi httpx beautifulsoup4 google-generativeai nltk uvicorn
   ```

3. **Download NLTK VADER Lexicon**
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

4. **Set your Google Gemini API key**
   - Replace the API key in `main.py` with your own for production use.

5. **Run the API server**
   ```
   uvicorn main:app --reload
   ```

6. **Access the API docs**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## Example Usage

1. **Login**
   ```json
   POST /login
   {
     "email": "user@example.com",
     "password": "securepassword123"
   }
   ```
   Response:
   ```json
   { "message": "Login successful", "token": "secret-token-123" }
   ```

2. **Scrape a Page**
   ```json
   POST /scrape
   Headers: { "token": "secret-token-123" }
   {
     "url": "https://example.com"
   }
   ```

