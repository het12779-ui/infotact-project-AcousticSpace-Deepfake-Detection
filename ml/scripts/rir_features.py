import librosa
import numpy as np
import os
import csv
import glob

SR = 16000

def schroeder_rt60(signal_segment, sr=SR):
    energy = signal_segment**2
    if np.sum(energy) == 0:
        return None
    edc = np.cumsum(energy[::-1])[::-1]
    edc_db = 10 * np.log10(edc / np.max(edc) + 1e-12)
    try:
        t5 = np.where(edc_db <= -5)[0][0] / sr
        t25 = np.where(edc_db <= -25)[0][0] / sr
        return 3 * (t25 - t5)
    except IndexError:
        return None

def direct_to_reverberant_ratio(signal_segment, sr=SR, direct_window_ms=5):
    direct_samples = int(sr * direct_window_ms / 1000)
    direct_energy = np.sum(signal_segment[:direct_samples]**2)
    reverberant_energy = np.sum(signal_segment[direct_samples:]**2)
    if reverberant_energy == 0:
        return None
    return 10 * np.log10(direct_energy / (reverberant_energy + 1e-12))

def extract_segment_features(audio_path, sr=SR, split_ratio=0.6):
    # Naive split: first part treated as voice-dominant, rest as background-dominant.
    # A production version would use voice-activity detection instead of a fixed ratio.
    y, _ = librosa.load(audio_path, sr=sr)
    split_idx = int(len(y) * split_ratio)
    voice_part = y[:split_idx]
    bg_part = y[split_idx:]
    
    return {
        "voice_rt60": schroeder_rt60(voice_part, sr),
        "voice_drr": direct_to_reverberant_ratio(voice_part, sr),
        "bg_rt60": schroeder_rt60(bg_part, sr),
        "bg_drr": direct_to_reverberant_ratio(bg_part, sr),
    }

if __name__ == "__main__":
    DEMO_DIR = "../data/demo_test_set"
    rows = []
    for path in sorted(glob.glob(f"{DEMO_DIR}/*.wav")):
        feats = extract_segment_features(path)
        feats["filename"] = os.path.basename(path)
        rows.append(feats)
        print(feats)
        
    if rows:
        with open(f"{DEMO_DIR}/rir_features.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["filename", "voice_rt60", "voice_drr", "bg_rt60", "bg_drr"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved rir_features.csv with {len(rows)} rows")
