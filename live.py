"""Live mode — follow a log file like `tail -f` and flag gaps as lines arrive."""
import os
import time
from typing import Callable, Optional
from rich.console import Console
from engine import GapDetector, EngineStats, Gap, check_log_path, DEFAULT_THRESHOLD

console = Console()


def print_event(event: Gap):
    color = {'LOW': 'green', 'MEDIUM': 'yellow', 'CRITICAL': 'red bold'}.get(event.severity, 'white')
    label = 'REVERSAL' if event.kind == 'REVERSAL' else 'GAP'
    console.print(f"[{color}]⚠ {label} {event.duration:.0f}s {event.severity}[/]  [dim]{event.notes}[/]")


def follow(filepath: str, threshold: float = DEFAULT_THRESHOLD, duration: float = 30,
           from_start: bool = False, poll_interval: float = 0.5,
           on_event: Optional[Callable[[Gap], None]] = None) -> EngineStats:
    """Read lines as they are appended to `filepath` for `duration` seconds.

    from_start=False starts at the end of the file (new lines only);
    from_start=True processes the existing content first, then keeps following.
    """
    clean_path, error = check_log_path(filepath)
    if error:
        return EngineStats(success=False, error=error)

    detector = GapDetector(threshold)
    partial = ''
    deadline = time.monotonic() + duration

    def feed(line):
        event = detector.feed(line)
        if event and on_event:
            on_event(event)

    with open(clean_path, 'r', errors='replace') as f:
        if not from_start:
            f.seek(0, os.SEEK_END)
        while time.monotonic() < deadline:
            chunk = f.readline()
            if chunk:
                if not chunk.endswith('\n'):
                    partial += chunk  # writer hasn't finished the line yet
                    continue
                feed(partial + chunk)
                partial = ''
                continue
            if os.path.getsize(clean_path) < f.tell():
                f.seek(0)  # file was truncated or rotated
                partial = ''
            time.sleep(poll_interval)
        if partial:
            feed(partial)

    return detector.stats


def run_live(filepath: str, threshold: float = DEFAULT_THRESHOLD, duration: float = 30):
    console.print(f"[bold yellow]Live monitoring for {duration:.0f}s — watching for new lines...[/]")
    return follow(filepath, threshold, duration, from_start=False, on_event=print_event)
