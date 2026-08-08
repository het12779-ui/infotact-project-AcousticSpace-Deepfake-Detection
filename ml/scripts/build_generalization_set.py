import numpy as np
import soundfile as sf
import librosa
import os
import csv
import glob
from scipy.signal import fftconvolve

RIR_DIR = "../data/rirs" if os.path.exists("../data/rirs") else "data/rirs"
TTS_DIR = "../data/tts_samples" if os.path.exists("../data/tts_samples") else "data/tts_samples"
REAL_DIR = "../data/samples" if os.path.exists("../data/samples") else "data/samples"
OUT_DIR = "../data/generalization_test_set" if os.path.exists("../data") else "data/generalization_test_set"
SR = 16000

def load_rir(name):
    rir, _ = librosa.load(f"{RIR_DIR}/{name}.wav", sr=SR)
    return rir / np.max(np.abs(rir))

def convolve_and_normalize(signal, rir):
    out = fftconvolve(signal, rir)[:len(signal)]
    return out / (np.max(np.abs(out)) + 1e-8)

def generate_background_noise(length, rir, noise_level=0.1):
    noise = np.random.normal(0, 1, length)
    noise = convolve_and_normalize(noise, rir)
    return noise * noise_level

def build_sample(voice_path, room_a, room_b, out_name, is_mismatched):
    voice, _ = librosa.load(voice_path, sr=SR)
    rir_a = load_rir(room_a)
    voice_conv = convolve_and_normalize(voice, rir_a)
    rir_b = load_rir(room_b) if is_mismatched else rir_a
    bg = generate_background_noise(len(voice), rir_b)
    mix = voice_conv + bg
    sf.write(f"{OUT_DIR}/{out_name}.wav", mix, SR)

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    rooms = [os.path.splitext(os.path.basename(p))[0] for p in sorted(glob.glob(f"{RIR_DIR}/*.wav"))]
    tts_files = sorted(glob.glob(f"{TTS_DIR}/*.wav"))
    real_files = sorted(glob.glob(f"{REAL_DIR}/*.wav"))
    
    if not tts_files or not rooms:
        print("Need RIRs and TTS samples - run generate_rirs.py and synthesize_tts.py first.")
    else:
        rows = []
        count = 0
        for i, tts_path in enumerate(tts_files):
            room_a = rooms[i % len(rooms)]
            room_b = rooms[(i + 2) % len(rooms)]
            name = f"gen_fake_{count:03d}"
            build_sample(tts_path, room_a, room_b, name, is_mismatched=True)
            rows.append((f"{name}.wav", 1, "unseen_noise_deepfake"))
            count += 1

        for i, real_path in enumerate(real_files):
            room_a = rooms[i % len(rooms)]
            name = f"gen_real_{count:03d}"
            build_sample(real_path, room_a, room_a, name, is_mismatched=False)
            rows.append((f"{name}.wav", 0, "unseen_noise_real"))
            count += 1

        with open(f"{OUT_DIR}/labels.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "label", "condition"])
            writer.writerows(rows)

        print(f"Generated {len(rows)} generalization samples in {OUT_DIR}/")
