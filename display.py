"""EVI Dashboard Display & Input."""
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from layout import create_dashboard_layout
from engine import EngineStats
import sys
import os
import time
from datetime import datetime

console = Console()
from rich.progress import Progress, BarColumn, TextColumn

def loading_bar(duration=2.0, steps=100):
    delay = duration / steps  # THIS controls total time

    with Progress(
        TextColumn("[bold green]{task.description}"),
        BarColumn(
            bar_width=40,
            complete_style="green",
            finished_style="green"
        ),
        console=console,
    ) as progress:

        task = progress.add_task("Scanning logs...", total=steps)

        for _ in range(steps):
            time.sleep(delay)
            progress.update(task, advance=1)


def show_dashboard(stats: EngineStats, last_scan="Never", mode="Idle"):
    """Dynamic dashboard with input."""
    layout = create_dashboard_layout(stats, last_scan, mode)
    console.clear()
    console.print(layout)
    choice = Prompt.ask("[bold white]EVI > [/bold white]")
    return choice.strip()


def run_dashboard():
    """Main dashboard loop."""
    from explainer import show_help
    stats = EngineStats()
    current_mode = "Idle"
    while True:
        choice = show_dashboard(stats, datetime.now().strftime("%H:%M:%S"), current_mode)
        if choice == "0":
            print("\n[bold green]👋 Thanks for using EVI. Stay vigilant.[/]")
            break
        elif choice == "1":
            current_mode = "Forensic Scan"
            filepath = Prompt.ask("[cyan]Enter log file path[/] (default test_logs/tampered.log)", default="test_logs/tampered.log")
            from forensic import run_forensic
            stats = run_forensic(filepath, 60)
            loading_bar(1.5,100)
            print("\n[bold green]Scan complete. Check findings panel.[/]")
            time.sleep(0.5)

        elif choice == "2":
            current_mode = "Live Monitor"
            filepath = Prompt.ask("[cyan]Enter log file path[/] (default test_logs/tampered.log)", default="test_logs/tampered.log")
            from live import run_live
            stats = run_live(filepath, 60.0)
            loading_bar(1,50)
            print("\n[bold green]Live monitor complete.[/]")
            time.sleep(0.5)

        elif choice == "3":
            current_mode = "Hybrid"
            filepath = Prompt.ask("[cyan]Enter log file path[/] (default test_logs/tampered.log)", default="test_logs/tampered.log")
            from hybrid import run_hybrid
            stats = run_hybrid(filepath, 60.0)
            loading_bar(2,100)
            print("\n[bold green]Hybrid analysis complete.[/]")
            time.sleep(0.5)

        elif choice == "4":
            current_mode = "Help"
            show_help()
        else:
            print("\n[bold yellow]Please choose 0-4[/]")
