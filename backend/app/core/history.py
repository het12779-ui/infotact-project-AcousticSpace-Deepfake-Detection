from datetime import datetime
from typing import List, Dict

_history: List[Dict] = []

def log_prediction(filename: str, is_fake: bool, confidence: float):
    _history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "filename": filename,
        "is_fake": is_fake,
        "confidence": confidence,
    })
    if len(_history) > 50:
        _history.pop(0)

def get_history():
    return list(reversed(_history))
