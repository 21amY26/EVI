"""Core Engine - Gap Detection."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re, os

# Gaps longer than this (seconds) are flagged. Below 60s they are LOW.
DEFAULT_THRESHOLD = 30.0

@dataclass
class Gap:
    id: int
    start_time: datetime
    end_time: datetime
    duration: float
    severity: str
    notes: str
    kind: str = 'GAP'  # 'GAP' (missing time) or 'REVERSAL' (timestamp went backwards)

@dataclass
class EngineStats:
    gaps: List[Gap] = field(default_factory=list)
    reversals: List[Gap] = field(default_factory=list)
    gaps_by_sev: Dict[str, int] = field(default_factory=lambda: {'LOW': 0, 'MEDIUM': 0, 'CRITICAL': 0})
    total_lines: int = 0
    unparsed_lines: int = 0
    total_missing_time: float = 0.0
    success: bool = True
    error: str = ''

def severity(gap_seconds: float) -> str:
    if gap_seconds < 60:
        return 'LOW'
    elif gap_seconds < 300:
        return 'MEDIUM'
    else:
        return 'CRITICAL'

# (regex, strptime format, has_year)
TIMESTAMP_FORMATS = [
    (re.compile(r'(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})'), '%Y-%m-%d %H:%M:%S', True),    # ISO-8601
    (re.compile(r'(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})'), '%d/%b/%Y:%H:%M:%S', True),  # Apache
    (re.compile(r'([A-Za-z]{3} +\d{1,2} \d{2}:\d{2}:\d{2})'), '%b %d %H:%M:%S', False),       # Syslog
]

def parse_timestamp(line: str, ref: Optional[datetime] = None) -> Optional[datetime]:
    """Extract a timestamp from a log line.

    Syslog timestamps carry no year, so it is taken from `ref` (the previous
    timestamp in the log) or the current year. A jump back of more than half
    a year is treated as a Dec -> Jan rollover.
    """
    for pattern, fmt, has_year in TIMESTAMP_FORMATS:
        match = pattern.search(line)
        if not match:
            continue
        text = match.group(1).replace('T', ' ') if has_year else ' '.join(match.group(1).split())
        if not has_year:
            year = ref.year if ref else datetime.now().year
            text, fmt = f'{year} {text}', f'%Y {fmt}'
        try:
            dt = datetime.strptime(text, fmt)
        except ValueError:
            continue
        if not has_year and ref and dt < ref - timedelta(days=183):
            dt = dt.replace(year=dt.year + 1)
        return dt
    return None

class GapDetector:
    """Feeds log lines one at a time and records gaps and timestamp reversals."""

    def __init__(self, threshold: float = DEFAULT_THRESHOLD):
        self.threshold = threshold
        self.stats = EngineStats()
        self._last = None  # (line_num, datetime) of the latest timestamp seen

    def feed(self, line: str) -> Optional[Gap]:
        """Process one line. Returns the gap or reversal it revealed, if any."""
        self.stats.total_lines += 1
        line_num = self.stats.total_lines
        dt = parse_timestamp(line, self._last[1] if self._last else None)
        if dt is None:
            if line.strip():
                self.stats.unparsed_lines += 1
            return None
        if self._last is None:
            self._last = (line_num, dt)
            return None

        prev_num, prev_dt = self._last
        delta = (dt - prev_dt).total_seconds()
        notes = f"Line {prev_num}-{line_num}"

        if delta < 0:
            # Keep the latest timestamp as the reference so the next gap isn't double counted
            rev = Gap(len(self.stats.reversals) + 1, prev_dt, dt, -delta, severity(-delta),
                      f"{notes}: timestamp went backwards", kind='REVERSAL')
            self.stats.reversals.append(rev)
            return rev

        self._last = (line_num, dt)
        if delta > self.threshold:
            sev = severity(delta)
            gap = Gap(len(self.stats.gaps) + 1, prev_dt, dt, delta, sev, notes)
            self.stats.gaps.append(gap)
            self.stats.gaps_by_sev[sev] += 1
            self.stats.total_missing_time += delta
            return gap
        return None

def check_log_path(filepath: str):
    """Return (clean_path, error). error is '' when the file can be read."""
    clean_path = filepath.strip().strip("'\"")
    if not os.path.exists(clean_path):
        return clean_path, f"File not found: {clean_path}"
    if not os.path.isfile(clean_path):
        return clean_path, f"Not a file: {clean_path}"
    if not os.access(clean_path, os.R_OK):
        return clean_path, f"Permission denied: {clean_path}"
    return clean_path, ''

def detect_gaps(filepath: str, threshold: float = DEFAULT_THRESHOLD) -> EngineStats:
    clean_path, error = check_log_path(filepath)
    if error:
        return EngineStats(success=False, error=error)

    detector = GapDetector(threshold)
    with open(clean_path, 'r', errors='replace') as f:
        for line in f:
            detector.feed(line)
    return detector.stats

def run_forensic(filepath: str, threshold: float = DEFAULT_THRESHOLD):
    return detect_gaps(filepath, threshold)
