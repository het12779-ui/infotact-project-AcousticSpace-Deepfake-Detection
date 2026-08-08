# AcousticSpace - Results Log

| Test set | Accuracy | EER | Notes |
|---|---|---|---|
| Training val split (Day 6) | 0.850 | 0.120 | Random 25% split of training data |
| Held-out demo_test_set (Day 8) | 0.800 | 0.250 | Genuinely unseen during training |
| Attack test set (Day 9) | 0.150 | 0.700 | RIR-matched adversarial deepfakes |

## Key finding
The model's accuracy drops from 0.800 to 0.150 when deepfake speech is convolved with a matching room RIR - confirming the model currently relies heavily on RIR-mismatch as its main signal, and that signal can be deliberately masked. Defending against this (RIR-augmented retraining) is planned for Week 3.

## Breathing / Pause Detection Heuristic (Day 10)
We implemented an independent heuristic breathing and pause detection module (`ml/scripts/breathing_detector.py`) based on short-time energy analysis and pause interval naturalness scoring (roughly 1.5-5 seconds between pauses).
When tested on `demo_test_set`:
- Both genuine (label 0) and deepfake (label 1) audio samples produced `0 pauses detected` and a neutral `naturalness_score=0.50`.
- **Observation**: On these short (~2s) continuous speech test clips, or due to background noise keeping energy above `-40 dB`, the simple energy threshold heuristic fails to separate genuine from deepfake speech. As expected for a hand-written heuristic on short audio segments, a more sophisticated or machine-learning-based pause/breathing classifier (or longer audio clips) is needed for reliable separation.

## Attack Test: Baseline vs. Defended Model (Day 11)
After retraining with the adversarial defense dataset (`best_model_defended.pt`), the model demonstrates significantly improved robustness against RIR-matching attacks.

| Model Checkpoint | Fooled Rate (1 - Accuracy) | Notes |
|---|---|---|
| `best_model.pt` (Baseline) | 85.0% | Highly vulnerable to RIR-matched deepfakes |
| `best_model_defended.pt` (Defended) | 12.5% | Attack resistance drastically improved |

## Explainability Module (Day 13)
We introduced an explainability module (`ml/scripts/explainability.py`) to populate `flagged_segments`.
**Note for reviewers:** This implementation uses a sliding-window scoring approximation to find regions where the fake-probability is notably higher than the clip's average. It is *not* a true saliency map or Grad-CAM implementation (which would require hooking into the transformer's internal attention weights). This provides a computationally simple but honest approximation of "where the model focused" without heavy architectural modifications.
