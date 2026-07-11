import torch
from torch.utils.data import DataLoader, random_split, Dataset
from transformers import ASTFeatureExtractor, ASTForAudioClassification
import librosa
import os
from evaluate_utils import compute_eer, compute_accuracy

MODEL_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"
CHECKPOINT_DIR = "../checkpoints"

class SpoofDataset(Dataset):
    def __init__(self, file_paths, labels, feature_extractor, sr=16000):
        self.file_paths = file_paths
        self.labels = labels
        self.feature_extractor = feature_extractor
        self.sr = sr

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        waveform, _ = librosa.load(self.file_paths[idx], sr=self.sr)
        inputs = self.feature_extractor(waveform, sampling_rate=self.sr, return_tensors="pt")
        item = {k: v.squeeze(0) for k, v in inputs.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

def evaluate(model, loader):
    model.eval()
    all_labels, all_scores, all_preds = [], [], []
    with torch.no_grad():
        for batch in loader:
            labels = batch.pop("labels")
            outputs = model(**batch)
            probs = torch.softmax(outputs.logits, dim=-1)
            spoof_scores = probs[:, 1]
            preds = torch.argmax(probs, dim=-1)
            
            all_labels.extend(labels.tolist())
            all_scores.extend(spoof_scores.tolist())
            all_preds.extend(preds.tolist())
            
    acc = compute_accuracy(all_labels, all_preds)
    eer, _ = compute_eer(all_labels, all_scores)
    return acc, eer

if __name__ == "__main__":
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    feature_extractor = ASTFeatureExtractor.from_pretrained(MODEL_ID)
    
    # placeholder file list - swap for Het's data/mismatch_dataset/labels.csv once ready
    file_paths = ["../data/samples/sample1.wav", "../data/samples/sample2.wav"] * 4
    labels = [0, 1] * 4
    
    dataset = SpoofDataset(file_paths, labels, feature_extractor)
    train_size = int(0.75 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_ds, batch_size=2, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=2)
    
    model = ASTForAudioClassification.from_pretrained(MODEL_ID, num_labels=2, ignore_mismatched_sizes=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
    
    best_eer = 1.0
    for epoch in range(2):
        model.train()
        for batch in train_loader:
            labels_batch = batch.pop("labels")
            outputs = model(**batch, labels=labels_batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
        acc, eer = evaluate(model, val_loader)
        print(f"Epoch {epoch+1}: val_accuracy={acc:.3f}, val_EER={eer:.3f}")
        
        if eer < best_eer:
            best_eer = eer
            torch.save(model.state_dict(), f"{CHECKPOINT_DIR}/best_model.pt")
            print(f"Saved new best checkpoint (EER={eer:.3f})")
