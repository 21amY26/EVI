"""Hybrid mode — forensic scan of existing lines, then keep following the file."""
from engine import EngineStats, DEFAULT_THRESHOLD
from live import follow, print_event
from rich.console import Console

console = Console()


def run_hybrid(filepath: str, threshold: float = DEFAULT_THRESHOLD, duration: float = 30) -> EngineStats:
    console.print(f"[bold cyan]Hybrid: scanning existing logs, then watching for {duration:.0f}s...[/]")
    # One detector covers both phases, so a gap between the last old line
    # and the first new line is caught too.
    return follow(filepath, threshold, duration, from_start=True, on_event=print_event)
