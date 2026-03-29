"""Hybrid mode — forensic + live relevance check."""
from engine import run_forensic, EngineStats, Gap
from rich.console import Console
from datetime import datetime

console = Console()


def run_hybrid(filepath: str, threshold: float = 60.0) -> EngineStats:
    console.print("[bold cyan]Hybrid: forensic + live analysis...[/]")

    # Step 1: forensic scan
    stats = run_forensic(filepath, threshold)
    console.print(f"[green]Forensic gaps found: {len(stats.gaps)}[/]")

    # Step 2: live relevance check — always initialise before the if
    recent_gaps = []
    now = datetime.now()

    if stats.gaps:
        for gap in stats.gaps:
            time_since = (now - gap.end_time).total_seconds()
            if time_since < 300:
                recent_gaps.append(gap)

    if recent_gaps:
        critical_recent = [g for g in recent_gaps if g.severity == 'CRITICAL']
        if critical_recent:
            console.print("[bold red]⚠ CRITICAL recent gaps — system may be compromised[/]")
        else:
            console.print("[bold yellow]Recent minor gaps detected[/]")
    else:
        console.print("[green]No recent anomalies[/]")

    return stats