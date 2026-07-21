from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import PredictionResponse, SegmentFlag
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "ml", "scripts"))
from inference import predict_mismatch

app = FastAPI(title="AcousticSpace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = predict_mismatch(tmp_path)
    finally:
        os.remove(tmp_path)

    return PredictionResponse(
        filename=file.filename,
        is_fake=result["is_fake"],
        confidence=result["confidence"],
        rir_mismatch_score=result["rir_mismatch_score"],
        breathing_score=result["breathing_score"],
        flagged_segments=[SegmentFlag(**s) for s in result["flagged_segments"]],
    )
