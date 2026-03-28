"""Forensic mode."""
from engine import run_forensic
import time

def run_forensic(filepath: str, threshold: float = 60.0):
    print("Forensic scan running...")
    time.sleep(0.5)
    from engine import detect_gaps
    return detect_gaps(filepath, threshold)