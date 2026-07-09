import torch
import librosa
from transformers import ASTFeatureExtractor, ASTForAudioClassification

MODEL_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"

feature_extractor = ASTFeatureExtractor.from_pretrained(MODEL_ID)
model = ASTForAudioClassification.from_pretrained(MODEL_ID)
model.eval()

sample_files = ["data/samples/sample1.wav", "data/samples/sample2.wav"]

for path in sample_files:
    waveform, sr = librosa.load(path, sr=16000)
    inputs = feature_extractor(waveform, sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)[0]
    top3 = torch.topk(probs, 3)
    print(f"\n{path}")
    for score, idx in zip(top3.values, top3.indices):
        print(f"  {model.config.id2label[idx.item()]}: {score.item():.3f}")
