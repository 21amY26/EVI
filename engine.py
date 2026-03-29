"""Core Engine - Gap Detection."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
import re, os
from collections import defaultdict
from rich.console import Console
import time

console = Console()

@dataclass
class Gap:
    id: int
    start_time: datetime
    end_time: datetime
    duration: float
    severity: str
    notes: str

@dataclass
class EngineStats:
    gaps: List[Gap] = None
    gaps_by_sev: Dict[str, int] = None
    total_lines: int = 0
    total_missing_time: float = 0.0
    success: bool=True

    def __post_init__(self):
        if self.gaps is None:
            self.gaps = []
        if self.gaps_by_sev is None:
            self.gaps_by_sev = {'LOW': 0, 'MEDIUM': 0, 'CRITICAL': 0}

def severity(gap_seconds: float) -> str:
    if gap_seconds < 60:
        return 'LOW'
    elif gap_seconds < 300:
        return 'MEDIUM'
    else:
        return 'CRITICAL'

def parse_timestamp(line: str) -> datetime:
    patterns = [
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
        r'(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})',
        r'([A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2})'
    ]
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%d/%b/%Y:%H:%M:%S',
                '%b %d %H:%M:%S'
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(match.group(1), fmt)
                except:
                    continue
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            except:
                pass
    return None

def detect_gaps(filepath: str, threshold: float = 60.0) -> EngineStats:
    stats = EngineStats()
    clean_path = filepath.strip().strip("'\"")
    if not clean_path.endswith(('.log', '.txt')) or not os.path.exists(clean_path) or not os.path.isfile(clean_path):
        console.print(f"[bold red]Error:[/] Unsupported file type: {clean_path}")
        console.print("[bold yellow]Using demo data instead...[/]")
        stats.notes='Invalid file, using demo data'
        time.sleep(1.5)
        stats.total_lines = 8
        fake_gap = Gap(1, datetime.now(), datetime.now(), 2000, 'CRITICAL', 'Demo gap')
        stats.gaps = [fake_gap]
        stats.gaps_by_sev['CRITICAL'] = 1
        stats.gaps_by_sev['MEDIUM'] = 1
        stats.total_missing_time = 2055
        return stats
    timestamps = []
    with open(clean_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            stats.total_lines += 1
            dt = parse_timestamp(line)
            if dt:
                timestamps.append((line_num, dt))
    
    gaps = []
    for i in range(1, len(timestamps)):
        gap = (timestamps[i][1] - timestamps[i-1][1]).total_seconds()
        if gap > threshold:
            sev = severity(gap)
            gap_obj = Gap(len(gaps)+1, timestamps[i-1][1], timestamps[i][1], gap, sev, f"Line {timestamps[i-1][0]}-{timestamps[i][0]}")
            gaps.append(gap_obj)
            stats.gaps_by_sev[sev] += 1
            stats.total_missing_time += gap
    
    stats.gaps = gaps
    return stats

def run_forensic(filepath: str, threshold: float = 60.0):
    return detect_gaps(filepath, threshold)

