import csv
import os

def load_mismatch_dataset(dataset_dir="../data/mismatch_dataset"):
    """
    Returns (file_paths, labels).
    labels: 0 = matched (genuine-like), 1 = mismatched (spoof-like)
    """
    labels_csv = os.path.join(dataset_dir, "labels.csv")
    file_paths, labels = [], []
    with open(labels_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_paths.append(os.path.join(dataset_dir, row["filename"]))
            labels.append(int(row["label"]))
    return file_paths, labels

if __name__ == "__main__":
    paths, labels = load_mismatch_dataset()
    n_mismatched = sum(labels)
    print(f"Loaded {len(paths)} samples - {n_mismatched} mismatched, {len(labels) - n_mismatched} matched")
