import numpy as np
from sklearn.metrics import roc_curve

def compute_eer(labels, scores):
    """
    labels: list of 0 (bonafide) / 1 (spoof)
    scores: predicted spoof probability
    Returns (eer, threshold)
    """
    fpr, tpr, thresholds = roc_curve(labels, scores)
    fnr = 1 - tpr
    idx = np.nanargmin(np.abs(fnr - fpr))
    return fpr[idx], thresholds[idx]

def compute_accuracy(labels, preds):
    labels = np.array(labels)
    preds = np.array(preds)
    return (labels == preds).mean()
