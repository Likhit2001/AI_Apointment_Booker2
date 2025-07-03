from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import sys
import os
from voice_agent import graph

app = FastAPI()

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once
model = whisper.load_model("small")

@app.post("/transcribe_audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        print("Backend")
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = graph.invoke({"audio_path": tmp_path})
    return result