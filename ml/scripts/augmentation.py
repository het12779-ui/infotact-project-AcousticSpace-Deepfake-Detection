import numpy as np
import librosa
from typing import Optional, List
import scipy.signal

def add_gaussian_noise(waveform: np.ndarray, noise_level: float = 0.005) -> np.ndarray:
    """Add Gaussian noise to the waveform."""
    noise = np.random.normal(0, noise_level, waveform.shape)
    return waveform + noise

def pitch_shift(waveform: np.ndarray, sr: int, n_steps: Optional[float] = None) -> np.ndarray:
    """Apply pitch shifting to the waveform."""
    if n_steps is None:
        n_steps = float(np.random.uniform(-2, 2))
    return librosa.effects.pitch_shift(y=waveform, sr=sr, n_steps=n_steps)

def time_stretch(waveform: np.ndarray, rate: Optional[float] = None) -> np.ndarray:
    """Apply time stretching to the waveform."""
    if rate is None:
        rate = float(np.random.uniform(0.9, 1.1))
    return librosa.effects.time_stretch(y=waveform, rate=rate)

def simulate_clipping(waveform: np.ndarray, threshold: float = 0.9) -> np.ndarray:
    """Apply non-linear distortion (clipping) to the waveform to simulate poor recording quality."""
    return np.clip(waveform, -threshold, threshold)

def apply_rir(waveform: np.ndarray, rir: np.ndarray) -> np.ndarray:
    """Apply Room Impulse Response via convolution."""
    # Convolution with RIR makes the audio sound like it's in a specific room
    convolved = scipy.signal.fftconvolve(waveform, rir, mode='full')
    # Match the original length
    convolved = convolved[:len(waveform)]
    # Normalize to prevent clipping
    if np.max(np.abs(convolved)) > 0:
        convolved = convolved / np.max(np.abs(convolved))
    return convolved

def augment_waveform(waveform: np.ndarray, sr: int, rir_waveforms: Optional[List[np.ndarray]] = None) -> np.ndarray:
    """Apply a random combination of augmentations to the waveform."""
    if np.random.rand() < 0.5:
        waveform = add_gaussian_noise(waveform)
    if np.random.rand() < 0.3:
        waveform = pitch_shift(waveform, sr)
    if np.random.rand() < 0.3:
        waveform = time_stretch(waveform)
    if np.random.rand() < 0.3:
        waveform = simulate_clipping(waveform)
    if rir_waveforms and np.random.rand() < 0.7:  # High probability to apply RIR if available
        import random
        rir = random.choice(rir_waveforms)
        waveform = apply_rir(waveform, rir)
    return waveform
