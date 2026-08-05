# Regenerating the Acoustic Space dataset
Run these scripts from `ml/scripts/`, in this exact order:
1. `python generate_rirs.py` - creates 20 randomized room RIRs in `data/rirs/`
2. `python build_mismatch_dataset.py` - builds matched/mismatched voice+background pairs
3. `python synthesize_tts.py` - synthesizes TTS deepfake speech (needs espeak on Linux)
4. `python build_deepfake_mismatch_dataset.py` - combines real+TTS speech with RIRs
5. `python prepare_demo_set.py` - curates a 5-sample held-out demo/test set
6. `python build_attack_test_set.py` - builds the RIR-matched adversarial attack set
7. `python rir_features.py` - extracts per-segment RT60/DRR features
Each script is independent after step 1-2, but step 3 must run before step 4,
and step 1-2 must run before everything else.
