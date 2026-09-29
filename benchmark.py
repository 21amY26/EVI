#!/usr/bin/env python3
"""Benchmark: detection rate and throughput on a synthetic log with injected gaps and reversals."""
import argparse
import os
import random
import tempfile
import time
from datetime import datetime, timedelta

from engine import detect_gaps, DEFAULT_THRESHOLD


def generate(path, lines, gap_rate, reversal_rate, seed):
    rng = random.Random(seed)
    t = datetime(2025, 1, 1)
    gaps = reversals = 0
    with open(path, 'w') as f:
        for _ in range(lines):
            roll = rng.random()
            if roll < gap_rate:
                t += timedelta(seconds=rng.randint(int(DEFAULT_THRESHOLD) + 1, 3600))
                gaps += 1
            else:
                t += timedelta(seconds=rng.randint(1, int(DEFAULT_THRESHOLD)))
            if gap_rate <= roll < gap_rate + reversal_rate:
                # One out-of-order line; the log then carries on from t
                f.write((t - timedelta(seconds=rng.randint(60, 600))).strftime('%Y-%m-%d %H:%M:%S') + ' injected\n')
                reversals += 1
            f.write(t.strftime('%Y-%m-%d %H:%M:%S') + ' event\n')
    return gaps, reversals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lines', type=int, default=1_000_000)
    ap.add_argument('--seed', type=int, default=42)
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'bench.log')
        gaps, reversals = generate(path, args.lines, 0.0005, 0.0002, args.seed)
        start = time.perf_counter()
        stats = detect_gaps(path)
        elapsed = time.perf_counter() - start

    print(f"Lines scanned     : {stats.total_lines:,}")
    print(f"Gaps detected     : {len(stats.gaps)}/{gaps}")
    print(f"Reversals detected: {len(stats.reversals)}/{reversals}")
    print(f"Time              : {elapsed:.2f}s ({stats.total_lines / elapsed:,.0f} lines/sec)")


if __name__ == '__main__':
    main()
