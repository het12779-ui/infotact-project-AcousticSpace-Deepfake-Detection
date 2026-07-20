from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import PredictionResponse, SegmentFlag
from app.core.history import log_prediction, get_history
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "ml", "scripts"))
from inference import predict_mismatch

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
MAX_FILE_SIZE_MB = 20

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

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict_v1(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB limit)",
        )

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = predict_mismatch(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not process audio file: {e}")
    finally:
        os.remove(tmp_path)

    log_prediction(file.filename, result["is_fake"], result["confidence"])
    return PredictionResponse(
        filename=file.filename,
        is_fake=result["is_fake"],
        confidence=result["confidence"],
        rir_mismatch_score=result["rir_mismatch_score"],
        breathing_score=result["breathing_score"],
        flagged_segments=[SegmentFlag(**s) for s in result["flagged_segments"]],
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_legacy(file: UploadFile = File(...)):
    return await predict_v1(file)

@app.get("/history")
def history():
    return {"history": get_history()}
