cd "$(dirname "$0")/app"
uvicorn main:app --host=0.0.0.0 --port=$PORT