"""EVI Dashboard Display & Input."""
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from layout import create_dashboard_layout
from engine import EngineStats
import time
from datetime import datetime

console = Console()
from rich.progress import Progress, BarColumn, TextColumn


def loading_bar(duration=2.0, steps=100):
    delay = duration / steps
    with Progress(
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning logs...", total=steps)
        for _ in range(steps):
            time.sleep(delay)
            progress.update(task, advance=1)


def print_stats(stats: EngineStats, mode: str = "Scan"):
    """Print scan results directly to console with rich colour."""
    console.print()
    console.print(f"[bold bright_magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")
    console.print(f"[bold white] 📊 {mode} Results[/]")
    console.print(f"[bold bright_magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")
    console.print(f"  [bold green]Logs Loaded       :[/]  [green]{stats.total_lines:,}[/]")
    console.print(f"  [bold cyan]Gaps Detected     :[/]  [{'red bold' if stats.gaps else 'dim'}]{len(stats.gaps)}[/]")
    console.print(f"  [bold orange1]Total Missing Time:[/]  [orange1]{stats.total_missing_time:.0f}s[/]")

    if stats.gaps:
        sev_score = {'LOW': 1, 'MEDIUM': 2, 'CRITICAL': 3}
        worst = max(stats.gaps, key=lambda g: sev_score.get(g.severity, 0))
        color = {'LOW': 'green', 'MEDIUM': 'yellow', 'CRITICAL': 'red bold'}.get(worst.severity, 'white')
        console.print(f"  [bold magenta]Highest Severity  :[/]  [{color}]{worst.severity}[/]")
        console.print()
        console.print(f"  [bold white]Gap Breakdown:[/]")
        console.print(f"    [green]LOW      : {stats.gaps_by_sev.get('LOW', 0)}[/]")
        console.print(f"    [yellow]MEDIUM   : {stats.gaps_by_sev.get('MEDIUM', 0)}[/]")
        console.print(f"    [red]CRITICAL : {stats.gaps_by_sev.get('CRITICAL', 0)}[/]")
        console.print()
        console.print(f"  [bold white]Gap Details:[/]")
        for gap in stats.gaps:
            color = {'LOW': 'green', 'MEDIUM': 'yellow', 'CRITICAL': 'red'}.get(gap.severity, 'white')
            console.print(
                f"    [{color}]#{gap.id:02d}[/]  "
                f"[dim]{gap.start_time.strftime('%H:%M:%S')} → {gap.end_time.strftime('%H:%M:%S')}[/]  "
                f"[{color}]{gap.duration:.0f}s[/]  "
                f"[{color} bold]{gap.severity}[/]  "
                f"[dim]{gap.notes}[/]"
            )
    else:
        console.print(f"  [green]✓ No gaps found — log appears clean.[/]")

    console.print(f"[bold bright_magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")
    console.print()


def show_dashboard(evi_message='"Tell me what you\'d like to do."'):
    """Render dashboard and return user input."""
    layout = create_dashboard_layout(evi_message)
    console.clear()
    console.print(layout)
    choice = Prompt.ask("[bold white]EVI > [/bold white]")
    return choice.strip()


def run_dashboard():
    """Main dashboard loop."""
    from explainer import show_help

    while True:
        choice = show_dashboard()

        if choice == "0":
            console.print("\n[bold green]👋 Thanks for using EVI. Stay vigilant.[/]")
            break

        elif choice == "1":
            filepath = Prompt.ask(
                "[cyan]Enter log file path[/] (default test_logs/tampered.log)",
                default="test_logs/tampered.log"
            )
            from forensic import run_forensic
            loading_bar(1.5, 100)
            stats = run_forensic(filepath, 60.0)
            print_stats(stats, "Forensic Scan")
            Prompt.ask("[dim]Press ENTER to return to menu[/dim]", default="")

        elif choice == "2":
            filepath = Prompt.ask(
                "[cyan]Enter log file path[/] (default test_logs/tampered.log)",
                default="test_logs/tampered.log"
            )
            from live import run_live
            stats = run_live(filepath, 60.0)
            loading_bar(1, 50)
            print_stats(stats, "Live Monitor")
            Prompt.ask("[dim]Press ENTER to return to menu[/dim]", default="")

        elif choice == "3":
            filepath = Prompt.ask(
                "[cyan]Enter log file path[/] (default test_logs/tampered.log)",
                default="test_logs/tampered.log"
            )
            from hybrid import run_hybrid
            stats = run_hybrid(filepath, 60.0)
            loading_bar(2, 100)
            print_stats(stats, "Hybrid")
            Prompt.ask("[dim]Press ENTER to return to menu[/dim]", default="")

        elif choice == "4":
            show_help()

        else:
            console.print("\n[bold yellow]Please choose 0-4[/]")
            time.sleep(1)