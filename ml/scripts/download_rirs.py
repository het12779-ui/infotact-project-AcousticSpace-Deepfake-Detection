import pyroomacoustics as pra
import numpy as np
import soundfile as sf
import os

# Custom pure-Python monkeypatch to fix "Windows fatal exception: access violation"
# when pyroomacoustics calls libroom.rir_builder on NumPy 2.x
def py_rir_builder(rir, time, alpha, fs, fdl, lut_gran, num_threads=1):
    fdl2 = (fdl - 1) // 2
    
    # Precompute sinc LUT (lookup table)
    lut_size = (fdl + 2) * lut_gran
    lut_delta = 1.0 / lut_gran
    
    # n values corresponding to each index in the LUT
    n = np.arange(lut_size) * lut_delta - fdl2 - 1
    # sinc(n) = sin(pi * n) / (pi * n)
    sinc_lut = np.zeros_like(n)
    zero_mask = (n == 0.0)
    sinc_lut[zero_mask] = 1.0
    sinc_lut[~zero_mask] = np.sin(np.pi * n[~zero_mask]) / (np.pi * n[~zero_mask])
    
    # Precompute Hann window
    k = np.arange(fdl)
    hann = 0.5 - 0.5 * np.cos((2 * np.pi * k) / (fdl - 1))
    
    # Convert inputs
    time = np.asarray(time)
    alpha = np.asarray(alpha)
    
    sample_frac = fs * time
    time_ip = np.floor(sample_frac).astype(int)
    time_fp = sample_frac - time_ip
    
    x_off_frac = (1.0 - time_fp) * lut_gran
    lut_gran_off = np.floor(x_off_frac).astype(int)
    x_off = x_off_frac - lut_gran_off
    
    # Loop over the length of the fractional delay filter
    for k_val in range(fdl):
        f = time_ip - fdl2 + k_val
        lut_pos = lut_gran_off + k_val * lut_gran
        
        # Linear interpolation from the LUT:
        val = sinc_lut[lut_pos] + x_off * (sinc_lut[lut_pos + 1] - sinc_lut[lut_pos])
        contrib = alpha * hann[k_val] * val
        
        # Accumulate in rir array safely using np.add.at
        valid = (f >= 0) & (f < len(rir))
        np.add.at(rir, f[valid], contrib[valid])

# Monkeypatch the C++ rir_builder function
pra.libroom.rir_builder = py_rir_builder

os.makedirs("../data/rirs", exist_ok=True)

room_configs = [
    {"name": "small_room",  "dim": [4, 3, 2.5],  "rt60": 0.3},
    {"name": "medium_room", "dim": [6, 5, 3],    "rt60": 0.5},
    {"name": "large_hall",  "dim": [12, 8, 4],   "rt60": 0.9},
    {"name": "bathroom",    "dim": [2, 2, 2.5],  "rt60": 0.6},
    {"name": "office",      "dim": [5, 4, 2.8],  "rt60": 0.4},
]

for cfg in room_configs:
    e_absorption, max_order = pra.inverse_sabine(cfg["rt60"], cfg["dim"])
    # Cap the maximum reflection order to 17. High orders take exponential computation
    # time and memory, but contribute negligible energy to the RIR.
    sim_max_order = min(max_order, 17)
    room = pra.ShoeBox(
        cfg["dim"],
        fs=16000,
        materials=pra.Material(e_absorption),
        max_order=sim_max_order
    )
    room.add_source([cfg["dim"][0] / 2, cfg["dim"][1] / 2, 1.5])
    room.add_microphone([cfg["dim"][0] / 4, cfg["dim"][1] / 4, 1.2])
    room.compute_rir()
    rir = room.rir[0][0]
    rir = rir / np.max(np.abs(rir))
    sf.write(f"../data/rirs/{cfg['name']}.wav", rir, 16000)
    print(f"Saved {cfg['name']}.wav — target RT60: {cfg['rt60']}s (sim_order={sim_max_order})", flush=True)
