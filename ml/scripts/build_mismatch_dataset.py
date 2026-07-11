import numpy as np
import soundfile as sf
import librosa
import os
import csv
from scipy.signal import fftconvolve

RIR_DIR = "../data/rirs"
SAMPLE_DIR = "data/samples"
OUT_DIR = "data/mismatch_dataset"
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

def build_pair(voice_path, room_a, room_b, out_prefix):
    voice, _ = librosa.load(voice_path, sr=SR)
    rir_a = load_rir(room_a)
    rir_b = load_rir(room_b)
    
    # MATCHED sample: voice and background share the same room RIR
    voice_matched = convolve_and_normalize(voice, rir_a)
    bg_matched = generate_background_noise(len(voice), rir_a)
    matched = voice_matched + bg_matched
    sf.write(f"{OUT_DIR}/{out_prefix}_matched_{room_a}.wav", matched, SR)
    
    # MISMATCHED sample: voice convolved with room A, background convolved with room B
    voice_mismatched = convolve_and_normalize(voice, rir_a)
    bg_mismatched = generate_background_noise(len(voice), rir_b)
    mismatched = voice_mismatched + bg_mismatched
    sf.write(f"{OUT_DIR}/{out_prefix}_mismatched_{room_a}_vs_{room_b}.wav", mismatched, SR)
    
    return [
        (f"{out_prefix}_matched_{room_a}.wav", 0, room_a, room_a),
        (f"{out_prefix}_mismatched_{room_a}_vs_{room_b}.wav", 1, room_a, room_b),
    ]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    rooms = ["small_room", "medium_room", "large_hall", "bathroom", "office"]
    voice_path = f"{SAMPLE_DIR}/sample1.wav"
    labels = []
    
    if not os.path.exists(voice_path):
        print(f"No voice sample found at {voice_path} - add one before running this script.")
    else:
        for i in range(len(rooms)):
            room_a = rooms[i]
            room_b = rooms[(i+1) % len(rooms)]
            labels.extend(build_pair(voice_path, room_a, room_b, f"pair{i}"))
            
        with open(f"{OUT_DIR}/labels.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "label", "voice_room", "background_room"])
            writer.writerows(labels)
            
        print(f"Generated {len(labels)} labeled samples in {OUT_DIR}/")
        print("label 0 = matched (genuine-like), label 1 = mismatched (spoof-like)")
