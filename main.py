import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from textblob import TextBlob
from dotenv import load_dotenv
import uvicorn
from googleapiclient.discovery import build, build_from_document
from googleapiclient.errors import HttpError
from typing import Optional
import re

# Path to locally cached discovery document (avoids googleapis.com DNS lookup)
DISCOVERY_DOC = Path(__file__).parent / "youtube_discovery.json"

# Load environment variables
load_dotenv()

# Configuration - Get this from your Google Cloud Console
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize FastAPI App
app = FastAPI(
    title="YouTube Sentiment Analysis API",
    description="Analyze YouTube video sentiments using TextBlob NLP",
    version="2.0"
)

# CORS Middleware - allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the frontend UI
import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# Request Model
class SearchRequest(BaseModel):
    keyword: str
    count: int = 10
    sort_by: Optional[str] = "relevance"  # relevance, date, viewCount, rating


# Response Model
class VideoSentiment(BaseModel):
    video_id: str
    title: str
    description: str
    channel: str
    published_at: str
    thumbnail: str
    sentiment: str
    polarity: float
    subjectivity: float


# Initialize YouTube Client
def get_youtube_service():
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "your_youtube_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="YouTube API Key not configured. Please add your key to .env file as YOUTUBE_API_KEY=your_key"
        )
    # Use locally cached discovery document — avoids DNS lookup to googleapis.com
    try:
        if DISCOVERY_DOC.exists():
            doc = DISCOVERY_DOC.read_text(encoding="utf-8")
            return build_from_document(doc, developerKey=YOUTUBE_API_KEY)
    except Exception:
        pass
    # Fallback: live build (requires internet access to googleapis.com)
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, cache_discovery=False)


# Sentiment Analysis Function
def analyze_sentiment(text: str) -> dict:
    # Clean text
    clean_text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    clean_text = re.sub(r'\@\w+|\#', '', clean_text)
    
    analysis = TextBlob(clean_text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 4),
        "subjectivity": round(subjectivity, 4)
    }


# Root - Serve the HTML Frontend
@app.get("/")
def read_root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {
        "message": "YouTube Sentiment Analysis API v2.0",
        "endpoints": {
            "POST /fetch_videos/": "Analyze YouTube video sentiments",
            "GET /health": "Health check",
            "GET /docs": "Swagger UI documentation"
        }
    }


# Health Check
@app.get("/health")
def health_check():
    api_configured = bool(YOUTUBE_API_KEY and YOUTUBE_API_KEY != "your_youtube_api_key_here")
    return {
        "status": "running",
        "api_configured": api_configured,
        "message": "YouTube API Key is set" if api_configured else "⚠️ Please set YOUTUBE_API_KEY in .env file"
    }


# Fetch Videos + Sentiment Analysis Endpoint
@app.post("/fetch_videos/", response_model=list[VideoSentiment])
def fetch_videos(request: SearchRequest):
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "your_youtube_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="YouTube API Key not configured. Please add your key to .env file."
        )

    try:
        service = get_youtube_service()

        # Search for videos
        search_response = service.search().list(
            q=request.keyword,
            part="snippet",
            maxResults=min(request.count, 50),
            type="video",
            order=request.sort_by
        ).execute()

        results = []
        for item in search_response.get("items", []):
            snippet = item["snippet"]
            video_id = item["id"]["videoId"]
            title = snippet.get("title", "")
            description = snippet.get("description", "")
            channel = snippet.get("channelTitle", "")
            published_at = snippet.get("publishedAt", "")
            thumbnail = snippet.get("thumbnails", {}).get("medium", {}).get("url", "")

            # Analyze sentiment of title + description
            full_text = f"{title}. {description}"
            sentiment_data = analyze_sentiment(full_text)

            results.append(VideoSentiment(
                video_id=video_id,
                title=title,
                description=description,
                channel=channel,
                published_at=published_at,
                thumbnail=thumbnail,
                sentiment=sentiment_data["sentiment"],
                polarity=sentiment_data["polarity"],
                subjectivity=sentiment_data["subjectivity"]
            ))

        return results

    except HttpError as e:
        raise HTTPException(status_code=500, detail=f"YouTube API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5003, reload=True)
