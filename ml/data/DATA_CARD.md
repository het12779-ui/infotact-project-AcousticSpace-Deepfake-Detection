# AcousticSpace - Dataset Card

## Synthetic RIRs
5 room configurations (small_room, medium_room, large_hall, bathroom, office)
generated with pyroomacoustics using the Sabine equation, targeting RT60 values
between 0.3s and 0.9s.

## Mismatch dataset
For each voice sample and each room, we generate:
- a MATCHED pair: voice + background noise both convolved with the same RIR (label 0)
- a MISMATCHED pair: voice convolved with one room's RIR, background noise
convolved with a different room's RIR (label 1)

Total samples: 50
Voice samples used: 5

## Known limitations
- Background "noise" is currently synthetic white/pink noise shaped by a
convolved RIR, not a real recorded ambience track - a real limitation to
mention honestly in the report.
- All RIRs are simulated (shoebox rooms), not measured in physical spaces.

## Demo test set
5 samples held out via prepare_demo_set.py (data/demo_test_set/), used for the
team's end-to-end integration test - not used during training.
