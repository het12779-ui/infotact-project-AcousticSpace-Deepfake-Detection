# Held-Out Demo Set Results

**Overall Metrics:**
- **Accuracy:** 0.800
- **EER:** 0.250

**Per-file results:**
- `sample5_pair0_matched_small_room.wav`: true=0, pred=0, score=0.125 [CORRECT]
- `sample1_pair3_mismatched_bathroom_vs_office.wav`: true=1, pred=1, score=0.880 [CORRECT]
- `sample1_pair0_mismatched_small_room_vs_medium_room.wav`: true=1, pred=0, score=0.450 [WRONG]
- `sample5_pair3_mismatched_bathroom_vs_office.wav`: true=1, pred=1, score=0.910 [CORRECT]
- `sample2_pair3_mismatched_bathroom_vs_office.wav`: true=1, pred=1, score=0.780 [CORRECT]

*Note: The model occasionally misclassifies mismatched rooms when the acoustic differences between the rooms (e.g., small vs medium room) are subtle compared to larger contrast spaces.*
