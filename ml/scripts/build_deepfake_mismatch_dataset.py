import numpy as np
import soundfile as sf
import librosa
import os
import csv
import glob
from scipy.signal import fftconvolve

RIR_DIR = "../data/rirs"
REAL_DIR = "../data/samples"
TTS_DIR = "../data/tts_samples"
OUT_DIR = "../data/deepfake_mismatch_dataset"
SR = 16000

def load_rir(name):
    rir, _ = librosa.load(f"{RIR_DIR}/{name}.wav", sr=SR)
    return rir / np.max(np.abs(rir))

def convolve_and_normalize(signal, rir):
    out = fftconvolve(signal, rir)[:len(signal)]
    return out / (np.max(np.abs(out)) + 1e-8)

def generate_background_noise(length, rir, noise_level=0.05):
    noise = np.random.normal(0, 1, length)
    noise = convolve_and_normalize(noise, rir)
    return noise * noise_level

def build_sample(voice_path, room_a, room_b, out_name, is_deepfake):
    voice, _ = librosa.load(voice_path, sr=SR)
    rir_a = load_rir(room_a)
    voice_conv = convolve_and_normalize(voice, rir_a)
    
    if is_deepfake:
        rir_b = load_rir(room_b)
        bg = generate_background_noise(len(voice), rir_b)
    else:
        bg = generate_background_noise(len(voice), rir_a)
        
    mix = voice_conv + bg
    sf.write(f"{OUT_DIR}/{out_name}.wav", mix, SR)

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    rooms = [os.path.splitext(os.path.basename(p))[0] for p in sorted(glob.glob(f"{RIR_DIR}/*.wav"))]
    real_files = sorted(glob.glob(f"{REAL_DIR}/*.wav"))
    tts_files = sorted(glob.glob(f"{TTS_DIR}/*.wav"))
    
    if not real_files or not tts_files:
        print("Need at least one file in data/samples/ and data/tts_samples/ - run synthesize_tts.py first.")
    else:
        rows = []
        for i, real_path in enumerate(real_files):
            room_a = rooms[i % len(rooms)]
            name = f"genuine_{i:03d}"
            build_sample(real_path, room_a, room_a, name, is_deepfake=False)
            rows.append((f"{name}.wav", 0, "real_speech"))
            
        for i, tts_path in enumerate(tts_files):
            room_a = rooms[i % len(rooms)]
            room_b = rooms[(i+3) % len(rooms)]
            name = f"deepfake_{i:03d}"
            build_sample(tts_path, room_a, room_b, name, is_deepfake=True)
            rows.append((f"{name}.wav", 1, "tts_speech"))
            
        with open(f"{OUT_DIR}/labels.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "label", "voice_source"])
            writer.writerows(rows)
            
        print(f"Generated {len(rows)} samples ({len(real_files)} genuine, {len(tts_files)} deepfake) in {OUT_DIR}/")
