import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

def compute_mel_spectrogram(audio_path, sr=16000, n_mels=128):
    y, sr = librosa.load(audio_path, sr=sr)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    return mel_db, sr

def estimate_rt60_schroeder(rir_path, sr=16000):
    rir, sr = librosa.load(rir_path, sr=sr)
    energy = rir ** 2
    edc = np.cumsum(energy[::-1])[::-1]  # Schroeder backward integration
    edc_db = 10 * np.log10(edc / np.max(edc) + 1e-12)
    try:
        t5 = np.where(edc_db <= -5)[0][0] / sr
        t25 = np.where(edc_db <= -25)[0][0] / sr
        rt60_est = 3 * (t25 - t5)  # T20 extrapolated to RT60
    except IndexError:
        rt60_est = None
    return edc_db, rt60_est

if __name__ == "__main__":
    os.makedirs("../data/features", exist_ok=True)
    sample_path = "../data/samples/sample1.wav"
    
    if os.path.exists(sample_path):
        mel_db, sr = compute_mel_spectrogram(sample_path)
        plt.figure(figsize=(8, 4))
        librosa.display.specshow(mel_db, sr=sr, x_axis="time", y_axis="mel")
        plt.colorbar(format="%+2.0f dB")
        plt.title("Mel Spectrogram - sample1")
        plt.tight_layout()
        plt.savefig("../data/features/sample1_melspec.png")
        print("Saved mel spectrogram plot for sample1.wav")
    else:
        print(f"No sample found at {sample_path}, skipping mel spectrogram step")
        
    for room in ["small_room", "medium_room", "large_hall", "bathroom", "office"]:
        rir_path = f"../data/rirs/{room}.wav"
        if os.path.exists(rir_path):
            _, rt60 = estimate_rt60_schroeder(rir_path)
            if rt60:
                print(f"{room}: estimated RT60 = {rt60:.3f}s")
            else:
                print(f"{room}: RT60 estimation failed")
