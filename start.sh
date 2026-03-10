#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: venv not found. Run 'python -m venv venv && pip install -r requirements.txt' first."
    exit 1
fi

# Verify dependencies
python -c "import streamlit; import fastapi; import uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Cleanup on exit — kill both backend and frontend
cleanup() {
    echo ""
    echo "Shutting down..."
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null
    wait 2>/dev/null
    echo "Done."
}
trap cleanup EXIT INT TERM

# Start backend
echo "Starting backend server on http://localhost:8000 ..."
uvicorn server:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
for i in $(seq 1 30); do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "Backend is ready!"
        break
    fi
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "Error: Backend failed to start."
        exit 1
    fi
    sleep 1
done

# Check if backend actually came up
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "Error: Backend did not become ready in time."
    exit 1
fi

# Start frontend
echo "Starting frontend on http://localhost:8501 ..."
streamlit run app.py --server.headless true --server.port 3000 &
FRONTEND_PID=$!

echo ""
echo "Blood Test Report Analyser is running!"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop."

# Wait for either process to exit
wait
