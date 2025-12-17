#!/bin/bash
# Chatterbox-FASTAPI Server Launcher
# This script helps launch the server with proper configuration

set -e

# Find free port function
find_free_port() {
    python3 -c "import socket; s = socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()"
}

# Check if PORT is set, otherwise find a free one
if [ -z "$PORT" ]; then
    PORT=$(find_free_port)
    echo "No PORT specified, using free port: $PORT"
else
    echo "Using specified PORT: $PORT"
fi

echo "Starting Chatterbox-FASTAPI server on port $PORT..."
echo "API docs will be available at: http://localhost:$PORT/docs"
echo "Health check at: http://localhost:$PORT/health"
echo ""
echo "Note: First run will download models (~500MB+), please be patient..."
echo ""

# Launch server
PORT=$PORT conda run -n chatterbox-fastapi python -m api.main
