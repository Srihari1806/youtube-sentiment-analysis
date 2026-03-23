@echo off
title YouTube Sentiment API - Experiment 6
echo.
echo  ==========================================
echo   YouTube Sentiment Analyzer - AD Lab
echo  ==========================================
echo.
call venv\Scripts\activate
echo Starting FastAPI server on http://127.0.0.1:5003
echo Open your browser at: http://127.0.0.1:5003
echo.
uvicorn main:app --reload --host 127.0.0.1 --port 5003
