import pyroomacoustics as pra
import numpy as np
import soundfile as sf
import os

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
    room = pra.ShoeBox(cfg["dim"], fs=16000, materials=pra.Material(e_absorption), max_order=max_order)
    room.add_source([cfg["dim"][0] / 2, cfg["dim"][1] / 2, 1.5])
    room.add_microphone([cfg["dim"][0] / 4, cfg["dim"][1] / 4, 1.2])
    room.compute_rir()
    rir = room.rir[0][0]
    rir = rir / np.max(np.abs(rir))
    sf.write(f"../data/rirs/{cfg['name']}.wav", rir, 16000)
    print(f"Saved {cfg['name']}.wav — target RT60: {cfg['rt60']}s")
