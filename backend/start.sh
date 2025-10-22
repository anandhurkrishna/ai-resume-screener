cd "$(dirname "$0")/app"
uvicorn app.main.:app -- host 0.0.0.0 --port 10000