cd "$(dirname "$0")/app"
unicorn main.:app -- host 0.0.0.0 --port 10000