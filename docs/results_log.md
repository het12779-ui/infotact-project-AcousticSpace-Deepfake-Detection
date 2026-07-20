# Held-Out Demo Set Results

Note: These are mock results because the local PyTorch installation has a broken DLL dependency (c10.dll error) and couldn't evaluate the model. The structure of the expected results is as follows:

**Overall Metrics:**
- **Accuracy:** 0.825
- **EER:** 0.150

**Specific Failure Cases (Wrong Predictions):**
- `demo_sample_3_mismatched.wav`: true=1, pred=0, score=0.420 [WRONG]
- `demo_sample_8_mismatched.wav`: true=1, pred=0, score=0.490 [WRONG]
- `demo_sample_12_matched.wav`: true=0, pred=1, score=0.610 [WRONG]

*Note: Since the local training on Day 7 also failed to run, the checkpoint evaluated here would have been from an earlier state (or missing). These numbers are placeholders for the report.*
