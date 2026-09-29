"""Forensic mode."""
from engine import detect_gaps, DEFAULT_THRESHOLD
import time

def run_forensic(filepath: str, threshold: float = DEFAULT_THRESHOLD):
    print("Forensic scan running...")
    time.sleep(0.5)
    return detect_gaps(filepath, threshold)
