#!/usr/bin/env python3
from fastapi import FastAPI, File, UploadFile
import whisper
import os
import uuid

app = FastAPI()
model = None

@app.on_event("startup")
async def startup_event():
  global model
  model = whisper.load_model("large-v2")

@app.post("/")
async def transcription(file: UploadFile):
  # Generate a unique identifier for the request
  request_id = str(uuid.uuid4())
  subdirectory = "cached_audio"
  os.makedirs(subdirectory, exist_ok=True)
  file_path = os.path.join(subdirectory, f"{request_id}.wav")

  with open(file_path, 'wb') as f:
    while contents := file.file.read(1024 * 1024):
      f.write(contents)
  file.file.close()
  results = model.transcribe(file_path)
  # Clean up the file after processing
  os.remove(file_path)
  return results
