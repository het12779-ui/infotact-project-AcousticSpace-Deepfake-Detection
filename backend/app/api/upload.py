import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
MAX_FILE_SIZE_MB = 20
TEMP_DIR = "temp_uploads"

os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
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
        
    temp_id = str(uuid.uuid4())
    temp_path = os.path.join(TEMP_DIR, f"{temp_id}{ext}")
    
    with open(temp_path, "wb") as f:
        f.write(contents)
        
    return {
        "upload_id": temp_id,
        "filename": file.filename,
        "size_mb": round(size_mb, 2),
        "stored_path": temp_path,
    }
