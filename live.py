from engine import run_forensic
from rich.console import Console
import time

console = Console()

def run_live(filepath: str, threshold: float = 60.0, duration: int = 10):
    console.print("[bold yellow]Live monitoring (real scan)...[/]")
    
    for _ in range(duration):
        stats = run_forensic(filepath, threshold)
        console.print(f"[cyan]Scan complete. Gaps: {len(stats.gaps)}[/]")
        time.sleep(2)

    return stats