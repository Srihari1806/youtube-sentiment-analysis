# Experiment 6: Sentiment Prediction API (YouTube Edition)

## Overview
This project implements a Sentiment Prediction API using FastAPI and the **Google YouTube Data API**. It allows you to search for recent YouTube videos and analyze the sentiment of their **titles and descriptions** as Positive, Negative, or Neutral.

## Setup Instructions

1.  **Extract/Navigate** to `Experiment 6` directory.
2.  **Install Dependencies & Run**:
    *   Double-click `setup_and_run.bat` to automatically setup the environment and start the server.

3.  **YouTube API Key**:
    *   You need a valid **YouTube Data API v3** key from the [Google Cloud Console](https://console.cloud.google.com/).
    *   Open `.env` file in a text editor.
    *   Replace `your_youtube_api_key_here` with your actual API Key.

## Usage

1.  **Start API**: Run `setup_and_run.bat`. The API will start at `http://127.0.0.1:8000`.
2.  **Test**:
    *   Open `http://127.0.0.1:8000/docs` in your browser.
    *   Use the `/fetch_videos/` endpoint.
    *   Enter a keyword (e.g., "AI Review") and count (e.g., 5).
    *   The API will return video titles, descriptions, and their sentiment analysis.

## Files
- `main.py`: The main application code with YouTube API integration.
- `requirements.txt`: Dependencies including `google-api-python-client`.
- `.env`: Configuration file for the API Key.
- `setup_and_run.bat`: Automation script.
