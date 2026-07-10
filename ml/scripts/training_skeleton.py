import torch
from torch.utils.data import Dataset, DataLoader
from transformers import ASTFeatureExtractor, ASTForAudioClassification
import librosa

MODEL_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"


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


def build_model(num_labels=2):
    return ASTForAudioClassification.from_pretrained(
        MODEL_ID, num_labels=num_labels, ignore_mismatched_sizes=True
    )


if __name__ == "__main__":
    feature_extractor = ASTFeatureExtractor.from_pretrained(MODEL_ID)

    # placeholder - replace with real ASVspoof file paths once M1's data is ready
    file_paths = ["../data/samples/sample1.wav", "../data/samples/sample2.wav"]
    labels = [0, 1]  # 0 = bonafide, 1 = spoof

    dataset = SpoofDataset(file_paths, labels, feature_extractor)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = build_model(num_labels=2)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

    model.train()
    for batch in loader:
        labels_batch = batch.pop("labels")
        outputs = model(**batch, labels=labels_batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        print(f"Batch loss: {loss.item():.4f}")

    print("Training loop skeleton ran successfully (not a real training run yet).")
