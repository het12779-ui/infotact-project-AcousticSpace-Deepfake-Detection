import torch
import librosa
from transformers import ASTFeatureExtractor, ASTForAudioClassification
import os

MODEL_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"
CHECKPOINT_PATH = os.path.join(os.path.dirname(__file__), "..", "checkpoints", "best_model.pt")

_feature_extractor = None
_model = None

def load_model():
    global _feature_extractor, _model
    if _model is None:
        _feature_extractor = ASTFeatureExtractor.from_pretrained(MODEL_ID)
        _model = ASTForAudioClassification.from_pretrained(
            MODEL_ID, num_labels=2, ignore_mismatched_sizes=True
        )
        if os.path.exists(CHECKPOINT_PATH):
            _model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location="cpu"))
            print(f"Loaded checkpoint from {CHECKPOINT_PATH}")
        else:
            print("No checkpoint found - using base pretrained weights (predictions will be unreliable).")
        _model.eval()
    return _feature_extractor, _model

def predict_mismatch(audio_path: str, sr: int = 16000) -> dict:
    feature_extractor, model = load_model()
    waveform, _ = librosa.load(audio_path, sr=sr)
    inputs = feature_extractor(waveform, sampling_rate=sr, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
        spoof_score = probs[1].item()
    return {
        "is_fake": spoof_score > 0.5,
        "confidence": round(max(spoof_score, 1 - spoof_score), 3),
        "rir_mismatch_score": round(spoof_score, 3),
        "breathing_score": None, # placeholder until the breathing module (Week 3) is added
        "flagged_segments": [], # placeholder until explainability (Week 3) is added
    }

if __name__ == "__main__":
    import sys
    test_path = sys.argv[1] if len(sys.argv) > 1 else "../data/samples/sample1.wav"
    result = predict_mismatch(test_path)
    print(result)
