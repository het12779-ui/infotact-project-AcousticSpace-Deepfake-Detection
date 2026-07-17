import numpy as np
import librosa

def add_gaussian_noise(waveform, noise_level=0.005):
    noise = np.random.normal(0, noise_level, waveform.shape)
    return waveform + noise

def pitch_shift(waveform, sr, n_steps=None):
    if n_steps is None:
        n_steps = np.random.uniform(-2, 2)
    return librosa.effects.pitch_shift(waveform, sr=sr, n_steps=n_steps)

def time_stretch(waveform, rate=None):
    if rate is None:
        rate = np.random.uniform(0.9, 1.1)
    return librosa.effects.time_stretch(waveform, rate=rate)

def augment_waveform(waveform, sr):
    if np.random.rand() < 0.5:
        waveform = add_gaussian_noise(waveform)
    if np.random.rand() < 0.3:
        waveform = pitch_shift(waveform, sr)
    if np.random.rand() < 0.3:
        waveform = time_stretch(waveform)
    return waveform
