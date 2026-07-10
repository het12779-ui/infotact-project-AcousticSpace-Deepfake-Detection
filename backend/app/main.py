from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import PredictionResponse, SegmentFlag
import random

app = FastAPI(title="AcousticSpace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # frontend dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    # MOCK - replace with real model inference in Week 2/3
    return PredictionResponse(
        filename=file.filename,
        is_fake=random.choice([True, False]),
        confidence=round(random.uniform(0.6, 0.99), 2),
        rir_mismatch_score=round(random.uniform(0, 1), 2),
        breathing_score=round(random.uniform(0, 1), 2),
        flagged_segments=[SegmentFlag(start_time=1.2, end_time=2.4, reason="RIR mismatch")],
    )

