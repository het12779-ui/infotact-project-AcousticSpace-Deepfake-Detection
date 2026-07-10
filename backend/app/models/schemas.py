from pydantic import BaseModel
from typing import List, Optional

class SegmentFlag(BaseModel):
    start_time: float
    end_time: float
    reason: str

class PredictionResponse(BaseModel):
    filename: str
    is_fake: bool
    confidence: float
    rir_mismatch_score: Optional[float] = None
    breathing_score: Optional[float] = None
    flagged_segments: List[SegmentFlag] = []
