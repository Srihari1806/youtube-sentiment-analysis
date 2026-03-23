@echo off
echo Setting up Experiment 6 with YouTube API...

REM Check if Python is installed
python --version
if errorlevel 1 goto python_error

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing requirements...
pip install -r requirements.txt

REM Download NLTK corpora for TextBlob
echo Downloading NLTK corpora...
python -m textblob.download_corpora

REM Check environment variables
if not exist ".env" (
    echo WARNING: .env file not found! Using default values which might fail.
    echo Please create/edit .env with your YouTube API key.
)

REM Run FastAPI application
echo Starting FastAPI application...
uvicorn main:app --reload --host 127.0.0.1 --port 5003

goto end

:python_error
echo Python is not installed or not in PATH. Please install Python.
pause
exit /b 1

:end
pause
