import pyroomacoustics as pra
import numpy as np
import soundfile as sf
import os
import random

OUT_DIR = "../data/rirs"
SR = 16000
random.seed(7)
np.random.seed(7)

def random_room_config(i):
    length = round(random.uniform(3, 15), 1)
    width = round(random.uniform(2.5, 10), 1)
    height = round(random.uniform(2.3, 4.5), 1)
    rt60 = round(random.uniform(0.2, 1.2), 2)
    return {"name": f"room_{i:02d}", "dim": [length, width, height], "rt60": rt60}

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    n_rooms = 20
    manifest = []
    for i in range(n_rooms):
        cfg = random_room_config(i)
        try:
            e_absorption, max_order = pra.inverse_sabine(cfg["rt60"], cfg["dim"])
            room = pra.ShoeBox(cfg["dim"], fs=SR, materials=pra.Material(e_absorption), max_order=max_order)
            room.add_source([cfg["dim"][0]/2, cfg["dim"][1]/2, 1.5])
            room.add_microphone([cfg["dim"][0]/4, cfg["dim"][1]/4, 1.2])
            room.compute_rir()
            rir = room.rir[0][0]
            rir = rir / np.max(np.abs(rir))
            sf.write(f"{OUT_DIR}/{cfg['name']}.wav", rir, SR)
            manifest.append(cfg)
            print(f"Generated {cfg['name']}: dim={cfg['dim']}, target RT60={cfg['rt60']}s")
        except Exception as e:
            print(f"Skipped {cfg['name']} due to error: {e}")
    print(f"\nGenerated {len(manifest)} rooms in {OUT_DIR}/")
