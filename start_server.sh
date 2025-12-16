#!/bin/bash
# Startup script for Chatterbox FastAPI server

echo "Starting Chatterbox FastAPI server..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if uvicorn is available
if ! python3 -c "import uvicorn" &> /dev/null; then
    echo "Error: uvicorn is not installed"
    echo "Install it with: pip install uvicorn[standard]"
    exit 1
fi

# Set default values
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WORKERS:-1}"

echo "Configuration:"
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Workers: $WORKERS"
echo ""

# Start the server
python3 -m uvicorn api.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS" \
    --log-level info
