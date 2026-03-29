"""Forensic mode."""
from engine import detect_gaps
import time

def run_forensic(filepath: str, threshold: float = 60.0):
    print("Forensic scan running...")
    time.sleep(0.5)
    return detect_gaps(filepath, threshold)