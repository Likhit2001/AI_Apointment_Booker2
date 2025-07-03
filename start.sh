#!/bin/bash
export GROQ_API_KEY=="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"
# Start FastAPI backend in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait a few seconds to ensure backend is ready
sleep 5

# Start Streamlit frontend
streamlit run frontend.py --server.port=5000 --server.address=0.0.0.0