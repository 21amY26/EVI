"""Rich Layout - EVI Dashboard - Exact Format."""
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text
from rich.console import Console
from engine import EngineStats
from datetime import datetime
import time

console = Console()

def create_header():
    header_text = Text("🤖 EVI — Evidence Investigator", style="bold bright_magenta")
    return Panel(header_text, box=box.HEAVY)

def create_system_status_panel(stats, last_scan="Never", mode="Idle"):
    total_lines = getattr(stats, 'total_lines', 0)
    table = Table.grid(expand=True)
    table.add_row("Logs Loaded", f"[green]{total_lines:,}[/]", style="green")
    table.add_row("Last Scan", f"[cyan]{last_scan}[/]", style="cyan")
    table.add_row("Current Mode", f"[{'yellow' if mode != 'Idle' else 'green'} bold]{mode}[/]", style="magenta")
    return Panel(table, title="[bold blue]📊 SYSTEM STATUS[/]", box=box.ROUNDED, padding=1)

def create_findings_panel(stats):
    gaps_len = len(getattr(stats, 'gaps', []))
    total_missing = getattr(stats, 'total_missing_time', 0.0)
    table = Table.grid(expand=True)
    if gaps_len == 0:
        table.add_row("Gaps Detected", "[dim]0[/]")
        table.add_row("Highest Severity", "[dim]None[/]")
        table.add_row("Total Missing Time", "[dim]0s[/]")
    else:
        try:
            sev_score = {'LOW':1, 'MEDIUM':2, 'CRITICAL':3}
            sev = max(stats.gaps, key=lambda g: sev_score[g.severity])
            color = {'LOW':'green', 'MEDIUM':'yellow', 'CRITICAL':'red'}.get(sev.severity, 'white')
            table.add_row("Gaps Detected", f"[red bold]{gaps_len}[/]", style="red")
            table.add_row("Highest Severity", f"[{color} bold]{sev.severity}[/]", style=color)
            table.add_row("Total Missing Time", f"[orange1]{total_missing:.0f}s[/]", style="orange1")
        except:
            table.add_row("Gaps Detected", f"[red bold]{gaps_len}[/]", style="red")
            table.add_row("Highest Severity", "[dim]Processing...[/]")
            table.add_row("Total Missing Time", f"[dim]{total_missing:.0f}s[/]")
    return Panel(table, title="[bold magenta]🔍 FINDINGS[/]", box=box.ROUNDED, padding=1)

def create_evi_panel():
    text = Text('''"Tell me what you'd like to do."''', style="italic cyan")
    return Panel(text, title="[bold cyan]🤖 EVI Assistant[/]", box=box.ROUNDED)

def create_actions_panel():
    text = Text.from_markup('''[bold cyan on black]▶ 1. Forensic Scan[/bold cyan on black]
[bold cyan on black]▶ 2. Live Monitor[/bold cyan on black]
[bold cyan on black]▶ 3. Hybrid Mode[/bold cyan on black]
[bold cyan on black]▶ 4. Help[/bold cyan on black]
[bold red on black]▶ 0. Exit[/bold red on black]
[bold white]Type 0-4 at EVI > prompt:[/bold white]''')
    return Panel(text, title="[bold yellow]⚡ QUICK ACTIONS[/]", box=box.ROUNDED)

def create_dashboard_layout(stats, last_scan="Never", mode="Idle"):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="evi", size=5),
        Layout(name="actions", size=12)
    )
    layout["header"].update(create_header())
    layout["main"].split_row(
        Layout(name="status", ratio=1),
        Layout(name="findings", ratio=1)
    )
    layout["main"]["status"].update(create_system_status_panel(stats, last_scan, mode))
    layout["main"]["findings"].update(create_findings_panel(stats))
    time.sleep(1)
    layout["evi"].update(create_evi_panel())
    layout["actions"].update(create_actions_panel())
    return layout

